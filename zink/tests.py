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

    def test_cloud(self):
        response = self.client.get(reverse("blog:blog"))
        self.assertEqual(response.status_code, 200)
        # cloud
        self.assertContains(response, '<a href="tag/6">Linux</a>')
        self.assertContains(response, '<a href="tag/7">Python</a>')
        self.assertContains(response, '<a href="tag/4">Django</a>')
        # the hello blog entry
        self.assertContains(response, '<a href="/blog/25/">')
        self.assertContains(response, "Hello")
        self.assertContains(response, "Friday, 19th February 2016, 2006hrs")
        self.assertContains(response, "jw")

    def test_tag(self):
        response = self.client.get(reverse("blog:tag", args=[11]))
        self.assertContains(response, "2 entries tagged with 'Maven'")
