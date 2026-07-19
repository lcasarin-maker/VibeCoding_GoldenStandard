#!/usr/bin/env python3
"""Hook commit-msg (VC-073, norma de continuidad agnóstica).

This module now does two things:

1. regenerate the `STATE.md` backlog section from `tasks/backlog/` when asked;
2. verify that backlog-related commits keep `STATE.md` in sync.

The generated section is marked so it is obvious that hand edits should not be
trusted.
"""

from __future__ import annotations

import logging
import os
import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

import yaml

_ROOT = Path(__file__).resolve().parent.parent
_STATE = _ROOT / "STATE.md"
_BACKLOG_DIR = _ROOT / "tasks" / "backlog"
_GENERATED_MARKER = "<!-- sección generada — no editar a mano -->"
_GENERATED_END_MARKER = "<!-- fin de sección generada — no editar a mano -->"
_SECTION_HEADING = "## Open backlog"
_SECTION_PATTERN = re.compile(r"(?ms)^## Open backlog\b.*?(?=^## |\Z)")

# Files whose staged changes should trigger a backlog/state sync check.
_DEBT_FILES = {
    "dimensions/*.py",
    "protocol_engine/*.py",
    "scripts/*.py",
    "SPEC.md",
    "tasks/backlog/*.md",
}

logger = logging.getLogger("check_backlog_sync")


def _staged_files() -> list[str]:
    """Return staged file paths from `git diff --cached`."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            cwd=str(_ROOT),
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        logger.warning("git diff --cached failed: %s", exc)
        return []
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _matches_debt_file(filepath: str) -> bool:
    """Return True when the staged path belongs to the backlog/debt surface."""
    from fnmatch import fnmatch

    normalized = filepath.replace("\\", "/")
    if normalized.startswith("tasks/backlog/"):
        return True
    for pattern in _DEBT_FILES:
        if fnmatch(normalized, pattern):
            return True
    return False


def _stringify(value: object, default: str = "—") -> str:
    if value is None:
        return default
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    text = str(value).strip()
    return text or default


def _task_frontmatter(task_path: Path) -> dict[str, object]:
    """Return the YAML frontmatter from a task file if it exists."""
    src = task_path.read_text(encoding="utf-8", errors="replace")
    if not src.startswith("---"):
        return {}
    parts = src.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        logger.warning("Invalid frontmatter in %s: %s", task_path, exc)
        return {}
    return data if isinstance(data, dict) else {}


def backlog_entries(
    backlog_dir: Path = _BACKLOG_DIR, workspace_root: Path = _ROOT
) -> list[dict[str, str]]:
    """Collect normalized backlog metadata from `tasks/backlog/`."""
    if not backlog_dir.exists():
        return []

    entries: list[dict[str, str]] = []
    for task_path in sorted(backlog_dir.rglob("*.md")):
        if not task_path.is_file():
            continue
        meta = _task_frontmatter(task_path)
        try:
            rel_path = task_path.relative_to(workspace_root).as_posix()
        except ValueError:
            rel_path = task_path.as_posix()
        entries.append(
            {
                "id": _stringify(meta.get("id"), task_path.stem),
                "title": _stringify(meta.get("title"), task_path.stem),
                "status": _stringify(meta.get("status"), "backlog"),
                "priority": _stringify(meta.get("priority"), "medium"),
                "created": _stringify(meta.get("created")),
                "path": rel_path,
            }
        )

    entries.sort(key=lambda item: (item["id"], item["title"], item["path"]))
    return entries


def render_backlog_section(
    backlog_dir: Path = _BACKLOG_DIR, workspace_root: Path = _ROOT
) -> str:
    """Render the STATE.md backlog section from the current backlog directory."""
    entries = backlog_entries(backlog_dir, workspace_root)
    lines = [
        _SECTION_HEADING,
        "",
        _GENERATED_MARKER,
        "",
        "_Sección generada desde `tasks/backlog/` por `scripts/check_backlog_sync.py`; no editar a mano._",
        "",
    ]
    if entries:
        lines.extend(
            [
                "| ID | Title | Status | Priority | Created | File |",
                "|---|---|---|---|---|---|",
            ]
        )
        for entry in entries:
            lines.append(
                f"| `{entry['id']}` | {entry['title']} | `{entry['status']}` | "
                f"`{entry['priority']}` | {entry['created']} | `{entry['path']}` |"
            )
        lines.append("")
    else:
        lines.extend(
            [
                "_No backlog items currently live under `tasks/backlog/`._",
                "",
            ]
        )
    lines.extend([_GENERATED_END_MARKER, ""])
    return "\n".join(lines)


def extract_backlog_section(state_text: str) -> str | None:
    """Extract the existing backlog section from STATE.md, if present."""
    match = _SECTION_PATTERN.search(state_text)
    if not match:
        return None
    return match.group(0).rstrip()


def upsert_backlog_section(state_text: str, section_text: str) -> str:
    """Insert or replace the generated backlog section in STATE.md."""
    section_text = section_text.rstrip()
    if _SECTION_PATTERN.search(state_text):
        return _SECTION_PATTERN.sub(section_text + "\n\n", state_text, count=1)

    stripped = state_text.rstrip()
    if not stripped:
        return section_text + "\n"
    return stripped + "\n\n" + section_text + "\n"


def sync_state_backlog_section(
    state_path: Path = _STATE,
    backlog_dir: Path = _BACKLOG_DIR,
    workspace_root: Path = _ROOT,
) -> bool:
    """Rewrite STATE.md from tasks/backlog/ and return True when the file changed."""
    current_text = state_path.read_text(encoding="utf-8") if state_path.exists() else ""
    updated_text = upsert_backlog_section(
        current_text, render_backlog_section(backlog_dir, workspace_root)
    )
    if updated_text == current_text:
        return False
    state_path.write_text(updated_text, encoding="utf-8")
    return True


def _stage_path(path: Path) -> None:
    subprocess.run(["git", "add", str(path)], cwd=str(_ROOT), check=True)


def check_backlog_sync(staged: list[str], state_text: str, msg: str) -> tuple[bool, str]:
    """Return `(ok, reason)` after comparing staged debt against STATE.md."""
    del msg
    if os.environ.get("CERBERUS_SKIP_BACKLOG") == "1":
        return True, "escape explícito (env CERBERUS_SKIP_BACKLOG)"

    debt_changes = [f for f in staged if _matches_debt_file(f)]
    if not debt_changes:
        return True, "sin cambios en archivos de deuda"

    # Lo que importa es que STATE.md refleje tasks/backlog/, no que aparezca
    # en el commit: si ya está sincronizado no hay nada que stagear y exigirlo
    # producía un bloqueo perpetuo (archivo sin diff no se puede stagear).
    current_section = extract_backlog_section(state_text)
    if current_section is None:
        return False, f"{_STATE.name} no contiene la sección generada del backlog"

    generated_section = render_backlog_section(_BACKLOG_DIR, _ROOT).rstrip()
    if current_section.rstrip() != generated_section:
        return (
            False,
            f"{_STATE.name} backlog desincronizado con tasks/backlog/ "
            f"({len(debt_changes)} archivos de deuda modificados); corre "
            "check_backlog_sync.py --sync-state y stagea STATE.md",
        )

    return True, "backlog sincronizado"


def _read_state_text() -> str:
    return _STATE.read_text(encoding="utf-8") if _STATE.exists() else ""


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description=(
            "VC-073: mantiene STATE.md sincronizado con tasks/backlog/ y bloquea "
            "commits con deuda viva desalineada."
        )
    )
    parser.add_argument(
        "message_file",
        nargs="?",
        help="commit message file passed by git commit-msg (accepted for compatibility)",
    )
    parser.add_argument(
        "--sync-state",
        action="store_true",
        help="regenerate STATE.md backlog section from tasks/backlog/ and stage STATE.md",
    )
    args = parser.parse_args()

    if len(sys.argv) <= 1 and not args.sync_state:
        print(
            "ℹ️ [BACKLOG VC-073] uso: check_backlog_sync.py [--sync-state] <archivo-mensaje-commit>; "
            "sin argumentos = modo informativo (no bloquea).",
            file=sys.stderr,
        )
        return 0

    if args.sync_state:
        changed = sync_state_backlog_section()
        if changed:
            try:
                _stage_path(_STATE)
            except (OSError, subprocess.CalledProcessError) as exc:
                print(
                    f"❌ [BACKLOG VC-073] no se pudo stagear {_STATE.name}: {exc}",
                    file=sys.stderr,
                )
                return 1
        state_text = _read_state_text()
        ok, reason = check_backlog_sync(_staged_files(), state_text, args.message_file or "")
        if ok:
            print(f"✅ [BACKLOG VC-073] {reason}", file=sys.stderr)
            return 0
        print(
            f"❌ [BACKLOG VC-073] BLOQUEADO — {reason}.\n"
            f"   Regenera {_STATE.name} desde `tasks/backlog/` y vuelve a stagear el archivo.",
            file=sys.stderr,
        )
        return 1

    state_text = _read_state_text()
    ok, reason = check_backlog_sync(_staged_files(), state_text, args.message_file or "")
    if ok:
        print(f"✅ [BACKLOG VC-073] {reason}", file=sys.stderr)
        return 0
    print(
        f"❌ [BACKLOG VC-073] BLOQUEADO — {reason}.\n"
        f"   Regenera {_STATE.name} desde `tasks/backlog/` y haz `git add {_STATE.name}`.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
