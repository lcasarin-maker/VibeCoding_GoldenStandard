# Inbox — Golden Standard Knowledge Ingestion

Este directorio es el **buzón de entrada** de la base de conocimiento.
Aquí se depositan hallazgos crudos antes de ser curados y promovidos al catálogo.

> **Para el protocolo completo de ingesta, ver:** [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md)  
> **Para las fuentes autorizadas y sus contratos, ver:** [`KNOWLEDGE_SOURCES.md`](../KNOWLEDGE_SOURCES.md)

---

## Estructura de este Directorio

```
Inbox/
├── cerberus/      ← Hallazgos de auditorías de CoderCerberus
├── manual/        ← Hallazgos de sesiones manuales del DRI
├── external/      ← Contribuciones externas (triageadas por mantenedores)
└── templates/
    ├── cerberus_finding.md        ← Plantilla para hallazgos de Cerberus
    ├── manual_finding.md          ← Plantilla para hallazgos manuales
    └── external_contribution.md  ← Plantilla para contribuciones externas
```

### Notas por Carpeta

- [`cerberus/README.md`](cerberus/README.md) — qué depositar y cómo nombrarlo.
- [`manual/README.md`](manual/README.md) — hallazgos observados por la DRI.
- [`external/README.md`](external/README.md) — flujo para issues y PRs externos; solo evidencia basada en el baseline activo y con purga fresca si se audita limpieza o completitud.
- [`templates/README.md`](templates/README.md) — referencia rápida de plantillas.

---

## Cómo Depositar un Hallazgo (resumen rápido)

1. Copia la plantilla correspondiente de `Inbox/templates/`
2. Completa todos los campos requeridos (marcados con ✅ en la plantilla)
3. Guarda el archivo en el subdirectorio correcto con la convención de nombre:
   ```
   YYYY-MM-DD_<slug>.md
   ```
4. Haz commit con el mensaje: `inbox: <fuente> finding <slug>`

El curador revisará el hallazgo y lo promoverá al catálogo YAML + Wiki siguiendo el [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md).

### Requisito de profundidad (Definition of Done)

Para evitar que el catálogo vuelva a llenarse de stubs declarativos, una entrada **no se promueve** hasta cumplir una de estas dos vías:

- **Falsable (`deep`)** — trae `example_bad`, `example_good`, una `detection` concreta y al menos una `evidence`. Si la firma es estáticamente verificable, debe además registrar un detector en [`scripts/detectors.py`](../scripts/detectors.py) probado contra sus ejemplos.
- **Doctrinal** — si es un principio conductual/epistémico sin firma estática, se marca `doctrinal: true` de forma explícita (stub por diseño, no por descuido). Fabricarle código de ejemplo está prohibido.

Un hallazgo que no es ni `deep` ni `doctrinal` declarado es un **stub** y queda en el Inbox hasta enriquecerse. La métrica `stubs` (badge en el README, calculada por [`scripts/metrics.py`](../scripts/metrics.py)) debe permanecer en **0** en el catálogo curado.

> Las plantillas bajo `Inbox/templates/` están aisladas por diseño. No son conocimiento vivo todavía; solo son moldes para nuevos hallazgos.

---

## Flujo de Ingesta

```
Fuente (Cerberus / Manual / External)
        ↓
Depositar en Inbox/<fuente>/YYYY-MM-DD_<slug>.md
        ↓
Curador valida → deduplica → mapea dominio
        ↓
Agregar entrada en golden_standard_*.yaml (status: KNOWLEDGE)
        ↓
Crear artículo en Wiki/Vices/
        ↓
Ejecutar generate_golden_audit.py
        ↓
Mover archivo a deprecated/
```
