from django.http import HttpResponse
from django.shortcuts import render


def index(request) -> HttpResponse:  # noqa: ANN001
    return render(request, "render/index.html", {})
