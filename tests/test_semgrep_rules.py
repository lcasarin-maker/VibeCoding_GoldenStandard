from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
import pytest


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


NEW_RULE_FIXTURES = {
    "gs-vc-094-bom-in-config": ("positive_bom.yaml", "negative_bom.yaml"),
    "gs-vc-050-runtime-dependency-install": ("positive_runtime_install.py", "negative_runtime_install.py"),
    "gs-vc-051-non-atomic-state-write": ("positive_non_atomic_state.py", "negative_non_atomic_state.py"),
    "gs-vt-080-physical-address-assert": ("positive_physical_address.py", "negative_physical_address.py"),
    "gs-vt-106-unjustified-coverage-exclusion": ("positive_coverage.ini", "negative_coverage.ini"),
}


@pytest.mark.parametrize("rule_id,fixtures", NEW_RULE_FIXTURES.items())
def test_each_new_rule_has_positive_and_negative_fixture(rule_id, fixtures):
    positive, negative = fixtures
    positive_ids = {
        item["check_id"].split(".")[-1]
        for item in _run_semgrep(positive)["results"]
    }
    negative_ids = {
        item["check_id"].split(".")[-1]
        for item in _run_semgrep(negative)["results"]
    }
    assert positive_ids == {rule_id}
    assert rule_id not in negative_ids
