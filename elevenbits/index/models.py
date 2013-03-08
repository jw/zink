from django.db import models

#
# Image
#

class Type(models.Model):
    """
        Type of an image.  Could be something like 'blog', or 'clients'.
        Also 'slider' can be used.
    """

    name = models.CharField(max_length=256, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug

class Image(models.Model):
    """
        An image.
    """

    name = models.CharField(max_length=256, help_text="The name of the image.")

    file = models.ImageField(upload_to=".", help_text="The image file.")

    title = models.CharField(max_length=256, help_text="The caption title.", blank=True)

    caption = models.CharField(max_length=512, help_text="The caption.", blank=True)

    types = models.ManyToManyField(Type, blank=True,
                                   help_text="The type of the image. An image can have multiple types.")

    def __unicode__(self):
        return self.name + " (file: " + str(self.file) + ")"

#
# Index section: believe, tools, about
#

class Believe(models.Model):
    """
        A believe we have.
    """

    icon = models.CharField(max_length=64, help_text="The logo associated with this believe", blank=True)

    title = models.CharField(max_length=256, help_text="The main subject of this believe")

    body = models.CharField(max_length=1024, help_text="The believe")

    def __unicode__(self):
        return self.title

class About(models.Model):

    string = models.CharField(max_length=1024, help_text="Some informational message")

    def __unicode__(self):
        return self.string

class Tool(models.Model):
    """
        A tool we like.  Or are good at.
    """

    icon = models.CharField(max_length=64, help_text="The logo associated with this tool", blank=True)

    title = models.CharField(max_length=256, help_text="A title describing this tool")

    body = models.CharField(max_length=1024, help_text="Some informationa message on this tool")

    def __unicode__(self):
        return self.title

#
# Clients
#

class Client(models.Model):
    """
        A client
    """

    name = models.CharField(max_length=256, help_text="The name of the client")

    url = models.CharField(max_length=1024, help_text="The url of the client's website")

    short = models.CharField(max_length=1024, help_text="A short description of what we did for this client")

    long = models.CharField(max_length=4096, help_text="A long description of what we did for this client")

    image = models.ImageField(upload_to=".", help_text="The image related to this client")

    def __unicode__(self):
        return self.name

#
# Last section (where about, usefull links, some images, and recent events are stored
#

class Link(models.Model):

    link = models.CharField(max_length=1024, help_text="The link itself")

    description = models.CharField(max_length=512, help_text="The description of the link")

    def __unicode__(self):
        return self.description


# TODO: Is this required?
# TODO: Can this not be retrieved via an API?
class Event(models.Model):

    message = models.CharField(max_length=512, help_text="The message of the event")

    link = models.CharField(max_length=1024, help_text="The link itself")
