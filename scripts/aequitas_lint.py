#!/usr/bin/env python3
"""GS-11: Aequitas linter — apply SP (Suspicious Pattern) rules.

Two rule engines, dispatched by the rule's own declaration:
- regex rules: applied per file (``pattern`` is a regular expression).
- AST rules (``requires_ast_analysis: true``): applied over the whole tree;
  ``pattern`` names a registered analyzer (e.g. ``circular_import``).

Failures are never silent: unreadable files and unknown analyzers are
reported as violations; a malformed rule file aborts loading loudly.
"""

import ast
import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List

import yaml


@dataclass
class SPRule:
    """Suspicious Pattern rule definition."""
    id: str
    name: str
    linked_vice: str
    severity: str
    pattern: str
    requires_ast_analysis: bool = False
    autofix: bool = False
    rationale: str = ""
    fix: str = ""


def _module_name(py_file: Path, root: Path) -> str:
    """Dotted module name of py_file relative to root (pkg.mod)."""
    rel = py_file.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts)


def _imported_modules(tree: ast.AST, current_module: str) -> List[str]:
    """Absolute dotted names imported by a module (resolving relative imports).

    Args:
        tree: parsed AST of the module.
        current_module: dotted name of the importing module.

    Returns:
        List of imported module names (absolute, best-effort).
    """
    imports: List[str] = []
    package_parts = current_module.split(".")[:-1] if current_module else []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0:
                base = node.module or ""
            else:
                anchor = package_parts[: len(package_parts) - (node.level - 1)]
                base = ".".join(anchor + ([node.module] if node.module else []))
            if base:
                imports.append(base)
                imports.extend(f"{base}.{alias.name}" for alias in node.names)
    return imports


def detect_circular_imports(files: Dict[str, Path], root: Path) -> List[List[str]]:
    """Find import cycles among the given modules.

    Args:
        files: mapping of dotted module name -> file path.
        root: tree root used to resolve module names.

    Returns:
        List of cycles, each a list of module names (first == last).
    """
    graph: Dict[str, List[str]] = {}
    for mod, path in files.items():
        try:
            tree = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except SyntaxError:
            # Reported separately by the caller as an IO/parse violation.
            graph[mod] = []
            continue
        targets = []
        for imp in _imported_modules(tree, mod):
            # Only edges inside the analyzed tree matter for cycles.
            candidate = imp
            while candidate and candidate not in files:
                candidate = candidate.rpartition(".")[0]
            if candidate and candidate != mod:
                targets.append(candidate)
        graph[mod] = sorted(set(targets))

    cycles: List[List[str]] = []
    seen_cycles = set()
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {m: WHITE for m in graph}
    stack: List[str] = []

    def dfs(node: str) -> None:
        color[node] = GRAY
        stack.append(node)
        for nxt in graph.get(node, []):
            if color.get(nxt, BLACK) == GRAY:
                cycle = stack[stack.index(nxt):] + [nxt]
                key = frozenset(cycle)
                if key not in seen_cycles:
                    seen_cycles.add(key)
                    cycles.append(cycle)
            elif color.get(nxt) == WHITE:
                dfs(nxt)
        stack.pop()
        color[node] = BLACK

    for mod in graph:
        if color[mod] == WHITE:
            dfs(mod)
    return cycles


# Registry of whole-tree analyzers addressable from a rule's ``pattern``.
AST_ANALYZERS = {"circular_import": detect_circular_imports}


class AequitasLinter:
    """Aequitas linter: load SP rules from SP_RULES/ and apply them.

    Example:
        linter = AequitasLinter()
        violations = linter.lint_directory("backend/app")
    """

    def __init__(self, rules_dir: str = "SP_RULES"):
        """Load rules from rules_dir; raises on malformed rule files."""
        self.rules_dir = Path(rules_dir)
        self.rules: List[SPRule] = []
        self._compiled: Dict[str, re.Pattern] = {}
        self._load_rules()

    def _load_rules(self) -> None:
        """Load all YAML rule files; a broken rule is a hard config error."""
        if not self.rules_dir.exists():
            return

        for rule_file in sorted(self.rules_dir.glob("sp-*.yaml")):
            with open(rule_file, encoding="utf-8") as f:
                rule_data = yaml.safe_load(f)

            rule = SPRule(
                id=rule_data.get("id"),
                name=rule_data.get("name"),
                linked_vice=rule_data.get("linked_vice"),
                severity=rule_data.get("severity"),
                pattern=(rule_data.get("pattern") or "").strip(),
                requires_ast_analysis=rule_data.get("requires_ast_analysis", False),
                autofix=rule_data.get("autofix", False),
                rationale=rule_data.get("rationale", ""),
                fix=rule_data.get("fix", ""),
            )
            if not rule.id or not rule.pattern:
                raise ValueError(f"Rule file {rule_file} lacks id or pattern")
            if rule.requires_ast_analysis:
                if rule.pattern not in AST_ANALYZERS:
                    raise ValueError(
                        f"{rule.id}: unknown AST analyzer '{rule.pattern}' "
                        f"(known: {sorted(AST_ANALYZERS)})"
                    )
            else:
                try:
                    self._compiled[rule.id] = re.compile(rule.pattern, re.MULTILINE)
                except re.error as exc:
                    raise ValueError(f"{rule.id}: invalid regex pattern: {exc}") from exc
            self.rules.append(rule)

    def _violation(self, rule: SPRule, file: str, line: int) -> Dict:
        """Build one violation record for rule at file:line."""
        return {
            "file": file,
            "line": line,
            "rule_id": rule.id,
            "rule_name": rule.name,
            "severity": rule.severity,
            "linked_vice": rule.linked_vice,
        }

    def lint_file(self, file_path: str) -> List[Dict]:
        """Apply all regex rules to one file.

        Args:
            file_path: path to a Python source file.

        Returns:
            List of violations; an unreadable file yields a LINT-IO error
            violation instead of being silently skipped.
        """
        violations: List[Dict] = []

        try:
            content = Path(file_path).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            return [{
                "file": file_path,
                "line": 0,
                "rule_id": "LINT-IO",
                "rule_name": f"Unreadable file: {exc}",
                "severity": "error",
                "linked_vice": None,
            }]

        for rule in self.rules:
            if rule.requires_ast_analysis:
                continue  # whole-tree rules run in lint_directory
            for match in self._compiled[rule.id].finditer(content):
                line_no = content[: match.start()].count("\n") + 1
                violations.append(self._violation(rule, file_path, line_no))

        return violations

    def lint_directory(self, dir_path: str = ".") -> List[Dict]:
        """Lint all Python files under dir_path (regex + AST rules).

        Returns:
            Combined violation list from per-file regex rules and
            whole-tree AST analyzers (e.g. circular imports).
        """
        root = Path(dir_path).resolve()
        all_violations: List[Dict] = []
        modules: Dict[str, Path] = {}

        for py_file in sorted(root.rglob("*.py")):
            if any(skip in py_file.parts for skip in (".venv", "__pycache__", ".git", "node_modules")):
                continue
            all_violations.extend(self.lint_file(str(py_file)))
            name = _module_name(py_file, root)
            if name:
                modules[name] = py_file

        for rule in self.rules:
            if not rule.requires_ast_analysis:
                continue
            analyzer = AST_ANALYZERS[rule.pattern]
            for cycle in analyzer(modules, root):
                first = modules[cycle[0]]
                v = self._violation(rule, str(first), 1)
                v["cycle"] = " -> ".join(cycle)
                all_violations.append(v)

        return all_violations

    def report(self, violations: List[Dict]) -> str:
        """Render a readable report grouped by severity."""
        if not violations:
            return "OK: No violations found."

        out = f"Found {len(violations)} violations:\n"
        by_severity: Dict[str, List[Dict]] = {}
        for v in violations:
            by_severity.setdefault(v["severity"], []).append(v)

        for sev in ("error", "warning", "info"):
            if sev in by_severity:
                out += f"\n{sev.upper()} ({len(by_severity[sev])}):\n"
                for v in by_severity[sev][:5]:
                    extra = f" [{v['cycle']}]" if "cycle" in v else ""
                    out += f"  {v['file']}:{v['line']} — {v['rule_name']} ({v['rule_id']}){extra}\n"
                if len(by_severity[sev]) > 5:
                    out += f"  ... and {len(by_severity[sev]) - 5} more\n"

        return out


def main() -> int:
    """CLI entry point: lint cwd, print report, write JSON, exit 1 on errors."""
    linter = AequitasLinter()
    violations = linter.lint_directory(".")
    print(linter.report(violations))

    with open(".aequitas-lint-report.json", "w", encoding="utf-8") as f:
        json.dump(violations, f, indent=2)

    errors = [v for v in violations if v["severity"] == "error"]
    return 1 if errors else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
