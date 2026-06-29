"""
gs_lint.py — GS inter-catalog contradiction & health detector (Karpathy-lint pattern).

Deterministic: uses regex/set operations, no LLM calls.
Runs against all YAML catalogs in the GS root.
Exits 0 if clean, 1 if hard contradictions found.
"""

import sys
import re
from pathlib import Path

import yaml

GS_ROOT = Path(__file__).resolve().parent.parent
CATALOGS = [
    "golden_standard_coding_vices.yaml",
    "golden_standard_testing_vices.yaml",
    "golden_standard_tokenomics.yaml",
    "golden_standard_principles.yaml",
    "golden_standard_structure_principles.yaml",
]

# IDs that are intentionally DOC_ONLY_PERMANENT (won't have validating_mechanism)
DOC_ONLY_EXEMPT_PATTERN = re.compile(r"DOC_ONLY_PERMANENT")


def load_catalogs(root: Path) -> dict[str, list[dict]]:
    catalogs = {}
    for name in CATALOGS:
        path = root / name
        if not path.exists():
            print(f"[WARN] Catalog not found: {name}")
            continue
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        catalogs[name] = data.get("items", [])
    return catalogs


def check_duplicate_ids(catalogs: dict) -> list[str]:
    """Each ID must be globally unique across all catalogs."""
    seen: dict[str, str] = {}
    errors = []
    for catalog_name, items in catalogs.items():
        for item in items:
            item_id = item.get("id", "")
            if item_id in seen:
                errors.append(
                    f"[HARD] Duplicate ID {item_id!r} in {catalog_name} "
                    f"and {seen[item_id]}"
                )
            else:
                seen[item_id] = catalog_name
    return errors


def check_orphaned_references(catalogs: dict) -> list[str]:
    """related_to and supersedes fields must reference existing IDs."""
    all_ids: set[str] = set()
    for items in catalogs.values():
        for item in items:
            all_ids.add(item.get("id", ""))

    warnings = []
    for catalog_name, items in catalogs.items():
        for item in items:
            item_id = item.get("id", "?")
            for field in ("related_to", "supersedes"):
                refs = item.get(field, []) or []
                if isinstance(refs, str):
                    refs = [refs]
                for ref in refs:
                    if ref and ref not in all_ids:
                        warnings.append(
                            f"[SOFT] {item_id} in {catalog_name}: "
                            f"{field}={ref!r} references unknown ID"
                        )
    return warnings


def check_missing_required_fields(catalogs: dict) -> list[str]:
    """Every item must have id, title, and status."""
    errors = []
    for catalog_name, items in catalogs.items():
        for item in items:
            for field in ("id", "title", "status"):
                if not item.get(field):
                    errors.append(
                        f"[HARD] Missing field {field!r} in item "
                        f"{item.get('id', '?')} of {catalog_name}"
                    )
    return errors


def check_doc_only_without_justification(catalogs: dict) -> list[str]:
    """DOC_ONLY items that are not PERMANENT should have a validating_mechanism planned."""
    warnings = []
    for catalog_name, items in catalogs.items():
        for item in items:
            status = item.get("status", "")
            if "DOC_ONLY" in status and "PERMANENT" not in status:
                mech = item.get("validating_mechanism", "")
                if not mech or mech.lower() in ("none", ""):
                    warnings.append(
                        f"[SOFT] {item.get('id', '?')} in {catalog_name}: "
                        f"DOC_ONLY without validating_mechanism — debt candidate"
                    )
    return warnings


def check_status_contradiction(catalogs: dict) -> list[str]:
    """PREVENTED items with no validating_mechanism are a contradiction."""
    errors = []
    for catalog_name, items in catalogs.items():
        for item in items:
            status = item.get("status", "")
            mech = item.get("validating_mechanism", "") or ""
            if status == "PREVENTED" and mech.lower() in ("none", ""):
                errors.append(
                    f"[HARD] {item.get('id', '?')} in {catalog_name}: "
                    f"status=PREVENTED but validating_mechanism=none — contradiction"
                )
    return errors


def main() -> int:
    catalogs = load_catalogs(GS_ROOT)
    if not catalogs:
        print("[ERROR] No catalogs loaded.")
        return 1

    total_items = sum(len(v) for v in catalogs.values())
    print(f"gs_lint: loaded {len(catalogs)} catalogs, {total_items} items")

    hard_errors: list[str] = []
    soft_warnings: list[str] = []

    hard_errors += check_duplicate_ids(catalogs)
    hard_errors += check_missing_required_fields(catalogs)
    hard_errors += check_status_contradiction(catalogs)
    soft_warnings += check_orphaned_references(catalogs)
    soft_warnings += check_doc_only_without_justification(catalogs)

    for w in soft_warnings:
        print(w)
    for e in hard_errors:
        print(e)

    if soft_warnings:
        print(f"\n{len(soft_warnings)} soft warning(s) — non-blocking")
    if hard_errors:
        print(f"\n{len(hard_errors)} hard error(s) — LINT FAILED")
        return 1

    print("\ngs_lint: CLEAN — no contradictions detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
