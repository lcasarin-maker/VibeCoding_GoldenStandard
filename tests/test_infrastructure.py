from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_audit_workflow_runs_validator_and_regenerator() -> None:
    workflow = ROOT / ".github" / "workflows" / "audit.yml"
    assert workflow.exists()

    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    steps = data["jobs"]["audit"]["steps"]
    matrix_versions = data["jobs"]["audit"]["strategy"]["matrix"]["python-version"]

    assert any(
        step.get("name") == "Validate catalogs and wiki coverage"
        and step.get("run")
        == "python scripts/validate_golden_standard_catalogs.py --check-wiki"
        for step in steps
    )
    assert matrix_versions == ["3.10", "3.11", "3.12", "3.13"]
    assert any(step.get("name") == "Run pytest suite" and step.get("run") == "pytest -W error" for step in steps)
    assert any(step.get("name") == "Run Semgrep guard rules" for step in steps)
    assert any(
        step.get("name") == "Regenerate Golden Standard audit artifacts"
        and step.get("run") == "python scripts/generate_golden_audit.py"
        for step in steps
    )


def test_versioned_hooks_include_secret_scan_and_backlog_sync() -> None:
    pre_commit = (ROOT / "scripts" / "hooks" / "pre-commit").read_text(encoding="utf-8")
    commit_msg = (ROOT / "scripts" / "hooks" / "commit-msg").read_text(encoding="utf-8")

    assert "gitleaks protect --staged" in pre_commit
    assert "gitleaks not found" in pre_commit
    assert "tools/secret_scan.py" in pre_commit
    assert "scripts/gs_lint.py" in pre_commit
    assert "check_backlog_sync.py" in commit_msg
    assert "--sync-state" in commit_msg


def test_onboarding_knowledge_loop_is_documented() -> None:
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    ingestion = (ROOT / "knowledge" / "INGESTION_PROTOCOL.md").read_text(encoding="utf-8")
    index = (ROOT / "knowledge" / "INDEX.md").read_text(encoding="utf-8")

    assert "Apply existing rules by default" in contributing
    assert (
        "If a hypothesis can be tested with today's work, test it now." in contributing
    )
    assert "3+ confirmations" in contributing
    assert "If it is safe, deterministic, and still in scope: execute it." in contributing
    assert "If it is useful but crosses a boundary of scope: ask for a specific authorization." in contributing
    assert "If it is ambiguous or blocked: move it to backlog." in contributing
    assert "Do not end a task by re-listing obvious next steps" in contributing
    assert "deterministic safe follow-through should be executed immediately" in contributing
    assert "boundary-crossing follow-ups should be escalated for authorization" in contributing
    assert "work that can still be done now" in contributing
    assert "Unconfirmed observations are hypotheses" in ingestion
    assert "today's work" in ingestion
    assert "INGESTION_PROTOCOL.md" in index
    assert "KNOWLEDGE_SOURCES.md" in index
    assert "CONSUMER_CONTRACT.md" in index


def _sandbox_repo(tmp_path):
    """Copy the repo into a sandbox so the compiler never mutates the live tree.

    Args:
        tmp_path: pytest-provided temporary directory.

    Returns:
        Path of the sandbox repo root.
    """
    import shutil

    sandbox = tmp_path / 'repo'
    shutil.copytree(
        ROOT,
        sandbox,
        ignore=shutil.ignore_patterns(
            '.git', '.venv', '__pycache__', 'node_modules', '.pytest_cache'
        ),
    )
    return sandbox


def _run_generator(sandbox, flag):
    """Run the vault compiler inside the sandbox via GS_GENERATOR_ROOT.

    Args:
        sandbox: sandbox repo root.
        flag: generator CLI flag (--audit-only / --wiki-only).

    Returns:
        CompletedProcess of the generator run.
    """
    import os

    env = dict(os.environ, GS_GENERATOR_ROOT=str(sandbox))
    return subprocess.run(
        [sys.executable, str(sandbox / 'scripts' / 'generate_golden_audit.py'), flag],
        cwd=sandbox,
        env=env,
        capture_output=True,
        text=True,
    )


def test_generator_audit_only_skips_wiki(tmp_path) -> None:
    # --audit-only must write JSON + MD but not regenerate Wiki/Home.md
    sandbox = _sandbox_repo(tmp_path)
    wiki_home = sandbox / 'Wiki' / 'Home.md'
    mtime_before = wiki_home.stat().st_mtime if wiki_home.exists() else 0.0
    result = _run_generator(sandbox, '--audit-only')
    assert result.returncode == 0, result.stderr
    assert (sandbox / 'output' / 'golden_standard_audit.json').exists()
    mtime_after = wiki_home.stat().st_mtime if wiki_home.exists() else 0.0
    assert mtime_after == mtime_before, 'Wiki/Home.md was touched by --audit-only'


def test_generator_wiki_only_skips_audit_json(tmp_path) -> None:
    # --wiki-only must write wiki files but not touch the audit JSON
    sandbox = _sandbox_repo(tmp_path)
    audit_json = sandbox / 'output' / 'golden_standard_audit.json'
    mtime_before = audit_json.stat().st_mtime if audit_json.exists() else 0.0
    result = _run_generator(sandbox, '--wiki-only')
    assert result.returncode == 0, result.stderr
    assert (sandbox / 'Wiki' / 'Home.md').exists()
    mtime_after = audit_json.stat().st_mtime if audit_json.exists() else 0.0
    assert mtime_after == mtime_before, 'output/golden_standard_audit.json was touched by --wiki-only'


def test_generator_never_mutates_live_tree(tmp_path) -> None:
    # Meta-guard: running the compiler in a sandbox leaves the repo intact.
    marker = ROOT / 'Wiki' / 'Falsifiability_Report.md'
    existed = marker.exists()
    content = marker.read_bytes() if existed else None
    sandbox = _sandbox_repo(tmp_path)
    result = _run_generator(sandbox, '--wiki-only')
    assert result.returncode == 0, result.stderr
    assert marker.exists() == existed, 'compiler run touched the live Wiki'
    if existed:
        assert marker.read_bytes() == content
