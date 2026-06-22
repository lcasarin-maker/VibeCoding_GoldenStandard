---
id: GS-077
title: Create scripts/audit.py for SP-001..009 auto-enforcement
status: backlog
priority: medium
created: 2026-06-22
---

## Goal
SP-001..009 are all RULE_DEFINED but have no automated enforcement. Create
`scripts/audit.py` that checks the repo against each SP rule and reports violations.

## Acceptance criteria
- [ ] `scripts/audit.py` checks presence of all V3.2 canonical structure files
- [ ] SP-002 check: warns if material fact found only in chat-format files (heuristic)
- [ ] SP-003 check: no done/blocked files in tasks/backlog/
- [ ] SP-004 check: no files in tasks/done/ (should be deleted in closing commit)
- [ ] Integrated into CI or runnable as pre-commit step
- [ ] SP entries updated from RULE_DEFINED to TEST_ASSOCIATED

## Blockers
none
