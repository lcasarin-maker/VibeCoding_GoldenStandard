#!/usr/bin/env python3
"""Validate Golden Standard catalogs and their generated wiki coverage."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "golden_standard.yaml"
WIKI_VICES_DIR = ROOT / "Wiki" / "Vices"
WIKI_INSIGHTS_DIR = ROOT / "Wiki" / "Project_Insights"
ALLOWED_STATUSES = {"DOC_ONLY", "AUDITED", "PREVENTED", "REMEDIATED"}
ALLOWED_SEVERITIES = {"critical", "high", "medium", "low"}
TAG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
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
)


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

    seen_ids: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            errors.append(f"{path}: item {index} is not a mapping.")
            continue

        item_id = str(item.get("id", "")).strip()
        missing = [field for field in CATALOG_REQUIRED_FIELDS if not str(item.get(field, "")).strip()]
        if missing:
            errors.append(f"{path}: {item_id or f'item {index}'} missing required fields: {', '.join(missing)}")

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

        if item_id and item_id.startswith(("VC-", "VT-", "TK-")):
            wiki_path = WIKI_VICES_DIR / f"{item_id}.md"
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
        if not str(value).strip():
            errors.append(f"{path}: {insight_id or 'unknown insight'} has empty text.")
        if check_wiki:
            wiki_path = WIKI_INSIGHTS_DIR / f"{insight_id}.md"
            if not wiki_path.exists():
                errors.append(f"Missing wiki article for {insight_id}: {wiki_path}")


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
