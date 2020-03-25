import logging

from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404, render

from blog.models import Entry, Tag, Menu
from elevenbits.generic import get_assets
from reading.models import Text
from util.deployment import get_deployment

logger = logging.getLogger("elevenbits")


def create_menus(root, active=None):
    def create_menu(menu, active):
        if active and menu.name.upper() == active.upper():
            menu.active = True
        else:
            menu.active = False
        return menu
    return [create_menu(menu, active) for menu in root.children]


def home(request):
    """Show the home page."""

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.info(f"Retrieved {len(entry_list)} blog entries.")

    books = list(Text.objects.filter(reading=True))
    if books:
        logger.info(f"Reading one (or more) books: {books}.")
    else:
        logger.info("Not reading any book! So sad.")

    try:
        entry = entry_list.first()
    except IndexError:
        entry = None

    attributes = {'entry': entry,
                  'entries': entry_list[1:],
                  'books': books,
                  'menus': menus,
                  'assets': assets}

    return render(request, 'index.html', attributes)


def stilus(request):

    assets = get_assets(prefix="index")

    menus = create_menus(Menu.roots[0], 'stilus')
    logger.info(f"Retrieved {len(menus)} menu items.")

    attributes = {'menus': menus,
                  'assets': assets}

    return render(request, 'stilus.html', attributes)


def blog(request, page=1):
    """Get all blog entries for a specific page."""

    static = get_assets()
    deployment = get_deployment()

    tags = Tag.objects.all()
    logger.info(f"Retrieved {len(tags)} tags.")

    menus = create_menus(Menu.roots[0], 'blog')
    logger.info(f"Retrieved {len(menus)} menu items.")

    all_entries = Entry.objects.filter(active=True).reverse()
    logger.info(f"Retrieved total of {len(all_entries)} blog entries.")

    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        size = 5
    paginator = Paginator(all_entries, size)

    attributes = {'deployment': deployment,
                  'assets': static,
                  'page_entries': paginator.get_page(page),
                  'menus': menus,
                  'tags': tags}

    return render(request, 'blog.html', attributes)


def tag(request, tag, page=1):
    """Get all entries for a specific tag."""

    static = get_assets()
    deployment = get_deployment()

    tags = Tag.objects.all()
    logger.info(f"Retrieved {len(tags)} tags.")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry_list = Entry.objects.filter(active=True, tags__pk=tag).reverse()

    # create the header
    try:
        tag = Tag.objects.get(id=tag)
        static['header'] = f"{entry_list.count()} entries " \
                           f"tagged with '{tag.tag}'"
        tag_id = tag.id
    except Tag.DoesNotExist:
        static['header'] = f"Tag with id {tag} not found."
        tag_id = None

    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        logger.warning("No blog page size found in settings. Defaulting to 5.")
        size = 5
    paginator = Paginator(entry_list, size)

    # make sure page request is an int; if not, deliver the first page
    try:
        page = int(page)
    except ValueError:
        logger.debug(f"'{page}' is an invalid page number; "
                     f"showing first page.")
        page = 1

    # if page is out of range, deliver last page
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    attributes = {'deployment': deployment,
                  'assets': static,
                  'entries': entries,
                  'tag_id': tag_id,
                  'menus': menus,
                  'tags': tags}

    return render(request, 'tags.html', attributes)


def detail(request, id):
    """Get one specific entry."""

    static = get_assets(prefix="static")

    deployment = get_deployment()

    tags = Tag.objects.all()
    logger.info(f"Retrieved {len(tags)} tags.")

    menus = create_menus(Menu.roots[0])
    logger.info(f"Retrieved {len(menus)} menu items.")

    entry = get_object_or_404(Entry, pk=id)

    attributes = {'deployment': deployment,
                  'assets': static,
                  'tags': tags,
                  'menus': menus,
                  'entry': entry}

    return render(request, 'detail.html', attributes)
