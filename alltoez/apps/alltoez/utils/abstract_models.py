from django.db import models
from django.contrib.auth.models import User

from filebrowser.fields import FileBrowseField

from apps.alltoez.utils.model_utils import unique_slugify
from apps.alltoez.utils.geo import geocode_location
from apps.alltoez.utils.fields import CountryField

"""
    Abstract model classes that define common uses cases
"""

class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return "%s" % self.id

class PhotoModel(BaseModel):
    submitted_by = models.ForeignKey(User)
    caption = models.TextField(blank=True, null=True)
    photo = FileBrowseField('Image (Initial Directory)', max_length=100, directory='uploads/')
    is_default = models.BooleanField(default=False)

    class Meta:
        abstract = True

class TitleAndSlugModel(BaseModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True, help_text="The part of the title that is used in the url. Leave this blank if you want the system to generate one for you.")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)

        return super(TitleAndSlugModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

class GeoModelMixin(models.Model):
    postcode = models.CharField(max_length=10, blank=True, db_index=True)
    longitude = models.DecimalField(null=True, blank=True, decimal_places=8, max_digits=15, db_index=True)
    latitude = models.DecimalField(null=True, blank=True, decimal_places=8, max_digits=15, db_index=True)

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(GeoModelMixin, self).__init__(*args, **kwargs)
        self.__postcode = self.postcode
        try:
            self.__address   = self._meta.get_field_by_name('address')
            self.__city      = self._meta.get_field_by_name('city')
            self.__state     = self._meta.get_field_by_name('state')
            self.__country   = self._meta.get_field_by_name('country')
            if hasattr(self, 'get_full_location'):
                self.__location = self.get_full_location()
        except models.FieldDoesNotExist:
            pass

    def save(self, *args, **kwargs):

        if (self.postcode != self.__postcode or self.address != self.__address or self.city != self.__city or self.country != self.__country ) and \
           (self.postcode or self.address or self.city or self.country) and hasattr(self, 'get_full_location'):
            full_location = self.get_full_location()
            if full_location != self.__location:
                try:
                    self.latitude, self.longitude = geocode_location(full_location)
                except GeocodeError:
                    pass
        return super(GeoModelMixin, self).save(*args, **kwargs)

class AddressMixin(GeoModelMixin):
    address = models.CharField(max_length=250, null=True, blank=True)
    address_line_2 = models.CharField(max_length=250, null=True, blank=True)
    address_line_3 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    state = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    country = CountryField(null=True, blank=True, default="GB", db_index=True)

    def get_location(self):
        if self.country == "US":
            if self.state and self.city and self.postcode:
                return "%s, %s, %s" % (self.city, self.postcode, self.state)
            elif self.postcode and self.state:
                return "%s, %s" % (self.postcode, self.state)
            elif self.postcode and self.city:
                return "%s, %s" % (self.city, self.postcode)
            elif self.city and self.state:
                return "%s, %s" % (self.city, self.state)
            elif self.postcode:
                return "postcode %s" % self.postcode
            elif self.state:
                return "%s" % self.state
            elif self.city:
                return "%s" % self.city
        else:
            if self.city and self.postcode:
                return "%s, %s, %s" % (self.city, self.postcode, self.get_country_display() )
            elif self.city:
                return "%s, %s" % (self.city, self.get_country_display() )
            else:
                return "%s" % self.get_country_display()

    def get_full_location(self):
        l = self.get_location()
        if not l: return ""
        if self.country == "US":
            return "%s, %s" % (l, self.get_country_display())
        return l

    class Meta:
        abstract = True
