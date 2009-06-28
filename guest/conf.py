"""
Utilities for combining default and custom settings files.

Example Usage:

>>>from conf import Settings, module_from_env_var
>>>from . import default_settings
>>>settings = Settings([module_from_env_var(), default_settings])

``settings.ATTR_NAME`` would then return the value of ``ATTR_NAME`` from the
module specified by the ``DJANGO_SETTINGS_MODULE`` environment variable.  If
this fails it returns the value from ``default_settings``.
"""

import os

from . import importlib

ENVIRONMENT_VARIABLE = "DJANGO_SETTINGS_MODULE"

# This function adapted from django.conf.Settings
def module_from_env_var(env_var=ENVIRONMENT_VARIABLE):
    """
    Returns the module specified by an environment variable, ``env_var``.
    """
    try:
        settings_module = os.environ[ENVIRONMENT_VARIABLE]
        if not settings_module: # If it's set but is an empty string.
            raise KeyError
    except KeyError:
        # NOTE: This is arguably an EnvironmentError, but that causes
        # problems with Python's interactive help.
        raise ImportError("Settings cannot be imported, because environment variable %s is undefined." % ENVIRONMENT_VARIABLE)
    try:
        mod = importlib.import_module(settings_module)
    except ImportError, e:
        raise ImportError, "Could not import settings '%s' (Is it on sys.path? Does it have syntax errors?): %s" % (self.SETTINGS_MODULE, e)
    return mod


class Settings(object):
    """
    A way of combining several settings files into one settings object.

    Attributes are looked up in the settings files in a specified order.  Useful
    for overriding default settings with custom settings.  Setting names must be
    all upper case."""

    def __init__(self, settings_sources):
        self.settings_sources = settings_sources

    class InvalidSettingName(Exception):
        pass

    def __getattr__(self, name):
        if name != name.upper():
            raise InvalidSettingName()
        value = None
        for settings_source in self.settings_sources:
            try:
                value = getattr(settings_source, name)
                break
            except AttributeError:
                pass
        if value is None:
            raise AttributeError
        # Assign this attribute to the class so we don't have to look it up
        # again.
        setattr(self, name, value)
        return value

