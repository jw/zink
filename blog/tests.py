import logging
from unittest import skipIf

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from blog.models import Tag, Static
from elevenbits.generic import get_assets

logger = logging.getLogger('elevenbits')


class TagTestCase(TestCase):
    """Test the basic tag creation."""

    def setUp(self):
        self.linux = Tag.objects.create(tag="linux")
        self.nginx = Tag.objects.create(tag="nginx")

    def test_tag_creation(self):
        self.assertEqual(self.linux.tag, 'linux')
        self.assertEqual(self.nginx.tag, 'nginx')


@skipIf(True, "I don't want to run this test yet")
class BlogTest(TestCase):
    """Test all the blog features."""

    fixtures = ['contact', 'menus', 'menu_extras', 'blog']

    def setUp(self):
        print("Hello there")

    def testBlog(self):
        """Test the full blog."""
        client = Client()
        response = client.get(reverse('blog:blog'))
        self.assertContains(response, "Welcome to our blog")
        self.assertContains(response, "Blog Categories")
        self.assertContains(response, '/">Java (2)</a>')

    def testTag(self):
        """Test one tag."""
        client = Client()
        response = client.get(reverse('blog:tag', args=[4]))  # django
        self.assertContains(response, "<title>Tags - elevenbits</title>")
        self.assertContains(response, "2 entries tagged with")
        self.assertContains(response, "Django")
        self.assertContains(response, "Blog Categories")
        self.assertContains(response, 'Java (2)')

    def testDetail(self):
        """Test one single blog entry."""
        client = Client()
        # get the 'how to access cherokee-admin...' entry
        response = client.get(reverse('blog:detail', args=[21]))
        self.assertContains(response, 'How to access cherokee-admin')

    def testPageTag(self):
        """Test the tag pages"""
        client = Client()
        # page 1
        response = client.get(reverse('blog:tagpage', args=[6, 1]))  # linux
        self.assertContains(response, 'How to access cherokee-admin')
        self.assertContains(response, 'Howto merge PDF documents')
        self.assertContains(response, 'How to ask questions the smart way')
        # page 2
        response = client.get(reverse('blog:tagpage', args=[6, 2]))  # linux
        self.assertContains(response, 'My first own blog!')
        self.assertContains(response, 'Howto create your own Ubuntu')

    def testInactiveTag(self):
        """Only active tags must be shown."""
        client = Client()
        response = client.get(reverse('blog:tag', args=[7]))  # python
        self.assertContains(response, 'Eclipse and Django development setup')
        self.assertContains(response, 'My first own blog!')
        # the inactive one must not be there!
        self.assertNotContains(response, 'Temporary entry')

    def testMarkup(self):
        """Make sure the codehilite works."""
        client = Client()
        response = client.get(reverse('blog:detail', args=[21]))
        self.assertContains(response, '<div class="codehilite"><pre>'
                                      '<span class="gp">')

    # TODO: this must be somewhere else
    def test404(self):
        """Test the 404 response."""
        client = Client()
        response = client.get("/this_page_does_not_exist")
        self.assertContains(response, "404 message", status_code=404)


class StaticsTestCase(TestCase):

    fixtures = ['static']

    def test_statics_are_available(self):
        """Ensure that the default assets are there"""
        logging.info("Trying to get static stuff...")
        rero = Static.objects.get(name="copyright").value
        copyright = Static.objects.get(name="copyright").value,
        title = Static.objects.get(name="title").value
        self.assertIsNotNone(rero)
        self.assertIsNotNone(copyright)
        self.assertIsNotNone(title)

    def test_get_statics(self):
        """Get the generic assets and more"""
        assets = get_assets('index.header')
        self.assertIn('rero', assets)
        self.assertIn('copyright', assets)
        self.assertIn('title', assets)
        self.assertIn('index.header', assets)

    def test_get_bigger_statics(self):
        """Get the generic assets and more"""
        assets = get_assets('index.header', 'contact.title')
        self.assertIn('rero', assets)
        self.assertIn('copyright', assets)
        self.assertIn('title', assets)
        self.assertIn('index.header', assets)
        self.assertIn('contact.title', assets)
