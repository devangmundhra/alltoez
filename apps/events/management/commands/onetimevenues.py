__author__ = 'devangmundhra'

from django.core.management.base import BaseCommand, CommandError
from django.contrib.gis.geos import GEOSGeometry

from apps.venues.models import Venue
from apps.alltoez_profile.models import UserProfile

class Command(BaseCommand):
    help = 'Update point field in venues'

    def handle(self, *args, **options):
        for venue in Venue.objects.all():
            if venue.longitude and venue.latitude:
                venue.point = GEOSGeometry("POINT(%s %s)" % (venue.longitude, venue.latitude))
                venue.save()

        for profile in UserProfile.objects.all():
            if profile.longitude and profile.latitude:
                profile.point = GEOSGeometry("POINT(%s %s)" % (profile.longitude, profile.latitude))
                profile.save()