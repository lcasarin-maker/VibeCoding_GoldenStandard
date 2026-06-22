---
id: GS-080
title: audit.py — enforce SP-005 session-close discipline (HANDOFF + STATE mandatory)
status: backlog
priority: medium
effort: S
created: 2026-06-22
---

## Goal

SP-005 ("Session close mandatory") is currently skipped in `audit.py` because it was
classified as behavioral. But two of its artifacts are static and checkable:
HANDOFF.md and STATE.md must be updated in the same commit that closes a task.

## Acceptance criteria

- [ ] `audit.py` adds `check_sp005()`:
  - HANDOFF.md `**Date:**` header matches today's date (YYYY-MM-DD)
  - STATE.md `**Last updated:**` header matches today's date
  - Both files are non-empty
- [ ] Failure message clearly states which header is stale and what date is expected
- [ ] SP-005 added to implemented list in audit.py success output
- [ ] Fail-first proven: stale date → exit 1

## Why

Without enforcement, HANDOFF/STATE drift silently. Next agent reads stale context.

## Blockers

none
