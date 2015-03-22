__author__ = 'devangmundhra'

from django.core.management.base import BaseCommand, CommandError

from apps.events.models import Event
from apps.venues.models import Venue


class Command(BaseCommand):
    help = 'Creates venues for events for first time migration'

    def handle(self, *args, **options):
        # Let the first venue created be unknown/generic venue
        venue, created = Venue.objects.get_or_create(name='Unknown')

        # Now go over each event and associate it with a venue. Use the 'location' field as a key to identifying
        # the same venue
        for event in Event.objects.all():
            venue, created = Venue.objects.get_or_create(location=event.location)
            if not venue:
                raise CommandError('Couldn\'t create venue for %s' % event)

            if not event.venue:
                venue.address = event.address
                venue.phone_number = event.phone_number
                venue.neighborhood = event.neighborhood
                venue.name = str.join(" ", event.address.splitlines())
                venue.location = event.location
                venue.save()
                event.venue = venue
                event.save()
            else:
                print 'Repeating venue %s for event %s' % (venue, event)