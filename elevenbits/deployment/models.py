from django.db import models


class Deployment(models.Model):
    """The deployment parameters of the website."""

    tag = models.CharField('tag', max_length=255,
                           help_text='The tag of this deployment.')
    
    version = models.CharField('version', max_length=255)
    
    timestamp = models.DateTimeField(unique=True)
    
    deployer = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.version

    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'
        verbose_name_plural = 'Deployments'
