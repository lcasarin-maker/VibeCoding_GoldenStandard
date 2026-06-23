# Canonical Structure V3.2

**Status:** FROZEN 2026-06-22. Supersedes V2.x, V3, V3.1.
**Scope:** Multi-agent vibecoding projects.
**Primary use:** CC, GS, Aequitas OS, and satellite repositories.
**Authoritative location:** `VibeCoding_GoldenStandard/knowledge/CANONICAL_STRUCTURE.md` (this file).
**Operating principle:** no material fact lives only in chat; all unresolved work lives in `tasks/`.

---

## 1. Core Principle

> No material fact may live only in chat. If it affects the project, it is written into the project.
> There is no separate technical-debt register. Every unresolved issue is executable work and lives in `tasks/backlog/`.

One function = one home. No bridges. No "someone." 100% agent-driven.

---

## 2. Structure (CORE vs optional)

```
project/
├─ README.md                  [CORE]  Humans: what / why / how to run
├─ SPEC.md                    [CORE]  What the system IS (stable)
├─ HANDOFF.md                 [CORE]  The baton: NOW / NEXT / BLOCKERS
├─ DECISIONS.md               [CORE]  Durable decisions only (NOT a log)
├─ STATE.md                   [CORE for multi-track projects]
├─ .agents/
│   ├─ AGENTS.md              [CORE]  Single governance hub (see §6)
│   ├─ ignore_patterns.yaml   [CORE]  Shared ignore rules
│   └─ .cursorrules / .geminirules / .codexrules  (opt) IDE shims -> AGENTS.md
├─ tasks/                     [CORE]  All executable work
│   ├─ backlog/ active/ blocked/ review/ done/
│   └─ README.md              task template + movement rules
├─ audit/                     [CORE]  Evidence / history
│   ├─ AUDIT_TRAIL.md         append-only session index
│   ├─ README.md              session-record template
│   └─ sessions/              one full record per session
├─ docs/                      [CORE]  Long-form (ARCHITECTURE.md + opt subdirs)
├─ src/                       [CORE]  application code
├─ tests/                     [CORE]  test suite
├─ scripts/                   [CORE]  automation (audit.py mandatory; sync_binding.py opt)
├─ knowledge/                 (opt)   imported rules; INDEX.md required if present
├─ config/                    (opt)
└─ .gitignore                 [CORE]
```

Templates are NOT duplicated here. Each lives in its home: `tasks/README.md`, `audit/README.md`, AGENTS.md §6.

---

## 3. Deleted on Purpose (do not recreate)

BOOTSTRAP, RULES, CODE_OF_CONDUCT, PERMISSIONS, DEFINITION_OF_DONE, AGENT_CONSUMPTION,
claude/gemini/codex.md, handoffs/, TECH_DEBT.md, docs/decisions/, archive/.

| Deleted | Folded into |
|---------|-------------|
| BOOTSTRAP / RULES / PERMISSIONS / DEFINITION_OF_DONE / [agent].md | `.agents/AGENTS.md` §0–§5 |
| handoffs/ | `HANDOFF.md` (current) + `audit/sessions/` (history) |
| TECH_DEBT.md | `tasks/backlog/` |
| docs/decisions/ | `DECISIONS.md` |
| archive/ | git history |

---

## 4. Routing

```
What the system IS            -> SPEC.md
Current baton                 -> HANDOFF.md
Health across tracks          -> STATE.md
A durable reason (the "why")  -> DECISIONS.md
Work to do / risk / cleanup   -> tasks/backlog/
In-flight / blocked / review  -> tasks/active|blocked|review/
Proof of what happened        -> audit/sessions/
Index of what happened        -> audit/AUDIT_TRAIL.md
Agent behavior                -> .agents/AGENTS.md
```

DECISIONS.md records only durable architectural/governance decisions — NOT routine work ("fixed bug", "moved task"). Routine work goes to `audit/sessions/`.

Accepted temporary limitation = BOTH a DECISIONS.md entry (the why) AND a tasks/backlog/ task (the removal work). They cross-reference.

---

## 5. Permission Tiers

| Tier | edit tasks | run tests | commit | push | propose decision | accept decision |
|------|:--:|:--:|:--:|:--:|:--:|:--:|
| `full` | yes | yes | yes | yes | yes | no (human) |
| `contributor` | yes | yes | no | no | yes | no |
| `proposer` | draft only | no | no | no | yes | no |
| `observer` | no | no | no | no | yes | no |

AGENTS.md §5 maps agents to tiers in one line each. Adding an agent = one line, never a new column.

---

## 6. AGENTS.md required sections

§0 Reading order: AGENTS.md → SPEC.md → HANDOFF.md → STATE.md → knowledge/INDEX.md → task
§1 Universal rules (no fact in chat; no hidden work; small changes; inspect only files you touch)
§2 Behavior (fail loudly; one task; cite ids; any shortcut → backlog task)
§3 Permission tiers
§4 Definition of Done (tests green; audit.py passes; HANDOFF updated; session written; AUDIT_TRAIL appended; task moved)
§5 Agent→tier map + capability notes
§6 Unknown-agent fallback (observer: read/analyze/propose only)

---

## 7. Workflow

```
Phase 1 Sync    : AGENTS.md → SPEC.md → HANDOFF.md (→ STATE/knowledge if present)
Phase 2 Baton   : HANDOFF.NEXT → open task → read acceptance → check BLOCKERS
Phase 3 Execute : inspect files+deps → implement → tests → audit.py → new issues to backlog
Phase 4 Close   : task → done/ ; HANDOFF + STATE updated ; audit/sessions/NNN written ;
                  AUDIT_TRAIL appended ; material decision recorded/proposed ; commit/push
Phase 5 Handoff : next agent starts Phase 1
```

Human needed only for: BLOCKER, tier-forbidden op, decision needing acceptance, credentials/legal.

---

## 8. Acceptance Test

1. What is this project?         → README.md
2. What is the system meant to be? → SPEC.md
3. What is happening now?        → HANDOFF.md
4. What work is pending?         → tasks/backlog/
5. What happened before?         → audit/AUDIT_TRAIL.md + audit/sessions/

If these five cannot be answered fast, the structure is wrong.

---

## 9. V3.2 Additions (FROZEN 2026-06-22)

- **Mandatory session close** (SP-005): Phase 4 is required, not optional.
- **Live debt only in backlog** (SP-003): completed items deleted; git log is the archive.
- **Resolved debt → git log** (SP-004): task file deleted after closing commit.
- **Consistent structure across repos** (SP-006): `audit.py` enforces; failing audit blocks close.
- **Templates mandatory** (SP-007): `tasks/README.md`, `audit/README.md`, AGENTS.md §6 required.
- **Agent self-certifies completion** (SP-008): DoD checklist in AGENTS.md §4 all pass → done/.

*GS canonical domain: CD18 (Multi-Agent Project Governance). SP-001 to SP-010 are the enforcement rules.*