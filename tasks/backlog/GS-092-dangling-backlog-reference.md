---
id: GS-092
title: Fix dangling BACKLOG.md reference in tasks/README.md
status: done
priority: low
effort: XS
created: 2026-07-01
---

## Goal
`tasks/README.md:42` says "Next available ID: check highest GS-NNN in tasks/ + BACKLOG.md" but
no `BACKLOG.md` exists in GS root (found during the 2026-07-01 audit) — a dangling reference to
a nonexistent file.

## Acceptance criteria
- [ ] Remove the `BACKLOG.md` reference, or create it if a root-level index is actually wanted
- [ ] Point ID-lookup instructions at the real source (e.g. `grep -r "^id: GS-" tasks/ audit/`)

## Blockers
none.
