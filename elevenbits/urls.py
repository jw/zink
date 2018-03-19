
from django.urls import include, path
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf.urls.static import static
from django.contrib import admin

from . import settings

admin.autodiscover()

app_name = "elevenbits"

urlpatterns = [

    # robots.txt
    path('robots.txt',
         TemplateView.as_view(template_name='robots.txt',
                              content_type='text/plain'),
         name='robots'),

    # favicon.ico
    path('favicon.ico',
         RedirectView.as_view(
             url=staticfiles_storage.url('favicon.ico'),
             permanent=False),
         name="favicon"),

    # 404 and 500 return codes
    path('500', TemplateView.as_view(template_name='500.html'), name='500'),
    path('404', TemplateView.as_view(template_name='404.html'), name='404'),

    # home, blog and contact sections
    path('', RedirectView.as_view(url='/home')),
    path('home', include('home.urls', namespace='home')),
    path('blog', include('blog.urls', namespace='blog')),
    path('contact', include('contact.urls', namespace='contact')),

    path('search', include('search.urls')),

    # TODO: handle these later
    # url('tracking/', include('tracking.urls')),

    # admin
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
