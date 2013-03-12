from django.db import models

#
# Contact
#

class Contact(models.Model):
    """
        Type of an image.  Could be something like 'blog', or 'clients'.
        Also 'slider' can be used.
    """

    name = models.CharField(max_length=256, unique=True)

    street = models.CharField(max_length=256, unique=True)

    city = models.CharField(max_length=256, unique=True)

    country = models.CharField(max_length=256, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug

