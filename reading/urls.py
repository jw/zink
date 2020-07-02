from django.contrib import admin
from django.urls import path

from .views import ping, home


def trigger_error(request):
    1 / 0


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('ping/', ping, name="ping"),
    path('sentry-debug/', trigger_error),
]
