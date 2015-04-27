__author__ = 'devangmundhra'

from datetime import datetime, timedelta

from haystack import indexes
from apps.events.models import Event


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    categories = indexes.FacetMultiValueField()
    title = indexes.CharField(model_attr='title')
    end_date = indexes.DateField(model_attr='end_date', default=lambda: datetime.now()+timedelta(days=(30*365)))
                                                                            # If no expiry, expire after 30 years
    city = indexes.CharField(model_attr='venue__city', faceted=True, null=True)
    neighborhood = indexes.CharField(model_attr='venue__neighborhood', faceted=True, null=True)
    point = indexes.LocationField(model_attr='venue__point', null=True)

    # We add this for autocomplete.
    title_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Event

    def prepare_categories(self, obj):
        return [category.name for category in obj.category.all()]