from django.shortcuts import render_to_response
from elevenbits.blog.models import Entry

def index(request):
    latest_entry_list = Entry.objects.all()[:5]
    return render_to_response('index.html', {'latest_entry_list': latest_entry_list})


