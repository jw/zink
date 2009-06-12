from django.shortcuts import render_to_response
from elevenbits.menu.models import Menu

def index(request):
    menu_list = Menu.objects.all()
    return render_to_response('index.html', {'menu_list': menu_list})


