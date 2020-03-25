
import logging

from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from blog.models import Menu
from blog.views import create_menus
from contact.models import ContactForm
from elevenbits import settings
from elevenbits.generic import get_assets
from util.deployment import get_deployment

logger = logging.getLogger("elevenbits")


def contact(request):
    static = get_assets(prefix='contact')
    deployment = get_deployment()

    menus = create_menus(Menu.roots[0], 'contact')
    logger.info(f"Retrieved {len(menus)} menu items.")

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            try:
                send_mail(f"[ZINK] {subject}", message, 'jw@elevenbits.com',
                          [email], fail_silently=False)
            except BadHeaderError:
                messages.warning(request, "Invalid header found!")

            # show success message to user
            highlight = "<strong>Thanks for your message!</strong>"
            question = "Want to send another one?"
            messages.success(request, f"{highlight} {question}")

            return HttpResponseRedirect(reverse('contact:contact'))

        # else:
        #     # report invalid form
        #     warning = "Form is invalid.  Please check carefully."
        #     messages.warning(request, warning)

    else:
        form = ContactForm()  # create an empty form

    attributes = {'deployment': deployment,
                  'assets': static,
                  'contact': contact,
                  'menus': menus,
                  'key': settings.GOOGLE_MAPS_KEY,
                  'form': form}

    return render(request, 'contact.html', attributes)
