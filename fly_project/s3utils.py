import copy
from django.conf import settings
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage
from compressor.storage import CompressorFileStorage


class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION


class CachedS3BotoStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class("compressor.storage.CompressorFileStorage")()

    def url(self, name):
        url = super(CachedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

    def save(self, name, content):
        content2 = copy.copy(content) #-> THE SECRET IS HERE
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content2) #-> AND HERE
        # print id(content)
        # print id(content2)
        return name

    def get_available_name(self, name):
        if self.exists(name):
            self.delete(name)
        return name
