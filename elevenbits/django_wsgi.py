from os import environ
from django.core.handlers.wsgi import WSGIHandler

environ['DJANGO_SETTINGS_MODULE'] = 'elevenbits.settings'
application = WSGIHandler()