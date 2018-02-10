from django.db import models
from elevenbits import settings


class Tag(models.Model):
    """Each blog entry can have zero to n tags."""
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        # return '%stag/%s/' % (settings.BLOG_ROOT, self.slug)
        return 'tag/%s/' % (self.pk)


class Image(models.Model):
    image = models.ImageField(upload_to="tmp",
                              height_field='height', width_field='width',
                              max_length=255)
    description = models.TextField(help_text='Description of the image.')
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)


class Entry(models.Model):
    """The blog entry."""

    created = models.DateTimeField('created',
                                   help_text='Date and time when '
                                             'this entry was created')

    title = models.CharField(max_length=200)

    body = models.TextField(help_text="The content of this entry.")

    active = models.BooleanField(default=False,
                                 help_text="Is this entry viewable on site?")

    posted = models.DateTimeField('posted',
                                  help_text='Date and time when this '
                                            'entry went public',
                                  blank=True)

    tags = models.ManyToManyField(Tag, blank=True)

    images = models.ManyToManyField(Image)

    class Meta:
        ordering = ['posted']
        verbose_name_plural = 'Entries'

    def __str__(self):
        return self.title


class Comment(models.Model):
    """An entry can have zero to n comments."""

    created = models.DateTimeField('created',
                                   help_text='Date and time when this '
                                             'comment was written')

    body = models.TextField(help_text="The content of this comment")

    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return self.body
