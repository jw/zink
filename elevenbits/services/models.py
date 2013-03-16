from django.db import models

class Feature(models.Model):
    """
        A feature.
    """

    feature = models.CharField(max_length=256, help_text="The feature.")

    show = models.BooleanField(default=False,
                               help_text="Must this feature be shown?")

    def __unicode__(self):
        return self.feature


class Service(models.Model):
    """
        A service.
    """

    icon = models.CharField(max_length=64, help_text="The logo associated with this service", blank=True)

    title = models.CharField(max_length=256, help_text="This service.")

    body = models.CharField(max_length=2048, help_text="The explanation of the service.")

    def __unicode__(self):
        return self.title

