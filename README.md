# 🏛️ Golden Standard — The AI Vibe Coding Knowledge Base

> **A living, open knowledge base of antipatterns, rules, and quality principles for AI-assisted software development.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Audit](https://github.com/lcasarin-maker/VibeCoding_GoldenStandard/actions/workflows/audit.yml/badge.svg?branch=master)](https://github.com/lcasarin-maker/VibeCoding_GoldenStandard/actions/workflows/audit.yml)
[![Entries](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/docs/badges/entries.json)](#catalogs)
[![Deep](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/docs/badges/deep.json)](Wiki/Graph.md)
[![Local detectors](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/docs/badges/detectors.json)](scripts/detectors.py)
[![With evidence](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/docs/badges/evidence.json)](#catalogs)
[![Stubs](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lcasarin-maker/VibeCoding_GoldenStandard/master/docs/badges/stubs.json)](Wiki/Graph.md)

<!-- Badges are generated from the catalog by scripts/metrics.py and kept in sync by CI. -->

---

## The Problem

AI-assisted programming ("vibe coding") is fast. Too fast for its own good.

It generates code that **looks** correct, tests that **look** thorough, and documentation that **looks** complete — while none of it actually works the way you think it does. The same mistakes appear in every project, in every language, with every AI agent — and lessons learned in one session are forgotten in the next.

**The Golden Standard exists to stop that cycle.**

→ For the full epistemological framing, see **[CONCEPTUAL_FRAMEWORK.md](CONCEPTUAL_FRAMEWORK.md)**.

---

## Quick Start

- **[Wiki Home](Wiki/Home.md)** — Entry point with category indexes
- **[Conceptual Framework](CONCEPTUAL_FRAMEWORK.md)** — What GS is, why it exists, domains, operativity rule
- **[Audit Report](output/golden_standard_audit_report.md)** — Machine-generated coverage map
- **[Graph](Wiki/Graph.md)** — Knowledge graph: hubs, orphan candidates, impact paths
- **[Canonical Domains](Wiki/Domains/README.md)** — Semantic domain taxonomy (`CDxx`)
- **[Inbox](Inbox/README.md)** — Intake process for raw findings
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — How to add a new entry

```bash
# Use as a git submodule
git submodule add https://github.com/lcasarin-maker/VibeCoding_GoldenStandard.git Golden_Standard

# Or clone for reading
git clone https://github.com/lcasarin-maker/VibeCoding_GoldenStandard.git

# Regenerate audit artifacts after editing catalogs
python scripts/generate_golden_audit.py
```

---

## Catalogs

| File | Domain | Entries |
|---|---|---|
| `golden_standard_coding_vices.yaml` | Vibe coding antipatterns | 94 |
| `golden_standard_testing_vices.yaml` | Testing failures | 116 |
| `golden_standard_tokenomics.yaml` | Token efficiency | 34 |
| `golden_standard_principles.yaml` | Principles | 121 |
| `golden_standard_structure_principles.yaml` | Structure principles | 10 |
| `golden_standard_adversarial_vectors.yaml` | Adversarial vectors | 104 |

**Total: 479 entries.** CI recalculates all six table rows and this total from the
live YAML through `validate_golden_standard_catalogs.py`; catalog shape and strict
SemVer compatibility are separately fixed by the G-03 consumer-contract tests.

Each entry includes ID, title, description, severity, status, detection criteria, and mitigation. See [CONCEPTUAL_FRAMEWORK.md](CONCEPTUAL_FRAMEWORK.md) for the full status model (`DOC_ONLY` → `PREVENTED` → `REMEDIATED`).

---

## License

MIT — See [LICENSE](LICENSE) for details. The knowledge is free to use, adapt, and build upon.

*Built from lessons learned during real AI-assisted development sessions in 2025–2026.*
