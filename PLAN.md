---
task: GS-deuda-final
title: Cerrar toda la deuda GS (GS-071, 075, 076, 080, 081)
started: 2026-06-22
agent: Claude
---

# Secuencia

```
GS-081 → GS-080 → GS-071 → GS-076 → GS-075
```

# GS-081 — Templates + campos frontmatter

1. Agregar `effort:` a GS-071, GS-075, GS-076 (faltan)
2. Crear `knowledge/templates/` con STATE_template.md, HANDOFF_template.md, TASK_template.md, README.md
3. Extender audit.py check_sp007(): verificar `priority:` y `effort:` además de id/title/status

# GS-080 — SP-005 en audit.py

4. Agregar check_sp005(): HANDOFF.md y STATE.md existen, no vacíos, tienen headers `**Date:**`/`**Last updated:**`
   NOTA: NO checkear que la fecha == hoy (falla en CI). Solo verificar estructura.

# GS-071 — DOC_ONLY promotion/justification (15 entries)

5. Promover a REMEDIATED (tienen static-regex o son promovibles):
   - VC-088: ya tiene `validating_mechanism: static-regex` → solo cambiar status
   - VC-012: `for now` pattern → agregar detector en detectors.py + status=REMEDIATED
6. Justificar como DOC_ONLY permanente (behavioral/AI-specific — no static signature):
   - VC-007, VC-009, VC-037, VC-042, VC-046, VC-058, VC-060, VC-062, VC-063, VC-064, VC-067, VC-068, VC-069
   - Agregar campo `justification_doc_only:` en cada entrada explicando por qué

# GS-076 — Graph hardening

7. En validate_golden_standard_catalogs.py: agregar check_graph_connectivity() — flaggear nodos aislados (0-in, 0-out)
8. En generate_golden_audit.py: Graph.md ya regenera; agregar sección `## Debt snapshot` con counts DOC_ONLY por catalog

# GS-075 — Generator split (minimal)

9. Agregar flags `--audit-only` y `--wiki-only` a generate_golden_audit.py
10. Agregar tests: uno que verifica `--audit-only` produce output/golden_standard_audit.json, otro verifica `--wiki-only` produce Wiki/

# Angry path
- GS-080: evitar date == today — solo headers existentes
- GS-071: VC-012 detector debe tener example_bad que lo dispare en test
- GS-076: nodos aislados = badge JSON files (0 edges) — marcarlos como "intentional" no como error
- GS-075: `--audit-only` no debe regenerar wiki (rompe git diff check) — solo el JSON
