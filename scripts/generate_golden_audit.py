#!/usr/bin/env python3
"""Stable CLI entrypoint for the Golden Standard generator package."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gs_generator.cli import main
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
    """Compatibility surface for tests and callers of the former module."""
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


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception:
        import traceback

        print("Error compiling audit report:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        raise SystemExit(1)
