from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.search, name='search')
    # url(r'^search/', include('haystack.urls')),
]
