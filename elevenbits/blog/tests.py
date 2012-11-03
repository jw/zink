from django.utils import unittest
from elevenbits.blog.models import Tag

class TagTestCase(unittest.TestCase):
    def setUp(self):
        self.linux = Tag.objects.create(tag="linux")
        self.nginx = Tag.objects.create(tag="nginx")

    def test_tag_creation(self):
        self.assertEqual(self.linux.tag, 'linux')
        self.assertEqual(self.nginx.tag, 'nginx')