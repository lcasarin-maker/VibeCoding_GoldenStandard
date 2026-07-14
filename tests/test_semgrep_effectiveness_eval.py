from __future__ import annotations

from scripts.semgrep_effectiveness_eval import (
    CorpusCase,
    evaluate_effectiveness,
    load_corpus,
    load_rubric,
)


def test_preregistered_rubric_and_corpus_are_loadable():
    rubric = load_rubric()
    cases = load_corpus()
    assert rubric["committed_before_run"] is True
    assert "false_negative_rate_by_rule" in {
        item["name"] for item in rubric["metrics"]
    }
    assert any(case.known_positive_rules for case in cases)


def test_effectiveness_reports_false_negative_by_rule():
    cases = (
        CorpusCase(
            id="known-vices-positive",
            fixture="tests/semgrep_fixtures/positive.py",
            known_positive_rules=("gs-vc-095-hardcoded-secret", "gs-vc-115-unsafe-eval"),
        ),
    )
    rubric = load_rubric()
    findings = {
        "known-vices-positive": [
            {
                "check_id": "config.gs-vc-095-hardcoded-secret",
                "path": "tests/semgrep_fixtures/positive.py",
            }
        ]
    }
    report = evaluate_effectiveness(cases, findings, rubric)
    assert report["rules"]["gs-vc-095-hardcoded-secret"]["false_negative_rate"] == 0
    assert report["rules"]["gs-vc-115-unsafe-eval"]["false_negative_rate"] == 1
    assert report["summary"]["passed"] is False


def test_effectiveness_passes_when_all_known_vices_fire():
    cases = load_corpus()
    findings = {
        case.id: [
            {"check_id": f"config.{rule}", "path": case.fixture}
            for rule in case.known_positive_rules
        ]
        for case in cases
    }
    report = evaluate_effectiveness(cases, findings, load_rubric())
    assert report["summary"] == {
        "rules_evaluated": 17,
        "false_positive_count": 0,
        "max_false_negative_rate": 0.0,
        "passed": True,
    }
