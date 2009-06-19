from django.db import models

# The page
class Page(models.Model):
    
    title = models.CharField(max_length=255, unique=True, help_text='The title of the page')
    
    header = models.CharField(max_length=255, help_text='The header of the page')
    
    def __unicode__(self):
        return self.title

