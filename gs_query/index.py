"""Indice invertido del catalogo GS (GS-03/GS-MCP-001).

Sin embeddings, sin red: solo tokenizacion lexica sobre los campos de texto
de cada entrada (title/symptom/cause/solution/action/insight/summary segun
el catalogo). El indice se reconstruye automaticamente cuando el hash de
contenido de los YAML fuente cambia -- no requiere un paso manual de
"reindexar".
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml

GS_ROOT = Path(__file__).resolve().parent.parent

CATALOG_FILES = {
    "VC": ("golden_standard_coding_vices.yaml", "Wiki/Vices"),
    "VT": ("golden_standard_testing_vices.yaml", "Wiki/Vices"),
    "TK": ("golden_standard_tokenomics.yaml", "Wiki/Tokenomics"),
    "PR": ("golden_standard_principles.yaml", "Wiki/Principles"),
    "SP": ("golden_standard_structure_principles.yaml", "Wiki/Principles"),
    "AV": ("golden_standard_adversarial_vectors.yaml", "Wiki/Vices"),
}

_TOKEN_RE = re.compile(r"[a-záéíóúñü0-9]+")

# Stopwords ES/EN: palabras cortas de conexion que generan falsos positivos
# ("no", "es", "the", "a"...) si se indexan como si fueran terminos de
# busqueda reales. Sin esto, una consulta sin sentido como "xyzzy no existe"
# devolvia resultados solo porque "no" aparece en decenas de entradas.
_STOPWORDS = {
    "a", "al", "de", "del", "el", "en", "es", "la", "las", "lo", "los", "no",
    "o", "por", "que", "se", "su", "un", "una", "y",
    "an", "and", "are", "as", "at", "be", "by", "for", "if", "in", "is",
    "it", "of", "on", "or", "the", "to", "was", "with",
}


def _tokenize(text: str) -> set[str]:
    tokens = _TOKEN_RE.findall((text or "").lower())
    return {t for t in tokens if t not in _STOPWORDS and len(t) > 2}


def _mitigation_two_lines(entry: dict) -> str:
    text = entry.get("solution") or entry.get("action") or entry.get("summary") or ""
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    return " ".join(lines)[:220]


def _prose_link(catalog_prefix: str, entry_id: str, root: Path) -> Optional[str]:
    """None si no existe prosa generada (p.ej. el catalogo AV no participa
    todavia del pipeline de generate_golden_audit.py -- mejor admitirlo que
    devolver un link roto."""
    _, wiki_dir = CATALOG_FILES[catalog_prefix]
    candidate = root / wiki_dir / f"{entry_id}.md"
    return f"{wiki_dir}/{entry_id}.md" if candidate.exists() else None


@dataclass
class Rule:
    id: str
    catalog: str
    title: str
    severity: Optional[str]
    mitigation: str
    prose_link: Optional[str]
    domain: Optional[str] = None
    tokens: set = field(default_factory=set, repr=False)


def _catalog_source_hash(root: Path) -> str:
    digest = hashlib.sha256()
    for fname, _ in sorted(CATALOG_FILES.values()):
        path = root / fname
        if path.exists():
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _entry_text_blob(entry: dict) -> str:
    fields = ("title", "symptom", "cause", "solution", "action", "insight", "summary")
    return " ".join(str(entry.get(f, "")) for f in fields)


def build_index(root: Optional[Path] = None) -> tuple[dict[str, Rule], dict[str, set[str]], str]:
    root = root or GS_ROOT
    rules: dict[str, Rule] = {}
    inverted: dict[str, set[str]] = {}

    for prefix, (fname, _wiki_dir) in CATALOG_FILES.items():
        path = root / fname
        if not path.exists():
            continue
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for entry in data.get("items", []):
            entry_id = entry.get("id")
            if not entry_id:
                continue
            title = entry.get("title") or entry.get("insight") or entry_id
            rule = Rule(
                id=entry_id,
                catalog=prefix,
                title=title,
                severity=entry.get("severity"),
                mitigation=_mitigation_two_lines(entry),
                prose_link=_prose_link(prefix, entry_id, root),
                domain=entry.get("canonical_domain") or entry.get("domain"),
            )
            tokens = _tokenize(_entry_text_blob(entry)) | _tokenize(entry_id)
            rule.tokens = tokens
            rules[entry_id] = rule
            for tok in tokens:
                inverted.setdefault(tok, set()).add(entry_id)

    return rules, inverted, _catalog_source_hash(root)
