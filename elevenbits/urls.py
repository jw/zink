
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import include, path
from django.views.generic import TemplateView, RedirectView

from blog import views
from . import settings

admin.autodiscover()

app_name = "elevenbits"

urlpatterns = [

    path('', views.home, name='home'),
    path('stilus/', views.stilus, name='stilus'),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', include('contact.urls', namespace='contact')),
    path('search', include('haystack.urls')),
    path('foo', views.empty, name='empty'),

    # robots.txt
    path('robots.txt',
         TemplateView.as_view(template_name='robots.txt',
                              content_type='text/plain'),
         name='robots'),

    # favicon.ico
    # path('favicon.ico',
    #      RedirectView.as_view(
    #          url=staticfiles_storage.url('favicon.ico'),
    #          permanent=False),
    #      name="favicon"),

    # 404 and 500 return codes
    path('500',
         TemplateView.as_view(
             template_name='500.html',
             extra_context={'assets': {'title': 'ElevenBits'}}
         ),
         name='500'),
    path('404',
         TemplateView.as_view(
            template_name='404.html',
            extra_context={'assets': {'title': 'ElevenBits'}}
         ),
         name='404'),

    # admin
    path('admin/', admin.site.urls),
    path('admin/doc/', include('django.contrib.admindocs.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
              static(settings.STATIC_URL,
                     document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
