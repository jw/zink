from django.contrib import admin
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm

from blog.models import Entry, Tag, Comment, Image, Static, Menu


class MenuAdmin(TreeNodeModelAdmin):
    treenode_display_mode = \
        TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION
    form = TreeNodeForm


admin.site.register(Entry)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Static)
admin.site.register(Menu, MenuAdmin)
