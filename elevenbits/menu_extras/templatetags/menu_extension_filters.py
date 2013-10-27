
#
# Zink
#

from re import compile
from django import template

register = template.Library()


def match_path(patterns, path):
    """
        Match a path with the patterns
        @patterns: a string containing a list of patterns
        @return True when path matches one of the patterns, False otherwise
    """
    if patterns:
        for pattern in patterns.splitlines():
            if compile(pattern).match(path):
                return True
    return False

register.filter('match_path', match_path)
