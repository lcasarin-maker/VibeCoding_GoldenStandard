"""Busqueda sobre el indice invertido (GS-03). Reconstruye el indice en cada
llamada a partir de los YAML fuente -- son catalogos chicos (cientos de
entradas), asi que no hace falta cachear, y la evidencia de "se reconstruye
por hash automaticamente" es simplemente que nunca hay un paso manual de
reindexado: siempre lee el estado actual del disco.

"Sin relleno": si no hay coincidencias, la respuesta es una lista vacia --
nunca resultados irrelevantes para no responder vacio."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from gs_query.index import Rule, _tokenize, build_index


def rule_to_dict(rule: Rule) -> dict:
    return {
        "id": rule.id,
        "title": rule.title,
        "class": rule.catalog,
        "severity": rule.severity,
        "mitigation": rule.mitigation,
        "prose_link": rule.prose_link,
    }


_SEVERITY_ES = {"alta": "high", "media": "medium", "baja": "low"}


def _normalize_severity(value: str) -> str:
    return _SEVERITY_ES.get(value.lower(), value.lower())


def search(
    query: str,
    *,
    domain: Optional[str] = None,
    severity: Optional[str] = None,
    max_results: int = 5,
    root: Optional[Path] = None,
) -> list[dict]:
    rules, inverted, _source_hash = build_index(root)
    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    scores: dict[str, int] = {}
    for tok in query_tokens:
        for rid in inverted.get(tok, ()):
            scores[rid] = scores.get(rid, 0) + 1

    candidates = [rules[rid] for rid in scores]
    if severity:
        target = _normalize_severity(severity)
        candidates = [r for r in candidates if (r.severity or "").lower() == target]
    if domain:
        candidates = [r for r in candidates if (r.domain or "").upper() == domain.upper()]

    candidates.sort(key=lambda r: (-scores[r.id], r.id))
    return [rule_to_dict(r) for r in candidates[:max_results]]
