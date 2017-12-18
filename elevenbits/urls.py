
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

from django.urls import include, path
from django.views.generic.base import TemplateView, RedirectView

from django.contrib import admin
admin.autodiscover()

from . import settings

app_name = "elevenbits"

urlpatterns = [
    # robots.txt
    path(r'^robots\.txt$',
        TemplateView.as_view(template_name='robots.txt',
                             content_type='text/plain'),
        name='robots'),

    # 404 and 500 return codes
    path(r'^500$', TemplateView.as_view(template_name='500.html'), name='500'),
    path(r'^404$', TemplateView.as_view(template_name='404.html'), name='404'),

    # home, blog and contact sections
    path(r'^$', RedirectView.as_view(url='/home')),
    path(r'^home', include('home.urls')),
    path(r'^blog', include('blog.urls')),
    path(r'^contact', include('contact.urls')),

    path(r'^search', include('search.urls')),

    # TODO: handle these later
    # url(r'^tracking/', include('tracking.urls')),

    # admin
    path(r'^admin/', admin.site.urls),
    path(r'^admin/doc/', include('django.contrib.admindocs.urls')),

]  # + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(path(r'^__debug__/', include(debug_toolbar.urls)))
