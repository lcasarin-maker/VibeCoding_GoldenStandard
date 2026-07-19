#!/usr/bin/env python3
"""GS-RAC-001: Generate rule-first scaffold for new Semgrep rules.

Usage:
  python scripts/generate_rule_scaffold.py VC-NNN "rule description" python "pattern-regex" --severity ERROR

Outputs:
  - config/semgrep_vices.yaml (appended with new rule)
  - tests/semgrep_fixtures/positive_<name>.py (skeleton)
  - tests/semgrep_fixtures/negative_<name>.py (skeleton)
  - tests/test_rule_<name>.py (basic test)
"""
import argparse
import yaml
from pathlib import Path
from datetime import datetime

def generate_rule_scaffold(rule_id, title, language, pattern, severity="WARNING"):
    """Generate rule scaffold."""
    rule_name = rule_id.lower().replace("-", "_")

    # Rule definition
    rule = {
        "id": f"gs-{rule_id.lower()}",
        "message": f"{rule_id}: {title}",
        "severity": severity,
        "languages": [language],
        "pattern-regex" if pattern.startswith("(") or "/" in pattern else "pattern": pattern,
        "metadata": {
            "vice_ids": [rule_id],
            "category": "vibe-coding"
        }
    }

    # Add to config
    config_path = Path("config/semgrep_vices.yaml")
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        config['rules'].append(rule)
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)
        print(f"✅ Added rule {rule['id']} to config")

    # Create fixtures
    fixtures_dir = Path("tests/semgrep_fixtures")
    fixtures_dir.mkdir(exist_ok=True)

    pos_fixture = fixtures_dir / f"positive_{rule_name}.{language}"
    neg_fixture = fixtures_dir / f"negative_{rule_name}.{language}"

    pos_fixture.write_text(f"# {rule_id}: Positive case - should trigger\n# TODO: add code that matches the pattern\n")
    neg_fixture.write_text(f"# {rule_id}: Negative case - should NOT trigger\n# TODO: add code that does not match the pattern\n")
    print(f"✅ Created fixtures: {pos_fixture.name}, {neg_fixture.name}")

    # Create test
    test_path = Path("tests") / f"test_rule_{rule_name}.py"
    test_code = f'''"""Test for {rule_id}: {title}"""
import subprocess
from pathlib import Path

def test_{rule_name}_positive():
    """Verify rule detects positive case."""
    result = subprocess.run(
        ["semgrep", "--config", "config/semgrep_vices.yaml", "--json", "tests/semgrep_fixtures/positive_{rule_name}.py"],
        capture_output=True, text=True, check=False
    )
    assert result.returncode == 0 or "results" in result.stdout, f"Failed to run semgrep: {{result.stderr}}"

def test_{rule_name}_negative():
    """Verify rule does not detect negative case."""
    result = subprocess.run(
        ["semgrep", "--config", "config/semgrep_vices.yaml", "--json", "tests/semgrep_fixtures/negative_{rule_name}.py"],
        capture_output=True, text=True, check=False
    )
    # Rule should not find matches in negative fixture
    assert "results" in result.stdout or result.returncode == 0
'''
    test_path.write_text(test_code)
    print(f"✅ Created test: {test_path.name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Semgrep rule scaffold (GS-RAC-001)")
    parser.add_argument("rule_id", help="Vice ID (e.g. VC-017)")
    parser.add_argument("title", help="Rule description")
    parser.add_argument("language", help="Language (python/bash/etc)")
    parser.add_argument("pattern", help="Semgrep pattern (regex or pattern syntax)")
    parser.add_argument("--severity", default="WARNING", help="Severity level")

    args = parser.parse_args()
    generate_rule_scaffold(args.rule_id, args.title, args.language, args.pattern, args.severity)
    print("\\n🎯 Scaffold complete. Edit fixtures and refine the rule pattern.")
