from django.test import TestCase
from django.test.client import Client


class HeaderTest(TestCase):
    def test_header_nav_links(self):
        response = Client().get("/")
        self.assertContains(response, "elevenbits")
        self.assertContains(response, "Home")
        self.assertContains(response, "Projects")
        self.assertContains(response, "Blog")
        self.assertContains(response, "Contact")


class ProjectsTest(TestCase):
    def test_projects(self):
        response = Client().get("/projects")
        self.assertEqual(response.status_code, 200)


class ContactTest(TestCase):
    def test_contact(self):
        response = Client().get("/contact")
        self.assertEqual(response.status_code, 200)
