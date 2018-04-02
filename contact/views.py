
import logging

from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from contact.models import ContactForm
from elevenbits import settings
from elevenbits.generic import get_assets
from util.deployment import get_deployment

logger = logging.getLogger("elevenbits")


def contact(request):

    static = get_assets("blog.header")
    deployment = get_deployment()

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
                  'assets': static,
                  'contact': contact,
                  'key': settings.GOOGLE_MAPS_KEY,
                  'form': form}
    return render(request, 'contact.html', attributes)
