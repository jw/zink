from django.conf.urls.defaults import *

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^elevenbits/', include('elevenbits.foo.urls')),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
