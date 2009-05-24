from django.conf.urls.defaults import *

# the elevenbits pages
from elevenbits.views import home

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Hello world
    ('^$', home),
    
    # blog
    (r'^blog/$', 'elevenbits.blog.views.index'),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
