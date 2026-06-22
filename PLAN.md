# PLAN — GS Root Cleanup (Immaculate)
**Created:** 2026-06-22 | **Agent:** Claude | **Ref:** Canonical Structure V3.2

---

## Blast radius map

| Item | Referencias activas | Riesgo |
|------|---------------------|--------|
| `knowledge/` (ghost: hypotheses.md, rules.md, knowledge.md — 40 líneas) | CONTRIBUTING.md (1 link) | BAJO |
| `INGESTION_PROTOCOL.md` → `knowledge/` | README.md, CONTRIBUTING.md, CONCEPTUAL_FRAMEWORK, Inbox/README, INGESTION_PROTOCOL propio, KNOWLEDGE_SOURCES | MEDIO |
| `KNOWLEDGE_SOURCES.md` → `knowledge/` | CONTRIBUTING.md, knowledge/rules.md | BAJO |
| `CONSUMER_CONTRACT.md` → `knowledge/` | CONTRIBUTING.md, knowledge/rules.md, cerberus_gs_id_audit.md, KNOWLEDGE_SOURCES.md | MEDIO |
| `badges/` → `docs/badges/` | README.md (image links), audit/AUDIT_TRAIL.md (mención) | BAJO |
| `generate_golden_audit.py` → `scripts/` | 20+ refs, tests lo importan (test_infrastructure.py) | ALTO — defer (GS-075) |
| `golden_standard_*.json` outputs → `output/` | tests los leen, generator los escribe | ALTO — defer (depende de GS-075) |

---

## Reglas nuevas detectadas (revisar SP antes de ejecutar)

**Falta SP-010:** GS es un repo de conocimiento, no de código. La canonical define `knowledge/` como
carpeta para *importar* reglas externas. GS ES la fuente — sus YAMLs SON el producto.
Necesita una regla que distinga raíz de knowledge repo (YAMLs + generator al root son válidos)
vs raíz de project repo (código va en src/).

---

## Pasos (ordenados por riesgo)

### Fase A — Reorganizar knowledge/ (bajo riesgo)

**A1** — Eliminar ghost files de `knowledge/`: `hypotheses.md`, `rules.md`, `knowledge.md`
- Contenido: 40 líneas sin valor, supersedidas por catalogs + INGESTION_PROTOCOL
- Absorber el concepto de "working loop" en `knowledge/INDEX.md` actualizado
- Acceptance: `knowledge/` contiene solo INDEX.md + los archivos que se moverán en A2/A3/A4

**A2** — Mover `CONSUMER_CONTRACT.md` → `knowledge/CONSUMER_CONTRACT.md` (canonical §2 lo ubica ahí)
- Actualizar refs: CONTRIBUTING.md, KNOWLEDGE_SOURCES.md, cerberus_gs_id_audit.md
- Acceptance: `git mv` limpio, validator verde, 0 links rotos

**A3** — Mover `KNOWLEDGE_SOURCES.md` → `knowledge/KNOWLEDGE_SOURCES.md`
- Actualizar refs: CONTRIBUTING.md, knowledge/rules.md (si sobrevive A1), INGESTION_PROTOCOL.md
- Acceptance: idem

**A4** — Mover `INGESTION_PROTOCOL.md` → `knowledge/INGESTION_PROTOCOL.md`
- Actualizar refs: README.md, CONTRIBUTING.md, CONCEPTUAL_FRAMEWORK.md, Inbox/README.md, KNOWLEDGE_SOURCES.md (ya movido)
- Acceptance: idem

**A5** — Actualizar `knowledge/INDEX.md` para reflejar la nueva estructura real de la carpeta
- Acceptance: INDEX.md lista los 3 archivos reales sin mencionar ghost files

### Fase B — Mover badges/ (bajo riesgo)

**B1** — Mover `badges/` → `docs/badges/`
- Actualizar refs: README.md (image links — son URLs relativas), audit/AUDIT_TRAIL.md (menciones)
- Acceptance: badges en docs/badges/, README.md renderiza badges correctamente

### Fase C — Agregar SP-010 (nueva regla)

**C1** — Agregar SP-010 a `golden_standard_structure_principles.yaml`
- Título: "Knowledge repo root discipline"
- Regla: en repos de conocimiento, los YAMLs de catálogo y su generator principal son artefactos raíz legítimos (son el producto, no código auxiliar). Los outputs generados van en `output/`. Los docs de protocolo van en `knowledge/`.
- Acceptance: SP-010 creado, CI verde

### Fase D — DEFERRED (requieren GS-075 primero)

**D1** — `generate_golden_audit.py` → `scripts/` (GS-075)
**D2** — JSON outputs → `output/` (depende de D1)

### Fase E — Cierre

**E1** — Verificar validator + pytest pasan
**E2** — Actualizar STATE.md migration complete
**E3** — Commit + session record + AUDIT_TRAIL
**E4** — Eliminar PLAN.md

---

## Aceptación global

- [ ] `python scripts/validate_golden_standard_catalogs.py` → green
- [ ] `pytest tests/ -q` → 10 passed
- [ ] `knowledge/` contiene solo archivos canon (no ghosts)
- [ ] `INGESTION_PROTOCOL.md`, `KNOWLEDGE_SOURCES.md`, `CONSUMER_CONTRACT.md` en `knowledge/`
- [ ] `badges/` en `docs/badges/`
- [ ] SP-010 creado
- [ ] 0 links rotos en README, CONTRIBUTING, CONCEPTUAL_FRAMEWORK, Inbox/README
- [ ] PLAN.md eliminado
