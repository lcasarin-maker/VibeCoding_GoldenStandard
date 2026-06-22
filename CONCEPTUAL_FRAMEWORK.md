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
Tokenomics is a separate governance category, not a vice catalog. It covers efficient use of AI context tokens during development — always subordinate to code quality.

It is organized around five operational lenses: memory/headroom, input/retrieval, output/compaction, measurement/telemetry, and automation/tooling.

**Current catalog:** [`golden_standard_tokenomics.yaml`](golden_standard_tokenomics.yaml)

### 4. Principles (`golden_standard_principles.yaml`)
Cross-cutting doctrine captured as first-class rules. These principles may be behavioral, operational, or graph-governance oriented; they exist to connect and contextualize the catalogs without duplicating them.

### 5. Canonical Domains (`Wiki/Domains/README.md`)
GS uses canonical domains (`CDxx`) as its semantic routing layer.

These domains are:

- stable problem spaces,
- separate from enforcement mechanisms,
- separate from runtime channels,
- separate from debt state,
- and separate from historical numbering conventions.

Their purpose is to make the knowledge graph operational:

- principles route into domains,
- domains define boundaries and exclusions,
- graph hubs become semantically meaningful,
- downstream consumers can map their own dimensions to the same ontology.

---

### 6. Repository and Execution Hygiene
Golden Standard also treats the execution surface as part of quality.

The repository should stay clean, descriptive, and auditable:

- temporary files should be removed or isolated;
- names should explain function, not advertise importance;
- helper scripts should be reusable, not disposable clutter;
- validation should prefer the simplest deterministic command;
- elevated permissions should be the exception, not the default;
- tooling steps should be reproducible and easy to inspect.
- the canonical GS surface should stay pure: no wrapper layers, shim layers, fake bridges, or ceremonial stubs in executable or schema logic.

This rule is formalized as `PI-019` so execution hygiene can be tracked as reusable project insight, not just as local advice.

---

## Knowledge Graph Governance

Golden Standard is not only a set of files; it is a navigable graph of knowledge.

To keep that graph useful instead of decorative:

- every active VC, VT, TK, and PI entry should connect to at least one index, map, or related concept page;
- zero-degree live nodes should be treated as suspicious unless they are intentional templates or deprecated artifacts;
- hub pages deserve first review when a catalog changes, because they carry the largest impact surface;
- graph exports are evidence artifacts, not just visualization output;
- intentional isolation must be explicit, not accidental.
- canonical domain pages are semantic graph hubs, not decorative indexes.

The graph layer is what makes GS easier to audit adversarially: it reveals clusters, bridges, and gaps that linear reading hides.

Protocol documents should also be written with explicit confidence discipline:

- `VERIFIED` for claims backed by logs, tests, or generated evidence;
- `INFERRED` for claims deduced from indirect evidence;
- `ASSUMED` for reasonable but unverified statements.

That tagging discipline makes semantic lint practical, because the lint can distinguish fact from inference instead of treating all prose equally.

Two additional operating rules come with that discipline:

- keep an explicit uncertainty ledger for claims, paths, and subsystems that were not mechanically verified in the current session;
- check shared state before editing when multiple sessions or agents may be active, so concurrent work is not overwritten silently.

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

Every VC/VT/TK catalog entry must declare `downstream_verification` explicitly so downstream tools do not mistake
documentation for exemption. Use `required` when the consumer repo should enforce the lesson with a test or harness,
and `none` when no consumer-side test is expected.

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
├── golden_standard_principles.yaml        ← Cross-cutting doctrine
│
├── Wiki/
│   ├── Home.md                            ← Wiki entry point
│   ├── Domains/                           ← Canonical domain hubs (`CDxx`)
│   └── Vices/                             ← Individual VC/VT articles
│       ├── VC-001.md
│       └── ...
│
├── Inbox/                                 ← Proposed new entries (pending review)
│
│   └── generate_golden_audit.py           ← Audit script (cross-references YAML ↔ Wiki)
│
└── deprecated/                            ← Historical artifacts (not active knowledge)
    ├── mandates_legacy/
    ├── knowledge_snapshots/
    ├── wiki_phases/
    └── planning/
```

---

## Golden Standard Lineage

Golden Standard is now a standalone knowledge base with its own canonical source of truth, public documentation, and generated wiki.

Its historical lineage includes an earlier enforcement context, but that lineage is no longer the active framing for this repository.
Legacy materials are preserved in git history (tag `pre-reset-2026-06-20`) for traceability and historical context.

---

## Source Ecosystem

Knowledge enters the Golden Standard through **authorized sources** with defined contracts.
See [`KNOWLEDGE_SOURCES.md`](knowledge/KNOWLEDGE_SOURCES.md) for the full source registry.

```
┌─────────────────┐    Inbox/manual/      ┌──────────────────────────────────┐
│  Manual / DRI   │ ──────────────────▶  │                                  │
└─────────────────┘                       │       Golden Standard            │
                                          │   (knowledge base — agnostic)    │
┌─────────────────┐    Inbox/external/    │                                  │
│  Community      │ ──────────────────▶  │   VC-xxx  VT-xxx  TK-xxx  PI-xxx │
└─────────────────┘                       │                                  │
                                          └──────────────────────────────────┘
                                                         │
                                                         │ (normative source)
                                                         └─────────────── consumed by any agent, tool, or team
```

## Feedback Loop

```
Source detects failure (manual session / external contribution / future automation)
        ↓
Deposit in Inbox/<source>/YYYY-MM-DD_<slug>.md  [see INGESTION_PROTOCOL.md]
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
(Optional) Implemented in a consuming system → BLOCKING
```

No learning should stay isolated in a single session.
Every discovery should become system-level knowledge.

---

## Origin

The Golden Standard was extracted from its original enforcement lineage in June 2026,
when it became clear that the knowledge base had value independent of any specific enforcement tool.

The original conceptual framework document is preserved in the historical snapshots under `deprecated/knowledge_snapshots/` for traceability.

---

## Shared Vocabulary (with attribution)

The Golden Standard adopts established community terminology so its entries align with the
language practitioners already use. Terms are attributed to their origin:

- **Context engineering** — the discipline of deliberately shaping an agent's context window
  (what goes in, what is pruned, what is cached). Popularized by HumanLayer and Tobi Lütke / Shopify (2025).
  See `VC-128` (context poisoning), `VC-131` (architecture drift), and the Tokenomics catalog.
- **Frequent Intentional Compaction (FIC)** — periodically summarizing and resetting context to
  keep utilization in a healthy band. Origin: HumanLayer ACE. See `TK-031`, `TK-044`.
- **AGENTS.md** — the emerging convention for a repo-level agent instruction file
  (>20k repos by 2025). Relevant to handoff and decision-externalization vices (`VC-045`, `VC-131`).
- **Context poisoning** — unverified/hallucinated claims that persist in context and self-reinforce.
  Community term; cataloged as `VC-128`.
- **Over-mocked / assertion-free tests** — test-theater patterns measured empirically in
  arxiv:2602.00409. Cataloged across the `VT-xxx` family (e.g. `VT-006`, `VT-023`).
- **Slopsquatting** — supply-chain risk from AI-hallucinated package names. Cataloged as `VC-129`.

These terms are descriptive anchors, not new claims; each links to the catalog entry that operationalizes it.
