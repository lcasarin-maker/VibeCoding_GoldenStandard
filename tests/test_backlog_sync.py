from __future__ import annotations

from pathlib import Path

import check_backlog_sync


def test_state_backlog_section_is_regenerated_from_tasks(tmp_path: Path) -> None:
    backlog_dir = tmp_path / "tasks" / "backlog"
    backlog_dir.mkdir(parents=True)
    state_path = tmp_path / "STATE.md"
    state_path.write_text(
        "# STATE — Demo\n\n## Open backlog\n\nold text\n\n## CI status\n\n",
        encoding="utf-8",
    )

    task_path = backlog_dir / "GS-999-fictitious-item.md"
    task_path.write_text(
        """---
id: GS-999
title: Fictitious backlog item
status: backlog
priority: high
created: 2026-07-10
---

## Goal
Probar la regeneración del backlog.
""",
        encoding="utf-8",
    )

    assert check_backlog_sync.sync_state_backlog_section(
        state_path, backlog_dir, workspace_root=tmp_path
    )
    regenerated = state_path.read_text(encoding="utf-8")
    assert "GS-999" in regenerated
    assert "Fictitious backlog item" in regenerated
    assert "sección generada — no editar a mano" in regenerated
    assert "## CI status" in regenerated

    task_path.unlink()

    assert check_backlog_sync.sync_state_backlog_section(
        state_path, backlog_dir, workspace_root=tmp_path
    )
    regenerated = state_path.read_text(encoding="utf-8")
    assert "GS-999" not in regenerated
    assert "Fictitious backlog item" not in regenerated
    assert "No backlog items currently live under `tasks/backlog/`." in regenerated


def test_staged_files_fails_closed_on_git_error(monkeypatch):
    def boom(*args, **kwargs):
        raise OSError("git diff boom")

    monkeypatch.setattr(check_backlog_sync.subprocess, "run", boom)

    assert check_backlog_sync._staged_files() is None


def test_main_returns_one_when_staging_cannot_be_read(monkeypatch) -> None:
    monkeypatch.setattr(check_backlog_sync, "sync_state_backlog_section", lambda: False)
    monkeypatch.setattr(check_backlog_sync, "_read_state_text", lambda: "")
    monkeypatch.setattr(
        check_backlog_sync.subprocess,
        "run",
        lambda *a, **k: (_ for _ in ()).throw(OSError("git diff boom")),
    )
    monkeypatch.setattr(
        check_backlog_sync.sys,
        "argv",
        ["check_backlog_sync.py", "--sync-state", "msg.txt"],
    )

    assert check_backlog_sync.main() == 1
