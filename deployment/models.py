from django.db import models
from django.utils.timezone import now
from git import Repo
from semantic_version.django_fields import VersionField

MASTER = "master"
GIT = "."


def branch_hash(branch=MASTER, git=GIT):
    repo = Repo(git)
    branch = repo.heads[branch]
    return branch.commit.hexsha


def branch_date(branch=MASTER):
    repo = Repo(".")
    branch = repo.heads[branch]
    return branch.commit.committed_datetime


class Deployment(models.Model):
    git = models.URLField("Repository")
    deployment_date = models.DateTimeField("Deployment date", default=now, unique=True)
    version = VersionField()
    hash = models.CharField("Hexadecimal hash", max_length=40, default=branch_hash)
    commit_date = models.DateTimeField("Commit date", default=branch_date)
    branch = models.CharField("Branch", max_length=2048, default=MASTER)

    class Meta:
        ordering = ["deployment_date"]
        get_latest_by = ["deployment_date"]

    def __str__(self):
        return (
            f"Version {self.version} ({self.hash}); deployed at {self.deployment_date}."
        )
