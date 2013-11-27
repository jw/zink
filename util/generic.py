
#
# Zink
#

from elevenbits.static.models import Static

import logging
logger = logging.getLogger("elevenbits")


def get_static(name):
    """Get generic static information."""
    static = {}
    static['copyright'] = Static.objects.get(name="copyright").value
    static['host'] = Static.objects.get(name="elevenbits").value
    static['title'] = Static.objects.get(name=name).value
    return static



