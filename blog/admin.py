
#
# Zink
#

from django.contrib import admin

from blog.models import Entry, Tag, Comment


admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Comment)
