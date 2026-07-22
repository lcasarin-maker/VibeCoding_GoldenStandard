#!/usr/bin/env python3
"""Stable CLI entrypoint for the Golden Standard generator package."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gs_generator.cli import main as generate_main
from gs_generator import engine as _engine
from gs_generator.engine import (
    GRAPH_MARKDOWN,
    GRAPH_OUTPUT,
    _ROOT,
    augment_with_file_layer,
    augment_with_test_ref_edges,
    build_gs_graph,
    classify_graph_node,
    infer_graph_relation,
    principle_wikilink,
    render_principle_refs,
)


def write_graph_artifacts(mapped_database=None):
    """Delegates to gs_generator.engine.write_graph_artifacts, temporarily
    applying this module's own globals (_ROOT, GRAPH_OUTPUT, GRAPH_MARKDOWN,
    augment_with_file_layer, augment_with_test_ref_edges, build_gs_graph) so
    callers/tests that monkeypatch attributes on THIS module (the public,
    documented CLI entrypoint) see those overrides take effect where the
    real work happens. gs_generator is the only engine implementation --
    there is nothing else this delegates around."""
    original = {
        "_ROOT": _engine._ROOT,
        "GRAPH_OUTPUT": _engine.GRAPH_OUTPUT,
        "GRAPH_MARKDOWN": _engine.GRAPH_MARKDOWN,
        "augment_with_file_layer": _engine.augment_with_file_layer,
        "augment_with_test_ref_edges": _engine.augment_with_test_ref_edges,
        "build_gs_graph": _engine.build_gs_graph,
    }
    try:
        _engine._ROOT = _ROOT
        _engine.GRAPH_OUTPUT = GRAPH_OUTPUT
        _engine.GRAPH_MARKDOWN = GRAPH_MARKDOWN
        _engine.augment_with_file_layer = augment_with_file_layer
        _engine.augment_with_test_ref_edges = augment_with_test_ref_edges
        _engine.build_gs_graph = build_gs_graph
        return _engine.write_graph_artifacts(mapped_database)
    finally:
        for name, value in original.items():
            setattr(_engine, name, value)


def main(argv: list[str] | None = None) -> int:
    """Run the GS generator CLI with a narrower, diagnostic-friendly error gate."""
    try:
        return generate_main(argv)
    except (FileNotFoundError, OSError, RuntimeError, TypeError, ValueError) as exc:
        print(f"Error compiling audit report: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
