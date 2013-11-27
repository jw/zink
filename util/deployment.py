
#
# Zink
#

from elevenbits.deployment.models import Deployment


def get_deployment():
    """Get deployment information."""
    deployment = {}
    try:
        last = Deployment.objects.all().reverse()[0]
        deployment['tag'] = last.tag
        deployment['timestamp'] = last.timestamp
        deployment['version'] = last.version
        deployment['deployer'] = last.deployer
    except IndexError:
        from datetime import datetime
        deployment['tag'] = "unknown"
        deployment['timestamp'] = datetime.now()
        deployment['version'] = "unknown"
        deployment['deployer'] = "unknown"
    return deployment