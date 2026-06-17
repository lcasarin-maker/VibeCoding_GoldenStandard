#!/usr/bin/env python3
"""Compute honest, dynamic quality metrics from the catalogs and emit shields.io badges.

Everything here is derived from the YAML at build time, so a badge can never drift from
reality: CI regenerates these files and fails if the committed copies are stale (the same
'artifacts up to date' gate used for the wiki). No hardcoded or inflated numbers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detectors import DETECTORS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BADGES = ROOT / "badges"
CATALOGS = (
    "golden_standard_coding_vices.yaml",
    "golden_standard_testing_vices.yaml",
    "golden_standard_tokenomics.yaml",
)


def _depth(item: dict) -> str:
    if str(item.get("alias_of", "")).strip():
        return "alias"
    if str(item.get("example_bad", "")).strip() and str(item.get("example_good", "")).strip():
        return "deep"
    if item.get("doctrinal"):
        return "doctrinal"
    return "stub"


def compute_metrics() -> dict:
    items = []
    for catalog in CATALOGS:
        data = yaml.safe_load((ROOT / catalog).read_text(encoding="utf-8"))
        items.extend(data.get("items", []))

    total = len(items)
    depth = {"deep": 0, "doctrinal": 0, "alias": 0, "stub": 0}
    ai_native = with_evidence = with_detector = 0
    for it in items:
        depth[_depth(it)] += 1
        if "ai-native" in it.get("tags", []):
            ai_native += 1
        if it.get("evidence"):
            with_evidence += 1
        if str(it.get("detector", "")).strip():
            with_detector += 1

    pi = yaml.safe_load((ROOT / "golden_standard_principles.yaml").read_text(encoding="utf-8"))
    pi_count = len([i for i in pi.get("items", []) if str(i.get("id", "")).startswith("PI-")])

    pct = lambda n: round(100 * n / total) if total else 0
    return {
        "total_entries": total,
        "project_insights": pi_count,
        "depth": depth,
        "deep_pct": pct(depth["deep"]),
        "ai_native": ai_native,
        "ai_native_pct": pct(ai_native),
        "with_evidence": with_evidence,
        "with_evidence_pct": pct(with_evidence),
        "local_detectors": with_detector,
        "registered_detectors": len(DETECTORS),
        "stub": depth["stub"],
    }


def _color(pct_value: int) -> str:
    return "brightgreen" if pct_value >= 70 else "yellow" if pct_value >= 40 else "red"


def _badge(label: str, message: str, color: str) -> dict:
    return {"schemaVersion": 1, "label": label, "message": message, "color": color}


def write_all() -> dict:
    m = compute_metrics()
    (ROOT / "golden_standard_metrics.json").write_text(
        json.dumps(m, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    BADGES.mkdir(exist_ok=True)
    badges = {
        "entries": _badge("entries", str(m["total_entries"]), "blue"),
        "deep": _badge("deep (falsable)", f"{m['deep_pct']}%", _color(m['deep_pct'])),
        "ai-native": _badge("AI-native", str(m["ai_native"]), "blue"),
        "evidence": _badge("with evidence", f"{m['with_evidence_pct']}%", _color(m['with_evidence_pct'])),
        "detectors": _badge("local detectors", str(m["local_detectors"]), "brightgreen"),
        "stubs": _badge("stubs", str(m["stub"]), "brightgreen" if m["stub"] == 0 else "yellow"),
    }
    for name, payload in badges.items():
        (BADGES / f"{name}.json").write_text(
            json.dumps(payload, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return m


def main() -> int:
    m = write_all()
    print("Metrics:", json.dumps(m, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
