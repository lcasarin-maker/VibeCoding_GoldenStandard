from __future__ import annotations

import json
import subprocess
from pathlib import Path

from scripts import audit as audit_script
from scripts import generate_golden_audit
from scripts.graph_artifact_policy import (
    GRAPH_RECEIPT_REL,
    audit_graph_artifact_receipts,
    has_fresh_graph_receipt,
    record_graph_regeneration,
)


def test_record_graph_regeneration_tracks_gs_graph_outputs(tmp_path: Path) -> None:
    graph_json = tmp_path / "output" / "golden_standard_graph.json"
    graph_md = tmp_path / "Wiki" / "Graph.md"
    graph_json.parent.mkdir(parents=True, exist_ok=True)
    graph_md.parent.mkdir(parents=True, exist_ok=True)
    graph_json.write_text('{"nodes":[],"edges":[]}\n', encoding="utf-8")
    graph_md.write_text("# GS Graph\n", encoding="utf-8")

    receipt = record_graph_regeneration(
        tmp_path,
        "python scripts/generate_golden_audit.py",
        [graph_json, graph_md],
    )

    assert receipt == tmp_path / GRAPH_RECEIPT_REL
    payload = json.loads(receipt.read_text(encoding="utf-8"))
    assert payload["outputs"] == [
        "Wiki/Graph.md",
        "output/golden_standard_graph.json",
    ]
    assert payload["output_hashes"]["Wiki/Graph.md"]
    assert payload["output_hashes"]["output/golden_standard_graph.json"]


def test_receipt_hash_rejects_gs_graph_tamper(tmp_path: Path) -> None:
    graph_md = tmp_path / "Wiki" / "Graph.md"
    graph_md.parent.mkdir(parents=True, exist_ok=True)
    graph_md.write_text("# generated\n", encoding="utf-8")
    record_graph_regeneration(
        tmp_path,
        "python scripts/generate_golden_audit.py",
        [graph_md],
    )
    assert has_fresh_graph_receipt(tmp_path, "Wiki/Graph.md") is True

    graph_md.write_text("# tampered\n", encoding="utf-8")

    assert has_fresh_graph_receipt(tmp_path, "Wiki/Graph.md") is False


def test_audit_graph_artifact_receipts_flags_missing_receipt(tmp_path: Path) -> None:
    graph_json = tmp_path / "output" / "golden_standard_graph.json"
    graph_json.parent.mkdir(parents=True, exist_ok=True)
    graph_json.write_text('{"patched": true}\n', encoding="utf-8")

    findings = audit_graph_artifact_receipts(
        tmp_path, ["output/golden_standard_graph.json"]
    )

    assert len(findings) == 1
    assert findings[0]["path"] == "output/golden_standard_graph.json"


def test_write_graph_artifacts_records_receipt(monkeypatch, tmp_path: Path) -> None:
    graph_json = tmp_path / "output" / "golden_standard_graph.json"
    graph_md = tmp_path / "Wiki" / "Graph.md"
    graph_md.parent.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(generate_golden_audit, "_ROOT", tmp_path)
    monkeypatch.setattr(generate_golden_audit, "GRAPH_OUTPUT", graph_json)
    monkeypatch.setattr(generate_golden_audit, "GRAPH_MARKDOWN", graph_md)
    monkeypatch.setattr(generate_golden_audit, "augment_with_file_layer", lambda graph: None)
    monkeypatch.setattr(
        generate_golden_audit, "augment_with_test_ref_edges", lambda graph: None
    )
    monkeypatch.setattr(
        generate_golden_audit,
        "build_gs_graph",
        lambda: {
            "nodes": [
                {
                    "id": "Home",
                    "path": "Wiki/Home.md",
                    "kind": "wiki",
                    "in_degree": 0,
                    "out_degree": 0,
                    "incoming": [],
                    "outgoing": [],
                    "degree": 0,
                    "semantic_reach": 0,
                    "relation_diversity": 0,
                    "hub_score": 0,
                }
            ],
            "edges": [],
            "node_count": 1,
            "edge_count": 0,
            "summary": {
                "hubs": [],
                "intentional_orphans": [],
                "orphan_candidates": [],
                "bridges": [],
                "relation_counts": {},
                "intentional_orphan_review": [],
                "reciprocal_pairs": 0,
                "average_edge_confidence": 0.0,
                "semantic_density": 0.0,
                "hub_ratio": 0.0,
                "bridge_ratio": 0.0,
            },
        },
    )

    generate_golden_audit.write_graph_artifacts({})

    receipt = json.loads((tmp_path / GRAPH_RECEIPT_REL).read_text(encoding="utf-8"))
    assert receipt["outputs"] == [
        "Wiki/Graph.md",
        "output/golden_standard_graph.json",
    ]


def test_audit_script_surfaces_manual_graph_patch(tmp_path: Path) -> None:
    def run_git(*args: str) -> None:
        subprocess.run(
            ["git", *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )

    run_git("init", "-q")
    run_git("config", "user.email", "tester@test.com")
    run_git("config", "user.name", "Tester")
    (tmp_path / "README.md").write_text("seed\n", encoding="utf-8")
    run_git("add", "README.md")
    run_git("commit", "-qm", "init")

    graph_md = tmp_path / "Wiki" / "Graph.md"
    graph_md.parent.mkdir(parents=True, exist_ok=True)
    graph_md.write_text("# patched\n", encoding="utf-8")

    original_root = audit_script._ROOT
    try:
        audit_script._ROOT = tmp_path.resolve()
        errors: list[str] = []
        audit_script.check_generated_graph_artifacts(errors)
    finally:
        audit_script._ROOT = original_root

    assert len(errors) == 1
    assert "Wiki/Graph.md" in errors[0]
