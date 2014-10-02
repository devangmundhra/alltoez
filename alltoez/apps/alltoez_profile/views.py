from allauth.account.views import SignupView
from alltoez.apps.alltoez.utils.view_utils import LoginRequiredMixin, MessageMixin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic import TemplateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import Http404, HttpResponseRedirect

from forms import UserProfileForm, ChildrenFormset
from models import UserProfile, GENDER_CHOICES


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

    def get_success_url(self):
        try:
            self.success_url = reverse('profile')
        except:
            self.success_url = '/'

        return self.success_url

    def get_form_class(self):
        self.form_class = self.kwargs.get('form_class', self.form_class)
        return self.form_class

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        context = self.get_context_data()
        children_form = context['children_formset']
        if children_form.is_valid():
            self.object = form.save()
            children_form.instance = self.object.user
            children_form.save()
            return HttpResponseRedirect('thanks/')
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            context['children_form'] = ChildrenFormset(self.request.POST)
        else:
            context['children_form'] = ChildrenFormset()
        return context

class AlltoezSignupView(SignupView):
    success_url = '/accounts/signup/step-2/'

# class RegisterChild(FormView):
#     template_name = "alltoez_profile/signup-step-2.html"


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
        context.update({'GENDER_CHOICES': GENDER_CHOICES.get_choices()})
        return context

    def form_valid(self, form):
        form.save()

        children = self.request.POST.get('chidlren', None)
        print "blah-", children
        return HttpResponseRedirect('thanks/')
