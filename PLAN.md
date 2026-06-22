# PLAN — Sprint GS-H+M (High + Medium backlog)
**Created:** 2026-06-22 | **Agent:** Claude
**Items:** GS-078, GS-010, GS-077, GS-079

---

## Secuencia

```
GS-079 (contenido, bajo riesgo, rápido)
  → GS-010 (pre-commit hook, bajo riesgo)
    → GS-077 (scripts/audit.py, integra CI)
      → GS-078 (graph blast radius, alta complejidad — sesión propia)
```

GS-078 va ÚLTIMO: es el más complejo y requiere que el generator ya esté en `scripts/`
(ya resuelto) y que el validator SP orphan check funcione (ya resuelto). Puede ser
una sesión dedicada si el scope crece.

---

## GS-079 — Dedup README ↔ CONCEPTUAL_FRAMEWORK

**Blast radius:** README.md, CONCEPTUAL_FRAMEWORK.md, Wiki/Home.md (1 link), CONTRIBUTING.md (1 link).
**Angry path:** Links externos de GitHub (shields.io, GitHub Actions badge) apuntan a README — no moverlos.

| Paso | Acción |
|------|--------|
| 79-1 | Leer ambos archivos completos — mapear secciones únicas vs duplicadas |
| 79-2 | CONCEPTUAL_FRAMEWORK.md absorbe toda la doctrina que README duplica |
| 79-3 | README.md → thin: badges + repo tree + quick start + links a CF y Wiki. Meta: <80 líneas |
| 79-4 | Verificar que generator usa CF como fuente (sin cambio requerido) |
| 79-5 | CI check + validator |
| 79-6 | Commit |

---

## GS-010 — Corruption guard (mojibake + truncation)

**Blast radius:** `.claude/settings.local.json` (agregar permiso si pre-commit), `scripts/check_backlog_sync.py` (modelo de referencia).
**Angry path:** ruamel/yaml reflow puede generar bytes distintos a UTF-8 NFC — el check debe validar encoding, no contenido.

| Paso | Acción |
|------|--------|
| 10-1 | Crear `scripts/check_catalog_integrity.py`: leer cada `golden_standard_*.yaml`, validar UTF-8 decodeable + len > 0 + yaml.safe_load sin error |
| 10-2 | Agregar a `.claude/hooks/` o pre-commit (según cómo está configurado en GS) |
| 10-3 | Documentar en `AGENTS.md §1` (una línea) |
| 10-4 | Angry test: crear YAML con bytes inválidos → verificar que el check retorna exit 1 |
| 10-5 | CI check + commit |

---

## GS-077 — `scripts/audit.py` para SP enforcement

**Blast radius:** `scripts/audit.py` (nuevo), `golden_standard_structure_principles.yaml` (status DOC_ONLY → TEST_ASSOCIATED tras verificación), `.github/workflows/audit.yml` (agregar step).
**Angry path:** SP-002 (no material fact in chat) no es checkeable estáticamente con confianza — ese check debe ser heurístico o skip. Documentar límite.

| Paso | Acción |
|------|--------|
| 77-1 | Crear `scripts/audit.py` con checks: |
|      | SP-001: `.agents/AGENTS.md` existe |
|      | SP-003: no hay archivos `status: done/blocked` en `tasks/backlog/` |
|      | SP-004: `tasks/done/` vacío o inexistente |
|      | SP-005: `audit/AUDIT_TRAIL.md` existe y tiene entrada del último commit (heurístico) |
|      | SP-006: presencia de `.agents/`, `tasks/`, `audit/`, `SPEC.md`, `HANDOFF.md`, `DECISIONS.md`, `STATE.md` |
|      | SP-008: `deprecated/` existe si hay entradas deprecadas en catalogs |
|      | SP-009: `HANDOFF.md` tiene sección NOW y NEXT no vacías |
|      | SP-010: raíz no tiene JSON generados (buscar `golden_standard_*.json` en root) |
| 77-2 | SP-002, SP-007 marcados como `skip_reason: no_static_signature` en el script |
| 77-3 | Agregar step a `.github/workflows/audit.yml`: `python scripts/audit.py` |
| 77-4 | Angry test: renombrar `.agents/AGENTS.md` temporalmente → verificar exit 1 |
| 77-5 | Actualizar `golden_standard_structure_principles.yaml`: SP checkeable → `status: AUDITED`, `validating_mechanism: runtime-test` |
| 77-6 | Regenerar + CI check + commit |

---

## GS-078 — Graph blast radius completo (sesión dedicada)

**Scope estimado:** alta complejidad. El generator tiene ~2400 líneas — agregar indexación de scripts + JSON + configs es una refactorización no trivial.

| Paso | Acción |
|------|--------|
| 78-1 | Definir schema de nodo extendido: tipo `script`, `config`, `json-output`, `yaml-catalog` |
| 78-2 | En generator: crawl `scripts/*.py` → extraer `Path("...")` y `from X import` como edges |
| 78-3 | En generator: crawl `*.yaml` catalogs → extraer `path:` refs como edges |
| 78-4 | En generator: crawl `.github/workflows/*.yml` → extraer `run:` commands como edges |
| 78-5 | En `scripts/analyze_graph.py`: agregar `--blast-radius <file>` mode |
| 78-6 | Verificar: `python scripts/analyze_graph.py --blast-radius scripts/generate_golden_audit.py` lista todos los nodos que lo referencian |
| 78-7 | CI check: graph regenerado pasa `git diff --exit-code` |
| 78-8 | Actualizar GS-078 acceptance criteria si scope cambia durante ejecución |

**Recomendación:** ejecutar GS-078 en sesión separada. Los otros 3 caben en una sesión.

---

## Angry path global

1. **GS-079 rompe links en README:** verificar con validator + grep antes de commit
2. **GS-010 check falla en CI por encoding CRLF (Windows):** el check debe abrir con `errors='replace'` y buscar replacement char U+FFFD
3. **GS-077 step en audit.yml falla en Ubuntu:** paths relativos — correr `python scripts/audit.py` desde root, verificar en Ubuntu que `.agents/` existe
4. **GS-078 graph crece demasiado:** si los edges de scripts disparan el node/edge count por 10x, puede haber impacto en performance del generator. Agregar benchmark antes de mergear.

---

## Acceptance criteria globales

- [ ] `pytest tests/ -q` → 10 passed (después de 079, 010, 077)
- [ ] `python scripts/validate_golden_standard_catalogs.py` → green
- [ ] `python scripts/audit.py` → green (después de 077)
- [ ] README.md < 80 líneas (después de 079)
- [ ] 0 archivos `golden_standard_*.json` en root (ya cumplido)
- [ ] PLAN.md eliminado al cierre
