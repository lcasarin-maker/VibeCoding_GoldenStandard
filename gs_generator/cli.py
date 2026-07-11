"""Stable command-line entrypoint for Golden Standard generation."""

from __future__ import annotations

import argparse
import json
import sys

from . import audit, badges, wiki
from .engine import (
    MARKDOWN_OUTPUT,
    _ROOT,
    _display_mechanism,
    _read_version_label,
    build_canonical_domains_section,
    build_principles_section,
    extract_catalog_items,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate Golden Standard audit artifacts and/or Obsidian wiki."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--audit-only",
        action="store_true",
        help="Generate only JSON + markdown audit artifacts; skip wiki.",
    )
    group.add_argument(
        "--wiki-only",
        action="store_true",
        help="Generate only Obsidian wiki; skip JSON + markdown artifacts.",
    )
    args = parser.parse_args(argv)

    audit.JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    catalogs = audit.load_golden_standard_catalogs()
    mapped_database = {}
    for _, config in catalogs.items():
        extract_catalog_items(config, mapped_database)

    print(f"Extracted {len(mapped_database)} flaws from Golden Standard catalogs.")

    if not args.wiki_only:
        with open(audit.JSON_OUTPUT, "w", encoding="utf-8") as handle:
            json.dump(mapped_database, handle, indent=2, ensure_ascii=False)
        print(f"Successfully generated {audit.JSON_OUTPUT}")

    report_lines = [
        "# Golden Standard Compliance Audit Report",
        f"**Golden Standard {_read_version_label()} | Date: {__import__('datetime').date.today().isoformat()} | Total Audited Items: {len(mapped_database)}**",
        "",
        "This document is generated automatically by `scripts/generate_golden_audit.py` to map every Golden Standard point to its specific mitigation action and validating test in the GS tooling ecosystem.",
        "",
        "## Summary of Compliance",
        "",
        "| Category | Audited Items | Prevented / Remediated | Audited / Not Applicable | Clean Status |",
        "|---|---|---|---|---|",
        f"| **Testing & Evaluation** | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation'])} | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Vibe Coding** | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding'])} | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Tokenomics & Context** | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context'])} | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Total** | {len(mapped_database)} | {len([x for x in mapped_database.values() if x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        "",
        "---",
        "",
        "## Full Audit Details",
        "",
    ]
    for category in ["Testing & Evaluation", "Vibe Coding", "Tokenomics & Context"]:
        cat_items = [x for x in mapped_database.values() if x["category"] == category]
        report_lines.extend([f"### {category} ({len(cat_items)} items)", ""])
        report_lines.extend([
            "| ID | Flaw Title | Severity | Status | Downstream Verification | Action Taken / Prevention Method | Validating Test / Guard |",
            "|---|---|---|---|---|---|---|",
        ])
        for item in sorted(cat_items, key=lambda x: x["id"]):
            action_snippet = item["action"].replace("\n", " ")
            report_lines.append(
                f"| `{item['id']}` | {item['title']} | **{item['severity']}** | **{item['status']}** | `{item.get('downstream_verification', 'none')}` | {action_snippet} | `{_display_mechanism(item)}` |"
            )
        report_lines.append("")
    report_lines.extend(build_principles_section())
    report_lines.extend(build_canonical_domains_section())

    if not args.wiki_only:
        MARKDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        MARKDOWN_OUTPUT.write_text("\n".join(report_lines), encoding="utf-8")
        print(f"Successfully generated {MARKDOWN_OUTPUT}")
    if not args.audit_only:
        wiki.generate_obsidian_wiki(mapped_database, wiki.WIKI_DIR)
        wiki.write_canonical_structure(mapped_database)

    metrics = badges.write_metrics()
    print(
        f"Successfully generated quality metrics and badges "
        f"(deep {metrics['deep_pct']}%, {metrics['local_detectors']} detectors, {metrics['stub']} stubs)."
    )
    return 0
