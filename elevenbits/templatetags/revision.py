"""
Creates a template tag called {% revision %} that returns the
current hg (or svn) version.  The svnversion or hg libraries are
required - when not there 'unknown' is returned.
"""

import sys
import os

# TODO: refactor this!
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                             "../../"))

from django import template

register = template.Library()


def get_svn_revision(path=None):

    from django.conf import settings
    import re
    import os

    rev = None
    if path is None:
        path = settings.SITE_ROOT
    entries_path = '%s/.svn/entries' % path

    if os.path.exists(entries_path):
        try:
            entries = open(entries_path, 'r').read()
            # Versions >= 7 of the entries file are flat text.
            # The first line is the version number. The next set
            # of digits after 'dir' is the revision.
            if re.match('(\d+)', entries):
                rev_match = re.search('\d+\s+dir\s+(\d+)', entries)
                if rev_match:
                    rev = rev_match.groups()[0]
            # Older XML versions of the file specify revision
            # as an attribute of the first entries node.
            else:
                from xml.dom import minidom
                dom = minidom.parse(entries_path)
                rev = dom.getElementsByTagName(
                    'entry')[0].getAttribute('revision')
        except IOError:
            rev = "invalid"

    if rev:
        return u'%s' % rev
    return u'unknown'


def get_hg_revision(path=None):

    import mercurial.ui
    import mercurial.hg
    from django.conf import settings

    rev = None

    if path is None:
        path = settings.SITE_ROOT

    if os.path.exists(path):
        myui = mercurial.ui.ui()
        myrepo = mercurial.hg.repository(myui, path)
        ps = mercurial.localrepo.localrepository.parents(myrepo)
        rev = str(ps[0].rev()) + ":" + str(ps[0])

    return rev


@register.simple_tag
def revision():
    """
        displays the revision number
        {% revision %}
    """
    #return get_hg_revision("/home/jw/python/workspace/elevenbits.org/")
    return get_hg_revision()
