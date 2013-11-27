
#
# Zink
#

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',

    # blog page
    url(r'^$', 'blog.views.blog', name='blog'),

    # pages of blog entries
    url(r'^/page/(?P<page>\d+)/$', 'blog.views.blog', name='page'),
    url(r'^/page/$', 'blog.views.blog'),

    # blog entries per tag (and pages thereof)
    url(r'^/tag/(?P<tag>\d+)/$', 'blog.views.tag', name='tag'),
    url(r'^/tag/(?P<tag>\d+)/page/(?P<page>\d+)/$',
        'blog.views.tag',
        name='tagpage'),

    # one single blog entry
    url(r'^/(?P<id>\d+)/$', 'blog.views.detail', name='detail'),
)
