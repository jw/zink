
#
# Copyright (C) 2013-2014 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

#
# public settings for [www.]elevenbits.org, [www.]elevenbits.com,
# vonk.elevenbits.org and m8n.be
#

from os.path import join, dirname, realpath
from socket import gethostname

SITE_ROOT = dirname(realpath(join(__file__, "..")))

hostname = gethostname()
if hostname.startswith("vonk"):
    HOSTNAME = "vonk"
elif "elevenbits" in hostname:
    HOSTNAME = "elevenbits"
elif "antwerp" in hostname:
    HOSTNAME = "antwerp"
elif "m8n" in hostname:
    HOSTNAME = "m8n"
else:
    print(hostname + " is an unknown hostname; using localhost as default")
    # TODO: this is not secure!
    HOSTNAME = "localhost"

DEBUG = False
if HOSTNAME in ["antwerp", "localhost", '127.0.0.1']:
    DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ["localhost", ".elevenbits.com", ".elevenbits.org", ".m8n.be"]

#
# Test properties
#

# TODO: check existence of rainbowtests first
TEST_RUNNER = 'rainbowtests.RainbowTestSuiteRunner'

# TODO: check this
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # needed for current menu identifier:
    "django.core.context_processors.request",
)


#
# Debug toolbar
#

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

# Note:
# never add 'debug_toolbar.middleware.DebugToolbarMiddleware' to
# the debug panel!
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

TIME_ZONE = 'Europe/Brussels'
LANGUAGE_CODE = 'en-BE'

# TODO: check this. Is this handy when using m8n.be, elevenbits.(com|org)
SITE_ID = 1

# use i18n, l10n and make dates time zone
USE_I18N = True
USE_L10N = True
USE_TZ = False

# The statics (css and images) location
# TODO: check this
STATICFILES_DIRS = (
    "",
)

# TODO: read up on this
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

# TODO: check this
# static location
STATIC_ROOT = '/var/www/zink/static/'
STATIC_URL = "http://elevenbits.org/static/"

# TODO: check this
# upload location
MEDIA_ROOT = "/var/www/zink/media/"
MEDIA_URL = "http://elevenbits.org/media/"

FIXTURE_DIRS = (join(SITE_ROOT, 'fixtures'),)

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
    'django.template.loaders.filesystem.Loader',
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
    'tracking.middleware.VisitorTrackingMiddleware',
    'tracking.middleware.VisitorCleanUpMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

ROOT_URLCONF = 'elevenbits.urls'

WSGI_APPLICATION = 'elevenbits.wsgi.application'

CRONJOBS = [
    ('*/5 * * * *', 'tweeter.admin.get_latest_tweets'),
]

# tweeter.admin

TEMPLATE_DIRS = (
    join(dirname(__file__), 'templates').replace('\\', '/'),
)

INSTALLED_APPS = (
    # django contribs
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # zink apps
    # 'elevenbits.index',
    'elevenbits.menu_extras',  # TODO: move this in apps root
    'blog',
    'elevenbits.static',  # TODO: move this in apps root
    'contact',
    'home',
    # 'elevenbits.services',
    'elevenbits.deployment',
    'elevenbits',
    # utility apps
    'treemenus',  # TODO: make sure to use the proper (Russian) one!
    'elevenbits.menu_extras',

    'tracking',

    'util',

    'django_crontab',
    'tweeter',


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
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s ' +
                      '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'elevenbits': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

from .local_settings import *
