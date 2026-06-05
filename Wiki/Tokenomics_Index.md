# Índice de Tokenomics

Tokenomics es una categoría propia del Golden Standard. No describe vicios de código ni de testing: describe cómo reducir ruido, preservar headroom, compactar contexto y externalizar estado sin sacrificar calidad.

La utilidad práctica de esta categoría es doble:

1. evitar que el agente queme contexto en relecturas, salidas verbosas o handoffs pobres;
2. convertir ahorro de tokens en una disciplina medible, no en una intuición.

Históricamente, esta capa se operó bajo nombres como *headspace*, *compact* y *token saving*. GS conserva el conocimiento y también define la doctrina de uso.

---

## Subíndices

- [[Memory_Headroom_Index|Memoria y Headroom]]
- [[Input_Retrieval_Index|Entrada y Recuperación]]
- [[Output_Compaction_Index|Salida y Compresión]]
- [[Measurement_Telemetry_Index|Medición y Telemetría]]
- [[Automation_Tooling_Index|Automatización y Herramientas]]
- [[Tokenomics_Map|Mapa de Tokenomics]]

---

## Estado de la categoría

| Estado | Entradas |
|---|---:|
| `PREVENTED` / `REMEDIATED` | 34 |
| `DOC_ONLY` / `AUDITED` | 12 |
| `Total` | 46 |

---

## Entradas

*   [[Tokenomics/TK-001|TK-001]] — **Checkpoint ausente** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-002|TK-002]] — **Memoria de chat como fuente principal** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-003|TK-003]] — **Cambio de proyecto sin cierre** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-004|TK-004]] — **Setup reexplicado** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-005|TK-005]] — **Handoff prose-heavy** (PREVENTED, medium, downstream:none)
*   [[Tokenomics/TK-006|TK-006]] — **Merge manual de historial** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-007|TK-007]] — **Fuente de verdad duplicada** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-008|TK-008]] — **Segregación Epistemológica de la Memoria** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-009|TK-009]] — **Poda semántica** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-010|TK-010]] — **Recuperación contextual** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-011|TK-011]] — **Delimitadores estructurados** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-012|TK-012]] — **Exploration tax** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-013|TK-013]] — **Tool schemas inflados** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-014|TK-014]] — **Lectura completa por defecto** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-015|TK-015]] — **Archivo completo para duda puntual** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-016|TK-016]] — **Prompt gigante multiobjetivo** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-017|TK-017]] — **Permisos narrados** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-018|TK-018]] — **Backlog mezclado con objetivo** (PREVENTED, medium, downstream:none)
*   [[Tokenomics/TK-019|TK-019]] — **Esqueleto Jerárquico de Dependencias** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-020|TK-020]] — **Restricción de salida** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-021|TK-021]] — **Prefilling** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-022|TK-022]] — **Optimización de ejemplos** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-023|TK-023]] — **Logs crudos** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-024|TK-024]] — **Resumen sin densidad** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-025|TK-025]] — **Salida de auditoría verbosa** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-026|TK-026]] — **Observabilidad ruidosa** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-027|TK-027]] — **Compresión Léxica de Diagnósticos** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-028|TK-028]] — **Caching de contexto estable** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-029|TK-029]] — **Procesamiento batch** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-030|TK-030]] — **Cascada de capacidades** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-031|TK-031]] — **Compactación de contexto** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-032|TK-032]] — **Cache cliff** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-033|TK-033]] — **Sin headroom** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-034|TK-034]] — **Costo de reversión invisible** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-035|TK-035]] — **Pensar con herramienta de ejecución** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-036|TK-036]] — **Respuesta sin modo** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-037|TK-037]] — **Monitoreo manual olvidable** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-038|TK-038]] — **Relectura de estado completo** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-039|TK-039]] — **Herramientas externas no integradas** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-040|TK-040]] — **Ahorro prometido no medido** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-041|TK-041]] — **Cuotas invisibles** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-042|TK-042]] — **Manifiestos sin restricción de tamaño** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-043|TK-043]] — **Entropía sin poda — gobernanza de entrada sin gobernanza de salida** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-F01|TK-F01]] — **Reprocesamiento de contexto estable** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-F02|TK-F02]] — **Poda contextual primitiva** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-F03|TK-F03]] — **Salida verbal excesiva** (DOC_ONLY, low, downstream:required)

---
## Referencia de uso

- Tokenomics define principios de eficiencia y gestión de contexto.
- La enforcement real de estos principios pertenece a los repositorios consumidores y herramientas que adopten GS.
- El vocabulario de la categoría debe mantenerse separado de VC y VT para evitar confusión semántica.
- Las estrategias modernas de reducción de ruido, como RTK e ICM, confirman que el ahorro de tokens se beneficia de herramientas de filtrado, memoria externa y compacción de contexto.

---
[[Home|Volver al Inicio]]
