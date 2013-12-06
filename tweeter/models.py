from django.db import models
from jsonfield import JSONField

from datetime import datetime


class Tweet(models.Model):
    """A very basic tweet."""

    json = JSONField()

    def _get_created_at(self):
        """Get the creation date of this tweet."""
        return self.json.get('created_at', "Sun Dec 28 00:00:00 +0000 1969")
    created_at = property(_get_created_at)

    def _get_created_at_as_datetime(self):
        """Get the creation date of this tweet in seconds."""
        d = datetime.strptime(self.created_at, '%a %b %d %H:%M:%S +0000 %Y')
        return d
    created_at_as_datetime = property(_get_created_at_as_datetime)

    def _get_text(self):
        """Return the text of this tweet."""
        return self.json.get('text')
    text = property(_get_text)

    def _get_entities(self):
        """Return the entities of this tweet."""
        return self.json.get('entities')
    entities = property(_get_entities)

    def _get_entities_urls(self):
        """Return the urls of the entities of this tweet."""
        if isinstance(self.entities, dict):
            return self.entities.get('urls')
        else:
            return None
    entities_urls = property(_get_entities_urls)
    urls = property(_get_entities_urls)

    def _get_first_url(self):
        """Return the url of this tweet,"""
        if isinstance(self.entities_urls, list):
            return self.entities_urls[0]
        else:
            return None
    first_url = property(_get_first_url)

    def _get_user(self):
        """Return the user of this tweet."""
        return self.json.get('user')
    user = property(_get_user)

    def _get_user_name(self):
        """Return the ``name`` of this tweet's user."""
        if isinstance(self.user, dict):
            return self.user.get('name')
        else:
            return None
    user_name = property(_get_user_name)

    def _get_user_screen_name(self):
        """Return the ``screen_name``` of this tweet's user"""
        if isinstance(self.user, dict):
            return self.user.get('screen_name')
        else:
            return None
    user_screen_name = property(_get_user_screen_name)

    def get_absolute_url(self):
        return self.json

    def __unicode__(self):
        return "%s (%s)" % (self.text, self.user_name)
