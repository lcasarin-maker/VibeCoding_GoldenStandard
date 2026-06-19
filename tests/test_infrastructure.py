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
        and step.get("run") == "python generate_golden_audit.py"
        for step in steps
    )


def test_onboarding_knowledge_loop_is_documented() -> None:
    contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
    ingestion = (ROOT / "INGESTION_PROTOCOL.md").read_text(encoding="utf-8")
    index = (ROOT / "knowledge" / "INDEX.md").read_text(encoding="utf-8")

    assert "Apply existing rules by default" in contributing
    assert (
        "If a hypothesis can be tested with today's work, test it now." in contributing
    )
    assert "3+ confirmations" in contributing
    assert "Unconfirmed observations are hypotheses" in ingestion
    assert "today's work" in ingestion
    assert "knowledge.md" in index
    assert "hypotheses.md" in index
    assert "rules.md" in index
