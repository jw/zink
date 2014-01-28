
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

from django.db import models
from django import forms


class ContactForm(forms.Form):
    """
        Web user can contact the admin via this form.  Not related to the
        Contact model object.
    """
    name = forms.CharField(max_length=256, help_text="Add your name.")

    email = forms.EmailField(help_text="Add your email address.")

    subject = forms.CharField(max_length=256, required=False,
                              help_text="Add your subject.")

    message = forms.CharField(max_length=1024, help_text="Your message.",
                              widget=forms.Textarea)

    spam = forms.CharField(max_length=0,
                           help_text='This should never be filled out!',
                           required=False, )

    def clean_spam(self):
        """Invalidate the form when there is spam."""
        spam = self.cleaned_data['spam']
        if spam:
            raise forms.ValidationError("No robots (or spam) allowed here!")
        return spam


class Contact(models.Model):
    """
        Contact information on the website.  Not related to the ContactForm.
    """
    name = models.CharField(max_length=256)

    street = models.CharField(max_length=256)

    city = models.CharField(max_length=128)

    country = models.CharField(max_length=128)

    phone = models.CharField(max_length=32)

    email = models.CharField(max_length=64)

    vat = models.CharField(max_length=16)

    account = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug
