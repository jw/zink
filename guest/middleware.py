import datetime

from .utils import get_guest
from .exceptions import NotAGuest

class GuestMiddleware(object):
    """
    If the user is a guest then their ``last_used`` attribute is updated
    to the current time.
    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_anonymous():
            return None
        try:
            guest = get_guest(request.user)
            guest.last_used = datetime.datetime.now()
            guest.save()
        except NotAGuest:
            pass
