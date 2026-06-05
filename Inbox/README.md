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
- [`external/README.md`](external/README.md) — flujo para issues y PRs externos.
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
