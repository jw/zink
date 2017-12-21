
#
# Copyright (c) 2013-2016 Jan Willems (ElevenBits)
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

from django.conf.urls import url
from blog import views

app_name = 'blog'

urlpatterns = [
    # blog page
    url('', views.blog, name='blog'),

    # pages of blog entries
    url('page/(?P<page>\d+)/', views.blog, name='page'),
    url('page/', views.blog),

    # blog entries per tag (and pages thereof)
    url('tag/(?P<tag>\d+)/', views.tag, name='tag'),
    url('tag/(?P<tag>\d+)/page/(?P<page>\d+)/',
        views.tag,
        name='tagpage'),

    # one single blog entry
    url('(?P<id>\d+)/', views.detail, name='detail'),
]
