from alltoez.apps.alltoez.views import Events
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView


class ShowEventsView(ListView):
    model = Events
    category = "outdoors"

    # def get(self, *args, **kwargs):
    #
    #     if Events.object.(category="outdoors"):
