# Golden Standard Wiki

Bienvenido a la bóveda Obsidian del **Golden Standard** (GS). Esta base de conocimiento representa la doctrina pura de ingeniería, mitigación de vicios y tokenomics acumulada por el proyecto.

---

## Acceso Rápido

- 📂 **[[Vices_Index|Índice de Vicios de Ingeniería]]**: Catálogo central de anomalías de código y tests (`VC`, `TV`).
- 📂 **[[Project_Insights_Index|Índice de Insights Satélite]]**: Lecciones y mejores prácticas (`PI`) extraídas de repositorios externos y automatizaciones.
- 🕸️ **[[Graph|Mapa de Grafo GS]]**: Hubs, huérfanos intencionales, huérfanos candidatos e impacto local del vault.
- 📘 **[[Concepts/Marco_Conceptual|Marco Conceptual del Golden Standard]]**: Doctrina epistemológica, niveles y bases de diseño.
- 🧼 **[[Concepts/Marco_Conceptual#11.-Higiene,-limpieza-y-organización-del-repositorio|Capítulo de Higiene del Repositorio]]**: Norma canónica para limpieza, nombres, root limpio y evidencia de organización.
- 🔧 **[[Project_Insights/PI-019|Higiene de ejecución y tooling]]**: Regla satélite para comandos simples, UTF-8 y pureza técnica.
- ⚠️ **[[Vices/VC-124|Deprecación precipitada]]**: Vicio espejo que evita mover a `deprecated/` sin análisis.
- 🏷️ **[[Project_Insights/PI-020|Confidence Tags]]**: Cada afirmación de protocolo debe declarar si es VERIFIED, INFERRED o ASSUMED.
- 🧪 **[[Project_Insights/PI-021|Wiki-Lint semántico]]**: Detecta contradicciones, referencias rotas y mandatos sin binding.
- 🧾 **[[Project_Insights/PI-022|Lista de incertidumbre]]**: Documenta lo no verificado para no fingir certeza.
- 🧭 **[[Project_Insights/PI-023|Conciencia de sesión dual]]**: Verifica estado compartido antes de editar.
- 🕸️ **[[Project_Insights/PI-024|Revisión basada en hubs]]**: Prioriza nodos de alto impacto en el grafo.
- 🧷 **[[Project_Insights/PI-025|Retrospectiva exportable]]**: Cierra cada sesión con una retrospectiva estructurada y persistente.
- 💠 **[[Tokenomics_Index|Índice de Tokenomics]]**: Catálogo separado de eficiencia, headroom y gestión de contexto (`TK`).
- 🗺️ **[[Tokenomics_Map|Mapa de Tokenomics]]**: Puente entre lentes `TK` y `PI` para navegar relaciones, huecos y cobertura.
- 🔹 **[[Tokenomics/Memory_Headroom_Index|Memoria y Headroom]]**: Checkpoints, handoff, persistencia y margen contextual.
- 🔹 **[[Tokenomics/Input_Retrieval_Index|Entrada y Recuperación]]**: Recuperación dirigida y reducción de ruido de entrada.
- 🔹 **[[Tokenomics/Output_Compaction_Index|Salida y Compresión]]**: Verbosidad, compresión y presupuesto de respuesta.
- 🔹 **[[Tokenomics/Measurement_Telemetry_Index|Medición y Telemetría]]**: Evidencia de ahorro y monitoreo de impacto.
- 🔹 **[[Tokenomics/Automation_Tooling_Index|Automatización y Herramientas]]**: Integraciones activas y tooling que ejecuta ahorro.
- 📄 **[Marco conceptual raíz](../CONCEPTUAL_FRAMEWORK.md)**: Documento base local del GS para lectura directa y navegación del grafo.
- 📥 **[Inbox](../Inbox/README.md)**: Buzón de entrada para hallazgos crudos y propuestas nuevas.
- 🧪 **[Audit Report](../golden_standard_audit_report.md)**: Estado compilado de cobertura y mapeo vigente.
- 🗺️ **[Graph JSON](../golden_standard_graph.json)**: Export estructurado para queries programáticas de impacto.
- 🏠 **[README](../README.md)**: Visión general del repositorio público.

---

## Mapa por Dominio

| Dominio | Catálogo | Entradas | Enlace |
|---|---|---:|---|
| Vibe Coding | `VC-xxx` | 134 | [[Vices_Index|Abrir índice]] |
| Testing & Evaluation | `VT-xxx` | 115 | [[Vices_Index|Abrir índice]] |
| Tokenomics | `TK-xxx` | 47 | [[Tokenomics_Index|Abrir índice]] |
| Project Insights | `PI-xxx` | 31 | [[Project_Insights_Index|Abrir índice]] |

---

## Estado de Operatividad

| Estado | Entradas | Significado |
|---|---:|---|
| `PREVENTED` + `REMEDIATED` | 92 | El catálogo ya tiene una compuerta ejecutable o una corrección concreta. |
| `AUDITED` + `DOC_ONLY` | 204 | La entrada existe como conocimiento, pero sigue siendo principalmente documental. |
| `Total` | 296 | Suma de las entradas de VC, VT y TK auditadas por el compilador. |

---

## Guía de Severidad

| Severidad | Qué significa | Acción típica |
|---|---|---|
| `critical` | Riesgo de seguridad, pérdida de datos o fallo total de una capacidad esencial. | Corregir antes de seguir. |
| `high` | Bug visible para usuarios o ruptura seria de confianza. | Priorizar en la siguiente iteración. |
| `medium` | Deuda de fiabilidad o mantenibilidad. | Programar remediación. |
| `low` | Ajuste de estilo, claridad o eficiencia. | Agrupar con limpieza general. |

> La severidad se usa en revisión de contribuciones; el estado operativo canónico en los catálogos sigue siendo `status`.

---

## Flujo de Entrada

1. Depositar el hallazgo en `Inbox/<fuente>/YYYY-MM-DD_<slug>.md`.
2. Validar campos mínimos con `INGESTION_PROTOCOL.md`.
3. Promover a YAML + Wiki solo después de deduplicar y mapear el dominio.
4. Recompilar con `python generate_golden_audit.py`.

---
*Bóveda auto-generada por el compilador `generate_golden_audit.py` el 2026-06-05.*