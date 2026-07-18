"""Tests for scripts.gs_lint_backlog (root-cause fix: gs_lint.py soft_warnings
were only ever printed and lost -- ported from Cerberus's proven
dimensions._warn_tasks write+prune pattern, see tests/test_warn_tasks_prune.py
in the Cerberus repo for the sibling test suite this mirrors).
"""

from scripts.gs_lint_backlog import prune_resolved_warn_tasks, write_warn_tasks


def test_write_creates_one_task_per_warning(tmp_path):
    warnings = [
        "[SOFT] VC-001: orphaned reference to XYZ",
        "[SOFT] VT-020: doc_only without justification",
    ]
    created = write_warn_tasks(tmp_path, warnings, today="2026-07-18")

    assert created == 2
    backlog = tmp_path / "tasks" / "backlog"
    files = sorted(backlog.glob("WARN-gslint-*.md"))
    assert len(files) == 2
    content = files[0].read_text(encoding="utf-8")
    assert "status: backlog" in content
    assert "created: 2026-07-18" in content


def test_write_is_idempotent_for_same_warning(tmp_path):
    warning = ["[SOFT] VC-001: orphaned reference to XYZ"]
    first = write_warn_tasks(tmp_path, warning, today="2026-07-18")
    second = write_warn_tasks(tmp_path, warning, today="2026-07-19")

    assert first == 1
    assert second == 0
    backlog = tmp_path / "tasks" / "backlog"
    assert len(list(backlog.glob("WARN-gslint-*.md"))) == 1


def test_prune_deletes_task_whose_warning_no_longer_reproduces(tmp_path):
    warning = "[SOFT] VC-001: orphaned reference to XYZ"
    write_warn_tasks(tmp_path, [warning], today="2026-07-18")

    pruned = prune_resolved_warn_tasks(tmp_path, live_warnings=[])

    assert pruned == 1
    backlog = tmp_path / "tasks" / "backlog"
    assert list(backlog.glob("WARN-gslint-*.md")) == []


def test_prune_keeps_task_whose_warning_still_reproduces(tmp_path):
    warning = "[SOFT] VC-001: orphaned reference to XYZ"
    write_warn_tasks(tmp_path, [warning], today="2026-07-18")

    pruned = prune_resolved_warn_tasks(tmp_path, live_warnings=[warning])

    assert pruned == 0
    backlog = tmp_path / "tasks" / "backlog"
    assert len(list(backlog.glob("WARN-gslint-*.md"))) == 1


def test_prune_never_touches_task_a_human_moved_off_backlog_status(tmp_path):
    warning = "[SOFT] VC-001: orphaned reference to XYZ"
    write_warn_tasks(tmp_path, [warning], today="2026-07-18")
    backlog = tmp_path / "tasks" / "backlog"
    task_path = next(backlog.glob("WARN-gslint-*.md"))
    task_path.write_text(
        task_path.read_text(encoding="utf-8").replace("status: backlog", "status: active", 1),
        encoding="utf-8",
    )

    pruned = prune_resolved_warn_tasks(tmp_path, live_warnings=[])

    assert pruned == 0
    assert task_path.exists()


def test_prune_on_missing_backlog_dir_returns_zero(tmp_path):
    assert prune_resolved_warn_tasks(tmp_path, live_warnings=[]) == 0


def test_write_with_no_warnings_creates_nothing(tmp_path):
    assert write_warn_tasks(tmp_path, [], today="2026-07-18") == 0
    assert not (tmp_path / "tasks" / "backlog").exists()
