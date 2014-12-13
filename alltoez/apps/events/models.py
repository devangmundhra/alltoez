import json, urllib

from django.db import models
from django.conf import settings

from jsonfield import JSONField
from location_field.models.plain import PlainLocationField
from phonenumber_field.modelfields import PhoneNumberField

from apps.alltoez.utils.model_utils import unique_slugify


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
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    draft = models.ForeignKey(DraftEvent, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    category = models.ManyToManyField(Category, db_index=True)
    address = models.TextField()
    location = PlainLocationField(based_fields=[address], zoom=16)
    neighborhood = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Neigborhood of activity. Leave blank for auto-fill")
    phone_number = PhoneNumberField(blank=True, help_text="Phone number, if available")
    image = JSONField(default="{\"url\":\"\",\"source_name\":\"\",\"source_url\":\"\"}")
    DEFAULT_MIN_AGE_EVENT = 0
    min_age = models.PositiveSmallIntegerField(default=DEFAULT_MIN_AGE_EVENT, db_index=True)
    DEFAULT_MAX_AGE_EVENT = 100
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
    time_detail = models.CharField(max_length=500, help_text="Enter time for different days, in different rows")
    url = models.URLField(blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at', '-start_date', 'end_date']

    def save(self, *args, **kwargs):
        if not self.neighborhood:
            self.neighborhood = Event.get_location_neighborhood(self.location)
        if not self.slug:
            unique_slugify(self, self.title)
        super(Event, self).save(*args, **kwargs)

    @classmethod
    def get_location_neighborhood(cls, latlng):

        google_maps_api_key = getattr(settings, 'GOOGLE_MAPS_V3_APIKEY', None)
        qt_latlng = urllib.quote_plus(latlng)
        result_type = 'neighborhood'
        geo = urllib.urlopen("https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}&result_type={2}".
                             format(qt_latlng,
                             google_maps_api_key,result_type))
        res = json.loads(geo.read())
        if res['status'] != 'OK':
            return ""
        # Example https://maps.googleapis.com/maps/api/geocodhttps://maps.googleapis.com/maps/api/geocode/json?latlng=37.7628848%2C-122.428514&key=AIzaSyDOtkrcR4QFGYTMdR71WkkUYsMQ735c_EU&result_type=neighborhood
        address = res['results'][0]['address_components'][0]['short_name']
        return address

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
