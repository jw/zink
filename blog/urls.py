
#
# Copyright (c) 2013-2015 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
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
