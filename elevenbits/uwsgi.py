from os import environ
settings = 'elevenbits.settings'
environ['DJANGO_SETTINGS_MODULE'] = settings

print("Starting uwsgi application (via %s)..." % settings)

from django.core.wsgi import get_wsgi_application  # noqa
application = get_wsgi_application()

print("Started uwsgi application successfully.")
