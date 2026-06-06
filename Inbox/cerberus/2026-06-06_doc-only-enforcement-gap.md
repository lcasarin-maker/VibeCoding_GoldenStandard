## Metadata
- source: cerberus
- cerberus_rule_id: PENDING
- project_audited: Cerberus (self-audit) + RED-Python
- date_detected: 2026-06-06

## Classification
- proposed_domain: VC
- proposed_severity: high
- tags: [enforcement-gap, doc-only, ceremonial-validation]
- refinement_target: VC-067
- evidence_for: VC-067
- severity_challenge: ~100/139 VC del propio GS están en DOC_ONLY → patrón sistémico, no caso aislado.

## Finding

### Symptom
`CERBERUS_CONTRACT.md` exige `golden_standard_ref` en cada regla Cerberus, y la
doctrina `00 audit/02` exige purga Fase 0 antes de auditar. Pero NADA lo verifica.
La auditoría de RED-Python saltó la purga Fase 0 y, al remediar, no ancló a ningún
mandato GS ni regla Cerberus — sin que ningún gate lo detuviera.

### Cause
Los mandatos son **DOC_ONLY** (prosa); no existe PreToolUse/gate/test que los
enforce. La conformidad depende de la disciplina del agente de turno → falla.
Es la misma raíz "validación ceremonial vs funcional" de las deudas interiores
de Cerberus (#1–#6, ver HISTORIAL.md 2026-06-06).

### Context / Example
RED-Python (auditoría exterior, 2026-06): agente omitió Fase 0 + remedió libremente.
Cerberus self-audit: TK-031 bloqueó por medir el transcript entero (Deuda #4),
demostrando el mismo patrón prosa-sin-gate en el propio hub.

### Proposed Mitigation
- Cerberus añade gate (C5) que **verifica presencia de `golden_standard_ref`** en
  cada regla antes del veredicto, y **evidencia de purga Fase 0** (p.ej.
  `purge_plan.md` + `phase_0_purge_result.md`) antes de emitir veredicto exterior.
- Toda remediación debe **citar el mandato/regla aplicada** (anclaje obligatorio).
- Promover VC-067 / VC-092 / VC-108 de DOC_ONLY → PREVENTED vía este gate.

### Evidence Artifact
- HISTORIAL.md [2026-06-06] Deuda #5 (rediseño auditoría exterior) y #6.
- TK-031 block empírico: 1,270,470 tokens out medidos sobre transcript completo.

## Resolution
(curator-only — pendiente)
