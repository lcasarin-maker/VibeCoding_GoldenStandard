#!/usr/bin/env python3
"""GS-11: Aequitas linter — apply SP (Suspicious Pattern) rules."""

import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict
import yaml


@dataclass
class SPRule:
    """Suspicious Pattern rule definition."""
    id: str
    name: str
    linked_vice: str
    severity: str
    pattern: str
    autofix: bool = False
    rationale: str = ""
    fix: str = ""


class AequitasLinter:
    """
    Aequitas linter: load SP rules from SP_RULES/ and apply to Python files.
    """
    
    def __init__(self, rules_dir: str = "SP_RULES"):
        self.rules_dir = Path(rules_dir)
        self.rules: List[SPRule] = []
        self._load_rules()
    
    def _load_rules(self):
        """Load all YAML rule files."""
        if not self.rules_dir.exists():
            return
        
        for rule_file in sorted(self.rules_dir.glob("sp-*.yaml")):
            with open(rule_file) as f:
                rule_data = yaml.safe_load(f)
            
            rule = SPRule(
                id=rule_data.get("id"),
                name=rule_data.get("name"),
                linked_vice=rule_data.get("linked_vice"),
                severity=rule_data.get("severity"),
                pattern=rule_data.get("pattern"),
                autofix=rule_data.get("autofix", False),
                rationale=rule_data.get("rationale", ""),
                fix=rule_data.get("fix", ""),
            )
            self.rules.append(rule)
    
    def lint_file(self, file_path: str) -> List[Dict]:
        """
        Lint a single Python file.
        
        Returns:
            List of violations {file, line, rule_id, rule_name, severity}
        """
        violations = []
        
        try:
            with open(file_path) as f:
                content = f.read()
            lines = content.split("\n")
        except Exception:
            return violations
        
        for rule in self.rules:
            if "circular" in rule.pattern.lower():
                continue  # Skip AST-only rules for now
            
            try:
                regex = re.compile(rule.pattern, re.MULTILINE)
                matches = regex.finditer(content)
                
                for match in matches:
                    # Find line number
                    line_no = content[:match.start()].count("\n") + 1
                    violations.append({
                        "file": file_path,
                        "line": line_no,
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "severity": rule.severity,
                        "linked_vice": rule.linked_vice,
                    })
            except Exception:
                pass
        
        return violations
    
    def lint_directory(self, dir_path: str = ".") -> List[Dict]:
        """Lint all Python files in directory recursively."""
        all_violations = []
        
        for py_file in Path(dir_path).rglob("*.py"):
            # Skip common exclusions
            if any(skip in str(py_file) for skip in [".venv", "__pycache__", ".git"]):
                continue
            
            violations = self.lint_file(str(py_file))
            all_violations.extend(violations)
        
        return all_violations
    
    def report(self, violations: List[Dict]) -> str:
        """Generate readable report."""
        if not violations:
            return "✓ No violations found."
        
        report = f"Found {len(violations)} violations:\n\n"
        
        # Group by severity
        by_severity = {}
        for v in violations:
            sev = v["severity"]
            if sev not in by_severity:
                by_severity[sev] = []
            by_severity[sev].append(v)
        
        for sev in ["error", "warning", "info"]:
            if sev in by_severity:
                report += f"\n{sev.upper()} ({len(by_severity[sev])}):\n"
                for v in by_severity[sev][:5]:
                    report += f"  {v['file']}:{v['line']} — {v['rule_name']} ({v['rule_id']})\n"
                if len(by_severity[sev]) > 5:
                    report += f"  ... and {len(by_severity[sev]) - 5} more\n"
        
        return report


def main():
    """Run linter."""
    linter = AequitasLinter()
    violations = linter.lint_directory(".")
    print(linter.report(violations))
    
    # Export JSON
    with open(".aequitas-lint-report.json", "w") as f:
        json.dump(violations, f, indent=2)
    
    # Exit code based on errors
    errors = [v for v in violations if v["severity"] == "error"]
    return 1 if errors else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
