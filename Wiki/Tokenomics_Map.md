# Mapa de Tokenomics

Este mapa sirve como puente entre la categoría `TK` y las lecciones satélite del GS. No repite el catálogo: muestra cómo leerlo y con qué insights se cruza.

## Para qué sirve

- Navegar relaciones entre vicios de contexto, ahorro de tokens y disciplina operativa.
- Identificar qué lecciones satélite refuerzan cada lente de tokenomics.
- Detectar huecos donde hay doctrina, pero todavía falta un artefacto de apoyo o una telemetría clara.

---

## Lentes operativos

| Lente | Subíndice | Project Insights relacionados | Intención |
|---|---|---|---|
| Memoria y Headroom | [[Tokenomics/Memory_Headroom_Index|Abrir lente]] | `PI-006, PI-010, PI-014, PI-018` | Evita pérdida de contexto, root pollution y aprendizaje olvidado. |
| Entrada y Recuperación | [[Tokenomics/Input_Retrieval_Index|Abrir lente]] | `PI-005, PI-012` | Reduce ruido de entrada y hace más precisa la recuperación dirigida. |
| Salida y Compresión | [[Tokenomics/Output_Compaction_Index|Abrir lente]] | `PI-003, PI-007, PI-009, PI-016` | Controla verbosidad, costo, pruning y honestidad documental. |
| Medición y Telemetría | [[Tokenomics/Measurement_Telemetry_Index|Abrir lente]] | `PI-003, PI-013` | Hace visible el ahorro real, no solo la intención de ahorrar. |
| Automatización y Herramientas | [[Tokenomics/Automation_Tooling_Index|Abrir lente]] | `PI-005, PI-006, PI-013` | Conecta la doctrina con tooling ejecutable y observabilidad continua. |

---

## Project Insights clave

| Insight | Resumen |
|---|---|
| `PI-003` | Tokencost – metering previo de tokens y conversión a USD para hacer visible el gasto antes de ejecutar una llamada LLM. [REMEDIATED Sprint 5: track_tokens.py cableado al gate D10; visualidad confirma.] |
| `PI-005` | Litellm – gateway agnóstico de proveedor con routing, fallback, cost tracking, guardrails, logging y load balancing. [NOT_APPLICABLE Sprint 10: análisis de 36 repos externos mostró que LiteLLM es útil como referencia arquitectónica pero la capa de abstracción de proveedor ya está cubierta por Cerberus gates; integración declarativa, no ejecutable.] |
| `PI-006` | Cerberus v0.3 – compuerta entre intención y ejecución que impone disciplina de contexto, observabilidad, redacción y control de estado. [ACTIVE Sprint 5-11: WARN→BLOCK en gate APPROVED (recomendaciones solo con FAILs); 12D dominios (D1-D12); 386 tests adversariales; 17 satélites sincronizados; naming verb_noun normalizado; Golden Standard = conocimiento puro (PI-015..PI-018 formalizados).] |
| `PI-007` | Gobernanza de salida (diagnóstico Cerberus 2026-05-30) – el sistema tenía gobernanza de ENTRADA (gates de calidad) pero no de SALIDA (poda de huérfanos), por eso acumuló residuo de refactor: 250MB de backups, dead code, 5 docs de plan, scripts espectrales, GLOBAL_LEARNING divergente, base-set stale, IDs TK-043/44/45 declarados sin contenido. Raíz: el gate validaba letra (Path.exists) no vigencia (ruta activa). Orden = el mismo gate que bloquea código malo bloquea la basura que sobra. Ejecutable en PLAN.md P0 (orphan-hunt) / P1 (vulture/VC-118) / P5 (catálogo=ejecución). |
| `PI-009` | Deuda cero antes de avanzar – todo warning o hallazgo no bloqueante se trata como error operativo hasta que se corrija o se bloquee explícitamente. [IMPLEMENTED Sprint 5: [RECOMENDACIONES POR DOMINIO] suprimida de gate APPROVED (ruido no bloqueante); solo aparece cuando hay FAILs de dominio para guiar el fix. Test failing-first valida ambas ramas. Refactor _print_recommendations (C901 compliance).] |
| `PI-010` | Higiene de salida y raíz limpia – los artefactos históricos son referencia, no fuente de verdad; al cerrar auditoría la raíz debe quedar libre de residuo operativo. |
| `PI-012` | Exclusiones mínimas y reales – whitelists, excludes, skips, xfails, stubs, mocks y placeholders solo con causa verificable; la cobertura falsa es deuda, no avance. |
| `PI-013` | Vigilancia en tiempo real – observar señales, costes y desvíos durante la ejecución, no solo en el post-mortem. |
| `PI-014` | Golden Standard vivo – conservar conocimiento puro, agnóstico y actualizado con los aprendizajes del proyecto y los satélites sin mezclarlo con herramientas concretas. |
| `PI-016` | Honestidad DOC_ONLY – si una lección no es falsable por una compuerta física, debe etiquetarse como DOC_ONLY en vez de simular cobertura automática. |
| `PI-018` | Ingesta canónica de aprendizajes – normalizar, deduplicar y registrar nuevas lecciones satélite antes de incorporarlas al conocimiento central. |

---

## Cruces adyacentes

| Nodo | Relación | Motivo |
|---|---|---|
| `[[Project_Insights/PI-019|PI-019]]` | Higiene satélite | Expande la disciplina de edición y validación hacia el trabajo diario con herramientas. |
| `[[Vices/VC-124|VC-124]]` | Vicio espejo | Representa el error de deprecar sin análisis ni trazabilidad. |

---

## Lectura práctica

1. Si un problema consume contexto, revisa primero `Memoria y Headroom`.
2. Si el problema nace en la entrada, revisa `Entrada y Recuperación`.
3. Si el costo está en la respuesta, revisa `Salida y Compresión`.
4. Si no hay evidencia del ahorro, revisa `Medición y Telemetría`.
5. Si la doctrina no se ejecuta sola, revisa `Automatización y Herramientas`.

---
[[Tokenomics_Index|Volver al Índice de Tokenomics]] | [[Project_Insights_Index|Ir a Insights]] | [[Home|Inicio]]
