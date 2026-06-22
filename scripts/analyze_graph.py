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


def blast_radius(graph: dict, target_file: str) -> list[dict]:
    """Return all nodes that have an incoming edge from target_file (direct referrers)."""
    nodes = {n["id"]: n for n in graph["nodes"]}
    # Normalize: accept relative posix path or node id
    node_id = target_file if target_file in nodes else target_file.replace("\\", "/")
    if node_id not in nodes:
        return []
    referrers = []
    for edge in graph["edges"]:
        if edge["target"] == node_id and edge["source"] in nodes:
            src = nodes[edge["source"]]
            referrers.append({"id": src["id"], "kind": src["kind"], "relation": edge["relation"]})
    return referrers


def coupling_report(graph: dict, top_n: int = 10) -> list[dict]:
    """Top N nodes by in-degree — highest coupling (most things reference them)."""
    nodes = sorted(graph["nodes"], key=lambda n: (-n["in_degree"], n["path"]))
    return [{"id": n["id"], "kind": n["kind"], "in_degree": n["in_degree"], "path": n["path"]} for n in nodes[:top_n]]


def detect_cycles(graph: dict) -> list[list[str]]:
    """Find import cycles using iterative DFS. Returns list of cycle node lists."""
    import_edges: dict[str, list[str]] = defaultdict(list)
    for e in graph["edges"]:
        if e["relation"] == "imports":
            import_edges[e["source"]].append(e["target"])

    visited: set[str] = set()
    rec_stack: set[str] = set()
    cycles: list[list[str]] = []

    def dfs(node: str, path: list[str]) -> None:
        visited.add(node)
        rec_stack.add(node)
        path.append(node)
        for neighbor in import_edges.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])
        path.pop()
        rec_stack.discard(node)

    for node_id in import_edges:
        if node_id not in visited:
            dfs(node_id, [])
    return cycles


def coverage_report(graph: dict) -> dict:
    """Check which VC/VT catalog entries have wiki pages, detector mentions, test mentions."""
    nodes_by_id = {n["id"]: n for n in graph["nodes"]}
    script_ids = {n["id"] for n in graph["nodes"] if n["kind"] in ("script", "test")}

    # File-layer nodes' text content is not stored in graph — check for edges instead
    # A wiki node connected (incoming) to a script node = script references the wiki entry
    wiki_nodes = [n for n in graph["nodes"] if n["kind"] == "vice"]
    results = []
    for wn in wiki_nodes:
        entry_id = wn["id"]  # e.g. "Wiki/Detectors/vc003_..."
        has_wiki = True  # the wiki node itself is the page
        connected_scripts = [s for s in wn["incoming"] if s in script_ids]
        results.append({
            "id": entry_id,
            "has_wiki": has_wiki,
            "referenced_by_scripts": connected_scripts,
        })
    return {
        "total": len(results),
        "with_script_ref": sum(1 for r in results if r["referenced_by_scripts"]),
        "without_script_ref": [r["id"] for r in results if not r["referenced_by_scripts"]][:20],
    }


def diff_impact(graph: dict, changed_files: list[str]) -> dict:
    """Union blast radius for a list of changed files."""
    all_referrers: dict[str, set[str]] = {}
    for f in changed_files:
        refs = blast_radius(graph, f)
        all_referrers[f] = {r["id"] for r in refs}
    union = set()
    for refs in all_referrers.values():
        union.update(refs)
    return {
        "changed_files": changed_files,
        "per_file": {f: sorted(refs) for f, refs in all_referrers.items()},
        "union_blast_radius": sorted(union),
        "total_affected": len(union),
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze GS knowledge graph")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    parser.add_argument("--graph", type=Path, default=Path("output/golden_standard_graph.json"))
    parser.add_argument("--blast-radius", metavar="FILE", help="List all nodes referencing FILE")
    parser.add_argument("--coupling", metavar="N", type=int, nargs="?", const=10, help="Top N nodes by in-degree")
    parser.add_argument("--diff-impact", metavar="FILE", nargs="+", help="Union blast radius for changed files")
    parser.add_argument("--cycles", action="store_true", help="Detect import cycles")
    parser.add_argument("--coverage", action="store_true", help="Check VC/VT wiki coverage vs scripts")
    args = parser.parse_args()

    if not args.graph.exists():
        print(f"Graph not found: {args.graph}", file=sys.stderr)
        sys.exit(1)

    graph = load_graph(args.graph)

    if args.blast_radius:
        refs = blast_radius(graph, args.blast_radius)
        if args.format == "json":
            print(json.dumps({"target": args.blast_radius, "referrers": refs}, indent=2))
        else:
            print(f"Blast radius of '{args.blast_radius}': {len(refs)} referrer(s)")
            for r in refs:
                print(f"  [{r['relation']}]  {r['id']}  ({r['kind']})")
        return

    if args.coupling is not None:
        rows = coupling_report(graph, args.coupling)
        if args.format == "json":
            print(json.dumps(rows, indent=2))
        else:
            print(f"Top {args.coupling} nodes by in-degree:")
            for r in rows:
                print(f"  in={r['in_degree']:3d}  {r['id']}  ({r['kind']})")
        return

    if args.diff_impact:
        report = diff_impact(graph, args.diff_impact)
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print(f"Diff impact for {len(report['changed_files'])} file(s):")
            for f, refs in report["per_file"].items():
                print(f"  {f}: {len(refs)} direct referrer(s)")
            print(f"Union blast radius: {report['total_affected']} node(s)")
            for n in report["union_blast_radius"]:
                print(f"  {n}")
        return

    if args.cycles:
        cycles = detect_cycles(graph)
        if args.format == "json":
            print(json.dumps({"cycles": cycles}, indent=2))
        else:
            if cycles:
                print(f"{len(cycles)} import cycle(s) detected:")
                for c in cycles:
                    print("  " + " -> ".join(c))
            else:
                print("No import cycles detected.")
        return

    if args.coverage:
        report = coverage_report(graph)
        if args.format == "json":
            print(json.dumps(report, indent=2))
        else:
            print(f"Coverage: {report['with_script_ref']}/{report['total']} vice wiki pages referenced by scripts")
            if report["without_script_ref"]:
                print(f"No script reference ({len(report['without_script_ref'])} shown):")
                for item in report["without_script_ref"]:
                    print(f"  {item}")
        return

    report = analyze(graph)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)


if __name__ == "__main__":
    main()
