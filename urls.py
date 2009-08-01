from django.conf.urls.defaults import *

# the elevenbits pages
from elevenbits.views import home

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # menu - seems quite useless to me
    (r'^menu/$', 'elevenbits.menu.views.index'),

    # blog
    ('^$', 'elevenbits.blog.views.index'),
    (r'^page/(?P<page>\d+)/$', 'elevenbits.blog.views.index'),
    (r'^page/$', 'elevenbits.blog.views.index'),
    (r'^detail/(?P<id>\d+)/$', 'elevenbits.blog.views.detail'),

    # tags
    (r'^tag/(?P<tag>\w+)/$', 'elevenbits.blog.views.tags'),

    # about
    (r'^about/', 'elevenbits.about.views.index'),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
