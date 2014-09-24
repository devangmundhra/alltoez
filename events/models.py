import json, urllib

from django.db import models

from jsonfield import JSONField


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
    * Tours and Trips
        - Museums
        - Aquariums and Zoos
        - Library events
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
    parent_category = models.ForeignKey('self', null=True, blank=True)
    name = models.CharField(max_length=200, db_index=True)
    description = models.CharField(max_length=200)


class Location(models.Model):
    """
    Location class
    This class stores location information about an event
    """
    address_1 = models.CharField(max_length=200)
    address_2 = models.CharField(max_length=200, blank=True, null=True)
    address_3 = models.CharField(max_length=200, blank=True, null=True)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    postcode = models.CharField(max_length=15)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    formatted_address = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        geo = json.loads(Location.get_latlon("%s,%s,%s,%s %s" % (self.address_1, self.address_2, self.address_3,
                                                                 self.city, self.postcode)))
        if geo['status'] == "OK":
            self.latitude = geo['results'][0]['geometry']['location']['lat']
            self.longitude = geo['results'][0]['geometry']['location']['lng']
            self.formatted_address = geo['results'][0]['formatted_address']
        super(Location, self).save(*args, **kwargs)

    @classmethod
    def get_latlon(cls, address):
        qt_address = urllib.quote_plus(address)
        geo = urllib.urlopen("http://maps.googleapis.com/maps/api/geocode/json?sensor=false&address=%s" % qt_address)
        return geo.read()


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


class Event(models.Model):
    """
    Event class
    This class describes the details of an event.
    The class also contains information about recurring events.
    TODO: Implement recurring event.
    More about implementing recurring events at: http://stackoverflow.com/q/5183630/712476
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    draft = models.ForeignKey(DraftEvent, blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    description = models.TextField()
    category = models.ManyToManyField(Category, db_index=True)
    location = JSONField()
    image = JSONField()
    min_age = models.PositiveSmallIntegerField(default=0)
    max_age = models.PositiveSmallIntegerField(default=100)
    cost = models.PositiveSmallIntegerField(default=0)
    recurring = models.BooleanField(default=False)
    recurring_start_date = models.DateTimeField(null=True, blank=True)
    recurring_end_date = models.DateTimeField(null=True, blank=True)
    recurring_frequency = JSONField(blank=True, null=True)
    next_date = models.DateTimeField(null=True, blank=True)
    url = models.URLField(blank=True, null=True, unique=True)

    class Meta:
        ordering = ['next_date']

class EventRecord(models.Model):
    """
    EventRecord class
    This class is the actual individual events shown to the user.
    """
    event = models.ForeignKey(Event)
    date = models.DateTimeField(db_index=True)

    class Meta:
        unique_together = ('event', 'date')
        ordering = ['date']