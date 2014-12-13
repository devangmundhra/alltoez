from django import http
from django.conf import settings
from django.core.urlresolvers import reverse


class RedirectIfIncompleteProfile(object):
    def process_request(self, request):
        """
        Redirects the user to the second step in the signup process if they have
        not yet completed their profile. Required for the FB signup route!
        """
        redirect_url = reverse('register_children')
        path = request.get_full_path()
        if request.user.is_authenticated() and not request.user.profile.profile_complete() and path != redirect_url and '/admin/' not in path and '/accounts/social/signup/' not in path and '/accounts/logout/' not in path:
            return http.HttpResponseRedirect(redirect_url)
        return None
