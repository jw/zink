from django.db import models
from django.conf import settings
from os.path import join

class Image(models.Model):

    name = models.CharField(max_length=256, help_text="The name of the image.")

    image = models.ImageField(upload_to=join("skeppsholmen/"), help_text="The image.")

    title = models.CharField(max_length=256, help_text="The caption title.", blank=True)
    caption = models.CharField(max_length=512, help_text="The caption.", blank=True)

    def __unicode__(self):
        return self.name
