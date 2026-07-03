# tasks/ — Executable work

Live work surface only. No historical items (SP-003).

```
tasks/
├── backlog/   not started
├── active/    in progress (max 1 per agent per session)
├── blocked/   waiting on dependency / human / external
├── review/    DoD met; human acceptance pending
└── done/      completed — delete file in closing commit (SP-004)
```

Agent reads HANDOFF.md NEXT → picks task → moves file to active/ → executes → done/.

---

## Task file template

Filename: `tasks/[status]/GS-NNN-short-title.md`

```markdown
---
id: GS-NNN
title: [short title]
status: backlog | active | blocked | review | done
priority: critical | high | medium | low
created: YYYY-MM-DD
---

## Goal
[one paragraph]

## Acceptance criteria
- [ ] [concrete, verifiable]
- [ ] [concrete, verifiable]

## Blockers
[description or "none"]
```

Next available ID: `grep -rh "^id: GS-" tasks/ audit/ | sort -V | tail -1` (no root-level BACKLOG.md exists — fixed 2026-07-01, GS-092).
