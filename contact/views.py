
#
# Copyright (c) 2013-2016 Jan Willems (ElevenBits)
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

from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.mail import send_mail

from util.generic import get_static
from util.deployment import get_deployment

from contact.models import Contact, ContactForm

import logging
logger = logging.getLogger("elevenbits")


def contact(request):
    """
    Show the contact page. If a POST arrives, check the contact form and
    if valid redirect to yourself, otherwise show errors to user.
    """

    #
    # Generate generic statics, deployment and contact data
    #

    static = get_static("contact.title")
    deployment = get_deployment()

    try:
        contact = Contact.objects.get(name="ElevenBits")
    except Contact.DoesNotExist:
        # TODO: mail administrator
        contact = None
        logger.warning("No ElevenBits contact available in the database!")

    #
    # create or check the form
    #

    if request.method == 'POST':
        # the form was submitted
        logger.debug("Contact form submitted.")
        form = ContactForm(request.POST)
        if form.is_valid():
            # valid form
            logger.debug("Form is valid.")
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # send mail
            logger.debug("Sending mail.")
            send_mail(subject, message, 'jw@elevenbits.com', [email],
                      fail_silently=False)

            # show success message to user
            highlight = "<strong>Thanks for your message!</strong>"
            question = "Want to send another one?"
            messages.success(request, "%s %s" % (highlight, question))

            # do a redirect (302)
            return HttpResponseRedirect(reverse('contact:contact'))
        else:
            # report invalid form
            logger.warn("Form is invalid.")
    else:
        # create an empty form
        logger.debug("Created an unbound form.")
        form = ContactForm()

    attributes = {'deployment': deployment,
                  'static': static,
                  'contact': contact,
                  'form': form}
    return render(request, 'contact.html', attributes)
