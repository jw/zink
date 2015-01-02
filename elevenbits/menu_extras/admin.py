
#
# Copyright (c) 2013-2015 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

from django.contrib import admin
from treemenus.admin import MenuAdmin, MenuItemAdmin
from treemenus.models import Menu
from .models import MenuItemExtension


class MenuItemExtensionInline(admin.StackedInline):
    model = MenuItemExtension
    max_num = 1


class CustomMenuItemAdmin(MenuItemAdmin):
    inlines = [MenuItemExtensionInline, ]


class CustomMenuAdmin(MenuAdmin):
    menu_item_admin_class = CustomMenuItemAdmin

# Unregister the standard admin options
admin.site.unregister(Menu)
# Register the new, customized, admin options
admin.site.register(Menu, CustomMenuAdmin)
