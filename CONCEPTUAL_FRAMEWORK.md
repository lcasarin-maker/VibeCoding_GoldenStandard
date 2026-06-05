# Golden Standard — Conceptual Framework

> **The living knowledge base for AI-assisted software development quality.**

---

## What is the Golden Standard?

The Golden Standard is an **open, project-agnostic, agent-agnostic knowledge base** that catalogs the most common quality failures observed in AI-assisted software development ("vibe coding") and defines the principles, rules, and criteria needed to prevent them.

It is **not** a linter, a CI pipeline, or a specific tool.
It is **not** tied to any single programming language, framework, or AI agent.

It is a **normative knowledge repository** — a structured, growing library of:

- Coding vices (antipatterns in AI-assisted development)
- Testing vices (ways tests become "security theater")
- Tokenomics principles (efficient AI token usage without sacrificing quality)
- Project insights (cross-cutting lessons from real development sessions)

---

## Why does it exist?

AI-assisted programming ("vibe coding") enables fast development but creates structural risks:

1. Code that *looks* correct but is poorly designed
2. Tests that validate ceremonies, not real functionality
3. Partial feature implementations disconnected from actual user flows
4. Invisible accumulation of technical debt
5. Loss of institutional memory between sessions and agents
6. Repetition of already-known mistakes

The Golden Standard was created so that those lessons are **captured once and applied always**, regardless of which project, agent, or session encounters them.

---

## Knowledge Domains

### 1. Vibe Coding Vices (`VC-xxx`)
Antipatterns specific to AI-assisted development: improvised code, hardcoded paths, ghost files, non-reversible solutions, architectural shortcuts.

**Current catalog:** [`golden_standard_coding_vices.yaml`](golden_standard_coding_vices.yaml)
**Wiki:** [`Wiki/Vices/`](Wiki/Vices/)

### 2. Testing Vices (`VT-xxx`)
Ways in which tests become useless or actively misleading: tests that check file existence but not behavior, mocks with no real-world correspondence, tests that pass despite broken user flows.

**Current catalog:** [`golden_standard_testing_vices.yaml`](golden_standard_testing_vices.yaml)
**Wiki:** [`Wiki/Vices/`](Wiki/Vices/)

### 3. Tokenomics (`golden_standard_tokenomics.yaml`)
Principles for efficient use of AI context tokens during development — always subordinate to code quality.

**Current catalog:** [`golden_standard_tokenomics.yaml`](golden_standard_tokenomics.yaml)

### 4. Project Insights (`golden_standard_project_insights.yaml`)
Cross-cutting lessons from real development sessions that don't fit neatly into the vice categories but are too valuable to lose.

---

## Operativity Rule

A principle in the Golden Standard is only considered **operationally active** when it has:

1. An **executable rule** (concrete mandate)
2. An **associated test** (verifiable check)
3. **Generated evidence** (an artifact proving the check ran)
4. A **defined consequence** (what happens when it fails)

Documentation alone does not make a principle operational.

```
Golden Standard principle
       ↓
  Executable rule
       ↓
  Associated test
       ↓
  Generated evidence
       ↓
  Defined consequence
```

Each entry uses this maturity status:

| Status | Meaning |
|---|---|
| `KNOWLEDGE` | Documented but not yet implemented |
| `RULE_DEFINED` | Has a mandate but no test |
| `TEST_ASSOCIATED` | Has a test but no evidence |
| `EVIDENCE_GENERATED` | Produces evidence but no consequence |
| `OPERATIONAL` | Full chain: rule → test → evidence → consequence |
| `BLOCKING` | Operational and can block commits / merges |

---

## Repository Structure

```
VibeCoding_GoldenStandard/
├── README.md                              ← You are here
├── CONCEPTUAL_FRAMEWORK.md               ← This document
├── CONTRIBUTING.md                        ← How to contribute
├── CODE_OF_CONDUCT.md                     ← Community standards
│
├── golden_standard.yaml                   ← Master index
├── golden_standard_coding_vices.yaml      ← VC-xxx catalog
├── golden_standard_testing_vices.yaml     ← VT-xxx catalog
├── golden_standard_tokenomics.yaml        ← Tokenomics principles
├── golden_standard_project_insights.yaml  ← Cross-cutting insights
│
├── Wiki/
│   ├── Home.md                            ← Wiki entry point
│   └── Vices/                             ← Individual VC/VT articles
│       ├── VC-001.md
│       └── ...
│
├── Inbox/                                 ← Proposed new entries (pending review)
│
├── generate_golden_audit.py               ← Audit script (cross-references YAML ↔ Wiki)
│
└── deprecated/                            ← Historical artifacts (not active knowledge)
    ├── mandates_legacy/
    ├── knowledge_snapshots/
    ├── wiki_phases/
    └── planning/
```

---

## Relationship with CoderCerberus

The Golden Standard and **CoderCerberus** are two separate but correlated projects:

| | Golden Standard | CoderCerberus |
|---|---|---|
| **Nature** | Knowledge base | Enforcement tool |
| **Scope** | Universal (any project, any agent) | Specific to Cerberus-guarded projects |
| **Language** | English (primary) | Spanish + English |
| **Audience** | Any developer using AI | Users of the Cerberus protocol |
| **Repo** | `lcasarin-maker/VibeCoding_GoldenStandard` | `lcasarin-maker/protocolo-agentes` |

CoderCerberus **consumes** Golden Standard as its normative source.
Every rule in Cerberus must be traceable to a Golden Standard entry.
Every new Golden Standard entry should eventually have a Cerberus implementation.

---

## Feedback Loop

```
Real development session
        ↓
New vice / failure detected
        ↓
Documented in Golden Standard (KNOWLEDGE status)
        ↓
Rule formulated → RULE_DEFINED
        ↓
Test written → TEST_ASSOCIATED
        ↓
Evidence generated → EVIDENCE_GENERATED
        ↓
Consequence defined → OPERATIONAL
        ↓
(Optional) Implemented in CoderCerberus → BLOCKING
```

No learning should stay isolated in a single session.
Every discovery should become system-level knowledge.

---

## Origin

The Golden Standard was extracted from [CoderCerberus](https://github.com/lcasarin-maker/protocolo-agentes) in June 2026,
when it became clear that the knowledge base had value independent of any specific enforcement tool.

The original conceptual framework document is preserved in [`deprecated/knowledge_snapshots/CODERCERBERUS_MARCO_CONCEPTUAL_original.md`](deprecated/knowledge_snapshots/CODERCERBERUS_MARCO_CONCEPTUAL_original.md).
