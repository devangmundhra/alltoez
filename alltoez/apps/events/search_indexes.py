__author__ = 'devangmundhra'

from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex
from apps.events.models import Event


class EventIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    categories = indexes.FacetMultiValueField()
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(use_template=True)

    def get_model(self):
        return Event

    def prepare_categories(self, obj):
        return [category.name for category in obj.category.all()]