from django.urls import include, path

from . import views  # noqa: I252

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("cookies", views.cookies, name="cookies"),
    path("blog/", include("blog.urls")),
]
