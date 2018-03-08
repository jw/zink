
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

from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    # blog page
    path('', views.blog, name='blog'),

    # pages of blog entries
    path('page/<int:page>/', views.blog, name='page'),
    path('page/', views.blog),

    # blog entries per tag (and pages thereof)
    path('tag/<int:tag>/', views.tag, name='tag'),
    path('tag/<int:tag>/page/<int:page>/', views.tag, name='tagpage'),

    # one single blog entry
    path('<int:id>/', views.detail, name='detail'),
]
