from elevenbits.index.models import Image, Type, About, Believe, Tool, Link, Client, Event
from django.contrib import admin

admin.site.register(Type)
admin.site.register(Image)

admin.site.register(Believe)
admin.site.register(Tool)
admin.site.register(About)

admin.site.register(Client)

admin.site.register(Link)
admin.site.register(Event)
