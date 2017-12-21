from django.test import TestCase

from django.template import Template, Context

from datetime import datetime, timedelta
from deployment.models import Deployment


class RelativeTimeTest(TestCase):

    def setUp(self):
        now = datetime.now()
        self.tensecondsago = Deployment.objects.create(
            timestamp=(now - timedelta(seconds=10)))
        self.fourtytwosecondsago = Deployment.objects.create(
            timestamp=(now - timedelta(seconds=42)))
        self.threeminutesago = Deployment.objects.create(
            timestamp=(now - timedelta(minutes=3)))
        self.threehoursago = Deployment.objects.create(
            timestamp=(now - timedelta(hours=3)))
        self.fiftyhoursago = Deployment.objects.create(
            timestamp=(now - timedelta(hours=50)))
        self.twoweeksago = Deployment.objects.create(
            timestamp=(now - timedelta(weeks=2)))
        self.fourweeksago = Deployment.objects.create(
            timestamp=(now - timedelta(weeks=4)))
        self.fourmonthsago = Deployment.objects.create(
            timestamp=(now - timedelta(weeks=4 * 4)))
        # a year is longer than 52 weeks it seems - but 55 will do
        self.twoyearsago = Deployment.objects.create(
            timestamp=(now - timedelta(weeks=55 * 2)))

    def test_relative_time_tensecondsago(self):
        """
        After ten seconds, the relative_time tag should
        just show 'moments ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.tensecondsago}))
        self.assertEqual(out, "moments ago")

    def test_relative_time_fourtytwosecondsago(self):
        """
        After 42 seconds, the relative_time tag should
        just show '42 seconds ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.fourtytwosecondsago}))
        self.assertEqual(out, "42 seconds ago")

    def test_relative_time_threeminutesago(self):
        """
        After three minutes, the relative_time tag should
        just show '3 minutes ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.threeminutesago}))
        self.assertEqual(out, "3 minutes ago")

    def test_relative_time_threehoursago(self):
        """
        After 3 hours, the relative_time tag should
        just show '3 hours ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.threehoursago}))
        self.assertEqual(out, "3 hours ago")

    def test_relative_time_fiftyhoursago(self):
        """
        After 50 hours, the relative_time tag should
        just show '2 days ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.fiftyhoursago}))
        self.assertEqual(out, "2 days ago")

    def test_relative_time_twoweeksago(self):
        """
        After two weeks, the relative_time tag should
        just show '14 days ago'"
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.twoweeksago}))
        self.assertEqual(out, "14 days ago")

    def test_relative_time_fourweeksago(self):
        """
        After four weeks, the relative_time tag should
        just show '4 weeks ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.fourweeksago}))
        self.assertEqual(out, "4 weeks ago")

    def test_relative_time_fourmonthsago(self):
        """
        After four months, the relative_time tag should
        just show '4 months ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.fourmonthsago}))
        self.assertEqual(out, "4 months ago")

    def test_relative_time_twoyearsago(self):
        """
        After two years, the relative_time tag should
        just show '2 years ago'
        """
        out = Template(
            "{% load relative_time %}"
            "{{deployment.timestamp|relative_time}}"
        ).render(Context({'deployment': self.twoyearsago}))
        self.assertEqual(out, "2 years ago")
