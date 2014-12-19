import re, unicodedata, os, random, string

from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver

from filebrowser.fields import FileBrowseField

from apps.alltoez.utils.fields import AutoOneToOneField
from apps.alltoez.utils.abstract_models import BaseModel, AddressMixin
from apps.alltoez.utils.model_utils import get_namedtuple_choices


GENDER_CHOICES = get_namedtuple_choices('GENDER_CHOICES', (
    (0, 'MALE', 'Male'),
    (1, 'FEMALE', 'Female'),
))
CHILD_GENDER_CHOICES = get_namedtuple_choices('CHILD_GENDER_CHOICES', (
    (0, 'BOY', 'Boy'),
    (1, 'GIRL', 'Girl'),
))


class UserProfile(BaseModel, AddressMixin):
    """
    Profile and configurations for a user
    """
    def get_upload_to(instance, filename):
        name, ext = os.path.splitext(filename)
        name = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(20))
        new_filename = '%s%s' % (name, ext.lower())

        return os.path.join('uploads/users/profile/images', new_filename)

    user = AutoOneToOneField(User, related_name="profile", editable=False)
    profile_image = models.ImageField(upload_to=get_upload_to, null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES.get_choices(), db_index=True, default=0)

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


class Child(BaseModel):
    """
    Profile to add children to a user's profile
    """
    user = models.ForeignKey(User, related_name="children")
    name = models.CharField(_('name'), max_length=60, blank=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.PositiveSmallIntegerField(choices=CHILD_GENDER_CHOICES.get_choices(), db_index=True, default='')
    age = models.PositiveSmallIntegerField(blank=True, null=True)

    @property
    def current_age(self):
        time_since_updated = timezone.now() - self.updated
        return self.age + int(time_since_updated.days/365.2425)