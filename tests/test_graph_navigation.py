from __future__ import annotations

from pathlib import Path
import json

from generate_golden_audit import (
    classify_graph_node,
    infer_graph_relation,
    principle_wikilink,
    render_principle_refs,
)


ROOT = Path(__file__).resolve().parents[1]


def test_principle_link_helpers_point_to_atomic_pages() -> None:
    assert principle_wikilink("PR-081") == "[[Principles/PR-081|PR-081]]"
    assert render_principle_refs("PR-081, PR-084") == (
        "[[Principles/PR-081|PR-081]], [[Principles/PR-084|PR-084]]"
    )


def test_atomic_principle_pages_are_classified_as_principles() -> None:
    assert classify_graph_node(ROOT / "Wiki" / "Principles" / "PR-081.md") == "principle"


def test_atomic_principle_page_exists_and_links_back() -> None:
    page = ROOT / "Wiki" / "Principles" / "PR-097.md"
    assert page.exists()
    content = page.read_text(encoding="utf-8")
    assert "[[Principles|Principles Index]]" in content
    assert "[[Domains/README|Canonical Domains Index]]" in content


def test_principles_index_points_to_atomic_principles() -> None:
    relation, confidence = infer_graph_relation(
        ROOT / "Wiki" / "Principles.md",
        ROOT / "Wiki" / "Principles" / "PR-081.md",
        "Principles",
        "Principles/PR-081",
        "wikilink",
    )
    assert relation == "indexes"
    assert confidence >= 0.9


def test_atomic_principles_create_semantic_edges_from_domains_and_vices() -> None:
    vice_relation, _ = infer_graph_relation(
        ROOT / "Wiki" / "Vices" / "VC-001.md",
        ROOT / "Wiki" / "Principles" / "PR-097.md",
        "Vices/VC-001",
        "Principles/PR-097",
        "wikilink",
    )
    domain_relation, _ = infer_graph_relation(
        ROOT / "Wiki" / "Domains" / "CD01.md",
        ROOT / "Wiki" / "Principles" / "PR-085.md",
        "Domains/CD01",
        "Principles/PR-085",
        "wikilink",
    )

    assert vice_relation == "governed_by"
    assert domain_relation == "operationalizes_domain"


def test_graph_export_materializes_atomic_principle_relations() -> None:
    graph = json.loads((ROOT / "golden_standard_graph.json").read_text(encoding="utf-8"))
    relations = {edge["relation"] for edge in graph["edges"]}

    assert "governed_by" in relations
    assert "thematic_bridge" in relations
