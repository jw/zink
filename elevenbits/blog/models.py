from django.db import models

# The tag
class Tag(models.Model):
    tag = models.CharField(max_length=255, unique=True)
    
    def __unicode__(self):
        return self.tag

    def get_absolute_url(self):
        return '%stag/%s/' % (settings.BLOG_ROOT, self.slug)

# the entry
class Entry(models.Model):
    
    created = models.DateTimeField('created',
                                   help_text='Date and time when this entry was created')

    title = models.CharField(max_length=200)
    
    body = models.TextField(help_text="The content of this entry")
    
    active = models.BooleanField(default=False, 
                                help_text="Is this entry viewable on site?")
    
    posted = models.DateTimeField('posted',
                                  help_text='Date and time when this entry went public',
                                  blank=True)
    
    tags = models.ManyToManyField(Tag, blank=True)
    
    class Meta:
        ordering = ['posted']
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title

# Comments
class Comment(models.Model):

    created = models.DateTimeField('created',
                                   help_text='Date and time when this comment was written')

    body  = models.TextField(help_text="The content of this comment")
    
    entry = models.ForeignKey(Entry)
    
    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __unicode__(self):
        return self.body
    