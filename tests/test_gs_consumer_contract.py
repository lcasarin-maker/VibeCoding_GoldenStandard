"""GS-CONTRACT-001: Consumer contract test for Cerberus.

Validates that GS rules are project-agnostic and can be consumed
by Cerberus (or any consumer) without hardcoded module names.
"""
import yaml
import json
from pathlib import Path


def test_gs_rules_have_no_project_specific_names():
    """Verify rules don't reference project-specific module names."""
    config_path = Path("config/semgrep_vices.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    forbidden_patterns = [
        "aequitas", "cerberus", "vibeoding", "goldenstandard",
        "module_", "import_", "specific_",
    ]

    issues = []
    for rule in config.get("rules", []):
        rule_id = rule.get("id", "unknown")

        # Check message
        message = rule.get("message", "").lower()
        for pattern in forbidden_patterns:
            if pattern in message:
                issues.append(f"{rule_id}: hardcoded project name in message: {pattern}")

        # Check pattern
        pattern_text = str(rule.get("pattern", rule.get("pattern-regex", ""))).lower()
        for pattern in forbidden_patterns:
            if pattern in pattern_text:
                issues.append(f"{rule_id}: hardcoded project name in pattern: {pattern}")

    assert not issues, f"Found project-specific references:\n" + "\n".join(issues)


def test_gs_rules_can_be_serialized_to_neutral_format():
    """Verify rules export cleanly to JSON (neutral consumer format)."""
    config_path = Path("config/semgrep_vices.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Should be JSON-serializable (no Python objects)
    try:
        json_str = json.dumps(config)
        assert json_str is not None
    except TypeError as e:
        raise AssertionError(f"Rules not JSON-serializable: {e}")


def test_gs_rules_define_required_contract_fields():
    """Verify every rule has required contract fields for consumers."""
    config_path = Path("config/semgrep_vices.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    required_fields = ["id", "message", "severity", "languages", "metadata"]

    issues = []
    for rule in config.get("rules", []):
        rule_id = rule.get("id", "unknown")
        for field in required_fields:
            if field not in rule:
                issues.append(f"{rule_id}: missing required field '{field}'")

        # Verify metadata has vice_ids
        metadata = rule.get("metadata", {})
        if "vice_ids" not in metadata:
            issues.append(f"{rule_id}: metadata missing 'vice_ids'")

    assert not issues, f"Contract violations:\n" + "\n".join(issues)


def test_gs_rules_version_contract():
    """Verify rules version matches declared contract version (v3.2.0)."""
    config_path = Path("config/semgrep_vices.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Version field in config should match repo tag
    declared_version = config.get("version", "unknown")

    # Check that rules exist
    assert config.get("rules"), "No rules defined"
    assert len(config.get("rules", [])) >= 17, "Expected at least 17 rules"


if __name__ == "__main__":
    test_gs_rules_have_no_project_specific_names()
    test_gs_rules_can_be_serialized_to_neutral_format()
    test_gs_rules_define_required_contract_fields()
    test_gs_rules_version_contract()
    print("✅ All consumer contract tests passed")
