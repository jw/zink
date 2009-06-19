from django.db import models

# a menu entry
class Menu(models.Model):
    
    name = models.CharField(max_length=30, help_text='The name of the menu')

    comment = models.CharField(max_length=100, help_text='Comment on this menu entry')

    link = models.CharField(max_length=300, help_text='The link this menu point to')
    
    highlight = models.BooleanField(help_text='Is this link selected?')
        
    def __unicode__(self):
        return self.name
