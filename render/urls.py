from django.urls import path

from . import views  # noqa: I252

urlpatterns = [
    path("", views.index, name="index"),
]
