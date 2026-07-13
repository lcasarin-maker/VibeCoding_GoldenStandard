"""Tests de gs_query (GS-03/GS-MCP-001): CLI + busqueda lexica sobre el
catalogo real. Sin red, sin embeddings."""

import json
import os
import subprocess
import sys
from pathlib import Path

from gs_query.search import search

ROOT = Path(__file__).resolve().parent.parent


def test_replace_file_devuelve_vc052_en_top3():
    results = search("replace file", max_results=3)
    ids = [r["id"] for r in results]
    assert "VC-052" in ids, f"VC-052 (Zombie Compatibility Theater) deberia estar en {ids}"


def test_consulta_sin_matches_devuelve_vacio_no_relleno():
    results = search("xyzzy_no_existe_este_termino_jamas_zzqq")
    assert results == []


def test_filtro_severidad():
    results = search("replace file", severity="alta", max_results=10)
    assert results
    assert all(r["severity"] == "high" for r in results)


def test_respuesta_bajo_1kb_por_regla():
    results = search("replace file", max_results=5)
    for r in results:
        assert len(json.dumps(r, ensure_ascii=False)) < 1024


def test_prose_link_apunta_a_archivo_existente_o_es_none():
    """AV-* no tiene prosa generada todavia (fuera del pipeline de
    generate_golden_audit.py) -- None es honesto, un link roto no lo es."""
    results = search("replace file", max_results=5)
    assert any(r["prose_link"] for r in results)
    for r in results:
        if r["prose_link"] is not None:
            assert (ROOT / r["prose_link"]).exists(), r["prose_link"]


def test_cli_end_to_end():
    env = {**os.environ, "PYTHONPATH": str(ROOT)}
    proc = subprocess.run(
        [sys.executable, "-m", "gs_query", "replace file", "--max", "3"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(proc.stdout)
    assert any(r["id"] == "VC-052" for r in payload)
