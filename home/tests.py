from django.test import TestCase, Client
from django.urls import reverse


class IndexTest(TestCase):
    """Test the home page."""

    fixtures = ['menus', 'blog']

    def testBlog(self):
        """Test the full home page."""
        client = Client()
        response = client.get(reverse('home:home'))
        self.assertContains(response, "Latest blog entry")
        self.assertContains(response, "Latest stuff from my blog")
        self.assertContains(response, 'Running on')
