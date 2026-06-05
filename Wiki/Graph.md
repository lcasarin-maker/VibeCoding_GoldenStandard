# GS Graph

Mapa local del vault generado automáticamente por `generate_golden_audit.py`.

Este grafo combina enlaces Obsidian, enlaces Markdown relativos y menciones explícitas de IDs (`VC-xxx`, `VT-xxx`, `TK-xxx`, `PI-xxx`).

---

## Snapshot

| Métrica | Valor |
|---|---:|
| Nodos | 349 |
| Aristas | 1721 |
| Huérfanos intencionales | 3 |
| Huérfanos candidatos | 0 |
| Hubs | 15 |

---

## Deuda de Validación

El grafo ahora también resalta las entradas que siguen siendo principalmente documentales. Esto no invalida el conocimiento, pero sí marca dónde faltan compuertas reales.

| Catálogo | VC DOC_ONLY | VT DOC_ONLY | TK DOC_ONLY |
|---|---:|---:|---:|
| `DOC_ONLY` | 93 | 0 | 12 |

| ID | Título | Categoría | Severidad | Estado |
|---|---|---|---|---|
| `VC-001` | Incompetencia no asumida | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-002` | Complacencia generativa | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-004` | Demo como calidad | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-005` | Prototipo convertido en deuda | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-006` | Estética como integridad | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-007` | Auditoría no humana del core | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-008` | Optimismo operativo | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-009` | Autoauditoría contaminada | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-010` | Fallo no convertido en doctrina | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-011` | Human test falso | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-012` | Se ve bien como métrica | `Vibe Coding` | `medium` | `DOC_ONLY` |
| `VC-013` | Calificación máxima gratuita | `Vibe Coding` | `medium` | `DOC_ONLY` |

---

## Deuda de Profundidad

Cada entrada se clasifica por profundidad: `deep` (trae ejemplos bad/good y receta de detección — vicio falsable), `doctrinal` (principio conductual/epistémico sin firma estática; stub por diseño, no se le fabrica código) y `stub` (enriquecible pero aún sin ejemplos — deuda real).

| Profundidad | VC | VT | TK |
|---|---:|---:|---:|
| `deep` | 46 | 115 | 46 |
| `stub` | 0 | 0 | 0 |
| `doctrinal` | 80 | 0 | 0 |

---

## Verificación Downstream

GS distingue explícitamente qué entradas esperan verificación downstream y cuáles no. Esto evita que `DOC_ONLY` se interprete como `test exempt` por defecto.

| Estado | VC | VT | TK |
|---|---:|---:|---:|
| `required` | 93 | 0 | 12 |
| `none` | 33 | 115 | 34 |

| ID | Título | Categoría | Downstream Verification |
|---|---|---|---|
| `VC-001` | Incompetencia no asumida | `Vibe Coding` | `required` |
| `VC-002` | Complacencia generativa | `Vibe Coding` | `required` |
| `VC-004` | Demo como calidad | `Vibe Coding` | `required` |
| `VC-005` | Prototipo convertido en deuda | `Vibe Coding` | `required` |
| `VC-006` | Estética como integridad | `Vibe Coding` | `required` |
| `VC-007` | Auditoría no humana del core | `Vibe Coding` | `required` |
| `VC-008` | Optimismo operativo | `Vibe Coding` | `required` |
| `VC-009` | Autoauditoría contaminada | `Vibe Coding` | `required` |
| `VC-010` | Fallo no convertido en doctrina | `Vibe Coding` | `required` |
| `VC-011` | Human test falso | `Vibe Coding` | `required` |
| `VC-012` | Se ve bien como métrica | `Vibe Coding` | `required` |
| `VC-013` | Calificación máxima gratuita | `Vibe Coding` | `required` |

---

## Hubs

Páginas con mayor superficie de impacto. Si cambian, revisa primero sus enlaces entrantes.

| Nodo | Tipo | In | Out | Entradas | Salidas |
|---|---|---:|---:|---|---|
| [[Vices_Index]] | `wiki` | 242 | 242 | [[Home]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]], [[Vices/VC-004]], [[Vices/VC-005]] +236 more | [[Home]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]], [[Vices/VC-004]], [[Vices/VC-005]] +236 more |
| [[Home]] | `wiki` | 332 | 21 | [[Concepts/Marco_Conceptual]], [[Domains/D1]], [[Domains/D10]], [[Domains/D11]], [[Domains/D12]], [[Domains/D2]] +326 more | [[CONCEPTUAL_FRAMEWORK]], [[Concepts/Marco_Conceptual]], [[Inbox/README]], [[Project_Insights/PI-019]], [[Project_Insights/PI-020]], [[Project_Insights/PI-021]] +15 more |
| [[Tokenomics_Map]] | `wiki` | 322 | 10 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +316 more | [[Home]], [[Project_Insights/PI-019]], [[Project_Insights_Index]], [[Tokenomics/Automation_Tooling_Index]], [[Tokenomics/Input_Retrieval_Index]], [[Tokenomics/Measurement_Telemetry_Index]] +4 more |
| [[Project_Insights/PI-019]] | `insight` | 244 | 4 | [[Home]], [[Project_Insights_Index]], [[Tokenomics_Map]], [[Vices/VC-001]], [[Vices/VC-002]], [[Vices/VC-003]] +238 more | [[Home]], [[Project_Insights_Index]], [[Tokenomics_Map]], [[Vices/VC-124]] |
| [[Tokenomics_Index]] | `wiki` | 54 | 48 | [[Home]], [[README]], [[Tokenomics/Automation_Tooling_Index]], [[Tokenomics/Input_Retrieval_Index]], [[Tokenomics/Measurement_Telemetry_Index]], [[Tokenomics/Memory_Headroom_Index]] +48 more | [[Home]], [[Tokenomics/TK-001]], [[Tokenomics/TK-002]], [[Tokenomics/TK-003]], [[Tokenomics/TK-004]], [[Tokenomics/TK-005]] +42 more |
| [[Project_Insights_Index]] | `wiki` | 29 | 28 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +23 more | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +22 more |
| [[Vices/VC-124]] | `vice` | 30 | 4 | [[Home]], [[Project_Insights/PI-001]], [[Project_Insights/PI-002]], [[Project_Insights/PI-003]], [[Project_Insights/PI-004]], [[Project_Insights/PI-005]] +24 more | [[Home]], [[Project_Insights/PI-019]], [[Tokenomics_Map]], [[Vices_Index]] |
| [[Tokenomics/Memory_Headroom_Index]] | `tokenomics` | 2 | 17 | [[Home]], [[Tokenomics_Map]] | [[Tokenomics/TK-001]], [[Tokenomics/TK-002]], [[Tokenomics/TK-003]], [[Tokenomics/TK-004]], [[Tokenomics/TK-005]], [[Tokenomics/TK-006]] +11 more |
| [[Tokenomics/Output_Compaction_Index]] | `tokenomics` | 2 | 14 | [[Home]], [[Tokenomics_Map]] | [[Tokenomics/TK-020]], [[Tokenomics/TK-021]], [[Tokenomics/TK-022]], [[Tokenomics/TK-024]], [[Tokenomics/TK-025]], [[Tokenomics/TK-027]] +8 more |
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
| [[Vices_Index]] | `wiki` | `vice`, `wiki` | 242 |
| [[Tokenomics_Index]] | `wiki` | `tokenomics`, `wiki` | 48 |
| [[Project_Insights_Index]] | `wiki` | `insight`, `wiki` | 28 |
| [[Home]] | `wiki` | `concept`, `conceptual-framework`, `inbox`, `insight`, `root`, `tokenomics`, `vice`, `wiki` | 21 |
| [[Tokenomics/Memory_Headroom_Index]] | `tokenomics` | `tokenomics`, `wiki` | 17 |
| [[Tokenomics/Output_Compaction_Index]] | `tokenomics` | `tokenomics`, `wiki` | 14 |
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
