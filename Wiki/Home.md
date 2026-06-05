# CoderCerberus Golden Standard Wiki

Bienvenido a la bóveda Obsidian del **Golden Standard** (GS) de CoderCerberus. Esta base de conocimiento representa la doctrina pura de ingeniería, mitigación de vicios y tokenomics acumulada del proyecto central y sus satélites.

---

## Acceso Rápido

- 📂 **[[Vices_Index|Índice de Vicios de Ingeniería]]**: Catálogo central de anomalías de código, tests y tokenomics (`VC`, `TV`, `TK`).
- 📂 **[[Project_Insights_Index|Índice de Insights Satélite]]**: Lecciones y mejores prácticas (`PI`) extraídas de repositorios externos y automatizaciones.
- 📘 **[[Concepts/Marco_Conceptual|Marco Conceptual de CoderCerberus]]**: Doctrina epistemológica, niveles y bases de diseño.
- 📥 **[Inbox](../Inbox/README.md)**: Buzón de entrada para hallazgos crudos y propuestas nuevas.
- 🧪 **[Audit Report](../golden_standard_audit_report.md)**: Estado compilado de cobertura y mapeo vigente.
- 🏠 **[README](../README.md)**: Visión general del repositorio público.

---

## Mapa por Dominio

| Dominio | Catálogo | Entradas | Enlace |
|---|---|---:|---|
| Vibe Coding | `VC-xxx` | 123 | [[Vices_Index|Abrir índice]] |
| Testing & Evaluation | `VT-xxx` | 115 | [[Vices_Index|Abrir índice]] |
| Tokenomics & Context | `TK-xxx` | 46 | [[Vices_Index|Abrir índice]] |
| Project Insights | `PI-xxx` | 18 | [[Project_Insights_Index|Abrir índice]] |

---

## Estado de Operatividad

| Estado | Entradas | Significado |
|---|---:|---|
| `PREVENTED` + `REMEDIATED` | 45 | El catálogo ya tiene una compuerta ejecutable o una corrección concreta. |
| `AUDITED` + `DOC_ONLY` | 239 | La entrada existe como conocimiento, pero sigue siendo principalmente documental. |
| `Total` | 284 | Suma de las entradas de VC, VT y TK auditadas por el compilador. |

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
*Bóveda auto-generada por el compilador `generate_golden_audit.py` el 2026-06-04.*
