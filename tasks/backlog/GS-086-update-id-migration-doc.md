---
id: GS-086
title: Update ID_MIGRATION.md to cover PR-114-121 and VC-087-091
status: done
priority: medium
effort: S
created: 2026-07-01
---

## Goal
`docs/reference/ID_MIGRATION.md` is presented as the consumer-facing ID-stability guarantee but
undercounts the live catalog: it stops at PR-113/VC-086, while the live catalogs go to PR-121
and VC-091 (found during the 2026-07-01 audit). A consumer relying only on this doc misses 8+
principle IDs and 5+ vice IDs.

## Acceptance criteria
- [ ] Add migration rows for PR-114 through PR-121
- [ ] Add migration rows for VC-087 through VC-091
- [ ] Confirm no other catalog (VT/TK/SP/AV) has the same undercount

## Blockers
none.
