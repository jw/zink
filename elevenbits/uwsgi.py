from os import environ
settings = 'elevenbits.settings'
environ['DJANGO_SETTINGS_MODULE'] = settings

print("Starting uwsgi application (via %s)..." % settings)

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler()

print("Started uwsgi application successfully.")
