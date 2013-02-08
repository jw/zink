from django.db import models

class Type(models.Model):
    """
        Type of an image.  Could be something like 'blog', or 'clients'.
        Also 'slider' can be used.
    """
    type = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.type

    def get_absolute_url(self):
        return self.slug

class Image(models.Model):
    """
        An image.
    """

    name = models.CharField(max_length=256, help_text="The name of the image.")

    file = models.ImageField(upload_to="upload", help_text="The image file.")

    title = models.CharField(max_length=256, help_text="The caption title.", blank=True)

    caption = models.CharField(max_length=512, help_text="The caption.", blank=True)

    type = models.ManyToManyField(Type, blank=True,
                                  help_text="The type of the image. An image can have multiple types.")

    def __unicode__(self):
        return self.name + "(" + str(file) + ")"
