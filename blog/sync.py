"""Compare blog Entry rows between two databases and copy over anything missing.

Split out from the `sync_blog_entries` management command so the comparison/copy logic
can be unit-tested without spinning up a real pg_restore scratch database.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from blog.models import Entry, Tag

EntryKey = tuple[str, datetime | None]


def entry_key(entry: Entry) -> EntryKey:
    """The (title, posted) pair used to recognize "the same" entry across two databases."""
    return (entry.title, entry.posted)


@dataclass
class SyncReport:
    matched: list[Entry] = field(default_factory=list)
    local_only: list[Entry] = field(default_factory=list)
    missing: list[Entry] = field(default_factory=list)


def diff_entries(local_entries: list[Entry], dump_entries: list[Entry]) -> SyncReport:
    """Classify dump entries as matched/missing against the local entries, by entry_key.

    Entries present locally but not in the dump are reported as local_only and are never
    touched by apply_missing - they're left alone, per the sync policy.
    """
    local_keys = {entry_key(entry) for entry in local_entries}
    dump_keys = {entry_key(entry) for entry in dump_entries}

    report = SyncReport()
    for entry in dump_entries:
        if entry_key(entry) in local_keys:
            report.matched.append(entry)
        else:
            report.missing.append(entry)
    report.local_only = [
        entry for entry in local_entries if entry_key(entry) not in dump_keys
    ]
    return report


def apply_missing(missing_entries: list[Entry]) -> list[str]:
    """Create each missing entry (plus its tags) in the default database.

    Images and comments are intentionally not copied (images reference files that don't
    exist in local media storage; comments are out of scope for this sync). Returns a
    warning string for each entry that had either, so nothing is silently dropped.
    """
    warnings: list[str] = []
    for source in missing_entries:
        new_entry = Entry(
            created=source.created,
            page=source.page,
            title=source.title,
            body=source.body,
            active=source.active,
            posted=source.posted,
        )
        new_entry.save()

        for tag in source.tags.all():
            local_tag, _ = Tag.objects.get_or_create(tag=tag.tag)
            new_entry.tags.add(local_tag)

        image_count = source.images.count()
        if image_count:
            noun = "image" if image_count == 1 else "images"
            warnings.append(
                f"{source.title!r}: {image_count} {noun} in the dump were not copied."
            )

        comment_count = source.comment_set.count()
        if comment_count:
            noun = "comment" if comment_count == 1 else "comments"
            warnings.append(
                f"{source.title!r}: {comment_count} {noun} in the dump were not copied."
            )

    return warnings
