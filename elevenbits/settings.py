
#
# settings for [www.]elevenbits.org, [www.]elevenbits.com, vonk.elevenbits.org and m8n.be
#

from os.path import join, dirname, realpath
from socket import gethostname

SITE_ROOT = dirname(realpath(join(__file__, "..")))

# get the hostname
if (gethostname().startswith("vonk")):
    HOSTNAME = "vonk"
elif ("elevenbits" in gethostname()):
    HOSTNAME = "elevenbits"
elif ("antwerp" in gethostname()):
    HOSTNAME = "antwerp"
elif ("m8n" in gethostname()):
    HOSTNAME = "m8n"
else:
    print(gethostname() + " is an unknown hostname; using localhost as default")
    HOSTNAME = "localhost"

DEBUG = False
if (HOSTNAME in ["antwerp", "localhost"]):
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

#
# Debug toolbar
#

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Note: never add 'debug_toolbar.middleware.DebugToolbarMiddleware' to the debug panel!
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

#
# Administrators
#

ADMINS = (
    ('Jan Willems', 'jw@elevenbits.com'),
)
MANAGERS = ADMINS

#
# Database
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'Reinhardt',
        'HOST': 'localhost',
        'DATABASE_PORT': '',
    }
}

TIME_ZONE = 'Europe/Brussels'
LANGUAGE_CODE = 'en-BE'

SITE_ID = 1

# use i18n, l10n and make dates time zone
USE_I18N = True
USE_L10N = True
USE_TZ = False

# The statics (css and images) location
STATICFILES_DIRS = (
    "",
)

# TODO: read up on this
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# static location
STATIC_ROOT = '/var/www/zink/static/'
STATIC_URL = "http://localhost/static/"

# upload location
MEDIA_ROOT = "/var/www/zink/media/"
MEDIA_URL = "http://localhost/media/"

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0u^l=%@(2_imjrza(c4hgitd2a^)bn0%)s8496m9!aoshfisqef3rf-j+sdxesq1'

# TODO: read up on this
#CONTEXT_PREPROCESSORS = (
#    "django.contrib.auth.context_processors.auth",
#    "django.core.context_processors.debug",
#    "django.core.context_processors.i18n",
#    "django.core.context_processors.media",
#    "django.core.context_processors.static",
#    "django.core.context_processors.tz",
#    "django.contrib.messages.context_processors.messages",
#)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'tracking.middleware.BannedIPMiddleware',
#    'django.middleware.gzip.GZipMiddleware',
#    'django.middleware.common.CommonMiddleware',
#    'django.contrib.sessions.middleware.SessionMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    'tracking.middleware.VisitorCleanUpMiddleware',

#    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'elevenbits.urls'

WSGI_APPLICATION = 'elevenbits.wsgi.application'

TEMPLATE_DIRS = (
    join(dirname(__file__), 'templates').replace('\\','/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'django.contrib.staticfiles',
    'elevenbits.index',
    'elevenbits.blog',
    'elevenbits.static',
    'elevenbits.deployment',
    'elevenbits',
    #'treemenus',
    'tracking',
    'south',
    'debug_toolbar',
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4
CLIENT_LOGO_MARGIN = 20

#
# TODO: update the logging part
#

LOGGING = { 
   'version': 1,
   'disable_existing_loggers': True,
   'formatters': {
       'simple': {
           'format': '%(levelname)s %(message)s',
       },  
   },  
   'handlers': {
       'console':{
           'level':'DEBUG',
           'class':'logging.StreamHandler',
           'formatter': 'simple'
       },  
   },  
   'loggers': {
       'django': {
           'handlers': ['console'],
           'level': 'DEBUG',
       },  
   }   
}

