from django.conf.urls.defaults import *

from elevenbits.views import home


# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^$', home),

    # Example:
    # (r'^elevenbits/', include('elevenbits.foo.urls')),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
