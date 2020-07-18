from django.contrib import admin
from django.urls import path, include

from blog.views import MySearchView
from zink.views import home, stilus, contact

urlpatterns = [
    path('', home, name='home'),
    path('stilus/', stilus, name="stilus"),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', contact, name="contact"),
    path('search/', MySearchView.as_view(), name="search_view"),
    path('admin/', admin.site.urls),
]
