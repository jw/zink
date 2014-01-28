
#
# Copyright (C) 2013-2014 Jan Willems (ElevenBits)
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

from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.conf import settings

from blog.models import Entry, Tag
from tweeter.models import Tweet

from util.generic import get_static
from util.deployment import get_deployment

import logging
logger = logging.getLogger("elevenbits")


def blog(request, page=1):
    """Get all blog entries for a specific page."""

    static = get_static("blog.header")
    deployment = get_deployment()

    tags = Tag.objects.all()
    logger.info("Retrieved %s tags." % len(tags))

    entry_list = Entry.objects.filter(active=True).reverse()
    logger.info("Retrieved %s blog entries." % len(entry_list))

    tweets = Tweet.objects.all()[:5]

    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        size = 5
    paginator = Paginator(entry_list, size)

    # make sure page request is an int - if not, deliver first page
    try:
        page = int(page)
    except ValueError:
        page = 1

    # if page is out of range, deliver last page
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    attributes = {'deployment': deployment,
                  'static': static,
                  'entries': entries,
                  'tweets': tweets,
                  'tags': tags}

    return render(request, 'blog.html', attributes)


def tag(request, tag, page=1):
    """Get all entries for a specific tag."""

    deployment = get_deployment()

    static = get_static("tags.title")

    tags = Tag.objects.all()
    logger.info("Retrieved %s tags." % len(tags))

    entry_list = Entry.objects.filter(active=True, tags__pk=tag).reverse()

    tweets = Tweet.objects.all()[:5]

    # create the header
    try:
        tag = Tag.objects.get(id=tag)
        static['header'] = "%s entries tagged with '%s'" % \
                           (entry_list.count(), tag.tag)
        tag_id = tag.id
    except Tag.DoesNotExist:
        static['header'] = "Tag with id %s not found." % tag
        tag_id = None

    try:
        size = settings.BLOG_PAGE_SIZE
    except AttributeError:
        logger.warn("No blog page size found in settings. Defaulting to 5.")
        size = 5
    paginator = Paginator(entry_list, size)

    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(page)
    except ValueError:
        logger.debug("'%s' is an invalid page number; showing first page." %
                     page)
        page = 1

    # If page is out of range, deliver last page.
    try:
        entries = paginator.page(page)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)

    attributes = {'deployment': deployment,
                  'static': static,
                  'entries': entries,
                  'tweets': tweets,
                  'tag_id': tag_id,
                  'tags': tags}

    return render(request, 'tags.html', attributes)


def detail(request, id):
    """Get one specific entry."""

    static = get_static("blog.header")

    deployment = get_deployment()

    tags = Tag.objects.all()
    logger.info("Retrieved %s tags." % len(tags))

    tweets = Tweet.objects.all()[:5]

    entry = get_object_or_404(Entry, pk=id)

    attributes = {'deployment': deployment,
                  'static': static,
                  'tags': tags,
                  'tweets': tweets,
                  'entry': entry}

    return render(request, 'detail.html', attributes)
