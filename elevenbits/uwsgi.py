from os import environ
from django.core.handlers.wsgi import WSGIHandler

print("Starting uwsgi application...")
environ['DJANGO_SETTINGS_MODULE'] = 'elevenbits.settings'
application = WSGIHandler()
print("Started uwsgi application...")
