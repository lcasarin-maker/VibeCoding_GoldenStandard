# AUDITORÍA ADVERSARIAL — VibeCoding_GoldenStandard
**Fecha:** 2026-07-10 | **Auditor:** Claude (Cowork) | **Método:** lectura de código + ejecución empírica de scripts/tests en sandbox Linux (Python 3.10)

---

## 1. Intención declarada
Base de conocimiento viva, agnóstica de agente y proyecto: 242 vicios + 121 principios + 34 tokenomics + 18 dominios, con regla de operatividad (`DOC_ONLY → PREVENTED → REMEDIATED`), grafo de conocimiento y pipeline de auditoría generada.

## 2. Estructura y arquitectura (lo que sí funciona)
- Separación limpia catálogo YAML → Wiki generada → grafo → badges; CI valida conteos.
- Protocolo de ingesta (Inbox/), plantillas, frontera GS↔CC documentada y mayormente respetada.
- `audit.py` 8/8 SP checks en verde y `validate_golden_standard_catalogs.py` pasa (verificado en vivo).
- Es el más sano de los tres repos: árbol git limpio, backlog real vacío.

## 3. Hallazgos (deuda registrada)

### GS-AUD-001 — Brecha de enforcement: estado legacy review transitorio [ALTA]
La auditoría original encontró 95 entradas `legacy review`, que mezclaban cobertura pendiente con conocimiento no automatizable. Esa ambigüedad era deuda: una entrada solo puede permanecer como enforcement probado (`PREVENTED`) o como doctrina explícita (`DOC_ONLY`).
**Corrección:** 2 entradas subieron a `PREVENTED` con detectores probados y 194 bajaron a `DOC_ONLY` con criterio de promoción falsable; el lint falla si reaparece cualquier `legacy review`.

### GS-AUD-002 — Dependencia dura de Python 3.13 por estilo, no por necesidad [ALTA]
Verificado empíricamente: `pytest` no puede ni COLECCIONAR en 3.10 (`SyntaxError: f-string expression part cannot include a backslash` en `generate_golden_audit.py`). El repo que cataloga VC-109 (hardcoded path) y VC-038 (optimistic config) fija un piso 3.13 por backslashes en f-strings — cosmético y trivialmente eliminable. Un consumidor en 3.10/3.11 no puede validar nada.
**Corrección:** extraer los backslashes a variables; bajar `requires-python` a >=3.10; CI matrix 3.10–3.13.

### GS-AUD-003 — `generate_golden_audit.py` es un monolito de 2,897 líneas [MEDIA]
El generador central concentra audit+wiki+grafo+badges+receipts. Cerberus impone S6/S8 (archivos chicos, Debt Tax) a todos, pero el proveedor de doctrina no se lo aplica. Ya existe ratchet SRP en CC; GS no tiene ninguno.
**Corrección:** partir en paquete `gs_generator/` (audit, wiki, graph, badges) con el mismo ratchet SRP de CC.

### GS-AUD-004 — STATE.md desincronizado de la realidad [MEDIA]
STATE.md (2026-07-02) afirma "10 items en tasks/backlog"; el folder está vacío (solo `.gitkeep`). El propio archivo advierte "no confíes en este resumen" — eso es admitir el vicio (VC-012 deuda invisible / VC-013 handoff ambiguo) en lugar de prevenirlo.
**Corrección:** generar la sección backlog de STATE.md desde `tasks/backlog/` vía script (ya existe `check_backlog_sync.py` — extenderlo para reescribir, no solo verificar).

### GS-AUD-005 — Teatro de evidencia [MEDIA]
Badge "with_evidence 99%", pero varias páginas de `Wiki/Evidence/` son placeholders genéricos ("cited generically per GSCC boundary see..."), producto del scrub GS-088. La métrica cuenta existencia de campo, no calidad de evidencia. Es exactamente VT-006 (test sin assert) aplicado a evidencia.
**Corrección:** clasificar evidencia en `primary | internal-generic | pending` y que el badge reporte solo primary.

### GS-AUD-006 — Colisiones y basura en Wiki/Detectors [BAJA]
`vc005_*` ×2, `vc061_*` ×2, `vc087_*` ×2 con contenidos distintos bajo el mismo ID, más `vc078_placeholder.md`. Naming no canónico en el único directorio que mapea vicio→detector.
**Corrección:** un archivo por ID (`vcNNN.md`), lint en `gs_lint.py`.

### GS-AUD-007 — Higiene menor [BAJA]
`.pyc` de 3 versiones de Python regados en `scripts/__pycache__` y `tests/__pycache__` (untracked pero ruido); `version = "0.0.0"` en pyproject.
**Corrección:** limpieza + `py.typed`/versión derivada de `golden_standard.yaml.format_version`.

## 4. Gap intención↔implementación (síntesis)
GS se vende como "prevención"; operativamente es un catálogo documental con un 14% de dientes. Su mayor riesgo no es lo que le falta sino la falsa sensación de cobertura que sus badges proyectan (100% deep, 99% evidence) — métricas de forma, no de fuerza.

## 5. Adopciones recomendadas (de repositorios_clasificados.md)
- **github/spec-kit** — formalizar la ruta Inbox→catálogo como spec-driven; plantillas de spec por entrada.
- **jorisnls/vibevetted (Semgrep)** — motor real para convertir vicios legacy review to PREVENTED sin escribir 200 detectores a mano: expresar VC/VT como reglas Semgrep donde aplique (VC-095, VC-115, VT-040 son triviales en Semgrep).
- **future-agi/agent-learning-kit** — ya adoptado en CC (`agent_learning_kit_evals.py`); portar rúbricas para evaluar la *efectividad* de detectores (falsos negativos), no solo su existencia.
- **MinishLab/semble / zeroentropy probe** — contexto exacto de código para detectores AST más precisos (ya hay evidencia previa de evaluación zilliztech).

---
*Registrado como deuda histórica GS-AUD-001…007. El cierre de ejecución y su evidencia están en la sección 6; no quedan items abiertos en `tasks/backlog/`.*

## 6. Cierre FASE 2 GS — evidencia 2026-07-10

- **GS-AUD-001:** cerrado sin `legacy review` residual. VC-027, VT-037 y VC-090 tienen detectores locales probados; las otras 194 entradas que eran `legacy review` se marcaron `DOC_ONLY` con justificación y trigger de promoción. Se retiraron 89 referencias aspiracionales a `tool:ruff`/`tool:pytest`; `scripts/gs_lint.py` falla si reaparece la categoría.
- **GS-AUD-002:** cerrado; la CLI colecciona en los runtimes disponibles 3.11/3.13 y CI declara matriz 3.10–3.13.
- **GS-AUD-003:** el monolito fue eliminado y reemplazado por `gs_generator/` con superficies `audit`, `wiki`, `graph` y `badges`, más un entrypoint delgado que conserva `--audit-only`, `--wiki-only` y receipts. La comparación de generación se ejecuta como contrato de no-regresión.
- **GS-AUD-004:** cerrado; `STATE.md` se regenera desde `tasks/backlog/`, con prueba de aparición y desaparición de un item ficticio.
- **GS-AUD-005:** evidencia se clasifica determinísticamente como `primary`, `internal-generic` o `pending`; `metrics.py` y badges cuentan solo evidencia `primary`.
- **GS-AUD-006:** `Wiki/Detectors` se regenera con un archivo canónico por ID y `gs_lint.py` rechaza archivos inesperados, faltantes o duplicados.
- **GS-AUD-007:** cerrado; `__pycache__` multi-versión fue eliminado y la higiene quedó verificada en el cierre.
- **Paridad:** dos ejecuciones consecutivas generaron 484 artefactos byte-idénticos; evidencia en `audit/sessions/2026-07-10-gs-phase2-parity.log`.
- **Semgrep:** siete reglas versionadas tienen fixture positivo y negativo: VC-095/VC-036, VC-115/VC-049, VC-109/VC-043, VT-040, VT-043, VT-005 y VT-009. `VT-043` pasó de `legacy review` a `PREVENTED` únicamente después de la prueba.
