from django.conf.urls.defaults import *

# the elevenbits pages
from elevenbits.views import home

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Hello world
    ('^$', home),
    
    # menu
    (r'^menu/$', 'elevenbits.menu.views.index'),

    # blog
    (r'^blog/$', 'elevenbits.blog.views.index'),
    (r'^blog/(?P<id>\d+)/$', 'elevenbits.blog.views.detail'),

    # tags
    (r'^tag/$', 'elevenbits.blog.views.index'),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
