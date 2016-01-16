
#
# Copyright (c) 2013-2016 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

from django.contrib import admin

from tweeter.models import Tweet
from elevenbits import settings

import twitter

import logging
logger = logging.getLogger("elevenbits")


def is_valid(api):
    """Make sure we are authenticated by Twitter."""
    try:
        name = api.VerifyCredentials().name
        if name == settings.TWITTER_NAME:
            logger.debug("Connected with twitter with user '%s'." %
                         settings.TWITTER_NAME)
            return True
        else:
            logger.warn("Invalid twitter name (%s) was provided." %
                        settings.TWITTER_NAME)
            return False
    except KeyError:
        logger.warn("Could not connect to twitter.")
        return False


def get_latest_tweets(number=20):
    """Get some tweets insert them in the database."""
    old_tweets = Tweet.objects.all()
    logger.info("Currently %s tweets are available." % len(old_tweets))
    api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                      consumer_secret=settings.CONSUMER_SECRET,
                      access_token_key=settings.OAUTH_TOKEN,
                      access_token_secret=settings.OAUTH_TOKEN_SECRET)
    if is_valid(api):
        stati = api.GetHomeTimeline(count=number)
        for status in stati:
            Tweet.objects.create(json=status.AsDict())
        if len(stati):
            logger.info("Retrieved %s tweets and saved them "
                        "in the database." % len(stati))
            logger.info("Old tweets: %s." % old_tweets)
            for t in old_tweets:
                print("Deleting '%s'..." % t.text)
                t.delete()
            logger.info("Deleted old tweets successfully.")
        else:
            logger.warn("No tweets retrieved. Leaving current tweets as is.")
        return stati
    else:
        logger.warn("No valid access.")
        return None
