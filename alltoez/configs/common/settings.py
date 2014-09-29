import os, django, urllib
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _

#-------------------------------------------------------------------------------
#	BASE SETTINGS
#-------------------------------------------------------------------------------
DEBUG = True
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)
SECRET_KEY = '-x83)5-^cugn@*t6gh%76j@cb)zj)q7l_rm!%3=)@sw&v&d_ww'

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
ADMIN_MEDIA_PREFIX = "/static/admin/"
STATIC_ROOT = os.path.join(SITE_ROOT, "static")
MEDIA_ROOT = os.path.join(SITE_ROOT, "media")
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

ADMINS = (('Raw Jam Dev', 'dev@rawjam.co.uk')),
MANAGERS = ('Raw Jam Dev', 'dev@rawjam.co.uk'),

# Local time
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
SITE_ID = 1
USE_I18N = False
DATE_INPUT_FORMATS = ('%d-%m-%Y','%Y-%m-%d')
USE_TZ = True

TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.Loader',
	'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
	"allauth.account.auth_backends.AuthenticationBackend",
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.media",
	'django.core.context_processors.static',
	"django.core.context_processors.request",
	"django.contrib.messages.context_processors.messages",
	"apps.alltoez.context_processors.app_wide_vars",
	"allauth.account.context_processors.account",
	"allauth.socialaccount.context_processors.socialaccount",
)

MIDDLEWARE_CLASSES = [
	'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'pipeline.middleware.MinifyHTMLMiddleware',
]
TEMPLATE_DIRS = (
	os.path.join(SITE_ROOT, 'templates'),
)

INSTALLED_APPS = [
	# Base Django Apps
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'djangocms_admin_style',
	'admin_shortcuts',
	'django.contrib.admin',
	'django.contrib.sitemaps',
	'django.contrib.humanize',

	# Utilities & Helper Apps
	'south',
	'filebrowser',
	'django_extensions',
	'endless_pagination',
	'pipeline',

	# Registration, Signin and Account Management
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.facebook',

	# Local Project Apps
	'apps.alltoez_profile',
	'apps.alltoez',
	'apps.events',
]

#if DEBUG:
#	TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.debug',)
#	MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
#	INSTALLED_APPS += ('debug_toolbar',)

if USE_I18N:
	TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.i18n',)


#-------------------------------------------------------------------------------
#	APP SETTINGS
#-------------------------------------------------------------------------------
DEFAULT_PROFILE_IMAGE = os.path.join(MEDIA_ROOT, 'uploads/alltoez_defaults/profile_portrait_default.png')
GOOGLE_ANALYTICS_CODE = None
LANGUAGES = (
    ('en', _('English')),
)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': 'alltoez',
		# 'USER': 'XXXXX',
		# 'PASSWORD': 'XXXX',
		'HOST': 'localhost',
	}
}
ROOT_URLCONF = 'alltoez.configs.common.urls'
AUTH_PROFILE_MODULE = 'alltoez_profile.UserProfile'

DEFAULT_FROM_EMAIL = 'noreply@rawjam.co.uk'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'noreply@rawjam.co.uk'
EMAIL_HOST_PASSWORD = '2M5394'


#-------------------------------------------------------------------------------
#	CACHE SETTINGS
#-------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '127.0.0.1:11211',
		'KEY_PREFIX': 'alltoez:'
    }
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'alltoez:'


#-------------------------------------------------------------------------------
#	PIPELINE SETTINGS
#-------------------------------------------------------------------------------
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_YUGLIFY_BINARY = os.path.join(SITE_ROOT, "../node_modules/yuglify/bin/yuglify")
PIPELINE_DISABLE_WRAPPER = True
PIPELINE_COMPILERS = (
'pipeline.compilers.less.LessCompiler',
)
PIPELINE_LESS_BINARY = 'lessc'
PIPELINE_CSS = {
	'theme': {
		'source_filenames': (
			'css/chosen.css',
			'less/theme.less' if not DEBUG else ''
		),
		'output_filename': 'css/theme.min.css',
		'variant': 'datauri'
	},
}
PIPELINE_JS = {
	'base': {
		'source_filenames': (
			'js/main.js',
			'js/ajax_request.js',
			'js/lib/jquery.class.js',
			'js/lib/jquery.cookie.js',
			'js/lib/bootstrap.min.js',
			'js/lib/chosen.jquery.min.js',
		),
		'output_filename': 'js/base.min.js',
	},
}


#-------------------------------------------------------------------------------
#	ALLAUTH SETTINGS
#-------------------------------------------------------------------------------
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = "/"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_AVATAR_SUPPORT = False
EMAIL_CONFIRMATION_DAYS = 99
FACEBOOK_ENABLED = True
TWITTER_ENABLED = True
OPENID_ENABLED = False
SOCIALACCOUNT_ENABLED = True
SOCIALACCOUNT_PROVIDERS = {}


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
	'thumb', 'small','medium','large',
]


#-------------------------------------------------------------------------------
#	CELERY SETTINGS
#-------------------------------------------------------------------------------
BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

CELERYBEAT_SCHEDULE = {
    'parse-events-every-day': {
        'task': 'events.tasks.scrape_events_look_ahead',
        'schedule': timedelta(days=1),
    },
}


CELERY_TASK_PUBLISH_RETRY_POLICY = {
    'max_retries': 15,
    'interval_start': 1,
    'interval_step': 10,
    'interval_max': 3600,
}


#-------------------------------------------------------------------------------
#	ADMIN SHORTCUT SETTINGS
#-------------------------------------------------------------------------------
ADMIN_SHORTCUTS = [
	{
		'shortcuts': [
			{
				'url': '/',
				'open_new_window': True,
			},
			{
				'url': '/admin/filebrowser/browse/',
				'title': 'Files',
				'class': 'folder'
			},
			{
				'url_name': 'admin:auth_user_changelist',
				'title': 'Users',
			},
		]
	},
]
ADMIN_SHORTCUTS_SETTINGS = {
	'hide_app_list': False,
	'open_new_window': False,
}

try:
	from local_settings import *
except ImportError:
	pass
