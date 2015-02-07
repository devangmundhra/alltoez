from __future__ import unicode_literals
from django.db import models
from django.core.urlresolvers import reverse

from jsonfield import JSONField

from apps.alltoez.utils.model_utils import unique_slugify
from apps.venues.models import Venue


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
    name = models.CharField(max_length=200, db_index=True, unique=True)
    slug = models.SlugField(null=True, blank=True, unique=True,
                            help_text="The part of the title that is used in the url. "
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


class EventManager(models.Manager):
    def nearby(self, latitude, longitude, proximity):
        """
        Return all object which distance to specified coordinates
        is less than proximity given in kilometers
        """
        # TODO This is currently unused. But can be looked into when distances are taken into account as well
        # Great circle distance formula
        gcd = """
              6371 * acos(
               cos(radians(%s)) * cos(radians(latitude))
               * cos(radians(longitude) - radians(%s)) +
               sin(radians(%s)) * sin(radians(latitude))
              )
              """
        gcd_lt = "{} < %s".format(gcd)
        return self.get_queryset()\
                   .exclude(latitude=None)\
                   .exclude(longitude=None)\
                   .extra(
                       select={'distance': gcd},
                       select_params=[latitude, longitude, latitude],
                       where=[gcd_lt],
                       params=[latitude, longitude, latitude, proximity],
                       order_by=['distance']
                   )


class Event(models.Model):
    """
    Event class
    This class describes the details of an event.
    """
    DEFAULT_MIN_AGE_EVENT = 0
    DEFAULT_MAX_AGE_EVENT = 100

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    draft = models.ForeignKey(DraftEvent, blank=True, null=True)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, verbose_name='Event name')
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(verbose_name='Event description')
    category = models.ManyToManyField(Category, db_index=True)
    image = JSONField(default="{\"url\":\"\",\"source_name\":\"\",\"source_url\":\"\"}")
    min_age = models.PositiveSmallIntegerField(default=DEFAULT_MIN_AGE_EVENT, db_index=True)
    max_age = models.PositiveSmallIntegerField(default=DEFAULT_MAX_AGE_EVENT, db_index=True)
    cost = models.PositiveSmallIntegerField(default=0, db_index=True)
    cost_detail = models.CharField(max_length=500, blank=True,
                                   help_text="Enter if there is more than one cost value")
    # Currently we expect an event to occur atmost once per day (so only one start time/end time)
    start_date = models.DateField(db_index=True)
    end_date = models.DateField(blank=True, null=True, db_index=True,
                                help_text="End date of the event, if applicable")
    recurrence_detail = models.CharField(max_length=500, blank=True, null=True,
                                         help_text="Enter a line about when this event is till, if it is recurring")
    time_detail = models.CharField(max_length=500, blank=True, null=True,
                                   help_text="Enter time for different days, in different rows")
    url = models.URLField(blank=True, null=True, verbose_name='Event link')
    additional_info = models.TextField(blank=True, null=True)
    publish = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at', '-start_date', 'end_date']

    def save(self, *args, **kwargs):
        if not self.pk:
            unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug])

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


class SimilarEvents(models.Model):
    """
    SimilarEvents class
    This class stores a temporary mapping of similar events between for a given event
    """
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, unique=True)
    similar_events = models.ManyToManyField(Event, related_name="+")