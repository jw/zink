from django.conf.urls.defaults import patterns, include, url
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# enable the admin
from django.contrib import admin
admin.autodiscover()

print("Processing")

urlpatterns = patterns('',
    
    # blog
    url('^$', 'elevenbits.blog.views.index'),
    url(r'^page/(?P<page>\d+)/$', 'elevenbits.blog.views.index'),
    url(r'^page/$', 'elevenbits.blog.views.index'),
    url(r'^detail/(?P<id>\d+)/$', 'elevenbits.blog.views.detail'),

    # tags
    url(r'^tag/(?P<tag>\w+)/page/(?P<page>\d+)$', 'elevenbits.blog.views.tags'),
    url(r'^tag/(?P<tag>\w+)', 'elevenbits.blog.views.tags'),

    # some elevenbits static stuff
    url(r'^elevenbits/clients/', 'elevenbits.firm.views.clients'),
    url(r'^elevenbits/projects/', 'elevenbits.firm.views.projects'),
    url(r'^elevenbits/about/', 'elevenbits.firm.views.about'),
    url(r'^elevenbits/contact/', 'elevenbits.firm.views.contact'),

    # users tracking
    #url(r'^tracking/', include('tracking.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

# only for local development (DEBUG needs to be true for this to work) 
#urlpatterns += staticfiles_urlpatterns()
