from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now


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
                                   default=now, null=True, blank=True)

    started_reading = models.DateTimeField('started_reading',
                                           help_text='Date and time when '
                                                     'I started to read '
                                                     'this text.',
                                           default=now)

    finished_reading = models.DateTimeField('finished_reading',
                                            help_text='Date and time when '
                                                      'I finished reading '
                                                      'this text.',
                                            default=now, null=True, blank=True)

    reading = models.BooleanField(default=False,
                                  help_text='Reading this next now.')

    completed = models.BooleanField(default=False,
                                    help_text='Read the text completely.')

    title = models.TextField(help_text="Title of the text.")

    author = models.TextField(help_text="Authors of the text.")

    type = models.ManyToManyField(Type, blank=True,
                                  help_text="The type of reading material.")

    pages = models.IntegerField(help_text="The number of pages.")

    current_page = models.IntegerField(help_text="The current page.")

    topics = models.ManyToManyField(Topic, blank=True,
                                    help_text="The topic this is about.")

    review = models.TextField(help_text="What you thought of it.")

    ranking = models.IntegerField(validators=[
        MaxValueValidator(10),
        MinValueValidator(-1)
    ], help_text="Its rank - how good was it?")

    def __str__(self):
        if self.reading:
            return f'{self.title} by {self.author} ' \
                   f'({self.current_page}/{self.pages}) ; reading it now.'
        if self.completed:
            return f'{self.title} by {self.author} ' \
                   f'({self.current_page}/{self.pages}).' \
                   f'; read it at {self.completed}.'
        return f'{self.title} by {self.author} ' \
               f'({self.current_page}/{self.pages}).'
