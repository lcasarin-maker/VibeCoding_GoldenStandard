#!/usr/bin/env python3
"""GS-SUPP-001: Suppression governance mechanism.

Enforces that all code suppressions (# nosemgrep, # noqa, # type: ignore)
must include a ticket reference and justification.

Maintains a central registry of approved suppressions.
"""
import re
from pathlib import Path
from datetime import datetime
import json


class SuppressionRegistry:
    """Central registry for code suppressions."""

    def __init__(self, registry_path=".protocol/suppressions.json"):
        self.registry_path = Path(registry_path)
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.entries = self._load_registry()

    def _load_registry(self):
        """Load existing registry or create empty."""
        if self.registry_path.exists():
            return json.loads(self.registry_path.read_text())
        return {"suppressions": [], "last_audit": None}

    def add_suppression(self, file_path: str, line_no: int, suppression_type: str,
                       ticket: str, justification: str):
        """Register a suppression."""
        entry = {
            "file": file_path,
            "line": line_no,
            "type": suppression_type,
            "ticket": ticket,
            "justification": justification,
            "timestamp": datetime.now().isoformat(),
        }
        self.entries["suppressions"].append(entry)
        self._save_registry()

    def _save_registry(self):
        """Persist registry to disk."""
        self.registry_path.write_text(json.dumps(self.entries, indent=2))

    def validate_file(self, file_path: str) -> list:
        """Scan file for suppressions and validate each one."""
        issues = []
        content = Path(file_path).read_text()

        # Pattern: suppression directive + ticket + justification
        suppression_pattern = r'#\s*(nosemgrep|noqa|type:\s*ignore)\s*(?:#\s*ticket=(\w+-\d+))?\s*(?:#\s*(.+))?'

        for line_no, line in enumerate(content.split('\n'), 1):
            match = re.search(suppression_pattern, line)
            if match:
                supp_type = match.group(1)
                ticket = match.group(2)
                justification = match.group(3)

                if not ticket:
                    issues.append({
                        "file": file_path,
                        "line": line_no,
                        "type": supp_type,
                        "error": "Suppression missing ticket reference (e.g., # ticket=JIRA-123)"
                    })
                if not justification:
                    issues.append({
                        "file": file_path,
                        "line": line_no,
                        "type": supp_type,
                        "error": "Suppression missing justification (e.g., # reason: <why>)"
                    })
                else:
                    # Record valid suppression
                    self.add_suppression(file_path, line_no, supp_type, ticket or "NONE", justification)

        return issues

    def audit_report(self) -> str:
        """Generate audit report."""
        report = f"Suppression Audit Report\n"
        report += f"Total suppressions: {len(self.entries['suppressions'])}\n"
        report += f"Last audit: {self.entries.get('last_audit', 'never')}\n\n"

        for entry in self.entries['suppressions'][-10:]:  # Last 10
            report += f"  [{entry['line']}] {entry['file']}: {entry['type']} ({entry['ticket']})\n"
            report += f"    Reason: {entry['justification']}\n"

        return report


# CLI
if __name__ == "__main__":
    import sys

    registry = SuppressionRegistry()

    if len(sys.argv) < 2:
        print("Usage: python suppression_registry.py <command> [args]")
        print("Commands:")
        print("  validate <file>        - Check file for unregistered suppressions")
        print("  audit                  - Print audit report")
        sys.exit(1)

    command = sys.argv[1]

    if command == "validate" and len(sys.argv) > 2:
        issues = registry.validate_file(sys.argv[2])
        if issues:
            print(f"❌ Found {len(issues)} suppression issues:")
            for issue in issues:
                print(f"  {issue['file']}:{issue['line']}: {issue['error']}")
            sys.exit(1)
        else:
            print(f"✅ All suppressions in {sys.argv[2]} are properly registered")
    elif command == "audit":
        print(registry.audit_report())
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
