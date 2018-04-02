
from django.conf.urls import url

from . import views

app_name = 'contact'

urlpatterns = [
    url('', views.contact, name='contact'),
]
