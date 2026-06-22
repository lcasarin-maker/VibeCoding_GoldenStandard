---
id: GS-075
title: Split generate_golden_audit.py (audit-report vs wiki generation)
status: backlog
priority: low
created: 2026-06-16
---

## Goal
`generate_golden_audit.py` (~77KB) mixes audit-report generation and wiki generation.
Split into two independently testable modules.

## Acceptance criteria
- [ ] Audit-report generation and wiki generation are in separate scripts/modules
- [ ] Each module has at least one test verifying it runs independently
- [ ] A documented fallback exists if either breaks
- [ ] Original behavior preserved end-to-end

## Blockers
none
