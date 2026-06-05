# GS Graph

Mapa local del vault generado automáticamente por `generate_golden_audit.py`.

Este grafo combina enlaces Obsidian, enlaces Markdown relativos y menciones explícitas de IDs (`VC-xxx`, `VT-xxx`, `TK-xxx`, `PI-xxx`).

---

## Snapshot

| Métrica | Valor |
|---|---:|
| Nodos | 370 |
| Aristas | 1824 |
| Huérfanos intencionales | 3 |
| Huérfanos candidatos | 0 |
| Hubs | 15 |

---

## Deuda de Validación

El grafo ahora también resalta las entradas que siguen siendo principalmente documentales. Esto no invalida el conocimiento, pero sí marca dónde faltan compuertas reales.

| Catálogo | VC DOC_ONLY | VT DOC_ONLY | TK DOC_ONLY |
|---|---:|---:|---:|
| `DOC_ONLY` | 106 | 0 | 13 |

| ID | Título | Categoría | Severidad | Estado |
|---|---|---|---|---|
| `VC-127` | Inyeccion de prompt en bucle de agente (Prompt Injection) | `Vibe Coding` | `critical` | `DOC_ONLY` |
| `VC-128` | Envenenamiento de contexto (Context Poisoning) | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-129` | Dependencia alucinada (Slopsquatting) | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-133` | Fallo de tool call no manejado en bucle de agente | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-134` | Coordinacion multiagente sin protocolo | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-135` | Uso de API obsoleta o alucinada de una libreria real | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-136` | Memoria persistente envenenada o stale (cross-session) | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-138` | Codigo generado inseguro por defecto | `Vibe Coding` | `high` | `DOC_ONLY` |
| `VC-139` | Confianza ciega en la salida del LLM (Insecure Output Handling) | `Vibe Coding` | `high` | `DOC_ONLY` |
| `TK-044` | Deuda de tokenomics acumulada (Cost Compounding) | `Tokenomics & Context` | `medium` | `DOC_ONLY` |
| `VC-001` | Incompetencia no asumida | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-002` | Complacencia generativa | `Vibe Coding` | `medium` | `DOC_ONLY` |

---

## Deuda de Profundidad

Cada entrada se clasifica por profundidad: `deep` (trae ejemplos bad/good y receta de detección — vicio falsable), `doctrinal` (principio conductual/epistémico sin firma estática; stub por diseño, no se le fabrica código), `stub` (enriquecible pero aún sin ejemplos — deuda real) y `alias` (duplicado semántico fusionado en su entrada canónica; el ID se conserva por estabilidad de referencias).

| Profundidad | VC | VT | TK |
|---|---:|---:|---:|
| `deep` | 67 | 115 | 47 |
| `stub` | 0 | 0 | 0 |
| `doctrinal` | 70 | 0 | 0 |
| `alias` | 2 | 0 | 0 |

**Enforcement local:** 16 entradas `deep` tienen un detector estático real en `scripts/detectors.py`, probado en CI contra sus propios `example_bad`/`example_good` (`scripts/test_detectors.py`). El resto son falsables-en-principio (traen receta de detección) pero aún sin detector implementado.

---

## Verificación Downstream

GS distingue explícitamente qué entradas esperan verificación downstream y cuáles no. Esto evita que `DOC_ONLY` se interprete como `test exempt` por defecto.

| Estado | VC | VT | TK |
|---|---:|---:|---:|
| `required` | 106 | 0 | 13 |
| `none` | 33 | 115 | 34 |

| ID | Título | Categoría | Downstream Verification |
|---|---|---|---|
| `VC-127` | Inyeccion de prompt en bucle de agente (Prompt Injection) | `Vibe Coding` | `required` |
| `VC-128` | Envenenamiento de contexto (Context Poisoning) | `Vibe Coding` | `required` |
| `VC-129` | Dependencia alucinada (Slopsquatting) | `Vibe Coding` | `required` |
| `VC-133` | Fallo de tool call no manejado en bucle de agente | `Vibe Coding` | `required` |
| `VC-134` | Coordinacion multiagente sin protocolo | `Vibe Coding` | `required` |
| `VC-135` | Uso de API obsoleta o alucinada de una libreria real | `Vibe Coding` | `required` |
| `VC-136` | Memoria persistente envenenada o stale (cross-session) | `Vibe Coding` | `required` |
| `VC-138` | Codigo generado inseguro por defecto | `Vibe Coding` | `required` |
| `VC-139` | Confianza ciega en la salida del LLM (Insecure Output Handling) | `Vibe Coding` | `required` |
| `TK-044` | Deuda de tokenomics acumulada (Cost Compounding) | `Tokenomics & Context` | `required` |
| `VC-001` | Incompetencia no asumida | `Vibe Coding` | `required` |
| `VC-002` | Complacencia generativa | `Vibe Coding` | `required` |

---

## Hubs

Páginas con mayor superficie de impacto. Si cambian, revisa primero sus enlaces entrantes.

| Nodo | Tipo | In | Out | Entradas | Salidas |
|---|---|---:|---:|---|---|
| [[Vices_Index]] | `wiki` | 255 | 255 | [[Home]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]], [[Vices/VC-004]], [[Vices/VC-005]] +249 more | [[Home]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]], [[Vices/VC-004]], [[Vices/VC-005]] +249 more |
| [[Home]] | `wiki` | 353 | 21 | [[Concepts/Marco_Conceptual]], [[Domains/D1]], [[Domains/D10]], [[Domains/D11]], [[Domains/D12]], [[Domains/D2]] +347 more | [[CONCEPTUAL_FRAMEWORK]], [[Concepts/Marco_Conceptual]], [[Inbox/README]], [[Project_Insights/PI-019]], [[Project_Insights/PI-020]], [[Project_Insights/PI-021]] +15 more |
| [[Tokenomics_Map]] | `wiki` | 341 | 10 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +335 more | [[Home]], [[Project_Insights/PI-019]], [[Project_Insights_Index]], [[Tokenomics/Automation_Tooling_Index]], [[Tokenomics/Input_Retrieval_Index]], [[Tokenomics/Measurement_Telemetry_Index]] +4 more |
| [[Project_Insights/PI-019]] | `insight` | 255 | 4 | [[Home]], [[Project_Insights_Index]], [[Tokenomics_Map]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]] +249 more | [[Home]], [[Project_Insights_Index]], [[Tokenomics_Map]], [[Vices/VC-124]] |
| [[Tokenomics_Index]] | `wiki` | 55 | 49 | [[Home]], [[README]], [[Tokenomics/Automation_Tooling_Index]], [[Tokenomics/Input_Retrieval_Index]], [[Tokenomics/Measurement_Telemetry_Index]], [[Tokenomics/Memory_Headroom_Index]] +49 more | [[Home]], [[Tokenomics/TK-001]], [[Tokenomics/TK-002]], [[Tokenomics/TK-003]], [[Tokenomics/TK-004]], [[Tokenomics/TK-005]] +43 more |
| [[Project_Insights_Index]] | `wiki` | 36 | 35 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +30 more | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +29 more |
| [[Vices/VC-124]] | `vice` | 37 | 4 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +31 more | [[Home]], [[Project_Insights/PI-019]], [[Tokenomics_Map]], [[Vices_Index]] |
| [[Tokenomics/Memory_Headroom_Index]] | `tokenomics` | 2 | 17 | [[Home]], [[Tokenomics_Map]] | [[Tokenomics/TK-001]], [[Tokenomics/TK-002]], [[Tokenomics/TK-003]], [[Tokenomics/TK-004]], [[Tokenomics/TK-005]], [[Tokenomics/TK-006]] +11 more |
| [[Tokenomics/Output_Compaction_Index]] | `tokenomics` | 2 | 15 | [[Home]], [[Tokenomics_Map]] | [[Tokenomics/TK-020]], [[Tokenomics/TK-021]], [[Tokenomics/TK-022]], [[Tokenomics/TK-024]], [[Tokenomics/TK-025]], [[Tokenomics/TK-027]] +9 more |
| [[Tokenomics/Input_Retrieval_Index]] | `tokenomics` | 2 | 12 | [[Home]], [[Tokenomics_Map]] | [[Tokenomics/TK-009]], [[Tokenomics/TK-010]], [[Tokenomics/TK-011]], [[Tokenomics/TK-012]], [[Tokenomics/TK-014]], [[Tokenomics/TK-015]] +6 more |

---

## Huérfanos Intencionales

Plantillas o fixtures que se mantienen aislados por diseño. No son deuda de navegación, pero sí conviene mantenerlos acotados.

| Nodo | Tipo | In | Out | Entradas | Salidas |
|---|---|---:|---:|---|---|
| [[Inbox/templates/cerberus_finding]] | `inbox` | 0 | 0 | — | — |
| [[Inbox/templates/external_contribution]] | `inbox` | 0 | 0 | — | — |
| [[Inbox/templates/manual_finding]] | `inbox` | 0 | 0 | — | — |

---

## Huérfanos Candidatos

Páginas dentro del surface live de GS que no reciben enlaces entrantes. Si alguna es importante, conviene enlazarla desde un índice o mapa principal.

| Nodo | Tipo | In | Out | Entradas | Salidas |
|---|---|---:|---:|---|---|
| — | — | 0 | 0 | — | — |

---

## Puentes

Nodos que enlazan a más de un tipo de página. Son útiles para navegar impacto entre dominios.

| Nodo | Tipo | Tipos alcanzados | Salidas |
|---|---|---|---:|
| [[Vices_Index]] | `wiki` | `vice`, `wiki` | 255 |
| [[Tokenomics_Index]] | `wiki` | `tokenomics`, `wiki` | 49 |
| [[Project_Insights_Index]] | `wiki` | `insight`, `wiki` | 35 |
| [[Home]] | `wiki` | `concept`, `conceptual-framework`, `inbox`, `insight`, `root`, `tokenomics`, `vice`, `wiki` | 21 |
| [[Tokenomics/Memory_Headroom_Index]] | `tokenomics` | `tokenomics`, `wiki` | 17 |
| [[Tokenomics/Output_Compaction_Index]] | `tokenomics` | `tokenomics`, `wiki` | 15 |
| [[Tokenomics/Input_Retrieval_Index]] | `tokenomics` | `tokenomics`, `wiki` | 12 |
| [[Tokenomics_Map]] | `wiki` | `insight`, `tokenomics`, `vice`, `wiki` | 10 |
| [[Project_Insights/PI-002]] | `insight` | `domain`, `vice`, `wiki` | 8 |
| [[Project_Insights/PI-006]] | `insight` | `domain`, `vice`, `wiki` | 8 |
| [[Project_Insights/PI-012]] | `insight` | `domain`, `vice`, `wiki` | 8 |
| [[Tokenomics/Measurement_Telemetry_Index]] | `tokenomics` | `tokenomics`, `wiki` | 8 |
| [[Domains/D10]] | `domain` | `insight`, `wiki` | 7 |
| [[Project_Insights/PI-001]] | `insight` | `domain`, `vice`, `wiki` | 7 |
| [[Project_Insights/PI-004]] | `insight` | `domain`, `vice`, `wiki` | 7 |

---

## Uso Rápido

1. Abre `[[Home]]` para entrar al vault.
2. Abre este mapa para ver hubs y huérfanos.
3. Usa el JSON `golden_standard_graph.json` si quieres automatizar análisis de impacto.

---
[[Home|Volver al Inicio]]
