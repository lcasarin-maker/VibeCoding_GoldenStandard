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
        and step.get("run") == "python scripts/validate_golden_standard_catalogs.py --check-wiki"
        for step in steps
    )
    assert any(
        step.get("name") == "Regenerate Golden Standard audit artifacts"
        and step.get("run") == "python generate_golden_audit.py"
        for step in steps
    )
