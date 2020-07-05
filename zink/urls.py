from django.contrib import admin
from django.urls import path

from zink.views import stilus

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stilus/', stilus, name="stilus")
]
