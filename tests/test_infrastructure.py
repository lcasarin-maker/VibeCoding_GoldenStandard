from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_audit_workflow_runs_validator_and_regenerator() -> None:
    workflow = ROOT / ".github" / "workflows" / "audit.yml"
    assert workflow.exists()

    data = yaml.safe_load(workflow.read_text(encoding="utf-8"))
    steps = data["jobs"]["audit"]["steps"]

    assert any(
        step.get("name") == "Validate catalogs and wiki coverage"
        and step.get("run")
        == "python scripts/validate_golden_standard_catalogs.py --check-wiki"
        for step in steps
    )
    assert any(
        step.get("name") == "Regenerate Golden Standard audit artifacts"
        and step.get("run") == "python scripts/generate_golden_audit.py"
        for step in steps
    )


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
