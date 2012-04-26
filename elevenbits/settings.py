#
# elevenbits.org (and later elevenbits.com and m8n.be)
#

from os.path import join, dirname, realpath

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
USE_TZ = True

#### tbd: start: needs to be checked with Django 1.4

# The css and images location
MEDIA_URL = 'http://www.elevenbits.com/media'
MEDIA_ROOT = join(dirname(__file__), "media")
# It might be better to place this in '/admin/'
ADMIN_MEDIA_PREFIX = '/media/'

#### tbd: stop: needs to be checked with Django 1.4

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0u^l=%@(2_imjrza(c4hgitd2a^)bn0%)8496m9!asshisqdf3rf-j+sdwxesq1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'elevenbits.guest.middleware.GuestMiddleware',
)

ROOT_URLCONF = 'elevenbits.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'elevenbits.wsgi.application'

TEMPLATE_DIRS = (
    join(dirname(__file__), 'templates').replace('\\','/'),
)

SITE_ROOT = dirname(realpath(join(__file__, "..")))

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.markup',
    'elevenbits.blog',
    'elevenbits.static',
    'elevenbits.guest',
    'elevenbits',
    'treemenus',
#    'photologue',
#    'fccv',
)

#
# ElevenBits constants
#

BLOG_PAGE_SIZE = 4

#
# log properly
#

#### TODO: update the logging part
import logging
logging.basicConfig(
    level = logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filename =  '/tmp/elevenbits.log',
    filemode = 'w'
)