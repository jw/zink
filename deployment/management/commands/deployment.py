from datetime import datetime

import semantic_version
from django.core.management import BaseCommand, CommandError
from git import InvalidGitRepositoryError, NoSuchPathError, Repo
from semantic_version import Version

from deployment.models import Deployment

DEFAULT_VERSION = Version("0.1.0")


class Command(BaseCommand):
    help = "Creates a deployment entry"

    def log(self, message: str):
        self.stdout.write(message)

    def debug(self, verbosity, message: str):
        if verbosity > 1:
            self.stdout.write(message)

    def add_arguments(self, parser):
        parser.add_argument(
            "-git",
            "--git",
            help="The local path of the git repository of this project.",
        )  # required
        parser.add_argument(
            "-dv",
            "--deployment_version",
            type=str,
            help="The version of the deployed project.",
        )  # required
        parser.add_argument(
            "-dd",
            "--deployment_date",
            type=datetime.fromisoformat,
            help="The date of the deployment.",
        )
        parser.add_argument(
            "-cd",
            "--commit_date",
            type=datetime.fromisoformat,
            help="The creation date of the commit being deployed.",
        )
        parser.add_argument("--branch", help="The branch that is deployed.")
        parser.add_argument("--hash", help="The hash of the commit being deployed.")

    def handle(self, *args, **options):

        verbosity = options["verbosity"]

        args = {}

        # handle git
        if options["git"]:
            repo = self._git_repo(options["git"])
        else:
            repo = self._git_repo(".")
        git = self._remote_repo_url(repo, verbosity=verbosity)
        args["git"] = git

        # handle version
        dv = options["deployment_version"]
        if dv:
            if semantic_version.validate(dv):
                self.debug(verbosity, f"{dv} is a valid semantic version.")
                version = Version(dv)
            else:
                raise CommandError(f"{dv} is not a valid semantic version.")
        else:
            deployments = Deployment.objects.all()
            if deployments.exists():
                # update version (patch plus 1)
                deployment = deployments[0]
                self.debug(
                    verbosity,
                    f"Found the latest deployment with version {deployment.version} at {deployment.deployment_date}.",
                )
                version = deployment.version.next_patch()
                self.debug(
                    verbosity, f"Updated version {deployment.version} to {version}."
                )
            else:
                self.log(f"First version ever, so using default: {DEFAULT_VERSION}.")
                version = DEFAULT_VERSION
        args["version"] = version

        # handle optional arguments
        if options["deployment_date"]:
            args["deployment_date"] = options["deployment_date"]
        if options["commit_date"]:
            args["commit_date"] = options["commit_date"]
        if options["branch"]:
            args["branch"] = options["branch"]
        if options["hash"]:
            args["hash"] = options["hash"]

        # create the entry
        deployment = Deployment(**args)
        deployment.save()
        self.log(
            f"Created a new deployment entry for version {deployment.version} "
            f"({deployment.hash[:7]}) at "
            f"{deployment.deployment_date.strftime('%m.%d.%Y@%H:%M:%S')}."
        )

    def _git_repo(self, path):
        try:
            repo = Repo(path)
        except (InvalidGitRepositoryError, NoSuchPathError) as e:
            raise CommandError(f"{path} is not a valid git url.") from e
        return repo

    def _remote_repo_url(self, repo, verbosity=0):
        for url in repo.remote().urls:
            git = url
            self.debug(verbosity, f"Using {git} as remote git repo.")
            break
        else:
            raise CommandError(f"{repo} has no remote url.")
        return git
