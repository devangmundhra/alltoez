import re, unicodedata, os, random, string
from uuid import uuid4
import logging

from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.contrib.gis.db import models

from allauth.socialaccount.models import SocialApp, SocialAccount
import facebook

from apps.alltoez.graph import *
from apps.alltoez.utils.fields import AutoOneToOneField
from apps.alltoez.utils.abstract_models import BaseModel, AddressMixin
from apps.alltoez.utils.model_utils import get_namedtuple_choices

logger = logging.getLogger(__name__)


class GraphName(object):
    class NodeLabel(object):
        User = "User"
        FbUser = "FbUser"

    class Relationship(object):
        FB_FRIEND = "FB_FRIEND"
        FOLLOWS = "Follows"
        SAME_USER_AS = "SAME_USER_AS"

GENDER_CHOICES = get_namedtuple_choices('GENDER_CHOICES', (
    (0, 'MALE', 'Male'),
    (1, 'FEMALE', 'Female'),
))
CHILD_GENDER_CHOICES = get_namedtuple_choices('CHILD_GENDER_CHOICES', (
    (0, 'BOY', 'Boy'),
    (1, 'GIRL', 'Girl'),
))


@deconstructible
class UploadToProfileImages(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        filename, ext = os.path.splitext(filename)
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)
get_upload_to = UploadToProfileImages('uploads/users/profile/images')


class UserProfile(BaseModel, AddressMixin):
    """
    Profile and configurations for a user
    """
    GRAPH_USER_NODE_NAME = "User"
    GRAPH_FBUSER_NODE_NAME = "FbUser"
    GRAPH_USER_FBUSER_RELATIONSHIP = "SAME_USER_AS"
    GRAPH_FBUSER_FRIEND_RELATIONSHIP = "FB_FRIEND"

    user = AutoOneToOneField(User, related_name="profile", editable=False)
    profile_image = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES.get_choices(), db_index=True, default=0)
    bio = models.TextField(verbose_name='User bio', blank=True)
    last_known_location_bounds = models.PolygonField(blank=True, null=True)
    last_map_zoom = models.PositiveSmallIntegerField(blank=True, null=True)

    objects = models.GeoManager()

    class Meta:
        app_label = 'alltoez_profile'

    def get_absolute_url(self):
        return reverse('profile', args=[self.user.username])

    def profile_complete(self):
        # Returns True if the profile is deemed complete
        if self.gender is None or not self.zipcode:
            return False
        else:
            return True

    @property
    def username(self):
        return self.user.username

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __unicode__(self):
        user = self.user
        if user.first_name:
            return "%s %s" % (user.first_name, user.last_name)
        else:
            return user.username

    def create_graph_node(self):
        try:
            facebook_app = SocialApp.objects.get(provider='facebook')
            user = self.user
            user_node = neo4j_graph.merge_one(UserProfile.GRAPH_USER_NODE_NAME, "id", user.id)
            user_node.properties['name'] = str(user)
            neo4j_graph.push(user_node)
            try:
                account = SocialAccount.objects.get(user_id=user.id, provider='facebook')
                fb_data = account.extra_data
                fbid = fb_data['id']
                fb_user_node = neo4j_graph.merge_one(UserProfile.GRAPH_FBUSER_NODE_NAME, "id", fbid)
                fb_user_node.properties['name'] = fb_data['name']
                neo4j_graph.push(fb_user_node)
                neo4j_graph.create_unique(Relationship(user_node, UserProfile.GRAPH_USER_FBUSER_RELATIONSHIP, fb_user_node))

                # Get user's fb friends
                token = account.socialtoken_set.all()[0].token
                fb_graph = facebook.GraphAPI(access_token=token)
                try:
                    fb_graph.extend_access_token(facebook_app.client_id, facebook_app.secret)
                    friends = fb_graph.get_connections(id='me', connection_name='friends').get('data', [])
                    for friend in friends:
                        friend_fbid = friend['id']
                        friend_fbuser_node = neo4j_graph.merge_one(UserProfile.GRAPH_FBUSER_NODE_NAME, "id", friend_fbid)
                        friend_fbuser_node.properties['name'] = friend['name']
                        neo4j_graph.push(friend_fbuser_node)
                        neo4j_graph.create_unique(Relationship(fb_user_node, UserProfile.GRAPH_FBUSER_FRIEND_RELATIONSHIP,
                                                               friend_fbuser_node))
                except facebook.GraphAPIError as e:
                    print logger.error("For user {}, FBGraphAPI error {}".format(user, e))
                    return None

            except SocialAccount.DoesNotExist:
                print logger.info("No fb account for {}".format(user))
                return None

            return user_node
        except IOError:
            pass

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

        # Send welcome email
        from apps.alltoez_profile.tasks import send_welcome_email
        send_welcome_email.delay(instance.email)


class Child(BaseModel):
    """
    Profile to add children to a user's profile
    """
    user = models.ForeignKey(User, related_name="children")
    name = models.CharField(_('name'), max_length=60, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.PositiveSmallIntegerField(default=0, choices=CHILD_GENDER_CHOICES.get_choices(), db_index=True)
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        app_label = 'alltoez_profile'

    @property
    def current_age(self):
        time_since_updated = timezone.now() - self.updated
        return self.age + int(time_since_updated.days/365.2425)
