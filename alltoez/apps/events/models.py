from django.db import models
from django.template.defaultfilters import slugify, truncatechars

from jsonfield import JSONField
from location_field.models import PlainLocationField


from apps.alltoez.utils.abstract_models import BaseModel
from apps.alltoez.utils.model_utils import unique_slugify


import json, urllib

class Category(models.Model):
    """
    Category class
    This class stores categories references by Django model
    Currently the categories are expected to be as follows:
    * Outdoors
        - Hiking trails
        - Biking trails
        - Parks and Playgrounds
        - Beaches
        - Dog Parks
    * Food
        - Restaurants
        - Food trucks
        - Sweet treats
    * Classes and Extra Curricular
        - Athletic Activities
        - Cooking
        - Crafts
        - Library events
    * Tours and Trips
        - Museums
        - Aquariums and Zoos
        - Mini family excursions
    * Seasonal
        - Concerts
        - Movies
        - Camps
        - Orchard picking
        - Halloween
        - Thanksgiving
        - Christmas
    """
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name="children")
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(null=True, blank=True, help_text="The part of the title that is used in the url. "
                                                             "Leave this blank if you want the system to generate one "
                                                             "for you.")
    description = models.CharField(max_length=200)
    font_awesome_icon_class = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ("-parent_category__name", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)

        return super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.description)

    def parent(self):
        return self.parent_category


class DraftEvent(models.Model):
    """
    DraftEvent class
    This class is used to store the events that are parsed from different websites
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200)
    raw = models.TextField(unique=True)
    '''
    These are some of the sources for the events
    '''
    SFKIDS = "sfkids.org"
    REDTRI = "redtri.com"
    source = models.CharField(max_length=200)
    source_url = models.URLField(blank=True, null=True, unique=True)
    processed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.event_set.count():
            self.processed = True
        super(DraftEvent, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'{} from {}'.format(self.title, self.source)


class Event(models.Model):
    """
    Event class
    This class describes the details of an event.
    The class also contains information about recurring events.
    Recurring events implemented through cron job format
    Another way of implementing recurring events- http://stackoverflow.com/q/5183630/712476
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    draft = models.ForeignKey(DraftEvent, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    category = models.ManyToManyField(Category, db_index=True)
    address = models.TextField()
    location = PlainLocationField(based_fields=[address], zoom=16)
    image = JSONField(default="{\"url\":\"\",\"source_name\":\"\",\"source_url\":\"\"}")
    min_age = models.PositiveSmallIntegerField(default=0)
    max_age = models.PositiveSmallIntegerField(default=100)
    cost = models.PositiveSmallIntegerField(default=0)
    # Currently we expect an event to occur atmost once per day (so only one start time/end time)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    end_date = models.DateField(blank=True, null=True)
    next_date = models.DateField(null=True, blank=True)
    cron_recurrence_format = models.CharField(max_length=50, null=True, blank=True,
                                              help_text="Repeating event? Use cron format "
                                                        "\'min hour day month day_of_week\' "
                                                        "\nMore details: http://en.wikipedia.org/wiki/Cron")
    url = models.URLField(blank=True, null=True, unique=True)
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['next_date', 'start_time']

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        if self.pk is None:
            # This is a new object being created
            self.next_date = self.start_date
        if not self.end_date:
            self.end_date = self.start_date
        super(Event, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.title)


class EventRecord(models.Model):
    """
    EventRecord class
    This class is the actual individual events shown to the user.
    """
    event = models.ForeignKey(Event)
    date = models.DateField(db_index=True)

    class Meta:
        unique_together = ('event', 'date')
        ordering = ['date']

    def __unicode__(self):
        return u'{} on {}'.format(self.event.title, self.date)
