"""Add blog entries from a production database dump that are missing locally.

See DEVELOPMENT.md for how to produce the dump file with export-render-db.sh.
"""

from __future__ import annotations

import os
import subprocess
import uuid
from typing import Any

from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.db import connections

from blog.models import Entry
from blog.sync import SyncReport, apply_missing, diff_entries


class Command(BaseCommand):
    help = (
        "Compare blog Entry rows in a pg_dump (custom-format) archive against the local "
        "database, and add any entries missing locally. Entries that only exist locally "
        "are left untouched. Images and comments are not copied; a warning is printed for "
        "any added entry that had either."
    )

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "dump_file",
            help="Path to a pg_dump -Fc custom-format archive (see export-render-db.sh).",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only print the report; don't add anything to the database.",
        )
        parser.add_argument(
            "--keep-scratch-db",
            action="store_true",
            help="Don't drop the scratch database used to inspect the dump (for debugging).",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        dump_file = options["dump_file"]
        if not os.path.isfile(dump_file):
            raise CommandError(f"No such file: {dump_file}")

        conn_params = self._connection_params()
        scratch_db = f"{conn_params['dbname']}_sync_{uuid.uuid4().hex[:8]}"
        scratch_alias = "dump_scratch"

        self._run_pg_tool("createdb", conn_params, scratch_db)
        try:
            self._restore_dump(conn_params, scratch_db, dump_file)
            connections.databases[scratch_alias] = {
                **connections.databases["default"],
                "NAME": scratch_db,
            }

            dump_entries = list(
                Entry.objects.using(scratch_alias).prefetch_related(
                    "tags", "images", "comment_set"
                )
            )
            local_entries = list(Entry.objects.using("default").all())
            report = diff_entries(local_entries, dump_entries)
            self._print_report(report)

            if report.missing and not options["dry_run"]:
                for warning in apply_missing(report.missing):
                    self.stdout.write(self.style.WARNING(warning))
                self.stdout.write(
                    self.style.SUCCESS(f"Added {len(report.missing)} entry/entries.")
                )
        finally:
            if scratch_alias in connections.databases:
                connections[scratch_alias].close()
                connections.databases.pop(scratch_alias, None)
            if not options["keep_scratch_db"]:
                self._run_pg_tool(
                    "dropdb", conn_params, scratch_db, extra_args=["--if-exists"]
                )

    def _connection_params(self) -> dict[str, str]:
        default = connections.databases["default"]
        return {
            "host": default["HOST"] or "localhost",
            "port": str(default["PORT"] or 5432),
            "user": default["USER"],
            "password": default["PASSWORD"] or "",
            "dbname": default["NAME"],
        }

    def _restore_dump(
        self, conn_params: dict[str, str], scratch_db: str, dump_file: str
    ) -> None:
        # pg_restore keeps going and exits non-zero even for errors it already recovered
        # from - e.g. Render-managed dumps include a `CREATE EXTENSION pg_stat_statements`
        # that a non-superuser local role can't run. Surface those as warnings instead of
        # treating them as fatal; the entries we actually care about still get restored.
        result = self._run_pg_tool(
            "pg_restore",
            conn_params,
            scratch_db,
            extra_args=["--no-owner", "--no-privileges", dump_file],
            fatal=False,
        )
        if result.returncode != 0:
            self.stderr.write(
                self.style.WARNING(
                    f"pg_restore reported errors (continuing):\n{result.stderr}"
                )
            )

    def _run_pg_tool(
        self,
        tool: str,
        conn_params: dict[str, str],
        dbname: str,
        extra_args: list[str] | None = None,
        fatal: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        command = [
            tool,
            "-h",
            conn_params["host"],
            "-p",
            conn_params["port"],
            "-U",
            conn_params["user"],
        ]
        if tool == "pg_restore":
            command += ["-d", dbname]
        else:
            command += [dbname]
        command += extra_args or []

        env = {**os.environ, "PGPASSWORD": conn_params["password"]}
        try:
            result = subprocess.run(
                command, env=env, check=fatal, capture_output=True, text=True
            )
        except FileNotFoundError as error:
            raise CommandError(f"{tool} is not installed or not on PATH.") from error
        except subprocess.CalledProcessError as error:
            raise CommandError(f"{tool} failed:\n{error.stderr}") from error
        return result

    def _print_report(self, report: SyncReport) -> None:
        if report.local_only:
            self.stdout.write(
                f"{len(report.local_only)} entry/entries only exist locally (left untouched):"
            )
            for entry in report.local_only:
                self.stdout.write(f"  - {entry.title!r} ({entry.posted})")

        if not report.missing:
            self.stdout.write(self.style.SUCCESS("Nothing missing locally."))
            return

        self.stdout.write(f"{len(report.missing)} entry/entries missing locally:")
        for entry in report.missing:
            self.stdout.write(f"  - {entry.title!r} ({entry.posted})")
