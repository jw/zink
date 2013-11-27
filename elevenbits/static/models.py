from django.db import models


class Static(models.Model):
    
    name = models.CharField(max_length=200, help_text="The name of the pair.")
    
    value = models.TextField(help_text="The value of the pair.")

    def __unicode__(self):
        return self.name
