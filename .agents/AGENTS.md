# AGENTS.md — VibeCoding Golden Standard
**Single governance hub. Absorbs: AGENT_CONSUMPTION.md, CODE_OF_CONDUCT.md.**
**Version:** V3.2 canonical | **Effective:** 2026-06-22

---

## §0 Reading order

1. This file (AGENTS.md) — 3 min
2. SPEC.md → CONCEPTUAL_FRAMEWORK.md — 5 min
3. HANDOFF.md — 1 min
4. STATE.md — 1 min
5. Load only catalogs relevant to your task:
   - `golden_standard_coding_vices.yaml` (VC, 88 entries)
   - `golden_standard_testing_vices.yaml` (VT, 116 entries)
   - `golden_standard_tokenomics.yaml` (TK, 34 entries)
   - `golden_standard_principles.yaml` (PR, 113 entries)
   - `golden_standard_structure_principles.yaml` (SP, 9 entries)
6. Active task in `tasks/active/` — 2 min

**Do NOT read:** Wiki/ (generated, token-inefficient), Inbox/ (raw intake), deprecated/.

---

## §1 Universal rules

- SP-002: No material fact lives only in chat. Write it or it doesn't exist.
- SP-009: Canonicalize every decision, finding, and new work item before session ends.
- SP-003: tasks/backlog/ contains live work only. No historical items.
- SP-004: Completed task → delete file after closing commit. Git log is the record.
- One function = one home. No bridges. No "someone will fix this."
- Cite entry IDs (VC-003, SP-001) when referencing rules — traceability is non-negotiable.
- Any shortcut taken → backlog task created in the same session.

---

## §2 Behavior

- When you find a potential vice: search the relevant YAML catalog → read detection recipe → cite the ID.
- If entry is `doctrinal`: apply as governance check, not static lint.
- If entry is `deep` and has a detector: run it.
- Fail loudly. A silent skip is a hidden failure.
- One task at a time. Findings outside task scope → tasks/backlog/, not executed now.
- Plan before execution: PLAN.md with numbered steps for any multi-file change (VC-088).

---

## §3 Trust tiers

| Tier | edit tasks | run scripts | commit | push | propose decision | accept decision |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| `full` | yes | yes | yes | yes | yes | no (human) |
| `contributor` | yes | yes | no | no | yes | no |
| `proposer` | draft only | no | no | no | yes | no |
| `observer` | no | no | no | no | yes | no |

Agent below `full`: stop before commit, leave changes staged, note required action in HANDOFF.md.

---

## §4 Definition of Done

A task is done when ALL of the following are true:

- [ ] Acceptance criteria from task file are met
- [ ] Existing tests pass (`pytest tests/ -q`)
- [ ] `scripts/validate_golden_standard_catalogs.py` passes (or failure documented)
- [ ] No unresolved issue exists outside tasks/
- [ ] HANDOFF.md updated (NOW/NEXT/BLOCKERS)
- [ ] Session record written to `audit/sessions/YYYY-MM-DD-NNN.md`
- [ ] `audit/AUDIT_TRAIL.md` appended
- [ ] Any material decision recorded in DECISIONS.md (Proposed or Accepted)
- [ ] Task file moved to `tasks/done/` then deleted in closing commit

If any item is unmet: task stays in `tasks/active/` or moves to `tasks/blocked/`.

---

## §5 Agent → tier map

| Agent | Tier | Notes |
|-------|------|-------|
| Claude | full | Primary maintainer |
| Codex | full | |
| Gemini | contributor | No commit/push |
| ChatGPT | proposer | Draft and propose only |
| Unknown | observer | See §6 |

---

## §6 Unknown-agent fallback

If your identity is not in §5: default to `observer` tier.
Actions: read, analyze, propose via DECISIONS.md (status: Proposed).
Do not edit files, commit, or execute scripts until declared in §5 by a human.
