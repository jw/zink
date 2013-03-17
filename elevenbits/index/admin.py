from elevenbits.index.models import Image, Type
from elevenbits.index.models import About, Believe, Tool
from elevenbits.index.models import Client, Project
from elevenbits.index.models import Link, Event

from django.contrib import admin

admin.site.register(Type)
admin.site.register(Image)

admin.site.register(Believe)
admin.site.register(Tool)
admin.site.register(About)

admin.site.register(Client)
admin.site.register(Project)

admin.site.register(Link)
admin.site.register(Event)
