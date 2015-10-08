import re

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from allauth.account.forms import LoginForm

from models import UserProfile, Child, GENDER_CHOICES, CHILD_GENDER_CHOICES


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='First name', max_length=30,
                                 widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label='Last name', max_length=30,
                                widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    gender = forms.Select(choices=GENDER_CHOICES)
    zipcode = forms.CharField(label='Zip Code', max_length=10,
                              widget=forms.TextInput(attrs={'placeholder': 'Zip Code'}))
    city = forms.CharField(label='City', max_length=150, required=False,
                           widget=forms.TextInput(attrs={'placeholder': 'City'}))
    state = forms.CharField(label='State', max_length=150, required=False,
                            widget=forms.TextInput(attrs={'placeholder': 'State'}))
    # email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'gender', 'zipcode', 'city', 'state')
        widgets = {
            'gender': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        # Get updated information from user model
        self.fields['first_name'].initial = self.instance.user.first_name
        self.fields['last_name'].initial = self.instance.user.last_name
        # self.fields['email'].initial = self.instance.user.email

    def save(self, *args, **kwargs):
        profile = super(UserProfileForm, self).save(*args, **kwargs)
        # Also persist this information to user model
        profile.user.first_name = self.cleaned_data.get('first_name')
        profile.user.last_name = self.cleaned_data.get('last_name')
        # profile.user.email = self.cleaned_data.get('email')
        profile.user.save()
        return profile

    def clean_zipcode(self):
        data = self.cleaned_data['zipcode']
        postal_code = re.match(r'^\d{5}(-\d{4})?$', data)
        if not postal_code:
            raise ValidationError(
                _('Invalid zipcode: %(value)s'),
                code='invalid',
                params={'value': data},
            )
        # Always return the cleaned data, whether you have changed it or
        # not.
        return data


class ChildForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=60,
                           widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    gender = forms.Select(choices=CHILD_GENDER_CHOICES)
    age = forms.IntegerField(min_value=0, max_value=100, label='Age',
                             widget=forms.NumberInput(attrs={'placeholder': 'Age'}))

    class Meta:
        model = Child
        fields = ('name', 'age', 'gender')
        widgets = {
            'gender': forms.RadioSelect(attrs={'class': 'radio-inline'}),
        }
ChildrenFormset = inlineformset_factory(User, Child, form=ChildForm, extra=1, labels='Children', max_num=8)