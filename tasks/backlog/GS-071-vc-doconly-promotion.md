---
id: GS-071
title: Promote remaining 26 DOC_ONLY VC entries
status: active
priority: low
created: 2026-06-16
---

## Goal
26 VC entries are currently DOC_ONLY (not falsifiable via detector or evidence).
Promote each to PREVENTED via a real detector, or justify as doctrinal with a documented rationale.

## Acceptance criteria
- [ ] All remaining DOC_ONLY entries have either: a working detector registered, or `doctrinal: true` with justification in `notes`
- [ ] `golden_standard_metrics.json` reflects zero unjustified DOC_ONLY entries
- [ ] CI passes after catalog update

## Notes
Batch 1 completed (2026-06-16). Batch 2 promoted VC-002/010/018/024/036 (2026-06-18). 26 remain.
