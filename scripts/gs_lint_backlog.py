"""gs_lint.py soft-warning -> tasks/backlog/*.md persistence and pruning.

Root cause this closes (found 2026-07-18, during the same cross-repo cleanup
audit that added dimensions/_warn_tasks.prune_resolved_warn_tasks to
Cerberus): gs_lint.py's soft_warnings were only ever printed to stdout and
then lost -- unlike Cerberus (which had auto-generation but no pruning), GS
had NEITHER: a finding that scrolled past in CI output was never captured
anywhere durable, so nothing forced it onto anyone's radar. This module
ports Cerberus's proven write+prune pattern (dimensions/_warn_tasks.py) to
GS's own tasks/backlog/ convention (see tasks/README.md): same idea, GS's
own frontmatter shape (id/title/status/priority/created, no `source` field)
and a `WARN-` id prefix chosen specifically so auto-generated entries are
never confused with the human-assigned sequential `GS-NNN` ids tasks/README.md
documents.
"""

from __future__ import annotations

import hashlib
import logging
import re
from pathlib import Path

_WARN_FINDINGS_START = "<!-- WARN_FINDINGS_START -->"
_WARN_FINDINGS_END = "<!-- WARN_FINDINGS_END -->"

_TASK_TEMPLATE = """---
id: {id}
title: "{title}"
status: backlog
priority: low
created: {created}
---

## Goal

Resolve the gs_lint.py finding(s) below.

## Findings

{start}
{finding}
{end}

## Acceptance criteria

- [ ] No matching gs_lint.py warning remains.
- [ ] Re-running `python scripts/gs_lint.py` does not regenerate this task.
"""


def _slug(warning: str, limit: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", warning.lower()).strip("-")
    return (slug[:limit].strip("-") or "warning")


def _task_id(warning: str) -> str:
    digest = hashlib.sha1(warning.encode("utf-8")).hexdigest()[:8]
    return f"WARN-gslint-{_slug(warning)}-{digest}"


def write_warn_tasks(root: Path, warnings: list[str], today: str) -> int:
    """Persist each gs_lint.py soft warning as its own backlog task (deduped
    by content hash, so a repeat run of an already-filed warning is a no-op).
    Returns how many NEW task files were created.
    """
    if not warnings:
        return 0
    backlog = Path(root) / "tasks" / "backlog"
    backlog.mkdir(parents=True, exist_ok=True)
    created = 0
    for warning in warnings:
        task_path = backlog / f"{_task_id(warning)}.md"
        if task_path.exists():
            continue
        content = _TASK_TEMPLATE.format(
            id=_task_id(warning),
            title=warning.strip().lstrip("[").split("]", 1)[-1].strip()[:80] or warning[:80],
            created=today,
            start=_WARN_FINDINGS_START,
            finding=f"- {warning}",
            end=_WARN_FINDINGS_END,
        )
        try:
            task_path.write_text(content, encoding="utf-8")
        except OSError as exc:
            logging.getLogger("gs_lint").warning(
                "gs_lint backlog: could not write %s: %s", task_path.name, exc
            )
            continue
        created += 1
    return created


def prune_resolved_warn_tasks(root: Path, live_warnings: list[str]) -> int:
    """Delete WARN-gslint-*.md tasks whose finding no longer reproduces.

    Matches Cerberus's dimensions._warn_tasks.prune_resolved_warn_tasks
    convention exactly: resolved tasks are deleted (git log is the record,
    same as this repo's own tasks/done/ SP-004 rule -- "completed — delete
    file in closing commit"), and any task a human already moved off
    `status: backlog` is left untouched.
    """
    backlog = Path(root) / "tasks" / "backlog"
    if not backlog.is_dir():
        return 0
    live = set(live_warnings)
    pruned = 0
    for task_path in sorted(backlog.glob("WARN-gslint-*.md")):
        try:
            content = task_path.read_text(encoding="utf-8")
        except OSError:
            continue
        status_match = re.search(r"^status:\s*(.+?)\s*$", content, re.M)
        if status_match is not None and status_match.group(1) != "backlog":
            continue
        if _WARN_FINDINGS_START not in content:
            continue
        block = content.split(_WARN_FINDINGS_START, 1)[1].split(_WARN_FINDINGS_END, 1)[0]
        lines = [ln.strip()[2:] for ln in block.splitlines() if ln.strip().startswith("- ")]
        if not lines:
            continue
        if any(line in live for line in lines):
            continue
        try:
            task_path.unlink()
        except OSError as exc:
            logging.getLogger("gs_lint").warning(
                "gs_lint backlog: could not delete %s: %s", task_path.name, exc
            )
            continue
        pruned += 1
    return pruned
