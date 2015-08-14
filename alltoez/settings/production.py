from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

SITE_ID = 2

DATABASES = {'default': dj_database_url.config()}
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

PROJECT_DOMAIN = "http://www.alltoez.com"

STATICFILES_STORAGE = 'apps.alltoez.storage.S3GZipPipelineStorage'

STATIC_FILES_BUCKET = 'alltoezstatic'
STATIC_S3_DOMAIN = '%s.s3.amazonaws.com' % STATIC_FILES_BUCKET

STATIC_URL = "https://%s/" % STATIC_S3_DOMAIN

MEDIA_FILES_BUCKET = 'alltoez'
MEDIA_S3_DOMAIN = '%s.s3.amazonaws.com' % MEDIA_FILES_BUCKET
# MEDIA_URL = "https://%s/" % MEDIA_S3_DOMAIN
MEDIA_URL = 'http://d1wqe2m0m7wb9o.cloudfront.net/'

AWS_STORAGE_BUCKET_NAME = MEDIA_FILES_BUCKET
AWS_S3_CUSTOM_DOMAIN = MEDIA_S3_DOMAIN
AWS_CLOUDFRONT_DOMAIN ='http://d1wqe2m0m7wb9o.cloudfront.net'
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }

ALLOWED_HOSTS = [
    '.alltoez.com',
    '.alltoez.herokuapp.com',
]

EMAIL_SUBJECT_PREFIX = "[Alltoez Server]"
SERVER_EMAIL = 'Alltoez Server <server@alltoez.com>'
DEFAULT_FROM_EMAIL = 'Alltoez Postmaster <postmaster@alltoez.com>'
EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

#-------------------------------------------------------------------------------
#	FILEBROWSER SETTINGS
#-------------------------------------------------------------------------------
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + "filebrowser/"
FILEBROWSER_PATH_FILEBROWSER_MEDIA = os.path.join(STATIC_URL, 'filebrowser/')
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg','.jpeg','.gif','.png','.tif','.tiff'],
    'Video': ['.mov','.wmv','.mpeg','.mpg','.avi','.rm','.swf'],
    'Document': ['.pdf','.doc','.rtf','.txt','.xls','.csv'],
    'Sound': ['.mp3','.mp4','.wav','.aiff','.midi','.m4p'],
    'Code': ['.html','.py','.js','.css'],
}
FILEBROWSER_ADMIN_THUMBNAIL = 'fb_thumb'
FILEBROWSER_IMAGE_MAXBLOCK = 1024*1024
FILEBROWSER_MAX_UPLOAD_SIZE = 10485760 # 10485760 bytes = about 10megs
FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumb': {'verbose_name': 'Grid Thumb', 'width': 150, 'height': 150, 'opts': 'crop upscale'},
    'small': {'verbose_name': 'Small (210px)', 'width': 210, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (370px)', 'width': 370, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (530px)', 'width': 530, 'height': '', 'opts': ''},
}
FILEBROWSER_ADMIN_VERSIONS = [
    'thumb', 'small', 'medium', 'large',
]

# Add the debug info apps after local settings has been imported
USE_DEBUG_TOOLBAR = False
if DEBUG and USE_DEBUG_TOOLBAR:
    TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('haystack_panel', 'debug_toolbar',)
    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'haystack_panel.panel.HaystackDebugPanel'
    ]
