from haystack import indexes
from celery_haystack.indexes import CelerySearchIndex

from feedback.models import Opinion


class OpinionIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    created = indexes.DateTimeField(model_attr='created')
    url = indexes.CharField(model_attr='url')
    user_agent = indexes.CharField(model_attr='user_agent')
    product = indexes.CharField(model_attr='product')
    version = indexes.CharField(model_attr='version')
    platform = indexes.CharField(model_attr='platform')
    locale = indexes.CharField(model_attr='locale')
    manufacturer = indexes.CharField(model_attr='manufacturer')
    device = indexes.CharField(model_attr='device')

    def get_model(self):
        return Opinion

    def index_queryset(self):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter()
