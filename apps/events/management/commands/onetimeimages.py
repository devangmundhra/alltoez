__author__ = 'devangmundhra'

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

import urllib2
from uuid import uuid4

from apps.events.models import Event


class Command(BaseCommand):
    help = 'Creates MediaField objects from image json objects'

    def handle(self, *args, **options):
        # Go over each event, read the image in image.url and store it in img object
        for event in Event.objects.all():
            url = event.image_info.get("url")
            try:
                resource = urllib2.urlopen(url)
                f = ContentFile(resource.read())
                new_value = default_storage.save("events_media/{}.jpg".format(str(uuid4())), f)
                event.image = new_value
                event.save()
            except:
                print "Error in image at url {} for event {}".format(url, event.id)
