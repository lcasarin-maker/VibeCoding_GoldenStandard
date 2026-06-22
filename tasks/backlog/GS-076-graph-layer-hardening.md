---
id: GS-076
title: Graph layer hardening (connectivity check + live debt table)
status: backlog
priority: low
created: 2026-06-16
---

## Goal
`Wiki/Graph.md` count drifts from YAML. Validator checks wiki existence but not graph
connectivity. The validation-debt table is static and doesn't auto-regenerate.

## Acceptance criteria
- [ ] Connectivity check added to `validate_golden_standard_catalogs.py`
- [ ] `Wiki/Graph.md` counts regenerate on commit (no manual update needed)
- [ ] Validation-debt table regenerates from live data

## Blockers
none
