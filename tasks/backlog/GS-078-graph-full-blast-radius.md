---
id: GS-078
title: Extender graph para cubrir blast radius completo (scripts, JSON, YAML, configs)
status: backlog
priority: high
created: 2026-06-22
---

## Goal

El `golden_standard_graph.json` actualmente solo indexa nodos de documentos markdown
(Wiki/, knowledge/). No rastrea scripts, JSON outputs, archivos YAML de catálogo, ni
artefactos generados. Esto hace que el grafo sea inútil para análisis de blast radius
antes de mover o renombrar archivos — se necesita grep manual en su lugar.

El grafo debería ser la fuente de verdad para responder: "si muevo X, ¿qué se rompe?"

## Acceptance criteria

- [ ] `generate_golden_audit.py` indexa como nodos todos los archivos relevantes del repo:
  scripts (`*.py`), outputs JSON, YAML catalogs, configs (`audit.yml`, `pyproject.toml`),
  markdown docs raíz (README, CONTRIBUTING, CONCEPTUAL_FRAMEWORK, etc.)
- [ ] Los edges incluyen: imports Python (`from X import`), markdown links `[](path)`,
  YAML `path:` references, y write/read paths en scripts (Path("x.json"))
- [ ] `scripts/analyze_graph.py` tiene un modo `--blast-radius <archivo>` que lista
  todos los nodos que referencian ese archivo (incoming edges)
- [ ] Blast radius de cualquier archivo del repo es consultable en < 5 segundos
- [ ] Grafo regenerado pasa CI (`git diff --exit-code`)

## Why this matters

Descubierto durante limpieza de GS root (2026-06-22): al mover `badges/`,
`generate_golden_audit.py`, y outputs JSON, el blast radius requirió múltiples
rondas de grep manual. El grafo debería haber respondido eso instantáneamente.
Sin esta capacidad, cada refactor estructural tiene riesgo de análisis incompleto.

## Extended scope — "correlate everything correlatable"

Beyond file blast radius, the graph should enable these queries:

### Semantic chains (entry → evidence)
- VC-003 → `Wiki/VC-003.md` → `scripts/test_detectors.py` → `docs/badges/detectors.json`
- Full chain: catalog entry → wiki page → detector → badge → test coverage
- Query: "which VC entries have no detector?" / "which have no badge?"

### Orphan detection
- Nodes with zero incoming edges = unreferenced files (dead docs, dead scripts)
- Query: "what can I delete safely?"

### Coupling score
- Nodes with highest in-degree = highest blast radius risk = refactor candidates
- Query: "what are the 5 most dangerous files to touch?"

### Test coverage map
- `tests/test_X.py` → references `scripts/X.py` → covers VC-YYY
- Query: "which scripts have no test?" / "which entries have no coverage?"

### Circular dependency detection
- Python import cycles across scripts/
- Query: "are there import cycles?"

### Diff impact preview
- Given a list of changed files (from `git diff --name-only`), output full blast radius
- Query: `analyze_graph.py --diff-impact` (reads stdin or git diff directly)

### CI step dependency graph
- audit.yml steps → which files they read/write → ordering constraints
- Query: "if I change X, which CI steps are affected?"

## Blockers
none
