from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


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

    author = models.TextField(help_text="Authors of the text.")

    review = models.TextField(help_text="What you thought of it.")

    type = models.OneToOneField(Type, on_delete=models.CASCADE)

    pages = models.IntegerField(help_text="The number of pages.")

    current_page = models.IntegerField(help_text="The current page.")

    topics = models.ManyToManyField(Topic, blank=True)

    ranking = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(-1)
    ])

    def __str__(self):
        return f'{self.title} by {self.author} ' \
               f'({self.current_page}/{self.pages})'
