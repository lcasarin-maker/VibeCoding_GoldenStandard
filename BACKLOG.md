# Backlog — VibeCoding_GoldenStandard

**Fuente de verdad:** `/srv/ai/VibeCoding_GoldenStandard` (ATOM)
**Última actualización:** 2026-07-23

---

## §1 ABIERTOS

### G4 · Corpus de regresión de incidentes — arquitectura, nunca implementada

Registrado 2026-07-20 (`70b0771`), borrado el mismo día en `8eff949` ("Close GS backlog debt") con única justificación "Suite 2026-07-20: 88 passed" — un pase genérico de la suite de tests, no evidencia que aborde el criterio de cierre específico de este ítem. Re-registrado 2026-07-23 tras auditoría de historia git (pedida por Luis): no existe ningún commit implementador en todo el historial (`git log --all --grep` para G4/incidente/regresión/regression no devuelve nada más).

**Contexto:** los vicios (findings de calidad) deben enlazarse al incidente histórico que los motivó; sin ese enlace, un vicio se "degrada solo" (pierde relevancia/prioridad) sin que nadie decida eso explícitamente — el mismo patrón de "cierre silencioso sin evidencia" que este propio hallazgo describe para sí mismo.

**PC:** existe un corpus de regresión que enlaza cada vicio detectado a su incidente histórico origen; un vicio sin ese enlace no se degrada automáticamente sin decisión explícita registrada.

**Bloques:** ninguno — arquitectura nueva, no depende de otra deuda.

**Fecha:** 2026-07-23

### GS-TAX-001 · Verificación formal de cobertura de Falsifiability — pendiente de reconciliación de conteo

Registrado 2026-07-20 (`70b0771`), cerrado un día antes en `d7215bd` (autor: "Claude Haiku 4.5") solo porque `Wiki/Falsifiability_Report.md` existía — sin hacer la verificación formal que el criterio de cierre exige. Reabierto el mismo día en `70b0771`, vuelto a borrar horas después en `8eff949` con el mismo "88 passed" genérico. Re-registrado 2026-07-23.

**Estado verificado 2026-07-23:** `Wiki/Falsifiability_Report.md` sí existe con contenido real (479 entradas clasificadas en 5 clases de falsificabilidad vía `scripts/classify_falsifiability.py`), pero el total de 479 no concilia obviamente con la cifra original del ítem ("363→320+ entradas") y nunca se corrió el chequeo formal de "cada entrada con clase G3 asignada, conteo cuadra".

**PC:** se ejecuta y documenta la verificación formal — cada entrada del Dictamen tiene clase G3 asignada, el conteo total concilia con la fuente original o se documenta explícitamente por qué cambió (479 vs. 363→320+).

**Bloques:** ninguno.

**Fecha:** 2026-07-23
