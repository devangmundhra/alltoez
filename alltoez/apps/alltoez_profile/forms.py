from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from allauth.account.forms import LoginForm

from models import UserProfile, Child, GENDER_CHOICES


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    gender = forms.Select(choices=GENDER_CHOICES)
    zip_code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))
    # child_age = forms.NumberInput
    # child_gender = forms.Select(choices=GENDER_CHOICES)
    # email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ('gender', 'first_name', 'last_name', 'zip_code')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        # self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        profile.user.first_name = self.cleaned_data.get('first_name')
        profile.user.last_name = self.cleaned_data.get('last_name')
        # profile.user.email = self.cleaned_data.get('email')
        profile.user.save()
        return profile

ChildrenFormset = inlineformset_factory(User, Child, extra=1)