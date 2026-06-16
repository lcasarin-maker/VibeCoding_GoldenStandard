# 🏛️ Golden Standard — The AI Vibe Coding Knowledge Base

> **A living, open knowledge base of antipatterns, rules, and quality principles for AI-assisted software development.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Audit](https://github.com/lcasarin-maker/VibeCoding_GoldenStandard/actions/workflows/audit.yml/badge.svg?branch=master)](https://github.com/lcasarin-maker/VibeCoding_GoldenStandard/actions/workflows/audit.yml)
[![Entries](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/badges/entries.json)](#knowledge-domains)
[![Deep](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/badges/deep.json)](Wiki/Graph.md)
[![Local detectors](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/badges/detectors.json)](scripts/detectors.py)
[![With evidence](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/badges/evidence.json)](#knowledge-domains)
[![Stubs](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/badges/stubs.json)](Wiki/Graph.md)

<!-- Badges above are generated from the catalog by scripts/metrics.py and kept in sync by CI; they cannot drift from the YAML. -->


---

## The Problem

AI-assisted programming ("vibe coding") is fast. Too fast for its own good.

It generates code that **looks** correct, tests that **look** thorough, and documentation that **looks** complete — while none of it actually works the way you think it does.

The same mistakes appear in every project, in every language, with every AI agent:

- Code that passes all tests but breaks when a real user touches it
- Tests that validate the *presence* of a file, not its *behavior*
- Features that exist in the backend but are unreachable from the UI
- Technical debt that compounds silently session after session
- Lessons learned in one project that are forgotten in the next

**The Golden Standard exists to stop that cycle.**

---

## What It Is

A structured, growing library of knowledge organized into four streams:

### 🔴 Vibe Coding Vices (`VC-xxx`)
Antipatterns specific to AI-assisted development: improvised architecture, non-reversible solutions, ghost files, hardcoded paths, invisible technical debt accumulation.

**154 entries** cataloged with severity, description, detection criteria, and mitigation.

### 🟡 Testing Vices (`VT-xxx`)
Ways tests become "security theater": checking file existence instead of behavior, mocks with no real-world correspondence, tests that pass despite broken user flows.

**116 entries** with examples of what bad tests look like and how to detect them.

### 🟢 Tokenomics
A separate governance category for efficient use of AI context tokens — because wasting tokens is also a form of technical debt. Always subordinate to code quality.

Tokenomics is navigated through its own index, a bridge map, and thematic subindices for memory/headroom, input/retrieval, output/compaction, measurement/telemetry, and automation/tooling.
The refined surfaces are memory/headroom, input/retrieval, output/compaction, measurement/telemetry, and automation/tooling.

### 🔵 Project Insights (`PI-xxx`)
Cross-cutting lessons and reusable observations that explain, connect, or contextualize the rule catalogs without duplicating them.

---

## Quick Start

### Browse the Knowledge Base

- **[Wiki Home](Wiki/Home.md)** — Entry point with category indexes
- **[Conceptual Framework](CONCEPTUAL_FRAMEWORK.md)** — Root doctrine and architectural baseline
- **[Repository Hygiene](Wiki/Concepts/Conceptual_Framework.md#5-repository-and-execution-hygiene)** — Canonical cleanup and naming doctrine
- **[Inbox](Inbox/README.md)** — Intake process for raw findings and proposed entries
- **[Audit Report](golden_standard_audit_report.md)** — Machine-generated coverage map
- **[Graph](Wiki/Graph.md)** — Local knowledge graph with hubs, intentional templates, orphan candidates, and impact paths
- **[Tokenomics Index](Wiki/Tokenomics_Index.md)** — Dedicated token-efficiency catalog
- **[Tokenomics Map](Wiki/Tokenomics_Map.md)** — Bridge between TK lenses and PI insights
- **[Coding Vices Index](Wiki/Vices/)** — All VC-xxx and VT-xxx articles
- **[YAML Catalogs](#catalogs)** — Machine-readable knowledge for tooling

### Optional Viewer

The Golden Standard is plain Markdown plus YAML plus git. You do **not** need Obsidian, Dataview, Web Clipper, or any other plugin stack for the repo to work.

If you want a nicer local reading experience, Obsidian is a good optional viewer because the `Wiki/` tree is already Obsidian-friendly.
The graph view is also generated locally in `Wiki/Graph.md` plus `golden_standard_graph.json`, so you can inspect relationships without installing any extra stack.

### Use It in Your Project

```bash
# Clone the Golden Standard as a git submodule in your project
git submodule add https://github.com/lcasarin-maker/VibeCoding_GoldenStandard.git Golden_Standard

# Or just reference it for reading
git clone https://github.com/lcasarin-maker/VibeCoding_GoldenStandard.git
```

### Run the Audit Script

```bash
# Cross-reference YAML catalogs with Wiki articles, generate audit report
python generate_golden_audit.py
```

Output: `golden_standard_audit_report.md` — shows the compliance map and generated status snapshot. CI also validates that the catalogs and Wiki stay in sync.

---

## Repository Structure

```
VibeCoding_GoldenStandard/
├── README.md                              ← You are here
├── CONCEPTUAL_FRAMEWORK.md               ← Philosophy and architecture
├── CONTRIBUTING.md                        ← How to contribute
├── CODE_OF_CONDUCT.md                     ← Community standards
│
├── golden_standard.yaml                   ← Master index
├── golden_standard_coding_vices.yaml      ← VC-xxx catalog (154 entries)
├── golden_standard_testing_vices.yaml     ← VT-xxx catalog (115 entries)
├── golden_standard_tokenomics.yaml        ← Tokenomics principles
├── golden_standard_project_insights.yaml  ← Cross-cutting lessons
│
 ├── Wiki/
 │   ├── Home.md                            ← Wiki entry point
 │   ├── Tokenomics_Index.md                ← Dedicated tokenomics index
 │   ├── Tokenomics_Map.md                  ← Bridge between tokenomics lenses and insights
 │   ├── Concepts/
 │   │   └── Conceptual_Framework.md            ← Canonical doctrine with hygiene chapter
 │   ├── Tokenomics/                        ← Individual TK articles
│   ├── Graph.md                           ← Generated graph summary
│   └── Vices/                             ← Individual articles (VC/VT)
│
├── Inbox/                                 ← Proposed entries (pending review)
├── scripts/                               ← Validation helpers for CI and local checks
│   └── validate_golden_standard_catalogs.py ← Catalog + wiki validator
├── generate_golden_audit.py               ← Audit tool
├── golden_standard_graph.json             ← Knowledge graph export
└── deprecated/                            ← Historical artifacts
```

---

## Catalogs

The knowledge is stored in human-readable YAML files:

| File | Domain | Entries |
|---|---|---|
| `golden_standard_coding_vices.yaml` | Vibe coding antipatterns | 154 |
| `golden_standard_testing_vices.yaml` | Testing failures | 116 |
| `golden_standard_tokenomics.yaml` | Token efficiency | 47 |
| `golden_standard_project_insights.yaml` | Cross-cutting insights | 35 |

**Total: 317 vices + 35 insights (352 entries).** Counts here are the source of truth and are validated against the YAML; the entries badge reflects the total number of flaws (317).

Each entry includes:
- **ID** (e.g., `VC-042`)
- **Title** and **Description**
- **Severity** (`critical`, `high`, `medium`, `low`)
- **Status** (`DOC_ONLY`, `AUDITED`, `PREVENTED`, `REMEDIATED`)
- Read the stored status through the self-describing lens tracked in issue #4: `PROPOSED` (`DOC_ONLY` / `AUDITED`), `ENFORCED_EXTERNAL` (`PREVENTED`), or `ENFORCED_LOCAL` (`REMEDIATED`).
- `DOC_ONLY` means the rule is documented in GS, not that downstream verification is forbidden. VC/VT/TK entries must declare `downstream_verification` explicitly as `required` or `none`.

> **What `PREVENTED` does and does not mean.** A `PREVENTED` status means a guard for this vice exists in a **downstream enforcing project** (e.g. Cerberus) — typically a test that fails when the vice's signature appears (such as missing JSON evidence in `.protocol/evidence/`). **This knowledge-base repo does not itself run those guards.** It catalogs the principle and names the mechanism; it does not execute it. The CI in *this* repo validates catalog/wiki integrity only. Treat `PREVENTED` as "enforceable, and enforced where Cerberus is wired in" — not as protection automatically present in any project that merely clones this repo. The human-facing enum above is the canonical reading.
>
> _Naming note:_ the "Cerberus" referenced here is this project's own downstream enforcement layer. It is **unrelated** to the unaffiliated `philips-software/cerberus` (a Java build quality-gate); a verified scan found no LLM-space repo colliding with the name.
- **Tags** (at least two normalized)
- **Detection criteria**
- **Mitigation**

---

## Operativity Principle

A knowledge entry is only **operationally active** when it has all four:

```
Principle  →  Executable Rule  →  Associated Test  →  Evidence  →  Consequence
```

Documentation alone does not make a principle real.

Entries progress through these statuses:

| Status | Meaning |
|---|---|
| `KNOWLEDGE` | Documented, not yet implemented |
| `RULE_DEFINED` | Has a mandate, no test yet |
| `TEST_ASSOCIATED` | Has a test, no evidence yet |
| `EVIDENCE_GENERATED` | Produces evidence, no consequence defined |
| `OPERATIONAL` | Full chain active |
| `BLOCKING` | Operational + can block commits |

---

## Contributing

The Golden Standard grows through real experience. If you've encountered a vibe coding failure that isn't in the catalog yet, **please contribute it**.

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the full guide.

Quick version:
1. Check the [Inbox/](Inbox/) folder and the YAML catalogs for similar/duplicate entries.
2. Open an Issue using the **"New Vice" template**, or submit a PR with the entry in YAML + a Wiki article.
3. Make the entry meet the **Definition of Done** (below). CI checks the rest.

### Definition of Done for a new entry

An entry is only merged when it is **falsifiable** or **honestly doctrinal** — never a bare stub:

- **Deep (falsifiable):** ships `example_bad`, `example_good`, a concrete `detection` recipe, and at least one `evidence` reference. If the signature is statically checkable on a snippet, also add a detector to [`scripts/detectors.py`](scripts/detectors.py) — `scripts/test_detectors.py` proves it fires on your `example_bad` and stays silent on your `example_good`.
- **Doctrinal:** if it's a behavioral/epistemic principle with no static signature, mark `doctrinal: true` explicitly. Fabricating example code for these is not allowed.
- Choose `downstream_verification` explicitly (`required` or `none`) so `DOC_ONLY` is never read as "test exempt".

The live `stubs` badge must stay at **0**, and all numbers (entries, deep %, detectors) are generated from the YAML by [`scripts/metrics.py`](scripts/metrics.py) — they can't be inflated by hand. Run `python generate_golden_audit.py` before committing; CI fails if generated artifacts, the wiki, or the badges are out of sync.

---

## Who Uses This

The Golden Standard is designed to be consumed by any agent, tool, or team that wants a portable knowledge base for AI-assisted development quality.

It is:
- **Agent-agnostic** — works with Claude, GPT, Gemini, or any AI
- **Framework-agnostic** — applies to any language or stack
- **Tool-agnostic** — can be integrated into any CI/CD or linting pipeline

---

## License

MIT — See [LICENSE](LICENSE) for details.

The knowledge is free to use, adapt, and build upon.
Attribution is appreciated but not required.

---

## Origin

Built from lessons learned during real AI-assisted development sessions in 2025–2026.
Extracted from its original enforcement lineage in June 2026 to become an independent, community-driven resource.

*The best way to fight AI-generated technical debt is to document it, name it, and share it.*
