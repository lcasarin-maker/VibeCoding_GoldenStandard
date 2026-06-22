---
id: GS-081
title: Enforced templates for STATE.md, HANDOFF.md, and backlog task files
status: backlog
priority: medium
effort: S
created: 2026-06-22
---

## Goal

STATE.md, HANDOFF.md, and backlog task files exist but have no enforced schema.
Each agent can drift the format. Templates + audit checks lock the shape.

## Acceptance criteria

- [ ] `knowledge/templates/STATE_template.md` — canonical schema with required headers:
  `Catalog health`, `Migration status`, `Open backlog`, `CI status`
- [ ] `knowledge/templates/HANDOFF_template.md` — canonical schema:
  `Agent`, `Date`, `Branch`, `NOW`, `NEXT`, `BLOCKERS`
- [ ] `knowledge/templates/TASK_template.md` — canonical frontmatter:
  `id`, `title`, `status`, `priority`, `effort`, `created` + sections `Goal`, `Acceptance criteria`, `Why`, `Blockers`
- [ ] `audit.py check_sp007()` extended: verify all 6 frontmatter fields present in every
  backlog/*.md (currently only checks id/title/status)
- [ ] README in `knowledge/templates/` explains when to use each
- [ ] Templates replicated to CC repo and any satellite using V3.2 structure

## Why

Consistent structure → any agent (or human) can read STATE/HANDOFF cold without
reverse-engineering the format. Also enables automated parsing (GS-080 date checks).

## Blockers

GS-080 (date check depends on canonical HANDOFF header format)
