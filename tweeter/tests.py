from django.test import TestCase
from tweeter.models import Tweet

from datetime import datetime

import logging
logger = logging.getLogger('elevenbits')


class TweetTest(TestCase):

    def test_empty_tweet(self):
        """Test empty tweet properties."""
        tweet = Tweet.objects.create(json={})
        self.assertEquals(tweet.json, {})
        self.assertEquals(tweet.created_at, 'Sun Dec 28 00:00:00 +0000 1969')
        self.assertEquals(tweet.created_at_as_datetime,
                          datetime(1969, 12, 28, 0, 0))
        self.assertIsNone(tweet.text)
        self.assertIsNone(tweet.user)
        self.assertIsNone(tweet.user_name)
        self.assertIsNone(tweet.user_screen_name)
        self.assertIsNone(tweet.urls)
        self.assertIsNone(tweet.first_url)

    def test_tweet_create(self):
        """Test first ElevenBits tweet's properties."""
        json = {
            "created_at": "Wed Nov 13 22:32:07 +0000 2013",
            "favorite_count": 1,
            "favorited": True,
            "id": 400752965994045441,
            "lang": "en",
            "retweeted": False,
            "source": "web",
            "text": "Hello world!",
            "truncated": False,
            "user": {
                "created_at": "Mon Nov 11 08:33:33 +0000 2013",
                "description": "Coder, Dancer, Cyclist.",
                "favourites_count": 1,
                "friends_count": 16,
                "id": 2187969354,
                "lang": "en-gb",
                "location": "Antwerp, Belgium",
                "name": "ElevenBits",
                "profile_background_color": "C0DEED",
                "profile_background_tile": False,
                "profile_image_url":
                    "https://pbs.twimg.com/profile_images/"
                    "378800000725170110/"
                    "34fc5a979d5303e93f74af228aeb2067_normal.png",
                "profile_link_color": "0084B4",
                "profile_sidebar_fill_color":
                    "http://abs.twimg.com/images/themes/theme1/bg.png",
                "profile_text_color": "333333",
                "protected": False,
                "screen_name": "ElevenBits",
                "statuses_count": 1,
                "url": "http://t.co/5OoVTqbklJ"
            }
        }
        tweet = Tweet.objects.create(json=json)
        new_tweet = Tweet.objects.get(id=tweet.id)

        self.assertEqual(tweet.json, new_tweet.json)
        self.assertEqual(new_tweet.text, "Hello world!")
        self.assertEqual(new_tweet.user_name, "ElevenBits")
        self.assertEqual(new_tweet.user_screen_name, "ElevenBits")
        self.assertIsNone(new_tweet.urls)
        self.assertIsNone(new_tweet.first_url)
        self.assertEquals(new_tweet.created_at,
                          'Wed Nov 13 22:32:07 +0000 2013')
        self.assertEquals(new_tweet.created_at_as_datetime,
                          datetime(2013, 11, 13, 22, 32, 7))
