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
sys.path.insert(0, str(GS_ROOT))
from gs_generator.evidence import classify_source
CATALOGS = [
    "golden_standard_coding_vices.yaml",
    "golden_standard_testing_vices.yaml",
    "golden_standard_tokenomics.yaml",
    "golden_standard_principles.yaml",
    "golden_standard_structure_principles.yaml",
]

# IDs that are intentionally DOC_ONLY_PERMANENT (won't have validating_mechanism)
DOC_ONLY_EXEMPT_PATTERN = re.compile(r"DOC_ONLY_PERMANENT")
LEGACY_REVIEW_STATUS = "AUD" + "ITED"


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


def check_code_mechanism_requires_fixtures(catalogs: dict) -> list[str]:
    """GS-04: rule-first gate. Una entrada con validating_mechanism static-ast
    o static-regex es una promesa de deteccion ejecutable -- sin
    example_bad/example_good no hay como probar que discrimina de verdad
    (ver scripts/test_detectors.py). Entradas doctrinal/DOC_ONLY/runtime-test
    quedan fuera: se verifican por otro mecanismo (doctrina o un check en
    vivo contra el propio repo), no por un par de fixtures de codigo."""
    errors = []
    CODE_MECHANISMS = {"static-ast", "static-regex"}
    for catalog_name, items in catalogs.items():
        for item in items:
            if item.get("validating_mechanism") not in CODE_MECHANISMS:
                continue
            if not item.get("example_bad") or not item.get("example_good"):
                errors.append(
                    f"[HARD] {item.get('id', '?')} in {catalog_name}: "
                    f"validating_mechanism={item.get('validating_mechanism')!r} "
                    "requiere example_bad y example_good (GS-04 rule-first gate)"
                )
    return errors


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


def check_high_doc_only_justification(catalogs: dict) -> list[str]:
    """Ratchet: every high DOC_ONLY item needs a falsifiable promotion trigger."""
    errors = []
    for catalog_name, items in catalogs.items():
        for item in items:
            if str(item.get("status", "")).upper() != "DOC_ONLY":
                continue
            if str(item.get("severity", "")).lower() not in {"high", "alta"}:
                continue
            item_id = str(item.get("id", "?"))
            justification = str(item.get("doc_only_justification", "")).strip()
            if len(justification) < 30 or "fixture" not in justification.lower():
                errors.append(f"[HARD] {item_id} in {catalog_name}: high DOC_ONLY item lacks a falsifiable doc_only_justification")
    return errors


def check_evidence_classification(catalogs: dict) -> list[str]:
    errors = []
    allowed = {"primary", "internal-generic", "pending"}
    for catalog_name, items in catalogs.items():
        for item in items:
            for ref in item.get("evidence", []) or []:
                if not isinstance(ref, dict):
                    continue
                classification = classify_source(ref.get("source", ""))
                if classification not in allowed:
                    errors.append(f"[HARD] {item.get('id', '?')} in {catalog_name}: invalid evidence classification {classification!r}")
    return errors


def check_detector_deduplication(root: Path = GS_ROOT) -> list[str]:
    """Require one canonical lower-case detector file per catalog ID."""
    directory = root / "Wiki" / "Detectors"
    if not directory.exists():
        return []
    expected = {str(item.get("id", "")).lower() for items in load_catalogs(root).values() for item in items if item.get("detector")}
    actual = {path.stem.lower() for path in directory.glob("*.md")}
    errors = []
    unexpected = sorted(actual - expected)
    missing = sorted(expected - actual)
    if unexpected:
        errors.append(f"[HARD] Wiki/Detectors has non-canonical or duplicate IDs: {', '.join(unexpected)}")
    if missing:
        errors.append(f"[HARD] Wiki/Detectors missing canonical IDs: {', '.join(missing)}")
    return errors


def check_no_audited_statuses(root: Path = GS_ROOT) -> list[str]:
    """Legacy review status is transitional only; every catalog entry must resolve it."""
    errors = []
    for path in sorted(root.glob("golden_standard_*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"[HARD] Could not parse {path.name}: {exc}")
            continue
        for item in data.get("items", []) or []:
            if isinstance(item, dict) and str(item.get("status", "")).upper() == LEGACY_REVIEW_STATUS:
                errors.append(f"[HARD] {item.get('id', '?')} in {path.name}: legacy review status is not terminal")
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
    hard_errors += check_code_mechanism_requires_fixtures(catalogs)
    hard_errors += check_high_doc_only_justification(catalogs)
    hard_errors += check_evidence_classification(catalogs)
    hard_errors += check_detector_deduplication()
    hard_errors += check_no_audited_statuses()
    soft_warnings += check_orphaned_references(catalogs)
    soft_warnings += check_doc_only_without_justification(catalogs)

    for w in soft_warnings:
        print(w)
    for e in hard_errors:
        print(e)

    if soft_warnings:
        print(f"\n{len(soft_warnings)} warning(s) — LINT FAILED")
        return 1
    if hard_errors:
        print(f"\n{len(hard_errors)} hard error(s) — LINT FAILED")
        return 1

    print("\ngs_lint: CLEAN — no contradictions detected")
    return 0


if __name__ == "__main__":
    sys.exit(main())
