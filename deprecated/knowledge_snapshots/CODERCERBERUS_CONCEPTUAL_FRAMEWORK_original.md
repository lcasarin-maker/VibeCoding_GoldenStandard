# CoderCerberus Conceptual Framework and Operational Philosophy
**Version:** v0.5 | **Updated:** 2026-06-13 | **Status:** SINGLE CANONICAL IDENTITY DOCUMENT

> **Normative source of rules:** [VibeCoding Golden Standard](https://github.com/lcasarin-maker/VibeCoding_GoldenStandard) — independent repository in `D:\AI\VibeCoding_GoldenStandard`
> This document does NOT duplicate GS rules. It explains what Cerberus is and why it exists.

## 1. Core idea

CoderCerberus takes its name from Cerberus, the guardian of the underworld. Its role was to prevent passage for anyone who did not meet the requirements.

That is the central philosophy: CoderCerberus is the **guardian, sentinel, and gatekeeper** for AI-assisted software projects.

Its purpose is to stop any code from reaching production if it is poorly made, malformed, fragile, undocumented, non-reversible, hard to audit, disconnected from real functionality, or built only to "pass tests" while still being a bad practice.

Cerberus does not validate formalities. It validates real quality.

The final criterion is not whether the project "looks correct". The criterion is whether it works, remains traceable, is reversible, maintainable, scalable, and usable by a human.

## 2. The problem it solves

AI-assisted development moves fast, but it creates structural risks:

1. Code that appears to work but is badly designed
2. Tests that only validate security theater
3. Features implemented only partially
4. Disconnection between backend, frontend, and user experience
5. Files created only to satisfy instructions, with no operational value
6. Non-reversible solutions and loss of traceability
7. Uncontrolled growth and invisible technical debt
8. Excessive token consumption caused by poor planning or weak structure
9. Missing institutional memory across sessions, agents, and projects
10. Repetition of errors that were already found before

CoderCerberus exists to prevent those vices from entering, staying, or reproducing.

## 3. Operator directives (Luis Casarin) — immutable

Every protocol, script, and test is evaluated against these 20 directives. They are the operator's intent.

1. I am not a programmer, I am a lawyer. The protocol cannot assume technical training.
2. The goal is vibe coding without the usual problems (drift, theater, token waste).
3. I use multiple agents at once. Token exhaustion is a critical operational issue.
4. Drift is serious. Agents make side quests and distract with suggestions that do not attack the problem.
5. Review must always go deep. Form matters, but it is not the goal. Tests must be unforgiving about substance.
6. If a project did not start inside the protocol, it gets a full adversarial audit.
7. The protocol is the governing brain for ALL projects.
8. The protocol must apply with authority to any agent: Claude, Codex, ChatGPT, Gemini.
9. When the protocol changes, the change propagates automatically to all agents and projects.
10. Discovery in a project must propagate back to the general protocol.
11. Agent permissions must be enough to operate, but never so broad that they can destroy.
12. The system must be 100% operational, not aspirational.
13. The agent must choose the right model for the task and suggest or switch automatically.
14. Always choose the minimum model necessary to protect tokens.
15. Implement token-saving strategies automatically.
16. Run periodic audits against these directives to prevent drift automatically.
17. Run periodic audits against `deprecated/` to prevent loss of functions or regressions.
18. Clear locks and blockers must exist to prevent destruction or regression.
19. 100% pass is requested, but as a consequence of real validation, not as a design goal for tests.
20. Tests come before code and are based on desired behavior.

## 4. Relationship with Golden Standard

CoderCerberus and the Golden Standard are correlated but distinct projects.

| | Golden Standard | CoderCerberus |
|---|---|---|
| **Nature** | Normative knowledge base | Enforcement tool |
| **Scope** | Universal (any project, any agent) | Projects supervised by Cerberus |
| **Repo** | `D:\AI\VibeCoding_GoldenStandard` (independent) | `D:\AI\Cerberus` |
| **Language** | English (primary) | English-first living docs, historical artifacts may still exist until migrated |

**Fundamental rule:**
> Every active Cerberus mandate must derive from an entry in the Golden Standard.
> No rule in Cerberus should exist without GS traceability.
> No critical item in GS should exist without an operational reflection in Cerberus.

**Minimum operational chain:**
```
Golden Standard -> Executable rule -> Associated test -> Generated evidence -> Defined consequence
```

Without that chain, there is no real control.

## 5. Three-layer architecture

### Layer 1 - Golden Standard
Independent Git repo at `D:\AI\VibeCoding_GoldenStandard`. Cerberus consumes it from an external path; there is no local copy.

### Layer 2 - Cerberus inside itself
This layer ensures Cerberus does not fall into the same vices it prevents. It includes its own 12D audit, compliance tests, and pre-commit enforcement.

### Layer 3 - Cerberus outside itself
Cerberus audits and blocks external projects in two moments:
1. **Real time:** pre-commit hooks with `exit 1`
2. **After the fact:** full adversarial 12D audit

## 6. Physical repository structure

```text
D:\AI\Cerberus\
├── AGENT.md / PROTOCOL_SYSTEM.md / PROTOCOL_BEHAVIOR.md  -> protocol for agents
├── SPEC.md                         -> memory bank: whitelist, architecture, handoff
├── AUDIT_TRAIL.md                    -> immutable audit trail of sessions
├── STATUS.md                       -> live status and next session
├── PLAN.md                         -> canonical forward plan
├── BACKLOG.md                      -> live debt and ordered sprints
├── scripts/                        -> shells and operational entrypoints
├── protocol_engine/                -> core logic
└── deprecated/                     -> retired artifacts and archival material
```

## 7. Canonical identity rule

Cerberus is not a generic automation repo.

Its identity is:
- a defensive quality and security guardian
- an English-first living system
- a protocol-driven core with shell-only scripts
- a repo that keeps evidence, history, and live debt separated

Legacy Spanish surfaces are treated as historical drift until they are migrated or retired.

## 8. Consolidated doctrine surface

The operational identity of Cerberus is now summarized here so the repo has one
place to answer "what is Cerberus?" and "how does it work?" without chasing
secondary mirrors.

- The three-layer architecture is the execution model: directive, orchestration,
  execution.
- The functional map is the living system view: authority, enforcement,
  coordination, memory, and support.
- The foundational directives define the operator contract that all protocol
  surfaces must honor.

The supporting docs that used to carry those slices separately are now treated
as archived reference views, not separate identity sources:

- `deprecated/docs_archive_legacy/2026-06-14/CERBERUS_FUNCTIONAL_MAP.md`
- `deprecated/docs_archive_legacy/2026-06-14/THREE_LAYER_ARCHITECTURE.md`

`deprecated/docs_archive_legacy/2026-06-14/architecture.md` remains a separately deprecated Spanish duplicate until
its code/test consumers are retired or repointed.
