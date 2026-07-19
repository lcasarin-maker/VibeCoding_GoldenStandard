#!/usr/bin/env python3
"""Tests for GS-11: SP linting rules."""

import sys
sys.path.insert(0, "scripts")

from aequitas_lint import AequitasLinter


def test_linter_loads_rules():
    """Test that linter loads SP rules."""
    linter = AequitasLinter()
    assert len(linter.rules) >= 5
    assert any(r.id == "SP-AQ-001" for r in linter.rules)
    assert any(r.id == "SP-AQ-002" for r in linter.rules)
    assert any(r.id == "SP-AQ-003" for r in linter.rules)
    print("✓ test_linter_loads_rules passed")


def test_rule_attributes():
    """Test that rules have correct attributes."""
    linter = AequitasLinter()
    rule = next((r for r in linter.rules if r.id == "SP-AQ-001"), None)
    assert rule is not None
    assert rule.name == "Mutable default arguments in task schemas"
    assert rule.severity == "error"
    assert rule.linked_vice == "VC-057"
    print("✓ test_rule_attributes passed")


def test_report_empty():
    """Test report for no violations."""
    linter = AequitasLinter()
    report = linter.report([])
    assert "No violations" in report
    print("✓ test_report_empty passed")


def test_report_with_violations():
    """Test report formatting with violations."""
    linter = AequitasLinter()
    violations = [
        {"file": "a.py", "line": 1, "rule_id": "SP-AQ-001", "rule_name": "Test", "severity": "error"},
        {"file": "b.py", "line": 2, "rule_id": "SP-AQ-002", "rule_name": "Test2", "severity": "warning"},
    ]
    
    report = linter.report(violations)
    assert "2 violations" in report
    assert "ERROR" in report
    assert "WARNING" in report
    print("✓ test_report_with_violations passed")


if __name__ == "__main__":
    test_linter_loads_rules()
    test_rule_attributes()
    test_report_empty()
    test_report_with_violations()
    print("\nAll GS-11 tests passed!")
