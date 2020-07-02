from django.http import JsonResponse
from django.shortcuts import render


def ping(request):
    data = {'ping': 'pong!'}
    return JsonResponse(data)


def home(request):
    attributes = {'hello': 'there'}
    return render(request, 'index.html', attributes)
