#!/usr/bin/env python3
"""analyze_graph.py — Analyze the Golden Standard knowledge graph.

Reads golden_standard_graph.json and produces a health report with:
- General metrics (nodes, edges, density)
- Hub analysis (overloaded nodes)
- Orphan analysis (unexpected isolates)
- Cluster detection (connected components)
- Bridge analysis (nodes connecting different kinds)
- Broken link detection (edges to non-existent nodes)

Usage:
    py.exe scripts/analyze_graph.py
    py.exe scripts/analyze_graph.py --format json
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def load_graph(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def analyze(graph: dict) -> dict:
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph["edges"]
    node_count = len(nodes)
    edge_count = len(edges)

    # Density (directed graph, no self-loops)
    max_edges = node_count * (node_count - 1)
    density = edge_count / max_edges if max_edges > 0 else 0.0

    # Kinds distribution
    kind_counts = Counter(n["kind"] for n in nodes.values())

    # Orphan candidates (unexpected 0-in-degree nodes)
    orphan_candidates = [
        n for n in nodes.values()
        if n["in_degree"] == 0
        and n["kind"] in {"wiki", "vice", "insight", "domain", "concept", "root"}
    ]

    # Isolated nodes (0 in, 0 out)
    isolated = [n for n in nodes.values() if n["in_degree"] == 0 and n["out_degree"] == 0]

    # Hubs (top 10 by degree)
    hubs = sorted(nodes.values(), key=lambda n: (-n["degree"], -n["in_degree"], n["path"]))[:10]

    # Bridges (connect multiple kinds)
    bridges = []
    for n in nodes.values():
        target_kinds = {nodes[t]["kind"] for t in n["outgoing"] if t in nodes}
        if len(target_kinds) > 1:
            bridges.append({
                "id": n["id"],
                "kind": n["kind"],
                "target_kinds": sorted(target_kinds),
                "out_degree": n["out_degree"],
            })
    bridges.sort(key=lambda b: (-b["out_degree"], b["id"]))

    # Connected components (clusters)
    visited = set()
    components = []
    for nid in nodes:
        if nid in visited:
            continue
        stack = [nid]
        comp = set()
        while stack:
            cur = stack.pop()
            if cur in comp:
                continue
            comp.add(cur)
            for neighbor in nodes[cur]["outgoing"] + nodes[cur]["incoming"]:
                if neighbor in nodes and neighbor not in comp:
                    stack.append(neighbor)
        visited.update(comp)
        components.append(sorted(comp))
    components.sort(key=lambda c: -len(c))

    # Broken links
    broken = []
    for e in edges:
        if e["target"] not in nodes:
            broken.append(e)

    # Edge kind distribution
    edge_kinds = Counter(e["kind"] for e in edges)

    return {
        "metrics": {
            "node_count": node_count,
            "edge_count": edge_count,
            "density": round(density, 4),
            "avg_degree": round(sum(n["degree"] for n in nodes.values()) / node_count, 2) if node_count else 0,
            "components": len(components),
            "largest_component": len(components[0]) if components else 0,
        },
        "kinds": dict(kind_counts),
        "edge_kinds": dict(edge_kinds),
        "hubs": [
            {"id": n["id"], "kind": n["kind"], "degree": n["degree"], "in_degree": n["in_degree"], "out_degree": n["out_degree"]}
            for n in hubs
        ],
        "orphans": [
            {"id": n["id"], "kind": n["kind"], "path": n["path"]}
            for n in orphan_candidates
        ],
        "isolated": [
            {"id": n["id"], "kind": n["kind"], "path": n["path"]}
            for n in isolated
        ],
        "bridges": bridges[:10],
        "components": components[:5],
        "broken_links": broken,
    }


def print_report(report: dict) -> None:
    m = report["metrics"]
    print("=" * 60)
    print("GOLDEN STANDARD GRAPH HEALTH REPORT")
    print("=" * 60)
    print(f"\nNodes: {m['node_count']} | Edges: {m['edge_count']} | Density: {m['density']}")
    print(f"Components: {m['components']} | Largest: {m['largest_component']} | Avg degree: {m['avg_degree']}")

    print("\n--- Node kinds ---")
    for kind, count in sorted(report["kinds"].items(), key=lambda x: -x[1]):
        print(f"  {kind}: {count}")

    print("\n--- Edge kinds ---")
    for kind, count in sorted(report["edge_kinds"].items(), key=lambda x: -x[1]):
        print(f"  {kind}: {count}")

    print("\n--- Top 10 hubs ---")
    for h in report["hubs"]:
        print(f"  {h['id']} ({h['kind']}) | degree={h['degree']} in={h['in_degree']} out={h['out_degree']}")

    print(f"\n--- Orphan candidates ({len(report['orphans'])}) ---")
    for o in report["orphans"]:
        print(f"  {o['id']} ({o['kind']})")

    print(f"\n--- Isolated nodes ({len(report['isolated'])}) ---")
    for n in report["isolated"]:
        print(f"  {n['id']} ({n['kind']})")

    print(f"\n--- Bridges (connect multiple kinds) ({len(report['bridges'])}) ---")
    for b in report["bridges"]:
        print(f"  {b['id']} ({b['kind']}) -> {', '.join(b['target_kinds'])} ({b['out_degree']} edges)")

    print(f"\n--- Components ({m['components']}) ---")
    for i, comp in enumerate(report["components"], 1):
        print(f"  Component {i}: {len(comp)} nodes ({', '.join(comp[:3])}{', ...' if len(comp) > 3 else ''})")

    if report["broken_links"]:
        print(f"\n--- BROKEN LINKS ({len(report['broken_links'])}) ---")
        for bl in report["broken_links"]:
            print(f"  {bl['source']} --({bl['kind']})--> {bl['target']}")
    else:
        print("\n--- Broken links: 0 ---")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Analyze GS knowledge graph")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--graph", type=Path, default=Path("golden_standard_graph.json"))
    args = parser.parse_args()

    if not args.graph.exists():
        print(f"Graph not found: {args.graph}", file=sys.stderr)
        sys.exit(1)

    graph = load_graph(args.graph)
    report = analyze(graph)

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
