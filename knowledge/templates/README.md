# Templates

Canonical schemas for GS governance files. Enforced by `scripts/audit.py`.

| Template | Used for | Required headers enforced by |
|----------|----------|------------------------------|
| TASK_template.md | tasks/backlog/*.md | audit.py check_sp007 |
| STATE_template.md | STATE.md | audit.py check_sp005 |
| HANDOFF_template.md | HANDOFF.md | audit.py check_sp005 |

## Rules

- Copy the template; fill in all fields; delete placeholder text.
- `effort` values: XS (<30min), S (<2h), M (<4h), L (<8h), XL (>8h).
- `priority` values: high, medium, low.
- All fields in TASK frontmatter are required. Missing any → audit.py exits 1.
