__author__ = 'devangmundhra'

from django.contrib.staticfiles.storage import CachedFilesMixin
from django.conf import settings

from pipeline.storage import PipelineMixin

from storages.backends.s3boto import S3BotoStorage


class S3PipelineStorage(PipelineMixin, CachedFilesMixin, S3BotoStorage):
    bucket_name = settings.STATIC_FILES_BUCKET