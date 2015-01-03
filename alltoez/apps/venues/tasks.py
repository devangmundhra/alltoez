from __future__ import absolute_import

__author__ = 'devangmundhra'

import logging
from datetime import datetime

from django.db.models import Q
from django.core.mail import send_mail
from django.core import urlresolvers
from django.contrib.sites.models import Site

from celery import shared_task

from apps.venues.models import Venue

# Get an instance of a logger
logger = logging.getLogger(__name__)

@shared_task()
def check_invalid_venues():
    """
    Find venues that have an invalid latitude and longitude
    :return:
    """
    invalid_venues = Venue.objects.filter(Q(latitude__isnull=True) | Q(latitude=0))

    if not invalid_venues:
        return

    body = "Invalid venues\n"
    body_html = "<p><strong>Invalid venues</strong></p>\n"

    for venue in invalid_venues:
        body = body + "{} [{}{}]\n".format(venue, Site.objects.get_current(),
                                           urlresolvers.reverse('admin:venues_venue_change', args=(venue.id,)))
        body_html = body_html + "<a href={}{}>{}</a><br/>".format(Site.objects.get_current(),
                                                             urlresolvers.reverse('admin:venues_venue_change',
                                                                                  args=(venue.id,)),
                                                             venue)

    subject = "Alltoez Invalid Venues | SF | {}".format(datetime.today().strftime("%A, %d. %B"))

    send_mail(subject, body, "noreply@alltoez.com", ["ruchikadamani90@gmail.com", "devangmundhra@gmail.com"],
              html_message=body_html)