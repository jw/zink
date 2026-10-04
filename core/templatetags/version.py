import os
import subprocess
import sys
from importlib import metadata
from importlib.metadata import PackageNotFoundError

from django import template
from django.conf import settings

register = template.Library()


def _commit_hash() -> str:
    """The short hash of the commit this process is running, Render in production or
    the local git/jj checkout in development ("unknown" if neither is available)."""
    render_commit = os.getenv("RENDER_GIT_COMMIT")
    if render_commit:
        return render_commit[:8]

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short=8", "HEAD"],
            cwd=settings.BASE_DIR,
            capture_output=True,
            text=True,
            check=True,
            timeout=2,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    return result.stdout.strip()


@register.simple_tag
def version(module: str) -> str:
    """
    Display the version number of the given module
    {% version("django") %}
    """
    if module == "python":
        return f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    elif module == "hash":
        return _commit_hash()
    else:
        try:
            version = metadata.version(module)
        except PackageNotFoundError:
            version = "unknown"

    return version


register.filter(version)
