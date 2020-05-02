
import logging

from django.test import TestCase, Client
from django.urls import reverse

logger = logging.getLogger('elevenbits')


class FormTest(TestCase):

    fixtures = ['blog']

    def test_get_contact_index_page(self):
        """Tests a valid contact post to the site."""
        c = Client()
        response = c.get(reverse('contact:contact'))
        self.assertContains(response,
                            '<h3 id="form">',
                            status_code=200)
        self.assertContains(response,
                            '<title>ElevenBits</title>',
                            status_code=200)

    def test_valid_post(self):
        """Tests a valid contact post to the site."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'email': 'jw@elevenbits.com',
                           'subject': 'test',
                           'message': 'Test message.'})
        self.assertEquals(response.status_code, 302)

    def test_empty_post(self):
        """Tests post of a form without a name."""
        c = Client()
        response = c.post(reverse('contact:contact'), {})
        self.assertContains(
            response,
            '<div class="alert alert-danger" role="alert">',
            status_code=200
        )

    def test_no_name_post(self):
        """Tests post of a form without a name."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'email': 'jw@elevenbits.com',
                           'subject': 'test',
                           'message': 'Test message.'})
        self.assertContains(
            response,
            'name="name" class="form-control is-invalid"',
            status_code=200
        )

    def test_no_email_post(self):
        """Tests post of a form without an email."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'subject': '[TEST]',
                           'message': 'Test message.'})
        self.assertContains(response,
                            '"Your email address" '
                            'class="form-control is-invalid" '
                            'required id="id_email">',
                            status_code=200)

    def test_no_message_post(self):
        """Tests post of a form without a message."""
        c = Client()
        response = c.post(reverse('contact:contact'),
                          {'name': 'test',
                           'subject': '[TEST]',
                           'email': 'jw@elevenbits.com'})
        self.assertContains(
            response,
            'placeholder="The message" class="form-control is-invalid"',
            status_code=200
        )


class DataTest(TestCase):

    # TODO: implement this test!
    def test_no_data(self):
        """When no data are available, a mail must be sent"""
        pass
