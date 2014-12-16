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
    slug = models.SlugField(null=True, blank=True, help_text="The part of the title that is used in the url. "
                                                             "Leave blank for auto-fill")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)

        return super(TitleAndSlugModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title


class GeoModelMixin(models.Model):
    zipcode = models.CharField(max_length=10, blank=True, db_index=True)
    longitude = models.DecimalField(null=True, blank=True, decimal_places=8, max_digits=15, db_index=True,
                                    help_text="longitude, leave empty for auto-fill")
    latitude = models.DecimalField(null=True, blank=True, decimal_places=8, max_digits=15, db_index=True,
                                   help_text="latitude, leave empty for auto-fill")

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(GeoModelMixin, self).__init__(*args, **kwargs)
        self.__zipcode = self.zipcode
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
        if (self.zipcode != self.__zipcode or self.address != self.__address or self.city != self.__city or self.country != self.__country ) and \
           (self.zipcode or self.address or self.city or self.country) and hasattr(self, 'get_full_location'):
            full_location = self.get_full_location()
            if full_location != self.__location:
                try:
                    self.latitude, self.longitude = geocode_location(full_location)
                except ValueError:
                    pass
        return super(GeoModelMixin, self).save(*args, **kwargs)


class AddressMixin(GeoModelMixin):
    address = models.CharField(max_length=250, null=True, blank=True)
    address_line_2 = models.CharField(max_length=250, null=True, blank=True)
    address_line_3 = models.CharField(max_length=250, null=True, blank=True)
    city = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    state = models.CharField(max_length=150, null=True, blank=True, db_index=True)
    country = CountryField(null=True, blank=True, default="US", db_index=True)

    def get_location(self):
        if self.country == "US":
            if self.address:
                return "%s" % self.address
            elif self.state and self.city and self.zipcode:
                return "%s, %s, %s" % (self.city, self.zipcode, self.state)
            elif self.zipcode and self.state:
                return "%s, %s" % (self.zipcode, self.state)
            elif self.zipcode and self.city:
                return "%s, %s" % (self.city, self.zipcode)
            elif self.city and self.state:
                return "%s, %s" % (self.city, self.state)
            elif self.zipcode:
                return "zipcode %s" % self.zipcode
            elif self.state:
                return "%s" % self.state
            elif self.city:
                return "%s" % self.city
        else:
            if self.city and self.zipcode:
                return "%s, %s, %s" % (self.city, self.zipcode, self.get_country_display() )
            elif self.city:
                return "%s, %s" % (self.city, self.get_country_display() )
            else:
                return "%s" % self.get_country_display()

    def get_full_location(self):
        l = self.get_location()
        if not l:
            return ""
        if self.country == "US":
            return "%s, %s" % (l, self.get_country_display())
        return l

    class Meta:
        abstract = True
