# PLAN.md — FASE 2 GS / Correcciones adversariales 2026-07-10

Este plan ejecuta la parte GS de la auditoría adversarial 2026-07-10, con
contexto en `docs/AUDITORIA_ADVERSARIAL_2026-07-10.md`. El plan maestro
original de Aequitas_OS (`PLAN_MAESTRO_CORRECCIONES_2026-07-10.md`) fue
consolidado y eliminado por redundante; su contenido vigente vive en
`Aequitas_OS/BACKLOG_MAESTRO_v3.md`.

## B10 — aprobación requerida

No se tocará código, configuración de CI, catálogo ni artefactos generados hasta que el responsable apruebe explícitamente este plan.

Regla S19: todo reemplazo será eliminación + creación. No se conservará `scripts/generate_golden_audit.py` como shim ni se añadirá compatibilidad transitoria. La eliminación del archivo viejo y la creación del paquete nuevo deberán quedar en el mismo commit.

## 1. Baseline y contrato de no-regresión

1.1. Registrar el estado inicial de trabajo y ejecutar la CLI existente con `--audit-only`, `--wiki-only` y el flujo de receipts.

1.2. Copiar los artefactos de referencia en un directorio temporal: `Wiki/`, `output/*.json`, reportes Markdown y badges.

1.3. Definir una comparación byte a byte que ignore únicamente timestamps explícitamente identificados; cualquier otra diferencia será fallo.

1.4. Confirmar que la suite y la auditoría actual pasan antes de iniciar la partición.

## 2.4-GS — partición de `generate_golden_audit.py`

2.4.1. Crear el paquete `gs_generator/` con módulos `audit/`, `wiki/`, `graph/` y `badges/`, separando responsabilidades sin cambiar reglas, orden de salida, nombres, formatos ni rutas de la CLI.

2.4.2. Mantener un entrypoint delgado que conserve exactamente `--audit-only`, `--wiki-only` y receipts, incluyendo códigos de salida, mensajes y comportamiento por defecto.

2.4.3. Ejecutar la generación antes/después y exigir diff byte-idéntico de `Wiki/`, `output/*.json` y badges, con timestamps como única excepción permitida.

2.4.4. Eliminar `scripts/generate_golden_audit.py` con `git rm` en el mismo commit que crea el paquete y el nuevo entrypoint; verificar que no queda shim ni import indirecto de compatibilidad.

## 2.5-GS — Semgrep y conversión probada

2.5.1. Añadir reglas Semgrep versionadas para los vicios ALTA estáticamente detectables: VC-095 secretos, VC-115 `eval`, VC-109 paths hardcodeados, VT-040 `except` ciego, VT-043 `exit(0)` incondicional y VT-005/VT-009 asserts vacuos.

2.5.2. Para cada regla añadir al menos un fixture positivo y uno negativo, ejecutar Semgrep sobre ambos y guardar evidencia reproducible en la suite.

2.5.3. Registrar el mapeo regla↔vicio en el catálogo y cambiar un vicio a `PREVENTED` únicamente cuando la regla y sus fixtures hayan pasado; los vicios sin enforcement pasan a `DOC_ONLY` con trigger de promoción falsable.

## 2.6 — ratchet GS, evidencia y deduplicación

2.6.1. Extender `scripts/gs_lint.py`: cualquier vicio nuevo de severidad ALTA sin detector, regla Semgrep o justificación falsable provoca fallo; la justificación debe estar vinculada al ID y ser verificable por una prueba.

2.6.2. Clasificar entradas de `Wiki/Evidence` como `primary`, `internal-generic` o `pending`; hacer que `metrics.py` y badges cuenten solamente `primary` para evidencia.

2.6.3. Impedir por lint las colisiones de `Wiki/Detectors`: un único archivo canónico por ID de vicio, sin placeholders ni duplicados.

2.6.4. Añadir pruebas de regresión para el ratchet, clasificación de evidencia y deduplicación.

## 2.8-GS — CI y cierre

2.8.1. Añadir job en `ubuntu-latest` que ejecute pytest en matriz Python 3.10–3.13, `scripts/audit.py` (8/8) y Semgrep con las reglas versionadas.

2.8.2. Verificar pytest verde en Python 3.10 y 3.13 y conservar logs de ambas ejecuciones, además del resultado 8/8 de `audit.py` y la salida Semgrep.

2.8.3. Re-generar y comparar artefactos; el cierre exige diff vacío salvo timestamps.

2.8.4. Actualizar la deuda `GS-AUD-001`, `GS-AUD-003`, `GS-AUD-005` y `GS-AUD-006` con evidencia concreta: reglas/fixtures, módulos particionados y diff de artefactos, clasificación de evidencia y deduplicación.

2.8.5. Limpiar `__pycache__` multi-versión, comprobar que no quedan archivos temporales y dejar un resumen de comandos, versiones, logs y vicios convertidos a `PREVENTED`.

## Criterios de aceptación

- Aprobación explícita de B10 registrada antes de tocar código.
- `scripts/generate_golden_audit.py` eliminado y reemplazado por `gs_generator/` sin shim.
- CLI exacta y receipts preservados.
- Artefactos byte-idénticos salvo timestamps.
- Cada regla Semgrep tiene positivo/negativo y evidencia; `legacy review` no es un estado permitido.
- Ratchet, clasificación `primary|internal-generic|pending` y deduplicación cubiertos por lint/tests.
- CI ejecuta pytest 3.10–3.13, `audit.py` 8/8 y Semgrep.
- GS-AUD-001/003/005/006 actualizados con evidencia y cierre reproducible.

El estado operativo vive en `STATE.md`, `HANDOFF.md`, `audit/AUDIT_TRAIL.md` y `tasks/backlog/`.
