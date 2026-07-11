from __future__ import annotations

from pathlib import Path

import yaml

from scripts.validate_golden_standard_catalogs import (
    validate_link_targets,
    validate_vices_catalog,
)


def test_validator_accepts_tolerated_legacy_mechanism_values(tmp_path: Path) -> None:
    catalog = {
        "items": [
            {
                "id": "VC-999",
                "title": "Legacy mechanism handle",
                "symptom": "Needs compatibility during migration",
                "cause": "Historic catalog metadata still references detector handles",
                "solution": "Keep the catalog readable while compatibility labels remain in live content",
                "status": "DOC_ONLY",
                "severity": "medium",
                "tags": ["vibe-coding", "compat-handle"],
                "action": "The validator must continue tolerating legacy mechanism labels already present in live catalogs.",
                "validating_mechanism": "d11_dependency.py",
                "downstream_verification": "required",
                "tier": "core",
            },
            {
                "id": "AV-999",
                "title": "Legacy downstream contract",
                "symptom": "Adversarial vector metadata still uses compatibility labels",
                "cause": "The catalog has not been fully normalized yet",
                "solution": "Treat the legacy labels as tolerated for compatibility with live catalogs",
                "status": "DOC_ONLY",
                "severity": "medium",
                "tags": ["adversarial", "BFS", "k=1"],
                "action": "Existing live catalog labels remain valid while compatibility is still required.",
                "validating_mechanism": "manual-review",
                "downstream_verification": "required",
                "tier": "core",
            },
        ]
    }
    path = tmp_path / "golden_standard_coding_vices.yaml"
    path.write_text(yaml.safe_dump(catalog, sort_keys=False), encoding="utf-8")

    errors: list[str] = []
    validate_vices_catalog(path, errors, check_wiki=False)

    assert errors == []


def test_validate_link_targets_reports_missing_source_instead_of_crashing(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing.md"
    errors: list[str] = []

    validate_link_targets(errors, [missing])

    assert errors == [f"Missing markdown source during link validation: {missing}"]
