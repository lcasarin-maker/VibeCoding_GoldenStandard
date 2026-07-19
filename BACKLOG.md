# Backlog — VibeCoding_GoldenStandard

**Fuente de verdad:** `/srv/ai/VibeCoding_GoldenStandard` (ATOM + clon local sincronizado)  
**Última actualización:** 2026-07-19  
**Coordinador:** PLAN_REMEDIACION_2026-07-19.md (maestro 3 fases)  
**Arquitectura de referencia:** REVISION_ARQUITECTONICA_Y_BACKLOG_V2.md §1 (G1-G5)

---

## SECCIÓN 1: CRÍTICO INDISPENSABLE (Auditoría Anti-Pragmatismo 2026-07-19)

Hallazgos de esta auditoría que bloquean otras tareas. Ejecutar en orden de PLAN_REMEDIACION.

### GS-14 · Compilador Wiki clobberea notas manuales
- **Prioridad:** P2 (acelerador, bloquea iteración manual)
- **Defecto:** `scripts/generate_golden_audit.py --wiki-only` borra `Wiki/Falsifiability_Report.md` y sobreescribe footer manual de `Home.md`
- **Contexto:** Tests ya sandboxeados (GS_GENERATOR_ROOT); pero corrida directa del compilador sigue siendo destructiva
- **Fix canónico:**
  1. Crear roster explícito de notas manuales (ej. `Wiki/.manual_notes` con lista de archivos/secciones)
  2. Compilador: preservar entradas en el roster
  3. Test: verificar que notas manuales sobreviven compilación
- **Decisión requerida:** Listar con Luis cuáles son notas manuales (mínimo: Home.md footer, Falsifiability_Report.md, entries manuales)
- **Criterio de cierre:** Roster explícito, compilador preserva, test de sobrevivencia pasa

### GS-15 · semgrep roto en Windows (7 tests FAILED pre-existentes)
- **Prioridad:** P2 (tooling de gates, bloquea validación en Windows)
- **Síntoma:** `tests/test_semgrep_rules.py`: semgrep 1.164.0 (`C:\Users\luiscasarin\.local\bin\semgrep.exe`) falla `--validate` con crash de semgrep-core
- **Contexto:** ATOM no tiene semgrep instalado (tests se saltan); cobertura cero en Linux
- **Investigación:**
  1. Instalar semgrep en ATOM (`pip install semgrep --break-system-packages`)
  2. Validar 17 reglas en Linux con `semgrep --validate --config config/semgrep_vices.yaml`
  3. Si validan en Linux pero fallan en Windows → problema Windows-específico (pinear versión o documentar plataforma)
  4. Si no validan → corregir reglas (bisección: validar regla por regla con `--config` parcial)
- **Criterio de cierre:** 17 reglas validan en Linux, tests pasan (skip en Windows OK si es plataforma no soportada)

### GS-16 · Notas Wiki en minúsculas duplicadas
- **Prioridad:** P3 (mecánico, bajo riesgo)
- **Hallazgo:** Existen `vc-002.md` … (37 archivos lowercase) junto a `VC-002.md` (canonical)
- **Decisión:** ¿Son duplicados a borrar o variantes de propósito?
- **Fix:** 
  1. Auditar 37 pares (diff quick)
  2. Unificar a canonical (uppercase)
  3. Re-lint con `lint_wiki.py` (debe quedar 0 rotos, 0 huérfanos)
- **Criterio de cierre:** Wiki lint-clean, sin duplicados lowercase

---

## CRÍTICO INDISPENSABLE (Hallazgos ya corregidos, sesión actual)

✅ **Commit `c9f5d45` pusheado:**
- GS-13 operaba sobre CERO items (loaders leían llaves incorrectas) → reescrito, 16 tests verdes, 320+ items reales
- Linter SP con tragado de excepciones y "skip for now" → AST real, detección de ciclos DFS
- SP-AQ-001 no detectaba primer argumento → patrón corregido
- Tests mutaban repo vivo → sandboxeados con GS_GENERATOR_ROOT
- VC-073 gate bloqueo perpetuo → verifica sincronización real
- `lint_wiki.py` landed (GS-11 huérfano) → Wiki 0 rotos, 0 huérfanas
- Windows cp1252 → UTF-8 forzado en `gs_query/__main__.py`
- **Suite:** 73 passed; 7 FAILED = semgrep pre-existente (GS-15)

---

## SECCIÓN 2: Arquitectura de Referencia (2026-07-12 — contexto a largo plazo)

Inversiones de diseño. Estos son ajustes estructurales que enmarcan el backlog.

### Uso deseable vs realidad hoy
**Uso real:** (a) agentes consultan reglas MIENTRAS codifican; (b) gates ejecutan reglas; (c) humanos exploran doctrina.
**Hoy:** YAMLs de cientos de KB, wiki generada, 7 reglas ejecutables. Consulta = grep; enforcement = excepción; prosa = regla. Problema: la regla nace como PROSA y el test se intenta añadir después — 85% nunca tuvo dientes.

### Ajustes estructurales (G1-G5)
- **G1:** Rule-as-code first (inversión pipeline): toda entrada NACE como regla ejecutable + fixtures; prosa se GENERA desde regla
- **G2:** GS como servicio de consulta (MCP): gs-query CLI/servidor (queries relevancia por dominio/severidad/keyword, <1KB response)
- **G3:** Taxonomía de falseabilidad (cinco clases): estático (Semgrep/AST), dinámico (pytest), procesal (hook flujo), juicio (LLM-judge), doctrina (no falseable)
- **G3b:** Funciones de la prosa (inyección dirigida reduce intentos; exposición de motivos cuando regla dispara; cobertura vicios de juicio; cantera de reglas futuras)
- **G4:** Corpus de regresión incidentes (vicios "prevenidos" que no atrapan su propio incidente histórico se degradan solos)
- **G5:** Gobernanza de supresiones (excepción inline con justificación + registro central + revisión periódica obligatoria)

---

## SECCIÓN 3: Backlogs Operacionales Ordenados (2026-07-19)

### Fase 1: Desbloqueo (PLAN_REMEDIACION fase 1)
*(No hay GS items en fase 1)*

### Fase 2: Implementación P2
**GS-14, GS-15** (ver SECCIÓN 1)

### Fase 3: Implementación P3
**GS-16** (ver SECCIÓN 1)

### Backlogs heredados (2026-07-19 — integrar en orden)
**De 07_BACKLOGS_REMEDIACION.md:**

| ID | Tarea | Prio | Est. | Dependencias |
|---|---|---|---|---|
| GS-10 | Release congelado V3.2 (tag SemVer) base federación | ALTA | — | fase 1 OK |
| GS-11 | Regla/excepción SP para ledger único Aequitas | MEDIA | — | AQ-adopción GS |
| GS-12 | Verificar vigencia CONCEPTUAL_FRAMEWORK | BAJA | — | — |
| GS-AUD-001r | Lote +5 reglas Semgrep | P1 (fue) | — | G1 pipeline |
| GS-TAX-001 | Falseabilidad: dictamen 363 entradas → 5 clases | P1 | — | G3 taxonomy |
| GS-MCP-001 | gs-query CLI + servidor MCP | P2 | — | G2 design |
| GS-RAC-001 | Pipeline rule-first para nuevas entradas | P2 | — | G1 inversión |
| GS-SUPP-001 | Mecanismo supresión justificada + registro | P2 | — | G5 governance |
| GS-CONTRACT-001 | Test contrato con consumidor fixture (CC) | P2 | — | ECO-001 |

---

## SECCIÓN 4: Criterios de Cierre Global

| Aspecto | Estado | Criterio |
|---|---|---|
| **Árbol limpio** | ✅ | Commit `c9f5d45` pusheado |
| **ATOM sincronizada** | ✅ | Pull post-push confirmado |
| **Suite** | 73p, 7f | 7 FAILED = GS-15 (semgrep pre-existente, OK) |
| **Hallazgos graves** | ✅ 11 | Sintaxis, GS-13 loaders, linter AST, patterns, tests, sandbox, gate VC-073, lint_wiki, UTF-8, S27 |
| **Catalogs** | ✅ 320+ items | VC 94+, TV 116+, PR 122 |

---

## SECCIÓN 5: Referencias

- **Plan maestro:** D:\AI\PLAN_REMEDIACION_2026-07-19.md
- **Arquitectura:** VibeCoding_GoldenStandard/golden_standard_principles.yaml (PR-122 + catálogos)
- **Backlogs integrales:** D:\AI\AUDITORIA_INTEGRAL_2026-07-18/07_BACKLOGS_REMEDIACION.md §7.2
- **Informe auditoría:** D:\AI\AUDITORIA_INTEGRAL_2026-07-18/10_AUDITORIA_ANTIPRAGMATISMO_2026-07-19.md
