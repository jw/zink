import logging

from django.core.mail import send_mail, BadHeaderError
from django.forms.utils import ErrorList
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse

from blog.models import Menu, Entry
from blog.views import get_assets, create_menus
from zink import settings
from zink.models import ContactForm

logger = logging.getLogger(__name__)


def home(request):
    """Show the home page."""

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry_list = Entry.objects.filter(page=Entry.BLOG, active=True).reverse()
    logger.info(f"Retrieved {len(entry_list)} blog entries.")

    # books = list(Text.objects.filter(reading=True))
    # if books:
    #     logger.info(f"Reading one (or more) books: {books}.")
    # else:
    #     logger.info("Not reading any book! So sad.")

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'entry': entry,
                  'entries': entry_list[1:],
                  # 'books': books,
                  'menus': menus,
                  'assets': assets}

    return render(request, 'index.html', attributes)


def stilus(request):
    """Stilus page"""

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0], 'stilus')
    logger.info(f"Retrieved {len(menus)} menu items.")

    stilus = Entry.objects.filter(page=Entry.STILUS, active=True)
    if stilus:
        stilus = stilus[0]
        logger.info(f"Retrieved stilus entry.")

    attributes = {'menus': menus,
                  'stilus': stilus,
                  'assets': assets}

    return render(request, 'stilus.html', attributes)


class UiKitErrorList(ErrorList):
    def __str__(self):
        if not self:
            return ''
        return ''.join([f'<div class="uk-text-danger">{e}</div>'
                        for e in self])


def contact(request):
    static = get_assets(prefix='contact')

    menus = create_menus(Menu.roots[0], 'contact')
    logger.info(f"Retrieved {len(menus)} menu items.")

    if request.method == 'POST':

        form = ContactForm(request.POST, error_class=UiKitErrorList)
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

            return HttpResponseRedirect(reverse('contact'))

    else:
        form = ContactForm()  # create an empty form

    attributes = {'assets': static,
                  'contact': contact,
                  'menus': menus,
                  'key': settings.GOOGLE_MAPS_KEY,
                  'form': form}

    return render(request, 'contact.html', attributes)
