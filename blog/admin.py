from django.contrib import admin

from blog.models import Entry, Tag, Comment, Image, Type, Topic, Text

admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Image)

admin.site.register(Type)
admin.site.register(Topic)
admin.site.register(Text)
