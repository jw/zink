from django.test import TestCase
from django.urls import reverse


class HomeViewTests(TestCase):

    fixtures = ["blog.json"]

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Eric S. Raymond")
        self.assertContains(response, "Release early")
        self.assertContains(response, "cyclist")
        self.assertContains(response, "Running on Python")

    def test_blog(self):
        response = self.client.get(reverse("blog:detail", args=[22]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Python 3 &lt;3")
        self.assertContains(response, "packages are now Python 3.")

    def test_contact(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "keep in touch!")
        self.assertContains(response, "VAT and bank account")
        self.assertContains(response, "ElevenBits")
