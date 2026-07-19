#!/usr/bin/env python3
"""
GS-13: Generate Golden Standard Conformity Reports

Tracks enforcement coverage of Golden Standard vices, testing vices, and
principles. Every figure is derived from the catalogs' own fields
(``status``, ``validating_mechanism``, ``test_ref``, ``doc_only_justification``)
and from enforcement infrastructure actually present on disk — nothing is
assumed or hardcoded.

Design: GS-13_CONFORMIDAD_DISEÑO_2026-07-19.md
"""

import json
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import yaml

# Mechanisms that run without a human in the loop.
AUTOMATED_MECHANISMS = {"runtime-test", "static-ast", "static-regex"}

CATALOG_FILES = {
    "VC": "golden_standard_coding_vices.yaml",
    "TV": "golden_standard_testing_vices.yaml",
    "PR": "golden_standard_principles.yaml",
}


@dataclass
class ConformityMetrics:
    """Conformity report metrics (all derived, none assumed)."""
    enforcement_coverage: float  # % of items with status PREVENTED/REMEDIATED
    doctrine_alignment: float  # % enforced or DOC_ONLY with justification
    automated_checks: int  # items whose mechanism is automated
    manual_reviews: int  # items requiring human judgment (DOC_ONLY)
    total_vices: int
    enforced_vices: int
    partial_vices: int  # REMEDIATED: fixed with evidence, not yet prevented
    proposed_only_vices: int  # DOC_ONLY
    audit_date: str
    satellite_name: str


@dataclass
class ViceStatus:
    """Status of a single catalog item, read from the catalog itself."""
    vice_id: str
    vice_type: str  # VC, TV, PR
    name: str
    status: str  # ENFORCED, REMEDIATED, DOC_ONLY
    enforcing_rules: List[str]
    coverage: float
    evidence: Optional[str] = None


class ConformityReportGenerator:
    """Generate Golden Standard conformity reports.

    Example:
        gen = ConformityReportGenerator(Path("."), satellite_name="Aequitas_OS")
        markdown = gen.generate_report(Path("out/conformity.md"))
    """

    def __init__(
        self,
        gs_path: Path,
        satellite_name: Optional[str] = None,
        satellite_path: Optional[Path] = None,
    ):
        """
        Initialize report generator.

        Args:
            gs_path: Path to Golden Standard repo root.
            satellite_name: Name of satellite repo (context label).
            satellite_path: Optional path to the satellite working tree; when
                given, its enforcement hooks are inspected too.
        """
        self.gs_path = Path(gs_path)
        self.satellite_name = satellite_name or "Unknown"
        self.satellite_path = Path(satellite_path) if satellite_path else None
        self.audit_date = datetime.now().isoformat()

        self.catalogs: Dict[str, Dict[str, dict]] = {
            prefix: self._load_catalog(filename)
            for prefix, filename in CATALOG_FILES.items()
        }

    # Backwards-compatible views used by callers/tests.
    @property
    def vices(self) -> Dict[str, dict]:
        """Coding vices catalog keyed by id."""
        return self.catalogs["VC"]

    @property
    def testing_vices(self) -> Dict[str, dict]:
        """Testing vices catalog keyed by id."""
        return self.catalogs["TV"]

    @property
    def principles(self) -> Dict[str, dict]:
        """Principles catalog keyed by id."""
        return self.catalogs["PR"]

    def _load_catalog(self, filename: str) -> Dict[str, dict]:
        """Load a v3 catalog (``items:`` list) into an id-keyed dict.

        Raises:
            FileNotFoundError / ValueError: a missing or malformed catalog is
            a hard error — reporting conformity over an empty catalog would
            silently fake 100% figures.
        """
        path = self.gs_path / filename
        if not path.exists():
            raise FileNotFoundError(f"Catalog not found: {path}")
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        items = data.get("items")
        if not isinstance(items, list) or not items:
            raise ValueError(f"Catalog {filename} has no 'items' list")
        return {item["id"]: item for item in items}

    def _collect_active_enforcers(self) -> Dict[str, List[str]]:
        """Enforcement mechanisms actually present on disk.

        Returns:
            Mapping of category -> list of detected enforcers.
        """
        enforcers: Dict[str, List[str]] = {}

        def add(category: str, name: str) -> None:
            enforcers.setdefault(category, []).append(name)

        # GS repo tooling
        for script, category in (
            ("scripts/gs_lint.py", "LINT"),
            ("scripts/aequitas_lint.py", "SP-RULES"),
            ("scripts/lint_wiki.py", "WIKI"),
        ):
            if (self.gs_path / script).exists():
                add(category, script)
        if (self.gs_path / "config" / "semgrep_vices.yaml").exists():
            add("SEMGREP", "config/semgrep_vices.yaml")
        hook = self.gs_path / ".git" / "hooks" / "pre-commit"
        if hook.exists():
            add("PRE-COMMIT", "pre-commit (GoldenStandard)")

        # CI workflows
        ci_dir = self.gs_path / ".github" / "workflows"
        if ci_dir.exists():
            for wf in sorted(ci_dir.glob("*.y*ml")):
                content = wf.read_text(encoding="utf-8", errors="replace")
                for needle, category in (
                    ("pytest", "TESTING"),
                    ("pylint", "LINT"),
                    ("mypy", "TYPE-CHECK"),
                    ("semgrep", "SEMGREP"),
                ):
                    if needle in content:
                        add(category, f"{wf.name} ({needle})")

        # Satellite tooling, only if a real path was provided.
        if self.satellite_path and self.satellite_path.exists():
            sat_hook = self.satellite_path / ".git" / "hooks" / "pre-commit"
            if sat_hook.exists():
                add("PRE-COMMIT", f"pre-commit ({self.satellite_name})")
            for lint in sorted((self.satellite_path / "scripts").glob("*lint*.py")) if (self.satellite_path / "scripts").exists() else []:
                add("SP-RULES", f"{self.satellite_name}/scripts/{lint.name}")

        return enforcers

    def _item_status(self, item: dict, vice_type: str) -> ViceStatus:
        """Translate one catalog item into a ViceStatus, no assumptions.

        Args:
            item: raw catalog entry.
            vice_type: VC, TV or PR.

        Returns:
            ViceStatus derived from the item's own status/mechanism fields.
        """
        raw_status = item.get("status", "DOC_ONLY")
        mechanism = str(item.get("validating_mechanism", "DOC_ONLY"))
        test_ref = item.get("test_ref") or ""
        rules = [r for r in (mechanism, test_ref) if r and r != "DOC_ONLY"]

        if raw_status == "PREVENTED":
            status, coverage = "ENFORCED", 1.0
        elif raw_status == "REMEDIATED":
            status, coverage = "REMEDIATED", 0.5
        else:
            status, coverage = "DOC_ONLY", 0.0

        return ViceStatus(
            vice_id=item["id"],
            vice_type=vice_type,
            name=item.get("title", "Unknown"),
            status=status,
            enforcing_rules=rules,
            coverage=coverage,
            evidence=item.get("evidence") or item.get("detection") or None,
        )

    def _calculate_vice_status(self) -> Dict[str, ViceStatus]:
        """Calculate enforcement status for every catalog item."""
        status_map: Dict[str, ViceStatus] = {}
        for vice_type, catalog in self.catalogs.items():
            for item in catalog.values():
                status = self._item_status(item, vice_type)
                status_map[status.vice_id] = status
        return status_map

    def _calculate_metrics(self, vice_status: Dict[str, ViceStatus]) -> ConformityMetrics:
        """Calculate conformity metrics from per-item statuses."""
        total = len(vice_status)
        enforced = sum(1 for v in vice_status.values() if v.status == "ENFORCED")
        partial = sum(1 for v in vice_status.values() if v.status == "REMEDIATED")
        proposed = total - enforced - partial

        automated = 0
        aligned = 0
        for v in vice_status.values():
            item = self.catalogs[v.vice_type].get(v.vice_id, {})
            if str(item.get("validating_mechanism")) in AUTOMATED_MECHANISMS:
                automated += 1
            if v.status in ("ENFORCED", "REMEDIATED") or item.get("doc_only_justification"):
                aligned += 1

        return ConformityMetrics(
            enforcement_coverage=(enforced / total * 100) if total else 0,
            doctrine_alignment=(aligned / total * 100) if total else 0,
            automated_checks=automated,
            manual_reviews=proposed,
            total_vices=total,
            enforced_vices=enforced,
            partial_vices=partial,
            proposed_only_vices=proposed,
            audit_date=self.audit_date,
            satellite_name=self.satellite_name,
        )

    def generate_report(self, output_path: Optional[Path] = None) -> str:
        """
        Generate conformity report as markdown.

        Args:
            output_path: Optional path to write report to file.

        Returns:
            Markdown report as string.
        """
        vice_status = self._calculate_vice_status()
        metrics = self._calculate_metrics(vice_status)
        date_str = datetime.fromisoformat(self.audit_date).strftime("%Y-%m-%d")

        lines: List[str] = []
        lines.append("# Golden Standard Conformity Report")
        lines.append("")
        lines.append(f"**Satellite:** {self.satellite_name}")
        lines.append(f"**Report Date:** {date_str}")
        lines.append("**Report Version:** 2.0")
        lines.append("")
        lines.append("---")
        lines.append("")

        lines.append("## Executive Summary")
        lines.append("")
        lines.append("| Metric | Value | Target |")
        lines.append("|---|---|---|")
        lines.append(f"| **Enforcement Coverage** | {metrics.enforcement_coverage:.0f}% | 90% |")
        lines.append(f"| **Doctrine Alignment** | {metrics.doctrine_alignment:.0f}% | 95% |")
        lines.append(f"| **Automated Checks** | {metrics.automated_checks}/{metrics.total_vices} | 100% |")
        lines.append(f"| **Items Needing Human Judgment (DOC_ONLY)** | {metrics.manual_reviews} | Ongoing |")
        lines.append("")

        def emit_section(title: str, vice_type: str) -> None:
            lines.append(f"## {title}")
            lines.append("")
            statuses = [v for v in vice_status.values() if v.vice_type == vice_type]
            enforced_n = sum(1 for v in statuses if v.status == "ENFORCED")
            lines.append(
                f"**{enforced_n}/{len(statuses)} enforced.** "
                "Only non-enforced items are listed (the gap is the actionable part)."
            )
            lines.append("")
            gaps = [v for v in statuses if v.status != "ENFORCED"]
            if gaps:
                lines.append("| ID | Name | Status | Mechanism |")
                lines.append("|---|---|---|---|")
                for v in sorted(gaps, key=lambda x: x.vice_id):
                    rules = ", ".join(v.enforcing_rules) or "—"
                    lines.append(f"| {v.vice_id} | {v.name} | {v.status} | {rules} |")
            else:
                lines.append("All items enforced.")
            lines.append("")

        emit_section("1. Coding Vices (VC-*)", "VC")
        emit_section("2. Testing Vices (TV-*)", "TV")
        emit_section("3. Principles (PR-*)", "PR")

        lines.append("## 4. Active Enforcement Mechanisms")
        lines.append("")
        enforcers = self._collect_active_enforcers()
        if enforcers:
            for category, enforcer_list in sorted(enforcers.items()):
                lines.append(f"### {category}")
                for enforcer in enforcer_list:
                    lines.append(f"- [OK] {enforcer}")
                lines.append("")
        else:
            lines.append("No active enforcement mechanisms detected.")
            lines.append("")

        lines.append("## 5. Recommendations")
        lines.append("")
        doc_only_with_gap = [
            v for v in vice_status.values()
            if v.status == "DOC_ONLY"
            and not self.catalogs[v.vice_type][v.vice_id].get("doc_only_justification")
        ]
        if metrics.enforcement_coverage < 90:
            lines.append("### HIGH PRIORITY")
            lines.append(
                f"1. **Enforcement coverage is {metrics.enforcement_coverage:.0f}%** "
                f"(target 90%): {metrics.proposed_only_vices} items are DOC_ONLY. "
                "Promote the ones with feasible oracles to static-ast/static-regex/runtime-test."
            )
            lines.append("")
        if doc_only_with_gap:
            lines.append(
                f"2. **{len(doc_only_with_gap)} DOC_ONLY items lack doc_only_justification** "
                "— each needs either a justification or a mechanical detector: "
                + ", ".join(v.vice_id for v in doc_only_with_gap[:10])
                + (" …" if len(doc_only_with_gap) > 10 else "")
            )
            lines.append("")
        if metrics.partial_vices:
            lines.append(
                f"3. **{metrics.partial_vices} REMEDIATED items** were fixed but have no "
                "preventive mechanism; add regression detectors to reach PREVENTED."
            )
            lines.append("")

        lines.append("## 6. Conformity Audit Trail")
        lines.append("")
        lines.append("| Date | Change | Justification |")
        lines.append("|---|---|---|")
        lines.append(f"| {date_str} | Conformity report generated from catalog data | Weekly conformity tracking |")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("**Generated by:** `scripts/generate_conformity_report.py`")
        lines.append(f"**Last updated:** {datetime.fromisoformat(self.audit_date).strftime('%Y-%m-%d %H:%M:%S')}")

        markdown = "\n".join(lines)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(markdown, encoding="utf-8")

        return markdown

    def generate_json(self, output_path: Optional[Path] = None) -> str:
        """Generate conformity report as JSON. Returns the JSON string."""
        vice_status = self._calculate_vice_status()
        metrics = self._calculate_metrics(vice_status)

        data = {
            "metrics": asdict(metrics),
            "vices": [asdict(v) for v in vice_status.values()],
        }

        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json_str, encoding="utf-8")

        return json_str


def main():
    """CLI entry point. Returns process exit code."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Golden Standard conformity report")
    parser.add_argument("--gs-path", type=Path, default=Path.cwd(), help="Path to GS repo")
    parser.add_argument("--satellite", type=str, default="Aequitas_OS", help="Satellite name")
    parser.add_argument("--satellite-path", type=Path, default=None, help="Path to satellite repo (optional)")
    parser.add_argument("--output", type=Path, help="Output markdown file")
    parser.add_argument("--json", type=Path, help="Output JSON file")

    args = parser.parse_args()

    generator = ConformityReportGenerator(args.gs_path, args.satellite, args.satellite_path)

    if args.output:
        generator.generate_report(args.output)
        print(f"Report written to {args.output}")
    else:
        print(generator.generate_report())

    if args.json:
        generator.generate_json(args.json)
        print(f"JSON written to {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
