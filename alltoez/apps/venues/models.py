from django.db import models

from phonenumber_field.modelfields import PhoneNumberField

from apps.alltoez.utils.abstract_models import BaseModel, AddressMixin
from apps.alltoez.utils.geo import rev_geocode_location_component
from apps.alltoez.utils.model_utils import unique_slugify


class Venue(BaseModel, AddressMixin):
    """
    Model to store information about venues
    """
    __original_name = None
    name = models.CharField(max_length=200, verbose_name='Venue name')
    slug = models.SlugField(null=True, blank=True,
                            help_text="The part of the name (if provided) that is used in the url. \
                            Leave this blank if you want the system to generate one for you.")
    neighborhood = models.CharField(max_length=200, blank=True, null=True,
                                    help_text="Neigborhood/rough area of venue. Leave blank for auto-fill")
    phone_number = PhoneNumberField(blank=True, verbose_name="Phone number", help_text="Phone number, if available")
    yelp_url = models.URLField(blank=True, null=True, verbose_name='Yelp Url')

    def __init__(self, *args, **kwargs):
        super(Venue, self).__init__(*args, **kwargs)
        self.__original_name = self.name

    def save(self, *args, **kwargs):
        if not self.slug or self.name != self.__original_name:
            unique_slugify(self, self.name)
        super(Venue, self).save(*args, **kwargs)
        # This is a bit hacky, need to do this twice because latitude/longitude are plugged in during
        # call to super's save
        if self.latitude and self.longitude and not self.neighborhood:
            if not self.neighborhood:
                self.neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'neighborhood')
            if not self.neighborhood:
                #If not succeed in first try, try again (with a bigger net)
                self.neighborhood = rev_geocode_location_component(self.latitude, self.longitude, 'political')
            super(Venue, self).save(*args, **kwargs)
        self.__original_name = self.name

    def __unicode__(self):
        return unicode(self.name)