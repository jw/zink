
#
# settings for elevenbits.org, elevenbits.com and m8n.be
#

from os.path import join, dirname, realpath
from os import uname

SITE_ROOT = dirname(realpath(join(__file__, "..")))

if (uname()[1] == "elevenbits.org" or uname()[1] == "elevenbits.com"):
    DEBUG = False
else:
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

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# The statics (css and images) location
STATICFILES_DIRS = (
    "",
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
#    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATIC_URL = "http://static." + uname()[1]
STATIC_ROOT = '/tmp/statics'

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0u^l=%@(2_imjrza(c4hgitd2a^)bn0%)8496m9!asshisqdf3rf-j+sdwxesq1'

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
    'elevenbits.blog',
    'elevenbits.static',
    'elevenbits.deployment',
    'elevenbits',
    'treemenus',
    'tracking',
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4

#
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

#### TODO: update the logging part
#import logging
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

