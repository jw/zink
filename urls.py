from django.conf.urls.defaults import *

# enable the admin
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # photologue
    (r'^photologue/', include('photologue.urls')),

    # blog
    ('^$', 'elevenbits.blog.views.index'),
    (r'^page/(?P<page>\d+)/$', 'elevenbits.blog.views.index'),
    (r'^page/$', 'elevenbits.blog.views.index'),
    (r'^detail/(?P<id>\d+)/$', 'elevenbits.blog.views.detail'),

    # tags
    (r'^tag/(?P<tag>\w+)/page/(?P<page>\d+)$', 'elevenbits.blog.views.tags'),
    (r'^tag/(?P<tag>\w+)', 'elevenbits.blog.views.tags'),

    # elevenbits
    (r'^elevenbits/clients/', 'elevenbits.firm.views.clients'),
    (r'^elevenbits/projects/', 'elevenbits.firm.views.projects'),
    (r'^elevenbits/about/', 'elevenbits.firm.views.about'),
    (r'^elevenbits/contact/', 'elevenbits.firm.views.contact'),

    # admin
    (r'^admin/(.*)', admin.site.root),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

)
