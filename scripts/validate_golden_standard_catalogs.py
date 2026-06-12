#!/usr/bin/env python3
"""Validate Golden Standard catalogs and their generated wiki coverage."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "golden_standard.yaml"
WIKI_VICES_DIR = ROOT / "Wiki" / "Vices"
WIKI_TOKENOMICS_DIR = ROOT / "Wiki" / "Tokenomics"
WIKI_INSIGHTS_DIR = ROOT / "Wiki" / "Project_Insights"
ALLOWED_STATUSES = {"DOC_ONLY", "AUDITED", "PREVENTED", "REMEDIATED"}
ALLOWED_DOWNSTREAM_VERIFICATIONS = {"required", "none"}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
TAG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+?)\]\]")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
CATALOG_REQUIRED_FIELDS = (
    "id",
    "title",
    "symptom",
    "cause",
    "solution",
    "status",
    "severity",
    "tags",
    "action",
    "validating_mechanism",
    "downstream_verification",
    "tier",
)


def is_ascii_text(value: object) -> bool:
    try:
        str(value).encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} does not contain a YAML mapping at the top level.")
    return data


def validate_vices_catalog(path: Path, errors: list[str], check_wiki: bool) -> None:
    data = load_yaml(path)
    items = data.get("items", [])
    if not isinstance(items, list):
        errors.append(f"{path}: 'items' must be a list.")
        return

    all_ids = {str(it.get("id", "")).strip() for it in items if isinstance(it, dict)}
    seen_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"{path}: item {index} is not a mapping.")
            continue

        item_id = str(item.get("id", "")).strip()
        missing = [field for field in CATALOG_REQUIRED_FIELDS if not str(item.get(field, "")).strip()]
        if missing:
            errors.append(f"{path}: {item_id or f'item {index}'} missing required fields: {', '.join(missing)}")

        if item_id and not is_ascii_text(item_id):
            errors.append(f"{path}: {item_id or f'item {index}'} must use ASCII-only technical identifiers.")

        if item_id in seen_ids:
            errors.append(f"{path}: duplicate id {item_id}.")
        elif item_id:
            seen_ids.add(item_id)

        status = str(item.get("status", "")).strip()
        if status and status not in ALLOWED_STATUSES:
            errors.append(f"{path}: {item_id or f'item {index}'} has unsupported status {status}.")

        severity = str(item.get("severity", "")).strip()
        if severity and severity not in ALLOWED_SEVERITIES:
            errors.append(f"{path}: {item_id or f'item {index}'} has unsupported severity {severity}.")

        tier = str(item.get("tier", "")).strip()
        if tier and tier not in {"core", "extended", "specialist"}:
            errors.append(f"{path}: {item_id or f'item {index}'} has unsupported tier {tier}.")

        downstream_verification = str(item.get("downstream_verification", "")).strip()
        if not downstream_verification:
            errors.append(f"{path}: {item_id or f'item {index}'} missing required field: downstream_verification")
        elif downstream_verification not in ALLOWED_DOWNSTREAM_VERIFICATIONS:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported downstream_verification {downstream_verification}."
            )
        else:
            expected_downstream_verification = "required" if status == "DOC_ONLY" else "none"
            if downstream_verification != expected_downstream_verification:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} has downstream_verification={downstream_verification} but expected {expected_downstream_verification} for status {status}."
                )

        tags = item.get("tags", None)
        if not isinstance(tags, list) or len(tags) < 2:
            errors.append(f"{path}: {item_id or f'item {index}'} must define at least two tags.")
        else:
            for tag in tags:
                tag_text = str(tag).strip()
                if not tag_text:
                    errors.append(f"{path}: {item_id or f'item {index}'} contains an empty tag value.")
                elif not TAG_PATTERN.fullmatch(tag_text):
                    errors.append(f"{path}: {item_id or f'item {index}'} has non-normalized tag {tag_text!r}.")
                elif not is_ascii_text(tag_text):
                    errors.append(f"{path}: {item_id or f'item {index}'} has non-ASCII tag {tag_text!r}.")

        for text_field in ("example_bad", "example_good", "example_lang", "detection", "detector"):
            value = item.get(text_field, None)
            if value is not None and not isinstance(value, str):
                errors.append(f"{path}: {item_id or f'item {index}'} field {text_field} must be a string.")

        evidence = item.get("evidence", None)
        if evidence is not None:
            if not isinstance(evidence, list):
                errors.append(f"{path}: {item_id or f'item {index}'} field evidence must be a list.")
            else:
                for ref in evidence:
                    if not isinstance(ref, dict) or not str(ref.get("source", "")).strip():
                        errors.append(
                            f"{path}: {item_id or f'item {index}'} evidence entries must be mappings with a non-empty 'source'."
                        )

        has_bad = bool(str(item.get("example_bad", "")).strip())
        has_good = bool(str(item.get("example_good", "")).strip())
        if has_bad != has_good:
            errors.append(
                f"{path}: {item_id or f'item {index}'} must provide both example_bad and example_good together (depth pairing)."
            )

        doctrinal = item.get("doctrinal", None)
        if doctrinal is not None and not isinstance(doctrinal, bool):
            errors.append(f"{path}: {item_id or f'item {index}'} field doctrinal must be a boolean.")
        if doctrinal and (has_bad or has_good):
            errors.append(
                f"{path}: {item_id or f'item {index}'} is flagged doctrinal but also ships examples; a vice is one or the other."
            )

        alias_of = str(item.get("alias_of", "")).strip()
        if alias_of:
            if alias_of == item_id:
                errors.append(f"{path}: {item_id or f'item {index}'} cannot be an alias of itself.")
            elif alias_of not in all_ids:
                errors.append(f"{path}: {item_id or f'item {index}'} alias_of references unknown id {alias_of}.")
            if has_bad or has_good or doctrinal:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} is an alias and must not also carry examples or the doctrinal flag."
                )

        if item_id and item_id.startswith(("VC-", "VT-")):
            wiki_path = WIKI_VICES_DIR / f"{item_id}.md"
            if check_wiki and not wiki_path.exists():
                errors.append(f"Missing wiki article for {item_id}: {wiki_path}")
        elif item_id and item_id.startswith("TK-"):
            wiki_path = WIKI_TOKENOMICS_DIR / f"{item_id}.md"
            if check_wiki and not wiki_path.exists():
                errors.append(f"Missing wiki article for {item_id}: {wiki_path}")


def validate_project_insights(path: Path, errors: list[str], check_wiki: bool) -> None:
    data = load_yaml(path)
    insights = data.get("project_insights", {})
    if not isinstance(insights, dict):
        errors.append(f"{path}: 'project_insights' must be a mapping.")
        return

    for key, value in insights.items():
        insight_id = str(key).strip()
        if not insight_id.startswith("PI-"):
            errors.append(f"{path}: invalid insight id {insight_id!r}.")
        if insight_id and not is_ascii_text(insight_id):
            errors.append(f"{path}: invalid insight id {insight_id!r}; technical identifiers must be ASCII-only.")
        if not str(value).strip():
            errors.append(f"{path}: {insight_id or 'unknown insight'} has empty text.")
        if check_wiki:
            wiki_path = WIKI_INSIGHTS_DIR / f"{insight_id}.md"
            if not wiki_path.exists():
                errors.append(f"Missing wiki article for {insight_id}: {wiki_path}")


def resolve_wiki_link_target(source_path: Path, raw_target: str) -> Path | None:
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if not target:
        return None

    cleaned = target.removesuffix(".md")
    candidates = [
        source_path.parent / target,
        ROOT / target,
        ROOT / f"{cleaned}.md",
        ROOT / "Wiki" / f"{cleaned}.md",
        ROOT / "Wiki" / cleaned,
    ]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.exists():
            return resolved

    basename_matches = sorted({path.resolve() for path in ROOT.rglob(f"{Path(cleaned).name}.md")})
    if len(basename_matches) == 1:
        return basename_matches[0]
    return None


def validate_link_targets(errors: list[str], sources: list[Path]) -> None:
    for path in sources:
        content = path.read_text(encoding="utf-8")

        for raw_target in WIKILINK_PATTERN.findall(content):
            resolved = resolve_wiki_link_target(path, raw_target)
            if resolved is None:
                errors.append(f"{path}: unresolved wikilink target [[{raw_target}]].")

        for raw_target in MARKDOWN_LINK_PATTERN.findall(content):
            target = raw_target.split("#", 1)[0].split("?", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            if "xxx" in target.lower() or "{" in target or "}" in target:
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                resolved = (ROOT / target).resolve()
            if not resolved.exists() and target.endswith("/"):
                resolved = (ROOT / target.rstrip("/")).resolve()
            if not resolved.exists():
                errors.append(f"{path}: unresolved markdown link target ({raw_target}).")


def validate_wiki_file_sets(errors: list[str]) -> None:
    """Ensure generated wiki folders do not accumulate orphan markdown files."""
    expected_vices = {item.stem for item in WIKI_VICES_DIR.glob("*.md")} if WIKI_VICES_DIR.exists() else set()
    expected_tokenomics = {item.stem for item in WIKI_TOKENOMICS_DIR.glob("*.md")} if WIKI_TOKENOMICS_DIR.exists() else set()

    catalog_data = load_yaml(MANIFEST)
    catalogs = catalog_data.get("catalogs", {})
    vices_path = ROOT / str(catalogs.get("coding_vices", ""))
    testing_path = ROOT / str(catalogs.get("testing_vices", ""))
    tokenomics_path = ROOT / str(catalogs.get("tokenomics", ""))

    allowed_vices: set[str] = set()
    for catalog_path in [vices_path, testing_path]:
        if catalog_path.exists():
            data = load_yaml(catalog_path)
            for item in data.get("items", []):
                item_id = str(item.get("id", "")).strip()
                if item_id.startswith(("VC-", "VT-")):
                    allowed_vices.add(item_id)

    allowed_tokenomics: set[str] = {
        str(item.get("id", "")).strip()
        for item in (load_yaml(tokenomics_path).get("items", []) if tokenomics_path.exists() else [])
        if str(item.get("id", "")).strip().startswith("TK-")
    }

    allowed_tokenomics.update(
        {
            "Memory_Headroom_Index",
            "Input_Retrieval_Index",
            "Output_Compaction_Index",
            "Measurement_Telemetry_Index",
            "Automation_Tooling_Index",
        }
    )

    unexpected_vices = sorted(expected_vices - allowed_vices)
    unexpected_tokenomics = sorted(expected_tokenomics - allowed_tokenomics)

    if unexpected_vices:
        errors.append(
            f"{WIKI_VICES_DIR}: orphan markdown files detected: {', '.join(unexpected_vices)}."
        )
    if unexpected_tokenomics:
        errors.append(
            f"{WIKI_TOKENOMICS_DIR}: orphan markdown files detected: {', '.join(unexpected_tokenomics)}."
        )


def parse_home_count(path: Path, label: str) -> int | None:
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.startswith(f"| {label} |"):
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 3 and parts[1].isdigit():
                return int(parts[1])
    return None


def validate_home_counts(errors: list[str]) -> None:
    home_path = ROOT / "Wiki" / "Home.md"
    if not home_path.exists():
        errors.append(f"Missing wiki home: {home_path}")
        return

    data = load_yaml(ROOT / "golden_standard_coding_vices.yaml")
    vices = data.get("items", [])
    data = load_yaml(ROOT / "golden_standard_testing_vices.yaml")
    tests = data.get("items", [])
    data = load_yaml(ROOT / "golden_standard_tokenomics.yaml")
    tokenomics = data.get("items", [])
    data = load_yaml(ROOT / "golden_standard_project_insights.yaml")
    insights = data.get("project_insights", {})

    expected_counts = {
        "Vibe Coding": len([item for item in vices if str(item.get("id", "")).startswith("VC-")]),
        "Testing & Evaluation": len([item for item in tests if str(item.get("id", "")).startswith("VT-")]),
        "Tokenomics": len([item for item in tokenomics if str(item.get("id", "")).startswith("TK-")]),
        "Project Insights": len([key for key in insights if str(key).startswith("PI-")]),
    }

    for label, expected in expected_counts.items():
        expected_row = f"| {label} | `{'VC-xxx' if label == 'Vibe Coding' else 'VT-xxx' if label == 'Testing & Evaluation' else 'TK-xxx' if label == 'Tokenomics' else 'PI-xxx'}` | {expected} |"
        if expected_row not in home_path.read_text(encoding="utf-8"):
            errors.append(f"{home_path}: missing or stale count row for {label}.")

    status_text = home_path.read_text(encoding="utf-8")
    total_expected = len(vices) + len(tests) + len(tokenomics)
    status_expected = Counter(
        str(item.get("status", "")).strip()
        for item in vices + tests + tokenomics
        if str(item.get("status", "")).strip()
    )
    prevented_remediated = status_expected.get("PREVENTED", 0) + status_expected.get("REMEDIATED", 0)
    audited_doc_only = status_expected.get("AUDITED", 0) + status_expected.get("DOC_ONLY", 0)
    total_row = f"| `Total` | {total_expected} |"
    if total_row not in status_text:
        errors.append(f"{home_path}: total count row does not match expected total {total_expected}.")
    if f"| `PREVENTED` + `REMEDIATED` | {prevented_remediated} |" not in status_text:
        errors.append(f"{home_path}: prevented/remediated count row mismatch.")
    if f"| `AUDITED` + `DOC_ONLY` | {audited_doc_only} |" not in status_text:
        errors.append(f"{home_path}: audited/doc_only count row mismatch.")


def validate_readme_counts(errors: list[str]) -> None:
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        errors.append(f"Missing README: {readme_path}")
        return

    data = load_yaml(ROOT / "golden_standard_coding_vices.yaml")
    vc_count = len([item for item in data.get("items", []) if str(item.get("id", "")).startswith("VC-")])
    data = load_yaml(ROOT / "golden_standard_testing_vices.yaml")
    tv_count = len([item for item in data.get("items", []) if str(item.get("id", "")).startswith("VT-")])
    data = load_yaml(ROOT / "golden_standard_tokenomics.yaml")
    tk_count = len([item for item in data.get("items", []) if str(item.get("id", "")).startswith("TK-")])
    data = load_yaml(ROOT / "golden_standard_project_insights.yaml")
    pi_count = len([key for key in data.get("project_insights", {}) if str(key).startswith("PI-")])

    readme_text = readme_path.read_text(encoding="utf-8")

    # Check paragraphs counts
    expected_vc_str = f"**{vc_count} entries** cataloged with severity"
    expected_tv_str = f"**{tv_count} entries** with examples"
    
    if expected_vc_str not in readme_text:
        errors.append(f"{readme_path}: missing or stale VC count ({expected_vc_str!r}).")
    if expected_tv_str not in readme_text:
        errors.append(f"{readme_path}: missing or stale VT count ({expected_tv_str!r}).")

    # Check catalog table rows
    expected_rows = [
        f"| `golden_standard_coding_vices.yaml` | Vibe coding antipatterns | {vc_count} |",
        f"| `golden_standard_testing_vices.yaml` | Testing failures | {tv_count} |",
        f"| `golden_standard_tokenomics.yaml` | Token efficiency | {tk_count} |",
        f"| `golden_standard_project_insights.yaml` | Cross-cutting insights | {pi_count} |",
    ]
    for row in expected_rows:
        if row not in readme_text:
            errors.append(f"{readme_path}: missing or stale table row ({row!r}).")

    # Check total line
    expected_total = f"**Total: {vc_count + tv_count + tk_count} vices + {pi_count} insights ({vc_count + tv_count + tk_count + pi_count} entries).**"
    if expected_total not in readme_text:
        errors.append(f"{readme_path}: missing or stale total line ({expected_total!r}).")


def validate_wiki_topology(errors: list[str]) -> None:
    """Check that the wiki exposes the canonical navigation and memory surfaces."""
    required_snippets: dict[Path, list[str]] = {
        ROOT / "Wiki" / "Home.md": [
            "[[Vices_Index|Índice de Vicios de Ingeniería]]",
            "[[Project_Insights/PI-025|Retrospectiva exportable]]",
            "[[Tokenomics_Index|Índice de Tokenomics]]",
            "[[Tokenomics_Map|Mapa de Tokenomics]]",
            "[Inbox](../Inbox/README.md)",
            "[[Graph|Mapa de Grafo GS]]",
            "[[Project_Insights/PI-019|Higiene de ejecución y tooling]]",
        ],
        ROOT / "Inbox" / "README.md": [
            "Inbox/templates/",
            "INGESTION_PROTOCOL.md",
            "KNOWLEDGE_SOURCES.md",
        ],
        ROOT / ".github" / "workflows" / "audit.yml": [
            "generate_golden_audit.py",
            "validate_golden_standard_catalogs.py",
        ],
        ROOT / "Wiki" / "Tokenomics_Index.md": [
            "[[Memory_Headroom_Index|Memoria y Headroom]]",
            "[[Input_Retrieval_Index|Entrada y Recuperación]]",
            "[[Output_Compaction_Index|Salida y Compresión]]",
            "[[Measurement_Telemetry_Index|Medición y Telemetría]]",
            "[[Automation_Tooling_Index|Automatización y Herramientas]]",
            "[[Tokenomics_Map|Mapa de Tokenomics]]",
            "RTK",
            "ICM",
        ],
        ROOT / "Wiki" / "Tokenomics_Map.md": [
            "Memoria y Headroom",
            "Entrada y Recuperación",
            "Salida y Compresión",
            "Medición y Telemetría",
            "Automatización y Herramientas",
            "PI-006",
            "PI-010",
            "PI-014",
            "PI-018",
        ],
        ROOT / "Wiki" / "Tokenomics" / "Memory_Headroom_Index.md": [
            "checkpoint",
            "handoff",
            "cache",
            "headroom",
            "TK-001",
            "TK-002",
            "TK-003",
            "TK-004",
            "TK-007",
            "TK-008",
            "TK-028",
            "TK-031",
            "TK-032",
            "TK-033",
            "TK-F01",
        ],
        ROOT / "Wiki" / "Tokenomics" / "Input_Retrieval_Index.md": [
            "TK-009",
            "TK-010",
            "TK-011",
            "TK-012",
            "TK-014",
            "TK-015",
            "TK-019",
            "TK-F02",
        ],
        ROOT / "Wiki" / "Tokenomics" / "Output_Compaction_Index.md": [
            "TK-020",
            "TK-021",
            "TK-022",
            "TK-024",
            "TK-025",
            "TK-027",
            "TK-029",
            "TK-030",
            "TK-035",
            "TK-036",
            "TK-043",
            "TK-F03",
        ],
        ROOT / "Wiki" / "Tokenomics" / "Measurement_Telemetry_Index.md": [
            "TK-023",
            "TK-026",
            "TK-037",
            "TK-040",
            "TK-041",
            "TK-042",
        ],
        ROOT / "Wiki" / "Tokenomics" / "Automation_Tooling_Index.md": [
            "TK-013",
            "TK-017",
            "TK-039",
        ],
        ROOT / "Wiki" / "Vices_Index.md": [
            "[[Vices/VC-125|VC-125]]",
            "[[Vices/VT-115|VT-115]]",
            "[[Vices/VC-104|VC-104]]",
            "[[Vices/VC-105|VC-105]]",
            "[[Vices/VC-106|VC-106]]",
        ],
        ROOT / "Wiki" / "Project_Insights_Index.md": [
            "[[Project_Insights/PI-025|PI-025]]",
        ],
        ROOT / "Wiki" / "Graph.md": [
            "## Deuda de Validación",
            "| Huérfanos candidatos | 0 |",
            "| `DOC_ONLY` |",
            "## Verificación Downstream",
            "| Estado | VC | VT | TK |",
        ],
    }

    for path, snippets in required_snippets.items():
        if not path.exists():
            errors.append(f"Missing wiki topology file: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in text:
                errors.append(f"{path}: missing required topology marker {snippet!r}.")

    link_sources = [
        ROOT / "README.md",
        ROOT / "CONTRIBUTING.md",
        ROOT / "CONCEPTUAL_FRAMEWORK.md",
        ROOT / "CODE_OF_CONDUCT.md",
    ]
    for relative_dir in ["Wiki", "Inbox"]:
        base_dir = ROOT / relative_dir
        if base_dir.exists():
            link_sources.extend(sorted(base_dir.rglob("*.md")))

    validate_link_targets(errors, link_sources)
    validate_wiki_file_sets(errors)
    validate_home_counts(errors)
    validate_readme_counts(errors)


def validate_manifest(path: Path, errors: list[str], check_wiki: bool) -> None:
    data = load_yaml(path)
    catalogs = data.get("catalogs", {})
    if not isinstance(catalogs, dict):
        errors.append(f"{path}: 'catalogs' must be a mapping.")
        return

    for catalog_name, relative_path in catalogs.items():
        catalog_path = ROOT / str(relative_path)
        if not catalog_path.exists():
            errors.append(f"{path}: catalog {catalog_name!r} points to missing file {catalog_path}.")
            continue

        if catalog_name == "project_insights":
            validate_project_insights(catalog_path, errors, check_wiki)
        else:
            validate_vices_catalog(catalog_path, errors, check_wiki)

    validate_wiki_topology(errors)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-wiki",
        action="store_true",
        help="Also verify that each catalog item has a corresponding wiki article.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    errors: list[str] = []
    if not MANIFEST.exists():
        errors.append(f"Missing manifest: {MANIFEST}")
    else:
        validate_manifest(MANIFEST, errors, args.check_wiki)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print("Golden Standard catalogs validated successfully.")
    if args.check_wiki:
        print("Wiki coverage verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
