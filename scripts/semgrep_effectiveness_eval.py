from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "config" / "semgrep_vices.yaml"
RUBRIC = ROOT / "config" / "semgrep_effectiveness_rubric.json"
CORPUS = ROOT / "tests" / "semgrep_effectiveness_corpus.json"
LEDGER = ROOT / "docs" / "semgrep_effectiveness_ledger.json"
BADGE = ROOT / "docs" / "badges" / "semgrep-effectiveness.json"


class EvalConfigError(ValueError):
    """Raised when the preregistered eval inputs are incomplete."""


@dataclass(frozen=True)
class CorpusCase:
    id: str
    fixture: str
    known_positive_rules: tuple[str, ...]


def _read_json(path: Path) -> dict:
    if not path.is_file():
        raise EvalConfigError(f"missing eval input: {path.relative_to(ROOT).as_posix()}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise EvalConfigError(f"eval input must be an object: {path.name}")
    return payload


def load_rubric(path: Path = RUBRIC) -> dict:
    rubric = _read_json(path)
    required = {"name", "version", "committed_before_run", "metrics", "gate"}
    missing = sorted(required - rubric.keys())
    if missing:
        raise EvalConfigError(f"rubric missing required keys: {', '.join(missing)}")
    if rubric["committed_before_run"] is not True:
        raise EvalConfigError("rubric must declare committed_before_run=true")
    if not isinstance(rubric["metrics"], list) or not rubric["metrics"]:
        raise EvalConfigError("rubric metrics must be a non-empty list")
    return rubric


def load_corpus(path: Path = CORPUS) -> tuple[CorpusCase, ...]:
    payload = _read_json(path)
    raw_cases = payload.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise EvalConfigError("corpus must define at least one case")
    cases: list[CorpusCase] = []
    for raw in raw_cases:
        if not isinstance(raw, dict):
            raise EvalConfigError("each corpus case must be an object")
        fixture = str(raw.get("fixture", "")).strip()
        case_id = str(raw.get("id", "")).strip()
        positives = raw.get("known_positive_rules", [])
        if not case_id or not fixture or not isinstance(positives, list):
            raise EvalConfigError("corpus cases require id, fixture, known_positive_rules")
        cases.append(
            CorpusCase(
                id=case_id,
                fixture=fixture.replace("\\", "/"),
                known_positive_rules=tuple(str(rule).strip() for rule in positives),
            )
        )
    return tuple(cases)


def _normalize_rule_id(check_id: str) -> str:
    return check_id.replace("\\", "/").split(".")[-1]


def _normalize_path(path: str) -> str:
    candidate = path.replace("\\", "/")
    if candidate.startswith(str(ROOT).replace("\\", "/")):
        return Path(candidate).relative_to(ROOT).as_posix()
    return candidate


def run_semgrep_for_case(case: CorpusCase) -> list[dict]:
    semgrep = shutil.which("semgrep")
    if semgrep is None:
        raise EvalConfigError("Semgrep must be installed to measure live effectiveness")
    result = subprocess.run(
        [semgrep, "--config", str(RULES), "--json", str(ROOT / case.fixture)],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise EvalConfigError(result.stderr.strip() or "semgrep execution failed")
    payload = json.loads(result.stdout)
    return list(payload.get("results", []))


def evaluate_effectiveness(
    cases: tuple[CorpusCase, ...],
    findings_by_case: dict[str, list[dict]],
    rubric: dict,
) -> dict:
    all_rules = sorted({rule for case in cases for rule in case.known_positive_rules})
    false_positive_count = 0
    by_rule: dict[str, dict] = {
        rule: {"known_positive_cases": 0, "detected_cases": 0, "false_negatives": []}
        for rule in all_rules
    }

    for case in cases:
        findings = findings_by_case.get(case.id, [])
        detected = {
            _normalize_rule_id(str(item.get("check_id", "")))
            for item in findings
            if _normalize_path(str(item.get("path", ""))) == case.fixture
        }
        expected = set(case.known_positive_rules)
        for rule in expected:
            by_rule[rule]["known_positive_cases"] += 1
            if rule in detected:
                by_rule[rule]["detected_cases"] += 1
            else:
                by_rule[rule]["false_negatives"].append(case.id)
        false_positive_count += len(detected - expected)

    for metrics in by_rule.values():
        denominator = metrics["known_positive_cases"] or 1
        metrics["false_negative_rate"] = (
            denominator - metrics["detected_cases"]
        ) / denominator

    gate = rubric["gate"]
    max_fn = max(
        (metrics["false_negative_rate"] for metrics in by_rule.values()),
        default=0.0,
    )
    passed = (
        max_fn <= float(gate["max_false_negative_rate"])
        and false_positive_count <= int(gate["max_false_positive_count"])
    )
    return {
        "schema_version": 1,
        "rubric": {
            "path": RUBRIC.relative_to(ROOT).as_posix(),
            "name": rubric["name"],
            "version": rubric["version"],
            "committed_before_run": True,
        },
        "corpus": CORPUS.relative_to(ROOT).as_posix(),
        "rules": by_rule,
        "summary": {
            "rules_evaluated": len(by_rule),
            "false_positive_count": false_positive_count,
            "max_false_negative_rate": max_fn,
            "passed": passed,
        },
    }


def write_ledgers(report: dict, ledger_path: Path = LEDGER, badge_path: Path = BADGE) -> None:
    stamped = {
        **report,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    ledger_path.write_text(json.dumps(stamped, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    color = "brightgreen" if report["summary"]["passed"] else "red"
    message = f"FN {report['summary']['max_false_negative_rate']:.1%}"
    badge_path.write_text(
        json.dumps(
            {
                "schemaVersion": 1,
                "label": "semgrep effectiveness",
                "message": message,
                "color": color,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Measure GS Semgrep rule effectiveness")
    parser.add_argument("--no-write", action="store_true", help="Do not update GS ledgers")
    args = parser.parse_args()

    rubric = load_rubric()
    cases = load_corpus()
    findings = {case.id: run_semgrep_for_case(case) for case in cases}
    report = evaluate_effectiveness(cases, findings, rubric)
    if not args.no_write:
        write_ledgers(report)
    print(json.dumps(report["summary"], sort_keys=True))
    return 0 if report["summary"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
