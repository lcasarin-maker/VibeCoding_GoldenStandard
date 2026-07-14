#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""G-01: Falsifiability dictamen for the 479 Golden Standard entries."""

import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

CATALOGS = [
    "golden_standard_coding_vices.yaml",
    "golden_standard_testing_vices.yaml",
    "golden_standard_tokenomics.yaml",
    "golden_standard_principles.yaml",
    "golden_standard_structure_principles.yaml",
    "golden_standard_adversarial_vectors.yaml",
]


def classify_falsifiability(item: dict) -> tuple[str, str]:
    """Classify the falsifiability class of a catalog item and generate its specific rationale."""
    item_id = item.get("id", "")
    title = item.get("title", "").lower()
    symptom = item.get("symptom", "").lower()
    cause = item.get("cause", "").lower()
    mech = item.get("validating_mechanism", "")

    # 1. Base on existing validating mechanism
    if mech == "static-regex":
        return "static-regex", "Falsifiable via static regex matching against source code patterns."
    if mech == "static-ast":
        return "static-ast", "Falsifiable via AST complexity and structure parsing."
    if mech in ("runtime-test", "pytest"):
        return "runtime-test", "Falsifiable under pytest suite by simulating the failure state."

    # 2. Heuristics for DOC_ONLY/doctrinal items
    text = f"{title} {symptom} {cause}"

    if any(k in text for k in ("empty", "null", "none", "collection", "index", "bounds", "length", "limit", "overflow", "range", "array", "list", "dict", "string")):
        return "runtime-test", "Falsifiable under runtime-test: requires boundary testing with empty/extreme values."
    if any(k in text for k in ("secret", "credentials", "hardcoded", "regex", "eval", "token", "lint", "naming", "path", "hardcode")):
        return "static-regex", "Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences."
    if any(k in text for k in ("concurrency", "async", "race", "lock", "thread", "timeout", "network", "hang")):
        return "runtime-test", "Falsifiable under runtime-test: requires stress/concurrency integration testing."
    if any(k in text for k in ("hallucination", "intent", "relevancy", "logic", "reasoning", "optimism", "model", "stochastic")):
        return "llm-judge", "Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator."

    return "manual-audit", "Falsifiable under manual-audit: requires human code review / peer verification."


def main() -> int:
    all_items = []
    classes_count = {
        "static-regex": 0,
        "static-ast": 0,
        "runtime-test": 0,
        "llm-judge": 0,
        "manual-audit": 0,
    }

    # Process all catalogs
    for name in CATALOGS:
        path = ROOT / name
        if not path.exists():
            print(f"⚠️ Catalog not found: {name}")
            continue

        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        items = data.get("items", []) or []
        updated_items = []
        mutated = False

        for item in items:
            f_class, rationale = classify_falsifiability(item)
            classes_count[f_class] += 1
            all_items.append((item.get("id"), item.get("title"), f_class, rationale))

            # Specifically update the boilerplate justifications for AV items
            if name == "golden_standard_adversarial_vectors.yaml" and item.get("status") == "DOC_ONLY":
                # Check if it has the boilerplate justification
                just = item.get("doc_only_justification", "")
                if "No generic executable oracle is registered" in just or not just:
                    item["doc_only_justification"] = f"{rationale} This remains documentary until a positive fixture and local test case are registered."
                    mutated = True

            updated_items.append(item)

        if mutated:
            data["items"] = updated_items
            with open(path, "w", encoding="utf-8") as f:
                yaml.safe_dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
            print(f"✅ Updated justifications in {name}")

    # Generate Report
    report_path = ROOT / "Wiki" / "Falsifiability_Report.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_content = [
        "# Falsifiability Report — Golden Standard Catalog",
        "",
        "This report classifies all catalog entries into 5 distinct falsifiability classes based on how they can be validated and prevented.",
        "",
        "## Distribution Summary",
        "",
        "| Falsifiability Class | Entry Count | Percentage | Description |",
        "| --- | --- | --- | --- |",
    ]

    total = len(all_items)
    for c, count in classes_count.items():
        pct = (count / total) * 100 if total > 0 else 0
        desc = {
            "static-regex": "Simple pattern matching of source code (e.g. banned functions, regex rules).",
            "static-ast": "Abstract Syntax Tree parsing (e.g. complexity, function structures).",
            "runtime-test": "Behavioral test runs (e.g. boundary testing, exception validation).",
            "llm-judge": "Semantic output validation (e.g. faithfulness, hallucinations).",
            "manual-audit": "Human review and peer verification (e.g. design alignment, workflow context)."
        }[c]
        report_content.append(f"| `{c}` | {count} | {pct:.1f}% | {desc} |")

    report_content.extend([
        "",
        f"**Total evaluated entries:** {total}",
        "",
        "## Detailed Inventory",
        "",
        "| ID | Title | Class | Verification Rationale |",
        "| --- | --- | --- | --- |",
    ])

    for rid, title, f_class, rationale in sorted(all_items, key=lambda x: x[0]):
        report_content.append(f"| {rid} | {title} | `{f_class}` | {rationale} |")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_content) + "\n")

    print(f"✅ Generated falsifiability report at {report_path}")
    print("\nSummary of classes:")
    for c, count in classes_count.items():
        print(f"  - {c}: {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
