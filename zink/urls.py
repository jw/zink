from django.contrib import admin
from django.urls import path, include

from zink.views import stilus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stilus/', stilus, name="stilus"),
    path('blog/', include('blog.urls', namespace='blog')),
]
