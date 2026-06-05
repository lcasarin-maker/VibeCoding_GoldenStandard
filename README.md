# 🏛️ Golden Standard — The AI Vibe Coding Knowledge Base

> **A living, open knowledge base of antipatterns, rules, and quality principles for AI-assisted software development.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Knowledge Entries](https://img.shields.io/badge/vices%20cataloged-600%2B-blue.svg)](#knowledge-domains)

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

A structured, growing library of knowledge organized into three domains:

### 🔴 Vibe Coding Vices (`VC-xxx`)
Antipatterns specific to AI-assisted development: improvised architecture, non-reversible solutions, ghost files, hardcoded paths, invisible technical debt accumulation.

**600+ entries** cataloged with severity, description, detection criteria, and mitigation.

### 🟡 Testing Vices (`VT-xxx`)
Ways tests become "security theater": checking file existence instead of behavior, mocks with no real-world correspondence, tests that pass despite broken user flows.

**100+ entries** with examples of what bad tests look like and how to detect them.

### 🟢 Tokenomics
Principles for efficient use of AI context tokens — because wasting tokens is also a form of technical debt. Always subordinate to code quality.

---

## Quick Start

### Browse the Knowledge Base

- **[Wiki Home](Wiki/Home.md)** — Entry point with category indexes
- **[Coding Vices Index](Wiki/Vices/)** — All VC-xxx and VT-xxx articles
- **[YAML Catalogs](#catalogs)** — Machine-readable knowledge for tooling

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

Output: `golden_standard_audit_report.md` — shows which entries have full Wiki coverage and which are missing documentation.

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
├── golden_standard_coding_vices.yaml      ← VC-xxx catalog (600+ entries)
├── golden_standard_testing_vices.yaml     ← VT-xxx catalog (100+ entries)
├── golden_standard_tokenomics.yaml        ← Tokenomics principles
├── golden_standard_project_insights.yaml  ← Cross-cutting lessons
│
├── Wiki/
│   ├── Home.md                            ← Wiki entry point
│   └── Vices/                             ← Individual articles (VC/VT)
│
├── Inbox/                                 ← Proposed entries (pending review)
├── generate_golden_audit.py               ← Audit tool
└── deprecated/                            ← Historical artifacts
```

---

## Catalogs

The knowledge is stored in human-readable YAML files:

| File | Domain | Entries |
|---|---|---|
| `golden_standard_coding_vices.yaml` | Vibe coding antipatterns | 600+ |
| `golden_standard_testing_vices.yaml` | Testing failures | 100+ |
| `golden_standard_tokenomics.yaml` | Token efficiency | — |
| `golden_standard_project_insights.yaml` | Cross-cutting insights | — |

Each entry includes:
- **ID** (e.g., `VC-042`)
- **Title** and **Description**
- **Severity** (`critical`, `high`, `medium`, `low`)
- **Detection criteria**
- **Mitigation**
- **Operativity status**

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
1. Check the [Inbox/](Inbox/) folder for similar proposed entries
2. Check the YAML catalogs to avoid duplicates
3. Open an Issue using the **"New Vice" template**
4. Or submit a PR directly with the entry in YAML + a Wiki article

---

## Who Uses This

The Golden Standard is the normative source for **[CoderCerberus](https://github.com/lcasarin-maker/protocolo-agentes)**, an AI agent quality protocol that uses these catalogs to enforce coding standards in real projects.

But the knowledge base is designed to be:
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
Extracted from the CoderCerberus protocol in June 2026 to become an independent, community-driven resource.

*The best way to fight AI-generated technical debt is to document it, name it, and share it.*
