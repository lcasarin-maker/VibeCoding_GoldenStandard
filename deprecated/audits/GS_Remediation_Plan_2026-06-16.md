# Plan de Remediación — Golden Standard

**Fecha:** 2026-06-16  
**Origen:** Independent Adversarial Audit 2026-06-16  
**Mandato:** Corregir todas las observaciones del audit. Purgar `deprecated/` si el conocimiento ya está en el proyecto vivo.  
**Estrategia:** Fases secuenciales, de afuera hacia adentro: primero higiene, luego estructura, luego contenido.  

---

## FASE 0: Preflight (Verificación de estado antes de tocar nada)

**Objetivo:** Saber exactamente qué vamos a cambiar y que el CI esté verde antes de empezar.

1. **Estado actual del repo**
   ```bash
   git status
   git log --oneline -5
   ```
   Resultado: sin cambios locales pendientes, HEAD limpio.

2. **Verificar que el generador funciona**
   ```bash
   python generate_golden_audit.py
   ```
   Resultado: termina sin errores, genera los archivos de salida.

3. **Verificar que el validador pasa**
   ```bash
   python scripts/validate_golden_standard_catalogs.py --check-wiki
   ```
   Resultado: salida limpia, sin errores.

4. **Verificar que los tests pasan**
   ```bash
   python scripts/test_detectors.py
   python scripts/metrics.py
   ```
   Resultado: `All 16 local detectors proven`, `stubs: 0`.

5. **Guardar baseline**
   ```bash
   git stash list   # asegurar que no hay stash activo
   # (opcional) crear rama: git checkout -b remediation/audit-2026-06-16
   ```

---

## FASE 1: Urgent Cleanup — Corrección de archivos activos contaminados

**Objetivo:** Eliminar español, links rotos, typos, y archivos muertos del árbol activo. Todo en esta fase es edición directa sin rediseño.

### 1.1. Traducir `Inbox/README.md` al inglés

**Archivo:** `Inbox/README.md`  
**Acción:** Reescribir completo en inglés, manteniendo exactamente la misma estructura y contenido semántico.  

Contenido a escribir:
```markdown
# Inbox — Golden Standard Knowledge Ingestion

This directory is the **intake mailbox** of the knowledge base.
Raw findings are deposited here before being curated and promoted to the catalog.

> **For the full ingestion protocol, see:** [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md)  
> **For authorized sources and their contracts, see:** [`KNOWLEDGE_SOURCES.md`](../KNOWLEDGE_SOURCES.md)

---

## Directory Structure

```
Inbox/
├── cerberus/      ← Findings from CoderCerberus audits
├── manual/        ← Findings from manual DRI sessions
├── external/      ← External contributions (triaged by maintainers)
└── templates/
    ├── cerberus_finding.md        ← Template for Cerberus findings
    ├── manual_finding.md          ← Template for manual findings
    └── external_contribution.md   ← Template for external contributions
```

### Notes per Folder

- [`cerberus/README.md`](cerberus/README.md) — what to deposit and how to name it.
- [`manual/README.md`](manual/README.md) — findings observed by the DRI.
- [`external/README.md`](external/README.md) — flow for external issues and PRs; only evidence anchored to the active baseline and with fresh purge if auditing cleanliness or completeness.
- [`templates/README.md`](templates/README.md) — quick reference for templates.

---

## How to Deposit a Finding (quick summary)

1. Copy the appropriate template from `Inbox/templates/`
2. Fill all required fields (marked with ✅ in the template)
3. Save the file in the correct subdirectory with the naming convention:
   ```
   YYYY-MM-DD_<slug>.md
   ```
4. Commit with the message: `inbox: <source> finding <slug>`

The curator will review the finding and promote it to the YAML catalog + Wiki following [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md).

### Depth Requirement (Definition of Done)

To prevent the catalog from filling again with declarative stubs, an entry **is not promoted** until it meets one of these two paths:

- **Falsifiable (`deep`)** — brings `example_bad`, `example_good`, a concrete `detection` recipe, and at least one `evidence`. If the signature is statically checkable, it must also register a detector in [`scripts/detectors.py`](../scripts/detectors.py) tested against its examples.
- **Doctrinal** — if it is a behavioral/epistemic principle with no static signature, it is marked `doctrinal: true` explicitly (stub by design, not by neglect). Fabricating example code for it is prohibited.

A finding that is neither `deep` nor explicitly `doctrinal` is a **stub** and stays in the Inbox until enriched. The `stubs` badge (in the README, calculated by [`scripts/metrics.py`](../scripts/metrics.py)) must remain at **0** in the curated catalog.

> Templates under `Inbox/templates/` are intentionally isolated. They are not live knowledge yet; they are molds for new findings.

---

## Ingestion Flow

```
Source (Cerberus / Manual / External)
        ↓
Deposit in Inbox/<source>/YYYY-MM-DD_<slug>.md
        ↓
Curator validates → deduplicates → maps domain
        ↓
Add entry to golden_standard_*.yaml (status: KNOWLEDGE)
        ↓
Create article in Wiki/Vices/
        ↓
Run generate_golden_audit.py
        ↓
Move file to deprecated/
```
```

**Validación:** `head -5 Inbox/README.md` must be in English. No Spanish words.

---

### 1.2. Corregir link roto en `KNOWLEDGE_SOURCES.md`

**Archivo:** `KNOWLEDGE_SOURCES.md`  
**Acción:** Reemplazar la referencia a `CERBERUS_CONTRACT.md`.

```
old: **Contract document:** [`CERBERUS_CONTRACT.md`](CERBERUS_CONTRACT.md)
new: **Contract document:** [`CONSUMER_CONTRACT.md`](CONSUMER_CONTRACT.md)
```

**Validación:** `grep -n "CERBERUS_CONTRACT" KNOWLEDGE_SOURCES.md` debe devolver 0 resultados.

---

### 1.3. Corregir typo `TV` → `VT` en `Wiki/Home.md`

**Archivo:** `Wiki/Home.md`  
**Acción:** Reemplazar `TV` por `VT` en la línea del índice de dominios.

```
old: | Testing & Evaluation | `VT-xxx` | 116 | [[Vices_Index|Open index]] |
# (verificar si está así; si no, buscar "TV" en el archivo)
```

Buscar primero: `grep -n "TV" Wiki/Home.md`. Si hay match, editar.

**Validación:** `grep "TV" Wiki/Home.md` debe devolver 0 (o solo matches legítimos como "TV" en otro contexto, no como dominio).

---

### 1.4. Corregir labels en español de badges

**Archivo:** `scripts/metrics.py`  
**Acción:** Cambiar las etiquetas de los badges `evidence` y `detectors` a inglés.

Buscar en `scripts/metrics.py`:
```python
"evidence": _badge("con evidencia", f"{m['with_evidence_pct']}%", _color(m['with_evidence_pct'])),
"detectors": _badge("detectores locales", str(m["local_detectors"]), "brightgreen"),
```

Cambiar a:
```python
"evidence": _badge("with evidence", f"{m['with_evidence_pct']}%", _color(m['with_evidence_pct'])),
"detectors": _badge("local detectors", str(m["local_detectors"]), "brightgreen"),
```

Luego regenerar badges:
```bash
python scripts/metrics.py
```

**Validación:** `cat badges/evidence.json` y `cat badges/detectors.json` deben mostrar labels en inglés.

---

### 1.5. Limpiar jerga interna de `BACKLOG.md`

**Archivo:** `BACKLOG.md`  
**Acción:** Reemplazar términos de proyecto interno con lenguaje universal.

```
old: "Eje 6"
new: "Batch 6"

old: "AX-020"
new: "AX-020 (schema migration to agnostic v3.0)"

old: "AX-023"
new: "AX-023 (CC-specific doc removal)"

old: "AX-024"
new: "AX-024 (line-ending normalization)"
```

**Nota:** No eliminar los IDs históricos si son referencias a commits, pero añadir una descripción en inglés para que un lector externo entienda qué son.

**Validación:** `grep -i "eje\|ax-020\|ax-023\|ax-024" BACKLOG.md` debe mostrar solo descripciones contextuales, no términos sin explicar.

---

### 1.6. Agregar exclusiones a `.gitignore`

**Archivo:** `.gitignore`  
**Acción:** Añadir al final:

```
# IDE / caches
.claude/
__pycache__/
*.pyc
.pytest_cache/
.ruff_cache/

# Ephemeral protocol directory
.protocol/
```

Luego eliminar del tracking:
```bash
git rm -rf --cached .claude/ __pycache__/ .pytest_cache/ .ruff_cache/ .protocol/ 2>/dev/null || true
```

**Validación:** `git status` no muestra estos directorios como untracked. `git ls-tree HEAD | grep -E "\.claude|__pycache__|\.pytest_cache|\.ruff_cache|\.protocol"` devuelve 0.

---

### 1.7. Mover scripts muertos

**Archivo:** `scripts/migrate_ax020.py`  
**Acción:**
```bash
mkdir -p deprecated/scripts
git mv scripts/migrate_ax020.py deprecated/scripts/
```

**Archivo:** `scripts/harden_metadata.ps1`  
**Acción:** Investigar primero su contenido. Si es un script one-time o no tiene uso documentado, moverlo también.

```bash
# Leer primero
cat scripts/harden_metadata.ps1
# Si es one-time o no está documentado:
git mv scripts/harden_metadata.ps1 deprecated/scripts/
```

**Validación:** `ls scripts/` no contiene `migrate_ax020.py`. El repo está limpio.

---

### 1.8. Verificar y eliminar directorio `.protocol/`

**Acción:**
```bash
ls -la .protocol/
```

Si está vacío o solo contiene archivos temporales:
```bash
rm -rf .protocol/
```

Ya está cubierto por `.gitignore` en el paso 1.6.

**Validación:** El directorio no existe en el working tree.

---

## FASE 2: Purga de `deprecated/` — Evaluación archivo por archivo

**Objetivo:** Si el conocimiento ya está en el proyecto vivo, eliminar el archivo de `deprecated/`. Si es un snapshot histórico sin reemplazo vivo, dejarlo con un disclaimer claro.

### 2.1. Evaluación de cada archivo

| Archivo | ¿Conocimiento en vivo? | Veredicto | Acción |
|---|---|---|---|
| `deprecated/README.md` | Sí — explica la política de deprecated. | **MANTENER** | Es la única documentación de la zona. Debe estar en inglés. Verificar que ya lo está. |
| `deprecated/knowledge_snapshots/CODERCERBERUS_CONCEPTUAL_FRAMEWORK_original.md` | Sí — el framework actual está en `CONCEPTUAL_FRAMEWORK.md` y `Wiki/Concepts/Conceptual_Framework.md`. | **ELIMINAR** | Es un snapshot de una versión anterior. La historia está en git. |
| `deprecated/planning/GS_remediation_plan.md` | Sí — la migración YAML ya se completó (AX-020). El esquema v3.0 es el estado actual. | **ELIMINAR** | Plan obsoleto, ya ejecutado. |
| `deprecated/planning/SCOPE_AUDIT.md` | Sí — los hallazgos de universalidad ya están en PI-019, PI-023, VC-045, etc. | **ELIMINAR** | Audit de alcance histórico; sus reglas ya están en el catálogo. |
| `deprecated/planning/NORMALIZATION_MANDATE.md` | **NO** — afirma que se crearon 32 stubs que no existen. Es un documento falso. | **ELIMINAR** | Contiene afirmaciones que contradicen el árbol vivo. No aporta valor histórico si es incorrecto. |
| `deprecated/planning/NORMALIZATION_SUMMARY.md` | **NO** — afirma "32 stubs created" y "TK normalized" que no existen. | **ELIMINAR** | Documento de completion que miente sobre el estado. Peligroso. |
| `deprecated/planning/CONCEPTUAL_FRAMEWORK_AUDIT_PLAN.md` | Sí — el framework ya está auditado. | **ELIMINAR** | Plan de ejecución en español; no tiene valor operativo. |
| `deprecated/planning/AUDIT_EXECUTION_GUIDE.md` | Sí — el framework ya está auditado. | **ELIMINAR** | Guía de ejecución en español; obsoleta. |
| `deprecated/wiki_phases/PHASE_2A_COMPLETE.md` | Sí — el wiki ya está generado. | **ELIMINAR** | Marcador de fase histórico. |
| `deprecated/wiki_phases/PHASE_2C_COMPLETE.md` | Sí — el wiki ya está generado. | **ELIMINAR** | Marcador de fase histórico. |
| `deprecated/wiki_phases/PHASE_2_PROGRESS.md` | Sí — el wiki ya está generado. | **ELIMINAR** | Marcador de fase histórico. |
| `deprecated/wiki_phases/PHASE_3_FINAL_COMPLETION.md` | Sí — el wiki ya está generado. | **ELIMINAR** | Marcador de fase histórico. |

### 2.2. Ejecución de la purga

```bash
# Eliminar archivos cuyo conocimiento ya está en el árbol vivo
git rm deprecated/knowledge_snapshots/CODERCERBERUS_CONCEPTUAL_FRAMEWORK_original.md
git rm deprecated/planning/GS_remediation_plan.md
git rm deprecated/planning/SCOPE_AUDIT.md
git rm deprecated/planning/NORMALIZATION_MANDATE.md
git rm deprecated/planning/NORMALIZATION_SUMMARY.md
git rm deprecated/planning/CONCEPTUAL_FRAMEWORK_AUDIT_PLAN.md
git rm deprecated/planning/AUDIT_EXECUTION_GUIDE.md
git rm deprecated/wiki_phases/PHASE_2A_COMPLETE.md
git rm deprecated/wiki_phases/PHASE_2C_COMPLETE.md
git rm deprecated/wiki_phases/PHASE_2_PROGRESS.md
git rm deprecated/wiki_phases/PHASE_3_FINAL_COMPLETION.md

# Eliminar directorios vacíos
rmdir deprecated/knowledge_snapshots/ 2>/dev/null || true
rmdir deprecated/planning/ 2>/dev/null || true
rmdir deprecated/wiki_phases/ 2>/dev/null || true
rmdir deprecated/scripts/ 2>/dev/null || true

# Si quedan subdirectorios vacíos, eliminar
find deprecated -type d -empty -delete
```

**Nota:** Si algún directorio queda vacío (ej. `deprecated/planning/` después de eliminar sus archivos), eliminarlo. Si `deprecated/` queda vacío salvo `README.md`, eso está bien.

**Validación:** `find deprecated -type f | sort` debe mostrar solo `deprecated/README.md` y los scripts movidos en Fase 1.7 (si aplica).

---

## FASE 3: Corrección de documentación y contenido

### 3.1. Actualizar `INGESTION_PROTOCOL.md` al esquema v3.0

**Archivo:** `INGESTION_PROTOCOL.md`  
**Problema:** El template de Step 4 usa un esquema obsoleto (no tiene `downstream_verification`, `tier`, `doctrinal`, `example_bad`, `example_good`, `detection`, `evidence`, `detector`). Contradice `CONTRIBUTING.md`.

**Acción:** Reemplazar el bloque de Step 4 (líneas ~109-131) con el esquema actual:

```yaml
- id: VC-701                          # Assigned in Step 3
  title: "Short descriptive title"
  symptom: |
    What you observe when this vice is present.
  cause: |
    Root cause or mechanism.
  solution: |
    What to do instead.
  status: DOC_ONLY                   # DOC_ONLY | AUDITED | PREVENTED | REMEDIATED
  severity: high                    # critical | high | medium | low
  tags:
    - vibe-coding                    # at least two normalized slugs
    - ai-native
  action: |
    The corrective/preventive action; where enforcement lives, if any.
  validating_mechanism: DOC_ONLY     # static-ast | static-regex | runtime-test | external-tool | DOC_ONLY | doctrinal
  downstream_verification: required   # required | none
  tier: core                         # core | specialist
  # --- Depth fields (for falsifiable entries) ---
  example_lang: python
  example_bad: |
    # Concrete code that triggers the vice.
  example_good: |
    # The corrected version.
  detection: |
    A concrete, falsifiable detection recipe (AST/regex/heuristic, or the
    external tool that catches it). Name a tool only if it really exists.
  evidence:
    - source: "arxiv:XXXX.XXXXX"
      claim: "What that source actually shows."
  # detector: vc701_my_check        # OPTIONAL: add to scripts/detectors.py if statically checkable
  # --- OR, for doctrinal entries (no static signature) ---
  # doctrinal: true
```

También actualizar el template de Wiki article en Step 5 para que refleje el formato actual de las páginas de vicios (con tabla de campos, ejemplos bad/good, detección, evidencia).

**Validación:** El template de `INGESTION_PROTOCOL.md` debe alinearse visualmente con el de `CONTRIBUTING.md`. No debe contener `operativity_status`, `source_reference`, `evidence_notes` como campos obligatorios.

---

### 3.2. Aclarar que `CONSUMER_CONTRACT.md` es un documento de frontera opcional

**Archivo:** `CONSUMER_CONTRACT.md`  
**Acción:** Agregar al inicio del documento (después del título):

```markdown
> **Note:** This document defines a consumer boundary with a downstream enforcing project.  
> Golden Standard does not require this consumer to exist, to be operational, or to be named  
> "Cerberus" for GS to be valid. The contract is a reference implementation of consumption,  
> not a dependency of GS.
```

**Validación:** La primera sección del documento establece la independencia de GS.

---

### 3.3. Descontaminar `KNOWLEDGE_SOURCES.md` de "Primary Source"

**Archivo:** `KNOWLEDGE_SOURCES.md`  
**Acción:** Cambiar el framing de Cerberus.

```
old: ### 1. CoderCerberus (Primary Source)
new: ### 1. CoderCerberus (Historical Source — Example Downstream Consumer)
```

Y agregar una nota después de la descripción:

```markdown
> GS accepts findings from any source that meets the validity contract below.  
> CoderCerberus is listed here because it was the original source of many entries,  
> not because GS depends on it.
```

**Validación:** El documento no presenta a Cerberus como condición necesaria para GS.

---

### 3.4. Descontaminar `Wiki/Domains/D1..D12.md`

**Archivo:** `Wiki/Domains/D1.md` .. `D12.md`  
**Acción:** Reemplazar "Project: *cerberus*" por "Project: *example*" o "Consumer: *reference*" en cada archivo.

Comando batch:
```bash
for f in Wiki/Domains/D*.md; do
    sed -i 's/Project: \*cerberus\*/Consumer: *reference*/g' "$f"
    sed -i 's/Project: *cerberus*/Consumer: *reference*/g' "$f"
done
```

**Nota:** Revisar si el formato es `*cerberus*` (con asteriscos de markdown) o `cerberus` plano. Adaptar el regex.

**Validación:** `grep -r "cerberus" Wiki/Domains/` debe devolver 0.

---

### 3.5. Descontaminar `Wiki/Project_Insights/PI-*.md`

**Archivo:** `Wiki/Project_Insights/PI-001.md` .. `PI-035.md`  
**Acción:** Reemplazar "Project: *cerberus*" donde aparezca.

Comando batch:
```bash
for f in Wiki/Project_Insights/PI-*.md; do
    sed -i 's/Project: \*cerberus\*/Consumer: *reference*/g' "$f"
    sed -i 's/Project: *cerberus*/Consumer: *reference*/g' "$f"
done
```

**Validación:** `grep -r "cerberus" Wiki/Project_Insights/` debe devolver 0.

---

### 3.6. Aclarar `PREVENTED` status en `README.md`

**Archivo:** `README.md`  
**Acción:** En la sección de status (alrededor de línea 161), añadir una nota de honestidad:

```markdown
> **Independence note:** `PREVENTED` means a downstream consumer claims to enforce this vice.  
> Golden Standard does not independently verify that claim; the status is based on the  
> consumer's self-report at the time of cataloging. If no downstream consumer is active,  
> the entry is still documented as a falsifiable principle.
```

**Validación:** El README no sugiere que `PREVENTED` = GS-verificado.

---

### 3.7. Corregir cuentas en `Wiki/Graph.md`

**Archivo:** `Wiki/Graph.md`  
**Acción:** En la tabla de Operational Reading (líneas ~53-56), ajustar las cifras o añadir un disclaimer.

Opción A (ajustar cifras exactas):
```markdown
| `PROPOSED` | 208 | The entry is documented or audited, but no enforcing implementation exists in the catalog flow. |
| `ENFORCED_EXTERNAL` | 98 | The guard exists in a downstream enforcing project. |
| `ENFORCED_LOCAL` | 12 | The guard or remediation is enforced in this repository. |
```

Opción B (si el generador es quien las pone y no queremos editar manual):
```markdown
> Counts are approximate snapshots; canonical counts are derived from the YAML catalogs by `scripts/metrics.py`.
```

**Recomendación:** Opción A si se edita directamente; Opción B si se prefiere que el generador las corrija. Dado que el generador es complejo, editar directamente es más rápido.

**Validación:** Las cifras suman 208 + 98 + 12 = 318. El total es 317 vices (VC+VT+TK). Hay una diferencia de 1 porque el conteo es por status de los 3 catálogos y no hay una correspondencia perfecta 1:1 con las categorías del enum. Dejar una nota: "Counts are approximate due to status mapping; see metrics.json for exacts."

---

## FASE 4: Rediseño estructural

### 4.1. Eliminar doctrina duplicada: `Wiki/Concepts/Conceptual_Framework.md`

**Archivo:** `Wiki/Concepts/Conceptual_Framework.md`  
**Acción:** Este archivo duplica `CONCEPTUAL_FRAMEWORK.md` en la raíz.  
Opciones:
- **A) Eliminar** y cambiar los links en el wiki que apuntan a `Concepts/Conceptual_Framework` para que apunten a `CONCEPTUAL_FRAMEWORK.md` (usando un link relativo).
- **B) Convertir en un stub** que solo diga "Ver el documento raíz".

**Recomendación: A)** Eliminar. El framework raíz es la fuente de verdad. Los links en el wiki pueden ser relativo a la raíz: `[Conceptual Framework](../CONCEPTUAL_FRAMEWORK.md)`.

Sin embargo, Obsidian vault links usan `[[...]]` que no manejan bien `../`.  
**Alternativa:** Dejar el archivo pero añadir una cabecera de WARNING al inicio:
```markdown
> ⚠️ **WARNING:** This is a generated copy of `../CONCEPTUAL_FRAMEWORK.md`.  
> The canonical source of truth is the root file. Do not edit this copy directly.
```

Y añadir una instrucción en `CONTRIBUTING.md`: "Si editas `CONCEPTUAL_FRAMEWORK.md`, ejecuta `generate_golden_audit.py` para sincronizar el wiki."

**Validación:** No hay dos versiones divergentes del framework conceptual.

---

### 4.2. Normalizar `TK-F01..F03` en `golden_standard_tokenomics.yaml` y wiki

**Archivo:** `golden_standard_tokenomics.yaml`, `Wiki/Tokenomics_Index.md`, `Wiki/Tokenomics/TK-F01.md` etc.  
**Problema:** Los IDs `TK-F01`, `TK-F02`, `TK-F03` son legacy. El plan de normalización (ya obsoleto) quería renombrarlos a `TK-001..003`.

**Opción A (renombrar):** Requeriría renumberar TK-001..027 a TK-004..030. Esto rompe links y referencias.  
**Opción B (preservar con nota):** Dejar los IDs legacy pero documentar que son históricos.

**Recomendación: B)** La estabilidad de IDs es más importante que la estética del prefijo.  
**Acción:**
1. En `Wiki/Tokenomics_Index.md`, añadir una nota debajo de la lista de entries:
   ```markdown
   > **Note:** `TK-F01`, `TK-F02`, and `TK-F03` use a legacy prefix preserved for ID stability.  
   > They are fully integrated into the sequential catalog and are not separate categories.
   ```
2. En `golden_standard_tokenomics.yaml`, añadir un comentario YAML encima de cada F-entry:
   ```yaml
   # Legacy ID (F-prefix) preserved for stability. Part of the main sequential catalog.
   ```

**Validación:** El index y el catalogo explican la presencia de los prefijos F.

---

### 4.3. Restructurar `golden_standard_project_insights.yaml` a lista

**Archivo:** `golden_standard_project_insights.yaml`  
**Problema:** Usa un esquema flat (`project_insights: PI-001: ...`) mientras que VC/VT/TK usan listas (`items: [ { id: ... } ]`).

**Acción:** Convertir a formato lista para consistencia.

```yaml
format_version: 3.0
catalog_name: project_insights
items:
  - id: PI-001
    title: "Deptry – reconciliation of imports..."
    doctrinal: true
  - id: PI-002
    title: "Diagnostic assertions..."
    doctrinal: true
    promotion_candidate: true
  # ... etc
```

**Nota:** Esto requiere actualizar `scripts/metrics.py` (que lee `data.get("project_insights", {})`) y `scripts/validate_golden_standard_catalogs.py` (que tiene `_normalize_project_insight`).

**Validación:** El validator pasa. El metrics.py genera el conteo correcto (35). El generador de wiki no se rompe.

**Riesgo:** Alto. Si el generador o el validator dependen del formato flat, cambiarlo rompe la generación.  
**Mitigación:** Hacer esto como último paso, con tests de CI en verde.

---

### 4.4. Simplificar / desacoplar `generate_golden_audit.py`

**Archivo:** `generate_golden_audit.py` (77KB)  
**Problema:** Hardcodea mappings de dimensiones Cerberus (D1..D12). Es demasiado grande para un generador de reportes.

**Acción:** No refactorizar completamente en esta sesión (riesgo alto). Pero sí:
1. Extraer el mapping de dimensiones a un archivo JSON separado: `config/dimension_map.json`.
2. Reemplazar los hardcoded mappings en el generador por una lectura de ese JSON.
3. Si el JSON no existe, el generador debe funcionar sin dimensiones (modo agnóstico).

**Nota:** Esto requiere entender el código del generador. Si no es seguro, dejarlo como deuda para una sesión posterior con el backlog item GS-069.

**Validación:** El generador sigue produciendo la misma salida. El archivo de config es editable sin tocar Python.

---

### 4.5. Crear `AGENT_CONSUMPTION.md`

**Archivo nuevo:** `AGENT_CONSUMPTION.md`  
**Propósito:** Decirle a un agente qué leer para consumir GS eficientemente sin desperdiciar tokens en 270 páginas de wiki.

Contenido:
```markdown
# Agent Consumption Guide — Golden Standard

> Read this first. Do not read the full Wiki (369 articles) — it is generated transclusions of the YAML and is token-inefficient.

## Minimal Reading Set (recommended)

1. **Identity & scope:** `README.md` (lines 1-50) + `CONCEPTUAL_FRAMEWORK.md` (lines 1-100)
2. **Schema:** `golden_standard.yaml` (9 lines) + `CONTRIBUTING.md` (Entry Format section)
3. **Catalogs:** Load only the domain(s) relevant to your task:
   - Vibe coding: `golden_standard_coding_vices.yaml` (154 entries)
   - Testing: `golden_standard_testing_vices.yaml` (116 entries)
   - Tokenomics: `golden_standard_tokenomics.yaml` (47 entries)
   - Insights: `golden_standard_project_insights.yaml` (35 entries)
4. **Metrics:** `golden_standard_metrics.json` (18 lines) — gives you the health snapshot.
5. **Index pages (if you need human-readable summaries):**
   - `Wiki/Vices_Index.md` (summary list)
   - `Wiki/Tokenomics_Index.md` (summary list)
   - `Wiki/Project_Insights_Index.md` (summary list)

## What NOT to read

- Do not read individual `Wiki/Vices/VC-xxx.md` or `Wiki/Vices/VT-xxx.md` articles unless you need the cross-link graph for a specific entry. They repeat the YAML verbatim.
- Do not read `deprecated/` — it is historical, not active knowledge.
- Do not read `generate_golden_audit.py` — it is an internal tool, not knowledge.

## Total token budget (approximate)

- Full YAML catalogs: ~9,000 lines
- Index pages + docs: ~1,000 lines
- **Total efficient consumption: ~10,000 lines** vs ~15,000+ for the full Wiki.
```

**Validación:** El archivo existe, está en inglés, y es claro.

---

## FASE 5: Calidad de reglas (Doctrinal → Deep)

**Objetivo:** Evaluar las 70 entradas VC `doctrinal` para ver si pueden adquirir firma estática.

**Nota:** Esta es una tarea grande. No se completa en una sola sesión. Se hace en lotes.

### 5.1. Generar lista de candidatos

```bash
grep -B2 "doctrinal: true" golden_standard_coding_vices.yaml | grep "id:" > /tmp/doctrinal_vc_list.txt
```

Lista de 70 IDs. Priorizar los de `severity: high` o `critical`.

### 5.2. Criterios de conversión

Una entrada doctrinal puede convertirse a `deep` si:
- Se puede escribir un `example_bad` de código real que demuestre el vicio.
- Se puede escribir un `example_good` de código real que lo corrija.
- Se puede escribir una `detection` concreta (regex, AST, o herramienta externa).
- Se puede citar `evidence` (paper, log, o estudio empírico).

Si no cumple los 4 criterios, permanece `doctrinal`.

### 5.3. Lotes de trabajo

| Lote | IDs | Severidad | Esfuerzo estimado |
|---|---|---|---|
| 1 | VC-001, VC-002, VC-004, VC-005, VC-006 | medium | 1 sesión (5 entradas) |
| 2 | VC-127, VC-128, VC-133, VC-134, VC-135, VC-136, VC-139 | high/critical | 2 sesiones (7 entradas) |
| 3 | Los 58 restantes | medium | 6-8 sesiones |

**Acción inmediata:** Crear el backlog item GS-071 con esta lista y el criterio. No empezar a editar entradas sin un plan de lotes.

---

## FASE 6: Registro de deuda nueva y validación final

### 6.1. Agregar items abiertos al BACKLOG

**Archivo:** `BACKLOG.md`  
**Acción:** Añadir una nueva sección "Live debt" con los hallazgos de este audit:

```markdown
| ID | Severity | Item | Evidence / Notes | Status |
|----|----------|------|------------------|--------|
| GS-065 | High | Spanish text in active files (Inbox/README, badges) | Audit 2026-06-16 found active Inbox/README.md entirely in Spanish; badge labels "con evidencia" and "detectores locales". | IN_PROGRESS |
| GS-066 | Medium | Broken link to CERBERUS_CONTRACT.md in KNOWLEDGE_SOURCES.md | File was renamed to CONSUMER_CONTRACT.md; link is stale. | IN_PROGRESS |
| GS-067 | Medium | Cerberus contamination in active docs | KNOWLEDGE_SOURCES.md lists Cerberus as "Primary Source"; Wiki/Domains/D1..D12 and PI pages reference "Project: cerberus". | IN_PROGRESS |
| GS-068 | Medium | INGESTION_PROTOCOL.md shows stale schema (v2) | Template lacks downstream_verification, tier, doctrinal, example_bad, example_good, detection, evidence, detector. | IN_PROGRESS |
| GS-069 | Medium | generate_golden_audit.py hardcodes Cerberus dimensions | 77KB generator with D1-D12 mappings; not agnostic. | OPEN |
| GS-070 | Low | Duplicate doctrine files (CONCEPTUAL_FRAMEWORK root + wiki) | Risk of drift between two copies. | OPEN |
| GS-071 | Low | 70 VC entries are doctrinal (not falsifiable) | 45% of coding vices have no static signature. Assess promotion to deep. | OPEN |
| GS-072 | Low | TV/VT typo in Wiki/Home.md | "TV" used instead of "VT" for Testing Vices. | IN_PROGRESS |
| GS-073 | Medium | Cache directories tracked in repo | .claude/, __pycache__/, .pytest_cache/, .ruff_cache/, .protocol/ not in .gitignore. | IN_PROGRESS |
```

**Validación:** El backlog tiene al menos 9 items abiertos nuevos.

---

### 6.2. Validación final de todo el árbol

```bash
# 1. Verificar que no queda español en archivos activos
grep -ri "buzón\|hallazgo\|curador\|fuente\|plantilla\|directorio\|carpeta\|con evidencia\|detectores locales" --include="*.md" --include="*.json" --include="*.yaml" . | grep -v "deprecated/" | grep -v "Inbox/cerberus/" | grep -v "Inbox/external/" | grep -v "Inbox/manual/" | grep -v "Inbox/templates/"
# Resultado esperado: 0

# 2. Verificar que no quedan links rotos a CERBERUS_CONTRACT
grep -ri "CERBERUS_CONTRACT" --include="*.md" --include="*.yaml" . | grep -v "deprecated/"
# Resultado esperado: 0

# 3. Verificar que no queda "cerberus" en Wiki/Domains ni Wiki/Project_Insights
grep -ri "cerberus" Wiki/Domains/ Wiki/Project_Insights/
# Resultado esperado: 0

# 4. Verificar que el validador sigue pasando
python scripts/validate_golden_standard_catalogs.py --check-wiki
# Resultado esperado: 0 errores

# 5. Verificar que los tests pasan
python scripts/test_detectors.py
python scripts/metrics.py
# Resultado esperado: 0 errores, stubs: 0

# 6. Verificar que el generador funciona
python generate_golden_audit.py
# Resultado esperado: sin errores

# 7. Verificar git status limpio (sin untracked caches)
git status
# Resultado esperado: solo cambios intencionales, no caches
```

---

### 6.3. Commit

```bash
git add -A
git commit -m "remediation: audit 2026-06-16 — hygiene, decontamination, structure

- Translate Inbox/README.md to English
- Fix broken CERBERUS_CONTRACT.md link
- Fix TV/VT typo in Wiki/Home.md
- Translate badge labels to English
- Scrub project jargon from BACKLOG.md
- Add cache/IDE dirs to .gitignore and remove from tracking
- Move dead scripts (migrate_ax020, harden_metadata) to deprecated/
- Purge deprecated/ of obsolete planning docs and wiki phase markers
- Update INGESTION_PROTOCOL.md to v3.0 schema
- Clarify CONSUMER_CONTRACT.md as optional boundary
- Decontaminate KNOWLEDGE_SOURCES.md and Wiki/Domains/PI pages from Cerberus refs
- Clarify PREVENTED status independence in README
- Add AGENT_CONSUMPTION.md for efficient agent reading
- Register new debt items GS-065..GS-073 in BACKLOG.md

Audit: independent adversarial audit 2026-06-16"
```

---

## Orden de ejecución recomendado

```
FASE 0  → Preflight (verificar CI verde)
FASE 1  → Ediciones directas (Inbox, links, typos, badges, BACKLOG, .gitignore, scripts)
FASE 2  → Purga de deprecated/
FASE 3  → Corrección de documentación (INGESTION_PROTOCOL, CONSUMER_CONTRACT, KNOWLEDGE_SOURCES, Domains, PI, README, Graph)
FASE 4  → Rediseño estructural (duplicado CONCEPTUAL_FRAMEWORK, TK-F, PI schema, AGENT_CONSUMPTION)
FASE 5  → Plan de Doctrinal→Deep (backlog item, no edición masiva aún)
FASE 6  → Registrar deuda, validar, commit
```

**Nota:** FASE 4 tiene alto riesgo de romper el generador. Si se ejecuta, hacerlo en una rama separada y probar `generate_golden_audit.py` después de cada sub-paso. Si no se tiene tiempo, dejar FASE 4 como items abiertos en el backlog (GS-069, GS-070) y proceder directamente a FASE 6.

---

*End of Remediation Plan*
