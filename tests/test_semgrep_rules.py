from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "config" / "semgrep_vices.yaml"
FIXTURES = ROOT / "tests" / "semgrep_fixtures"


def _run_semgrep(fixture: str) -> dict:
    semgrep = shutil.which("semgrep")
    if semgrep is None:
        raise AssertionError("Semgrep must be installed to run the GS rule contract")
    result = subprocess.run(
        [semgrep, "--config", str(RULES), "--json", str(FIXTURES / fixture)],
        cwd=ROOT,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


def test_semgrep_rules_fire_on_positive_fixture():
    findings = _run_semgrep("positive.py")["results"]
    rule_ids = {item["check_id"].split(".")[-1] for item in findings}
    assert rule_ids == {
        "gs-vc-095-hardcoded-secret",
        "gs-vc-115-unsafe-eval",
        "gs-vc-109-hardcoded-path",
        "gs-vt-040-blind-except",
        "gs-vt-043-unconditional-exit-zero",
        "gs-vt-005-vacuous-assert",
        "gs-vt-009-tautological-assert",
        "gs-vc-036-destructive-without-dryrun",
        "gs-vc-038-optimistic-config",
        "gs-vc-025-io-without-validation",
        "gs-vc-017-deadlock-without-heartbeat",
        "gs-vt-006-test-without-assert",
    }


def test_semgrep_rules_do_not_fire_on_negative_fixture():
    assert _run_semgrep("negative.py")["results"] == []
