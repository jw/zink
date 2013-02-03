
#
# settings for [www.]elevenbits.org, [www.]elevenbits.com, vonk.elevenbits.org and m8n.be
#

from os.path import join, dirname, realpath
from socket import gethostname

SITE_ROOT = dirname(realpath(join(__file__, "..")))

# derive the site
if (gethostname().startswith("vonk")):
    SITE_NAME = "vonk"
elif ("elevenbits" in gethostname()):
    SITE_NAME = "elevenbits"
elif ("m8n" in gethostname()):
    SITE_NAME = "m8n"
else:
    print("Invalid hostname - please check settings.py; using elevenbits as default")
    SITE_NAME = "elevenbits"

DEBUG = False
if (gethostname() == "antwerp"):
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Jan Willems', 'jw@elevenbits.com'),
)

MANAGERS = ADMINS

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

# use i18n, l10n and make dates time zone aware
USE_I18N = True
USE_L10N = True
USE_TZ = False

# The statics (css and images) location
STATICFILES_DIRS = (
    "",
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
#    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATIC_URL = "/static/"
STATIC_ROOT = '/tmp/statics'

#MEDIA_ROOT = "/home/jw/python/projects/elevenbits/static/"
MEDIA_ROOT = "/var/www/elevenbits/static/"
MEDIA_URL = "http://localhost/static/"

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0u^l=%@(2_imjrza(c4hgitd2a^)bn0%)s8496m9!aoshfisqef3rf-j+sdxesq1'

CONTEXT_PREPROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'tracking.middleware.BannedIPMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'tracking.middleware.VisitorTrackingMiddleware',
    'tracking.middleware.VisitorCleanUpMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
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
    'treemenus',
    'tracking',
    'south',
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4

#
# TODO: update the logging part
# log properly
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

#try:
#    logging.basicConfig(
#        level = logging.DEBUG,
#        format = "%(asctime)s - %(levelname)s - %(message)s",
#        filename =  '/tmp/elevenbits.log',
#        filemode = 'w'
#    )
#except IOError:
#    print("No logging possible - please update the log environment.")
#    print("Please check the /tmp/elevenbits.log permissions.")

