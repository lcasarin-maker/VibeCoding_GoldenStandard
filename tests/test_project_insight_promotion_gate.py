from __future__ import annotations

from scripts.validate_golden_standard_catalogs import (
    validate_project_insight_promotion,
)


def test_static_project_insight_must_graduate_to_vc_vt() -> None:
    errors: list[str] = []
    validate_project_insight_promotion(
        {
            "PI-999": {
                "title": "Synthetic promotable insight",
                "example_bad": "print('bad')",
                "detection": "regex: print('bad')",
            }
        },
        promoted_ids=set(),
        errors=errors,
    )

    assert "PI-999: has static signature, must graduate to VC/VT" in errors


def test_behavioral_project_insight_must_declare_doctrinal_true() -> None:
    errors: list[str] = []
    validate_project_insight_promotion(
        {
            "PI-998": {
                "title": "Synthetic behavioral insight",
            }
        },
        promoted_ids=set(),
        errors=errors,
    )

    assert "PI-998: behavioral insight must declare doctrinal: true" in errors
