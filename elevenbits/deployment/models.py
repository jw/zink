
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

from django.db import models


class Deployment(models.Model):
    """The deployment parameters of the website."""

    tag = models.CharField('tag', max_length=255,
                           help_text='The tag of this deployment.')

    version = models.CharField('version', max_length=255)

    timestamp = models.DateTimeField(unique=True)

    deployer = models.CharField(max_length=255)

    def __unicode__(self):
        return self.version

    class Meta:
        ordering = ['timestamp']
        get_latest_by = 'timestamp'
        verbose_name_plural = 'Deployments'
