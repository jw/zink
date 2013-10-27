
#
# Zink
#

from django.db import models
from treemenus.models import MenuItem


class MenuItemExtension(models.Model):
    menu_item = models.OneToOneField(MenuItem, related_name="extension")
    published = models.BooleanField(default=False)
    description = models.CharField(max_length=512,
                                   help_text="Description.",
                                   blank=True)
    selected_patterns = models.TextField(blank=True)
