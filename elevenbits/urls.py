
#
# Zink
#

from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView

from django.contrib import admin
import settings

admin.autodiscover()

urlpatterns = patterns(
    '',

    # robots.txt
    url(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain'),
        name='robots'),

    # 404 and 500 return codes
    url(r'^500$', TemplateView.as_view(template_name='500.html'), name='500'),
    url(r'^404$', TemplateView.as_view(template_name='404.html'), name='404'),

    # home, blog and contact sections
    url(r'^$', include('home.urls', namespace='home')),
    url(r'^blog', include('blog.urls', namespace='blog')),
    url(r'^contact', include('contact.urls', namespace='contact')),

    # TODO: handle these later
    url(r'^services', 'elevenbits.services.views.services'),
    url(r'^clients', 'elevenbits.index.views.clients'),
    url(r'^projects', 'elevenbits.index.views.projects'),
    #url(r'^tracking/', include('tracking.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
