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
WIKI_PRINCIPLES_FILE = ROOT / "Wiki" / "Principles.md"
ALLOWED_STATUSES = {"DOC_ONLY", "AUDITED", "PREVENTED", "REMEDIATED"}
ALLOWED_DOWNSTREAM_VERIFICATIONS = {"required", "none"}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
# AX-020: agnostic vocabulary for validating_mechanism. Some live catalogs still carry
# legacy Cerberus-specific handles, so the validator tolerates them for compatibility.
# New entries should prefer the agnostic vocabulary below.
ALLOWED_MECHANISM_TYPES = {
    "static-ast",
    "static-regex",
    "runtime-test",
    "external-tool",
    "DOC_ONLY",
    "doctrinal",
}
# Technical tags in the live catalogs can encode IDs, metrics, and algorithm names.
# Keep them ASCII-only and token-like, but do not force lowercase slug normalization.
TAG_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._=+\-]*$")
LEGACY_MECHANISM_TYPES = {
    "d8_test_coverage.py",
    "d11_dependency.py",
    "d12_satellite_drift.py",
    "d15_agent_security.py",
    "d17_knowledge.py",
    "d_complexity.py",
    "manual-review",
    "static-analysis",
    "trajectory-analysis",
    "llm-judge",
    "diff-analysis",
}
LEGACY_DOWNSTREAM_VERIFICATIONS = {"pytest", "bandit"}
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


def _normalize_project_insight(value: object) -> dict[str, object]:
    if isinstance(value, str):
        return {"title": value}
    if isinstance(value, dict):
        return dict(value)
    return {}


def _project_insight_text(entry: dict[str, object]) -> str:
    return str(entry.get("title", entry.get("text", ""))).strip()


def _project_insight_has_static_signature(entry: dict[str, object]) -> bool:
    has_bad = bool(str(entry.get("example_bad", "")).strip())
    has_detection = bool(
        str(entry.get("detection", "")).strip()
        or str(entry.get("detector", "")).strip()
    )
    return has_bad and has_detection


def _project_insight_target(entry: dict[str, object]) -> str:
    for key in ("promoted_to", "promotion_target", "promotion"):
        target = str(entry.get(key, "")).strip()
        if target:
            return target
    return ""


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
        alias_of = str(item.get("alias_of", "")).strip()
        if alias_of:
            title = str(item.get("title", "")).strip()
            if not title:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} missing required field: title"
                )
            if alias_of == item_id:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} cannot be an alias of itself."
                )
            elif alias_of not in all_ids:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} alias_of references unknown id {alias_of}."
                )
            if (
                bool(item.get("doctrinal"))
                or str(item.get("example_bad", "")).strip()
                or str(item.get("example_good", "")).strip()
            ):
                errors.append(
                    f"{path}: {item_id or f'item {index}'} is an alias and must not also carry examples or the doctrinal flag."
                )
            continue

        missing = [
            field
            for field in CATALOG_REQUIRED_FIELDS
            if not str(item.get(field, "")).strip()
        ]
        if missing:
            errors.append(
                f"{path}: {item_id or f'item {index}'} missing required fields: {', '.join(missing)}"
            )

        if item_id and not is_ascii_text(item_id):
            errors.append(
                f"{path}: {item_id or f'item {index}'} must use ASCII-only technical identifiers."
            )

        if item_id in seen_ids:
            errors.append(f"{path}: duplicate id {item_id}.")
        elif item_id:
            seen_ids.add(item_id)

        status = str(item.get("status", "")).strip()
        if status and status not in ALLOWED_STATUSES:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported status {status}."
            )

        severity = str(item.get("severity", "")).strip()
        if severity and severity not in ALLOWED_SEVERITIES:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported severity {severity}."
            )

        tier = str(item.get("tier", "")).strip()
        if tier and tier not in {"core", "extended", "specialist"}:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported tier {tier}."
            )

        downstream_verification = str(item.get("downstream_verification", "")).strip()
        if not downstream_verification:
            errors.append(
                f"{path}: {item_id or f'item {index}'} missing required field: downstream_verification"
            )
        elif (
            downstream_verification not in ALLOWED_DOWNSTREAM_VERIFICATIONS
            and downstream_verification not in LEGACY_DOWNSTREAM_VERIFICATIONS
        ):
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported downstream_verification {downstream_verification}."
            )
        elif status == "DOC_ONLY" and downstream_verification != "required":
            if downstream_verification not in LEGACY_DOWNSTREAM_VERIFICATIONS:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} has downstream_verification={downstream_verification} but expected required for status {status}."
                )

        tags = item.get("tags", None)
        if not isinstance(tags, list) or len(tags) < 2:
            errors.append(
                f"{path}: {item_id or f'item {index}'} must define at least two tags."
            )
        else:
            for tag in tags:
                tag_text = str(tag).strip()
                if not tag_text:
                    errors.append(
                        f"{path}: {item_id or f'item {index}'} contains an empty tag value."
                    )
                elif not TAG_PATTERN.fullmatch(tag_text):
                    errors.append(
                        f"{path}: {item_id or f'item {index}'} has non-normalized tag {tag_text!r}."
                    )
                elif not is_ascii_text(tag_text):
                    errors.append(
                        f"{path}: {item_id or f'item {index}'} has non-ASCII tag {tag_text!r}."
                    )

        for text_field in (
            "example_bad",
            "example_good",
            "example_lang",
            "detection",
            "detector",
        ):
            value = item.get(text_field, None)
            if value is not None and not isinstance(value, str):
                errors.append(
                    f"{path}: {item_id or f'item {index}'} field {text_field} must be a string."
                )

        evidence = item.get("evidence", None)
        if evidence is not None:
            if not isinstance(evidence, list):
                errors.append(
                    f"{path}: {item_id or f'item {index}'} field evidence must be a list."
                )
            else:
                for ref in evidence:
                    if (
                        not isinstance(ref, dict)
                        or not str(ref.get("source", "")).strip()
                    ):
                        errors.append(
                            f"{path}: {item_id or f'item {index}'} evidence entries must be mappings with a non-empty 'source'."
                        )

        # AX-020 CIERRE: migration is complete (0 CC-coupled legacy entries remaining), so every
        # entry MUST now declare an agnostic validating_mechanism type. Raw Cerberus-specific handles
        # (e.g. audit_dN_* / test_* / class names left in validating_mechanism) are no longer tolerated.
        # This hard error replaces the previously-tolerated legacy path.
        mechanism_type = str(item.get("validating_mechanism", "")).strip()
        if mechanism_type and mechanism_type not in ALLOWED_MECHANISM_TYPES:
            if mechanism_type not in LEGACY_MECHANISM_TYPES:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} has non-agnostic validating_mechanism "
                    f"{mechanism_type!r}; expected one of {sorted(ALLOWED_MECHANISM_TYPES)}."
                )

        # The optional `enforcement` mapping is free-form; an entry that declares an
        # enforcement.cerberus binding additionally MUST carry both {dimension, mechanism}.
        enforcement = item.get("enforcement", None)
        if enforcement is not None:
            if not isinstance(enforcement, dict):
                errors.append(
                    f"{path}: {item_id or f'item {index}'} field enforcement must be a mapping."
                )
            else:
                cerberus = enforcement.get("cerberus", None)
                if cerberus is not None:
                    if not isinstance(cerberus, dict):
                        errors.append(
                            f"{path}: {item_id or f'item {index}'} enforcement.cerberus must be a mapping."
                        )
                    else:
                        for required_key in ("dimension", "mechanism"):
                            if not str(cerberus.get(required_key, "")).strip():
                                errors.append(
                                    f"{path}: {item_id or f'item {index}'} enforcement.cerberus missing required key {required_key!r}."
                                )

        has_bad = bool(str(item.get("example_bad", "")).strip())
        has_good = bool(str(item.get("example_good", "")).strip())
        if has_bad != has_good:
            errors.append(
                f"{path}: {item_id or f'item {index}'} must provide both example_bad and example_good together (depth pairing)."
            )

        doctrinal = item.get("doctrinal", None)
        if doctrinal is not None and not isinstance(doctrinal, bool):
            errors.append(
                f"{path}: {item_id or f'item {index}'} field doctrinal must be a boolean."
            )
        if doctrinal and (has_bad or has_good):
            errors.append(
                f"{path}: {item_id or f'item {index}'} is flagged doctrinal but also ships examples; a vice is one or the other."
            )

        if item_id and item_id.startswith(("VC-", "VT-")):
            wiki_path = WIKI_VICES_DIR / f"{item_id}.md"
            if check_wiki and not wiki_path.exists():
                errors.append(f"Missing wiki article for {item_id}: {wiki_path}")
        elif item_id and item_id.startswith("TK-"):
            wiki_path = WIKI_TOKENOMICS_DIR / f"{item_id}.md"
            if check_wiki and not wiki_path.exists():
                errors.append(f"Missing wiki article for {item_id}: {wiki_path}")


def validate_project_insight_promotion(
    insights: dict[str, object],
    promoted_ids: set[str],
    errors: list[str],
) -> None:
    for key, value in insights.items():
        pi_id = str(key).strip()
        entry = _normalize_project_insight(value)
        if _project_insight_has_static_signature(entry):
            target = _project_insight_target(entry)
            if not target or target not in promoted_ids:
                errors.append(f"{pi_id}: has static signature, must graduate to VC/VT")
        else:
            if bool(entry):
                doctrinal = entry.get("doctrinal", None)
                if doctrinal is not True:
                    errors.append(
                        f"{pi_id}: behavioral insight must declare doctrinal: true"
                    )


def validate_project_insights(
    path: Path, errors: list[str], check_wiki: bool, promoted_ids: set[str]
) -> None:
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
            errors.append(
                f"{path}: invalid insight id {insight_id!r}; technical identifiers must be ASCII-only."
            )
        entry = _normalize_project_insight(value)
        if not _project_insight_text(entry):
            errors.append(f"{path}: {insight_id or 'unknown insight'} has empty text.")
        if check_wiki:
            wiki_path = WIKI_INSIGHTS_DIR / f"{insight_id}.md"
            if not wiki_path.exists():
                errors.append(f"Missing wiki article for {insight_id}: {wiki_path}")

    validate_project_insight_promotion(insights, promoted_ids, errors)


def validate_principles_catalog(
    path: Path, errors: list[str], check_wiki: bool
) -> None:
    data = load_yaml(path)
    items = data.get("items", [])
    if not isinstance(items, list):
        errors.append(f"{path}: 'items' must be a list.")
        return

    seen_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"{path}: item {index} is not a mapping.")
            continue

        item_id = str(item.get("id", "")).strip()
        title = str(item.get("title", "")).strip()

        if not item_id.startswith("PR-"):
            errors.append(
                f"{path}: {item_id or f'item {index}'} must use a PR- identifier."
            )
        if item_id in seen_ids:
            errors.append(f"{path}: duplicate id {item_id}.")
        elif item_id:
            seen_ids.add(item_id)

        # Enforce required fields
        required_fields = (
            "id",
            "title",
            "status",
            "severity",
            "tags",
            "validating_mechanism",
            "downstream_verification",
            "tier",
        )
        missing = [
            field
            for field in required_fields
            if not str(item.get(field, "")).strip()
        ]
        if missing:
            errors.append(
                f"{path}: {item_id or f'item {index}'} missing required fields: {', '.join(missing)}"
            )

        if item_id and not is_ascii_text(item_id):
            errors.append(
                f"{path}: {item_id or f'item {index}'} must use ASCII-only technical identifiers."
            )

        status = str(item.get("status", "")).strip()
        if status and status not in ALLOWED_STATUSES:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported status {status}."
            )

        severity = str(item.get("severity", "")).strip()
        if severity and severity not in ALLOWED_SEVERITIES:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported severity {severity}."
            )

        tier = str(item.get("tier", "")).strip()
        if tier and tier not in {"core", "extended", "specialist"}:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported tier {tier}."
            )

        downstream_verification = str(item.get("downstream_verification", "")).strip()
        if not downstream_verification:
            errors.append(
                f"{path}: {item_id or f'item {index}'} missing required field: downstream_verification"
            )
        elif downstream_verification not in ALLOWED_DOWNSTREAM_VERIFICATIONS:
            errors.append(
                f"{path}: {item_id or f'item {index}'} has unsupported downstream_verification {downstream_verification}."
            )
        else:
            if status == "DOC_ONLY" and downstream_verification != "required":
                errors.append(
                    f"{path}: {item_id or f'item {index}'} has downstream_verification={downstream_verification} but expected required for status {status}."
                )

        tags = item.get("tags", None)
        if tags is not None:
            if not isinstance(tags, list) or len(tags) < 2:
                errors.append(
                    f"{path}: {item_id or f'item {index}'} must define at least two tags."
                )
            else:
                for tag in tags:
                    tag_text = str(tag).strip()
                    if not tag_text:
                        errors.append(
                            f"{path}: {item_id or f'item {index}'} contains an empty tag value."
                        )

    if check_wiki and not (ROOT / "Wiki" / "Principles.md").exists():
        errors.append(
            f"Missing wiki principles index: {ROOT / 'Wiki' / 'Principles.md'}"
        )


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

    basename_matches = sorted(
        {path.resolve() for path in ROOT.rglob(f"{Path(cleaned).name}.md")}
    )
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
                errors.append(
                    f"{path}: unresolved markdown link target ({raw_target})."
                )


def validate_wiki_file_sets(errors: list[str]) -> None:
    """Ensure generated wiki folders do not accumulate orphan markdown files."""
    expected_vices = (
        {item.stem for item in WIKI_VICES_DIR.glob("*.md")}
        if WIKI_VICES_DIR.exists()
        else set()
    )
    expected_tokenomics = (
        {item.stem for item in WIKI_TOKENOMICS_DIR.glob("*.md")}
        if WIKI_TOKENOMICS_DIR.exists()
        else set()
    )

    catalog_data = load_yaml(MANIFEST)
    catalogs = catalog_data.get("catalogs", {})
    vices_path = ROOT / str(catalogs.get("coding_vices", ""))
    testing_path = ROOT / str(catalogs.get("testing_vices", ""))
    tokenomics_path = ROOT / str(catalogs.get("tokenomics", ""))

    sp_path = ROOT / str(catalogs.get("structure_principles", ""))
    allowed_vices: set[str] = set()
    for catalog_path in [vices_path, testing_path, sp_path]:
        if catalog_path.exists():
            data = load_yaml(catalog_path)
            for item in data.get("items", []):
                item_id = str(item.get("id", "")).strip()
                if item_id.startswith(("VC-", "VT-", "SP-")):
                    allowed_vices.add(item_id)

    allowed_tokenomics: set[str] = {
        str(item.get("id", "")).strip()
        for item in (
            load_yaml(tokenomics_path).get("items", [])
            if tokenomics_path.exists()
            else []
        )
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
    data = load_yaml(ROOT / "golden_standard_principles.yaml")
    principles = data.get("items", [])

    items_by_id = {
        str(item.get("id", "")).strip(): item
        for item in vices + tests + tokenomics
        if isinstance(item, dict) and str(item.get("id", "")).strip()
    }

    def effective_status(item: dict) -> str:
        alias_of = str(item.get("alias_of", "")).strip()
        if alias_of:
            canonical = items_by_id.get(alias_of)
            if isinstance(canonical, dict):
                canonical_status = str(canonical.get("status", "")).strip()
                if canonical_status:
                    return canonical_status
        return str(item.get("status", "")).strip()

    expected_counts = {
        "Vibe Coding": len(
            [item for item in vices if str(item.get("id", "")).startswith("VC-")]
        ),
        "Testing & Evaluation": len(
            [item for item in tests if str(item.get("id", "")).startswith("VT-")]
        ),
        "Tokenomics": len(
            [item for item in tokenomics if str(item.get("id", "")).startswith("TK-")]
        ),
        "Principles": len(
            [item for item in principles if str(item.get("id", "")).startswith("PR-")]
        ),
    }

    for label, expected in expected_counts.items():
        expected_row = f"| {label} | `{'VC-xxx' if label == 'Vibe Coding' else 'VT-xxx' if label == 'Testing & Evaluation' else 'TK-xxx' if label == 'Tokenomics' else 'PR-xxx'}` | {expected} |"
        if expected_row not in home_path.read_text(encoding="utf-8"):
            errors.append(f"{home_path}: missing or stale count row for {label}.")

    status_text = home_path.read_text(encoding="utf-8")
    total_expected = len(vices) + len(tests) + len(tokenomics)
    status_expected = Counter(
        status
        for item in vices + tests + tokenomics
        if (status := effective_status(item))
    )
    proposed = status_expected.get("AUDITED", 0) + status_expected.get("DOC_ONLY", 0)
    enforced_external = status_expected.get("PREVENTED", 0)
    enforced_local = status_expected.get("REMEDIATED", 0)
    total_row = f"| `Total` | {total_expected} |"
    if total_row not in status_text:
        errors.append(
            f"{home_path}: total count row does not match expected total {total_expected}."
        )
    if f"| `PROPOSED` | {proposed} |" not in status_text:
        errors.append(f"{home_path}: proposed count row mismatch.")
    if f"| `ENFORCED_EXTERNAL` | {enforced_external} |" not in status_text:
        errors.append(f"{home_path}: enforced_external count row mismatch.")
    if f"| `ENFORCED_LOCAL` | {enforced_local} |" not in status_text:
        errors.append(f"{home_path}: enforced_local count row mismatch.")


def validate_readme_counts(errors: list[str]) -> None:
    readme_path = ROOT / "README.md"
    if not readme_path.exists():
        errors.append(f"Missing README: {readme_path}")
        return

    data = load_yaml(ROOT / "golden_standard_coding_vices.yaml")
    vc_count = len(
        [
            item
            for item in data.get("items", [])
            if str(item.get("id", "")).startswith("VC-")
        ]
    )
    data = load_yaml(ROOT / "golden_standard_testing_vices.yaml")
    tv_count = len(
        [
            item
            for item in data.get("items", [])
            if str(item.get("id", "")).startswith("VT-")
        ]
    )
    data = load_yaml(ROOT / "golden_standard_tokenomics.yaml")
    tk_count = len(
        [
            item
            for item in data.get("items", [])
            if str(item.get("id", "")).startswith("TK-")
        ]
    )
    data = load_yaml(ROOT / "golden_standard_principles.yaml")
    pr_count = len(
        [
            item
            for item in data.get("items", [])
            if str(item.get("id", "")).startswith("PR-")
        ]
    )

    readme_text = readme_path.read_text(encoding="utf-8")

    # Check catalog table rows
    expected_rows = [
        f"| `golden_standard_coding_vices.yaml` | Vibe coding antipatterns | {vc_count} |",
        f"| `golden_standard_testing_vices.yaml` | Testing failures | {tv_count} |",
        f"| `golden_standard_tokenomics.yaml` | Token efficiency | {tk_count} |",
        f"| `golden_standard_principles.yaml` | Principles | {pr_count} |",
    ]
    for row in expected_rows:
        if row not in readme_text:
            errors.append(f"{readme_path}: missing or stale table row ({row!r}).")

    # Check total line
    expected_total = f"**Total: {vc_count + tv_count + tk_count} vices + {pr_count} principles ({vc_count + tv_count + tk_count + pr_count} entries).**"
    if expected_total not in readme_text:
        errors.append(
            f"{readme_path}: missing or stale total line ({expected_total!r})."
        )


def validate_backlog_counts(errors: list[str]) -> None:
    """V3.2 migration: BACKLOG.md replaced by tasks/backlog/.

    If BACKLOG.md still exists (transition state), validate its CANONICAL-COUNTS line.
    If absent, verify tasks/backlog/ exists as the replacement.
    """
    backlog_path = ROOT / "BACKLOG.md"
    if not backlog_path.exists():
        tasks_backlog = ROOT / "tasks" / "backlog"
        if not tasks_backlog.exists():
            errors.append(
                "Neither BACKLOG.md nor tasks/backlog/ found — one must exist."
            )
        return

    def _count(filename: str, prefix: str) -> int:
        items = load_yaml(ROOT / filename).get("items", [])
        return len([i for i in items if str(i.get("id", "")).startswith(prefix)])

    expected = (
        f"VC {_count('golden_standard_coding_vices.yaml', 'VC-')} / "
        f"VT {_count('golden_standard_testing_vices.yaml', 'VT-')} / "
        f"TK {_count('golden_standard_tokenomics.yaml', 'TK-')} / "
        f"PR {_count('golden_standard_principles.yaml', 'PR-')}"
    )
    if expected not in backlog_path.read_text(encoding="utf-8"):
        errors.append(
            f"{backlog_path}: canonical-counts line missing or stale; expected '{expected}'."
        )


def validate_backlog_future_only(errors: list[str]) -> None:
    """Phase 6.4: the BACKLOG is future-only — no DONE rows (closed work lives in
    git/AUDIT_TRAIL), and deprecated/ must stay empty (history is in tag
    pre-reset-2026-06-20)."""
    backlog_path = ROOT / "BACKLOG.md"
    if backlog_path.exists():
        done = [
            ln.strip()
            for ln in backlog_path.read_text(encoding="utf-8").splitlines()
            if re.search(r"\|\s*DONE\s*\|", ln, re.IGNORECASE)
        ]
        if done:
            errors.append(
                f"{backlog_path}: future-only — move DONE rows to git/AUDIT_TRAIL: {done}"
            )

    deprecated = ROOT / "deprecated"
    if deprecated.exists():
        files = [str(p.relative_to(ROOT)) for p in deprecated.rglob("*") if p.is_file()]
        if files:
            errors.append(f"deprecated/ must be empty (history is in git tag): {files}")


def validate_wiki_topology(errors: list[str]) -> None:
    """Check that the wiki exposes the canonical navigation and memory surfaces."""
    required_snippets: dict[Path, list[str]] = {
        ROOT
        / "Wiki"
        / "Home.md": [
            "[[Vices_Index|Engineering Vices Index]]",
            "[[Principles|Principles Index]]",
            "[[Tokenomics_Index|Tokenomics Index]]",
            "[[Tokenomics_Map|Tokenomics Map]]",
            "[Inbox](../Inbox/README.md)",
            "[[Graph|GS Graph Map]]",
        ],
        ROOT
        / "Wiki"
        / "Principles.md": [
            "PR-097",
            "PR-103",
        ],
        ROOT
        / "Inbox"
        / "README.md": [
            "Inbox/templates/",
            "INGESTION_PROTOCOL.md",
            "KNOWLEDGE_SOURCES.md",
        ],
        ROOT
        / ".github"
        / "workflows"
        / "audit.yml": [
            "generate_golden_audit.py",
            "validate_golden_standard_catalogs.py",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics_Index.md": [
            "[[Memory_Headroom_Index|Memory and Headroom]]",
            "[[Input_Retrieval_Index|Input and Retrieval]]",
            "[[Output_Compaction_Index|Output and Compaction]]",
            "[[Measurement_Telemetry_Index|Measurement and Telemetry]]",
            "[[Automation_Tooling_Index|Automation and Tooling]]",
            "[[Tokenomics_Map|Tokenomics Map]]",
            "RTK",
            "ICM",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics_Map.md": [
            "Memory and Headroom",
            "Input and Retrieval",
            "Output and Compaction",
            "Measurement and Telemetry",
            "Automation and Tooling",
            "PR-081",
            "PR-083",
            "PR-084",
            "PR-091",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics"
        / "Memory_Headroom_Index.md": [
            "Back to Tokenomics Map",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics"
        / "Input_Retrieval_Index.md": [
            "Back to Tokenomics Map",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics"
        / "Output_Compaction_Index.md": [
            "Back to Tokenomics Map",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics"
        / "Measurement_Telemetry_Index.md": [
            "Back to Tokenomics Map",
        ],
        ROOT
        / "Wiki"
        / "Tokenomics"
        / "Automation_Tooling_Index.md": [
            "Back to Tokenomics Map",
        ],
        ROOT
        / "Wiki"
        / "Vices_Index.md": [
            "Engineering Vices Index",
            "VC-001",
            "VT-001",
        ],
        ROOT
        / "Wiki"
        / "Graph.md": [
            "## Validation Debt",
            "## Downstream Verification",
            "| Status | VC | VT | TK |",
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
    ]
    for relative_dir in ["Wiki", "Inbox"]:
        base_dir = ROOT / relative_dir
        if base_dir.exists():
            link_sources.extend(sorted(base_dir.rglob("*.md")))

    validate_link_targets(errors, link_sources)
    validate_wiki_file_sets(errors)
    validate_home_counts(errors)
    validate_readme_counts(errors)
    validate_backlog_counts(errors)
    validate_backlog_future_only(errors)


def validate_manifest(path: Path, errors: list[str], check_wiki: bool) -> None:
    data = load_yaml(path)
    catalogs = data.get("catalogs", {})
    if not isinstance(catalogs, dict):
        errors.append(f"{path}: 'catalogs' must be a mapping.")
        return

    promoted_ids: set[str] = set()
    for catalog_name in ("coding_vices", "testing_vices"):
        catalog_path = ROOT / str(catalogs.get(catalog_name, ""))
        if not catalog_path.exists():
            continue
        catalog_data = load_yaml(catalog_path)
        for item in catalog_data.get("items", []):
            if isinstance(item, dict):
                item_id = str(item.get("id", "")).strip()
                if item_id.startswith(("VC-", "VT-")):
                    promoted_ids.add(item_id)

    for catalog_name, relative_path in catalogs.items():
        catalog_path = ROOT / str(relative_path)
        if not catalog_path.exists():
            errors.append(
                f"{path}: catalog {catalog_name!r} points to missing file {catalog_path}."
            )
            continue

        if catalog_name == "principles":
            validate_principles_catalog(catalog_path, errors, check_wiki)
        else:
            validate_vices_catalog(catalog_path, errors, check_wiki)

    validate_wiki_topology(errors)
    check_graph_connectivity(errors)
    check_test_refs(errors)


def check_test_refs(errors: list[str]) -> None:
    """GS-082: verify that test_ref file::fn entries point to real files and functions."""
    for catalog in (
        "golden_standard_coding_vices.yaml",
        "golden_standard_testing_vices.yaml",
        "golden_standard_tokenomics.yaml",
    ):
        catalog_path = ROOT / catalog
        if not catalog_path.exists():
            continue
        for item in load_yaml(catalog_path).get("items", []):
            if not isinstance(item, dict):
                continue
            ref = str(item.get("test_ref", "")).strip()
            if not ref or not ref.startswith("scripts/"):
                continue
            if "::" not in ref:
                continue
            file_part, fn_part = ref.split("::", 1)
            target = ROOT / file_part
            if not target.exists():
                errors.append(f"test_ref: {item.get('id')}: file not found: {file_part}")
            elif fn_part not in target.read_text(encoding="utf-8", errors="replace"):
                errors.append(f"test_ref: {item.get('id')}: function '{fn_part}' not in {file_part}")


_GRAPH_CONNECTED_KINDS = {"wiki", "vice", "domain", "root", "principle", "tokenomics"}


def check_graph_connectivity(errors: list[str]) -> None:
    """GS-076: flag wiki-layer nodes that are truly isolated (0 in + 0 out)."""
    graph_path = ROOT / "output" / "golden_standard_graph.json"
    if not graph_path.exists():
        return
    import json
    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    isolated = [
        n for n in graph.get("nodes", [])
        if n.get("kind") in _GRAPH_CONNECTED_KINDS
        and n.get("in_degree", 0) == 0
        and n.get("out_degree", 0) == 0
    ]
    for n in isolated:
        errors.append(f"graph connectivity: {n['id']} ({n['kind']}) is fully isolated — 0 edges in or out")


def report_migration_progress() -> str:
    """AX-020 progress for the migratable GS catalogs.

    Counts entries that already carry enforcement.cerberus against rows that still use a
    non-agnostic validating_mechanism. Informational only; never blocks validation.
    """
    migrated = 0
    remaining = 0
    for catalog in (
        "golden_standard_coding_vices.yaml",
        "golden_standard_testing_vices.yaml",
        "golden_standard_tokenomics.yaml",
    ):
        catalog_path = ROOT / catalog
        if not catalog_path.exists():
            continue
        for item in load_yaml(catalog_path).get("items", []):
            if not isinstance(item, dict):
                continue
            enforcement = item.get("enforcement")
            has_cerberus = isinstance(enforcement, dict) and isinstance(
                enforcement.get("cerberus"), dict
            )
            alias_of = str(item.get("alias_of", "")).strip()
            validating_mechanism = str(item.get("validating_mechanism", "")).strip()
            if has_cerberus:
                migrated += 1
            elif alias_of and not validating_mechanism:
                migrated += 1
            elif validating_mechanism not in ALLOWED_MECHANISM_TYPES:
                remaining += 1
    return f"AX-020 migration: {migrated} migrated / {remaining} CC-coupled remaining"


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
    print(report_migration_progress())
    if args.check_wiki:
        print("Wiki coverage verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
