from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now


class Tag(models.Model):
    """Each blog entry can have zero to n tags."""
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        # return '%stag/%s/' % (settings.BLOG_ROOT, self.slug)
        return 'tag/%s/' % (self.pk)


class Image(models.Model):
    image = models.ImageField(upload_to="tmp/",
                              height_field='height', width_field='width',
                              max_length=255)
    description = models.TextField(help_text='Description of the image.')
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return self.image.name + " (" + self.description + ")"


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

    images = models.ManyToManyField(Image, blank=True)

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


class Type(models.Model):
    type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.type


class Topic(models.Model):
    topic = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.topic


class Text(models.Model):
    """Stuff I am reading"""

    created = models.DateTimeField('created',
                                   help_text='Date and time when '
                                             'this text came into my hands.',
                                   default=now)

    read = models.DateTimeField('created',
                                help_text='Date and time when '
                                          'this text was read.',
                                default=now)

    reading = models.BooleanField(default=False,
                                  help_text='Reading this next now.')

    title = models.TextField(help_text="Title of the text.")

    author = models.TextField(help_text="Authors of the text")

    type = models.OneToOneField(Type, on_delete=models.CASCADE)

    pages = models.IntegerField()

    current_page = models.IntegerField()

    topics = models.ManyToManyField(Topic, blank=True)

    ranking = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(-1)
    ])

    def __str__(self):
        return f'{self.title} ({self.current_page}/{self.pages})'
