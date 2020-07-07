from django.contrib import admin
from django.urls import path, include

from zink.views import home, stilus, contact

urlpatterns = [
    path('', home, name='home'),
    path('stilus/', stilus, name="stilus"),
    path('blog/', include('blog.urls', namespace='blog')),
    path('contact/', contact, name="contact"),
    path('admin/', admin.site.urls),
]
