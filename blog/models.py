import re

import mistune
from bs4 import BeautifulSoup
from django.db import models
from treenode.models import TreeNodeModel

from zink import settings


class Menu(TreeNodeModel):

    treenode_display_field = 'name'

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    active = False


class Tag(models.Model):
    """Each blog entry can have zero to n tags."""
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return f'tag/{self.pk}'


class Image(models.Model):
    image = models.ImageField(upload_to="tmp/",
                              height_field='height', width_field='width',
                              max_length=255)
    description = models.TextField(help_text='Description of the image.')
    height = models.PositiveIntegerField(default=0, editable=False)
    width = models.PositiveIntegerField(default=0, editable=False)

    def __str__(self):
        return f'{self.image.name} ({self.description})'


class Entry(models.Model):
    """The blog entry."""

    BLOG = 'BG'
    STILUS = 'SS'
    CONTACT = 'CT'
    MISC = 'MC'
    PAGE_CHOICES = [
        (BLOG, 'Blog'),
        (STILUS, 'Stilus'),
        (CONTACT, 'Contact'),
        (MISC, 'Miscellaneous')
    ]

    created = models.DateTimeField('created',
                                   help_text='Date and time when '
                                             'this entry was created')

    page = models.CharField(max_length=2, choices=PAGE_CHOICES, default=BLOG,
                            help_text='The page this entry is for.')

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
        page = [choice[1] for choice in self.PAGE_CHOICES
                if choice[0] == self.page][0]
        return f"[{page}] {self.title}"

    @property
    def slug(self):
        html = mistune.markdown(self.body)
        text = ''.join(BeautifulSoup(html).findAll(text=True))
        no_hash = text.replace("#", "").strip()
        if len(no_hash) < settings.SLUG_LENGTH:
            return no_hash

        return f"{no_hash[:settings.SLUG_LENGTH]}..."


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


class Static(models.Model):
    name = models.CharField(max_length=200, help_text="The name of the pair.")

    value = models.TextField(help_text="The value of the pair.")

    def __str__(self):
        return f'{self.name}: {self.value}'
