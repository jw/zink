from django.urls import path

from elevenbits.blog.views import index

urlpatterns = [
    path("", index, name="index"),
]
