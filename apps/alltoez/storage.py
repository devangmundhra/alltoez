__author__ = 'devangmundhra'

import urlparse

from django.contrib.staticfiles.storage import ManifestFilesMixin
from django.conf import settings

from pipeline.storage import PipelineMixin, GZIPMixin, PipelineStorage

from storages.backends.s3boto import S3BotoStorage


def domain(url):
    return urlparse.urlparse(url).hostname


class S3GZipPipelineStorage(PipelineMixin, GZIPMixin, ManifestFilesMixin, S3BotoStorage):
    bucket_name = settings.STATIC_FILES_BUCKET
    custom_domain = settings.STATIC_S3_DOMAIN


class MediaFilesStorage(S3BotoStorage):
    def __init__(self, *args, **kwargs):
        kwargs['bucket'] = settings.MEDIA_FILES_BUCKET
        kwargs['custom_domain'] = domain(settings.MEDIA_URL)
        super(MediaFilesStorage, self).__init__(*args, **kwargs)
