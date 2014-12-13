import json

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.http.response import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import NoReverseMatch

from allauth.account.views import SignupView

from apps.alltoez.utils.view_utils import LoginRequiredMixin, MessageMixin
from apps.alltoez_profile.forms import UserProfileForm, ChildrenFormset
from apps.alltoez_profile.models import UserProfile, GENDER_CHOICES, Child, CHILD_GENDER_CHOICES


class UserProfileDetail(LoginRequiredMixin, DetailView):
    model = UserProfile
    slug_field = 'user__username'
    slug_url_kwarg = 'username'
    template_name = "profile/userprofile_detail.html"

    def get_context_data(self, **kwargs):
        context = super(UserProfileDetail, self).get_context_data(**kwargs)
        context['profile_user'] = self.object.user
        return context


class UserProfileUpdate(MessageMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "profile/userprofile_form.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UserProfileUpdate, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        try:
            self.success_url = reverse('show_profile', args=[self.object.username])
        except NoReverseMatch:
            self.success_url = '/'

        return self.success_url

    def get_form_class(self):
        self.form_class = self.kwargs.get('form_class', self.form_class)
        return self.form_class

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        """
        This form is valid. Check to see if the children form is valid as well and then save them
        :param form:
        :return:
        """
        context = self.get_context_data()
        children_formset = context['children_formset']
        if children_formset.is_valid():
            # TODO: Check if these saves needs to be called explicitly
            self.object = form.save()
            children_formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        user = self.object.user

        if self.request.POST:
            context['children_formset'] = ChildrenFormset(self.request.POST, instance=user)
        else:
            context['children_formset'] = ChildrenFormset(instance=user)
        return context


class AlltoezSignupView(SignupView):
    success_url = '/accounts/signup/step-2/'


class AlltoezSignupStep2View(UpdateView):
    template_name = 'alltoez_profile/signup_step2.html'
    form_class = UserProfileForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AlltoezSignupStep2View, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(AlltoezSignupStep2View, self).get_context_data(**kwargs)
        context.update({
            'GENDER_CHOICES': GENDER_CHOICES.get_choices(),
            'CHILD_GENDER_CHOICES': CHILD_GENDER_CHOICES.get_choices()
        })
        return context

    def form_valid(self, form):
        form.save()
        children = self.request.POST.get('children', None)
        try:
            children = json.loads(children)
            for child in children:
                new_child = Child()
                new_child.age = child['age']
                new_child.gender = child['gender']
                new_child.user = self.request.user
                new_child.save()
        except ValueError:
            return HttpResponseBadRequest
        return HttpResponseRedirect('/')
