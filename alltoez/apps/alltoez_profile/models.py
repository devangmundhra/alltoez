from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_delete, post_save, pre_save
from django.dispatch import receiver

from filebrowser.fields import FileBrowseField
from apps.alltoez.utils.fields import AutoOneToOneField
from apps.alltoez.utils.abstract_models import BaseModel

import re, unicodedata, os, random, string

class UserProfile(BaseModel):
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

	def get_absolute_url(self):
		return reverse('profile', args=[self.user.username])

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
