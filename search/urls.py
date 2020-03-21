from django.conf.urls import url

from . import views

app_name = 'search'

urlpatterns = [
    url('', views.search, name='search')
    # url(r'^search/', include('haystack.urls')),
]
