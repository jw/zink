from django.utils import unittest
from elevenbits.static.models import Static

class StaticTestCase(unittest.TestCase):
    
    def setUp(self):
        self.foo = Static.objects.create(name="foo", value="FOO")
        self.bar = Static.objects.create(name="BAR", value="bar")

    def test_statics(self):
        """Tesing foo and bar."""
        self.assertEqual(self.foo.name, "foo")
        self.assertEqual(self.bar.value, "bar")