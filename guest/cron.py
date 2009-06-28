from django_cron import Job, cronScheduler

from .utils import cleanup_guests
from . import settings

class DeleteOldGuests(Job):
    """
        Cron Job that deletes expired Sessions
    """
    run_every = settings.GUEST_DELETE_FREQUENCY
    def job(self, *args, **kwargs):
        cleanup_guests()

cronScheduler.register(DeleteOldGuests)
