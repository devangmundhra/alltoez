__author__ = 'devangmundhra'

from haystack import indexes
from apps.venues.models import Venue


class VenueIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')

    def get_model(self):
        return Venue
