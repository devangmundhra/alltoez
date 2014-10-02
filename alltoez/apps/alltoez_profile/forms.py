from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from allauth.account.forms import LoginForm

from models import UserProfile

class UserProfileForm(forms.ModelForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	email = forms.EmailField()

	class Meta:
		model = UserProfile

	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['first_name'].initial = self.instance.user.first_name
		self.fields['last_name'].initial = self.instance.user.last_name
		self.fields['email'].initial = self.instance.user.email

	def save(self, *args, **kwargs):
		profile = super(UserProfileForm, self).save(*args, **kwargs)
		profile.user.first_name = self.cleaned_data.get('first_name')
		profile.user.last_name = self.cleaned_data.get('last_name')
		profile.user.email = self.cleaned_data.get('email')
		profile.user.save()
		return profile

ChildrenFormset = inlineformset_factory(UserProfileForm, Child, extra=2)