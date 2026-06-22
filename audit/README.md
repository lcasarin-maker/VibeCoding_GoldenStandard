# audit/ — Session records

`audit/AUDIT_TRAIL.md` — append-only index of all sessions.
`audit/sessions/` — one full record per session.

---

## Session record template

Filename: `audit/sessions/YYYY-MM-DD-NNN.md`

```markdown
# Session YYYY-MM-DD-NNN
**Agent:** [name] | **Date:** YYYY-MM-DD | **Branch:** [branch]

## What was done
- [bullet list of completed work]

## Files changed
- [path] — [what changed]

## Tests run
- [command] → [result]

## Decisions made
- [DEC-xxx] or "none"

## Blockers found
- [description] or "none"

## Tasks created
- [task file] or "none"
```

---

## AUDIT_TRAIL.md format

Each entry: `| YYYY-MM-DD | Agent | Session file | Summary (one line) |`
