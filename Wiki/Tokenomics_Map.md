# Tokenomics Map

This map serves as a bridge between the `TK` category and the GS satellite lessons. It does not repeat the catalog: it shows how to read it and which insights it crosses.

## What it is for

- Navigate relations between context vices, token savings, and operational discipline.
- Identify which satellite lessons reinforce each tokenomics lens.
- Detect gaps where doctrine exists, but a supporting artifact or clear telemetry is still missing.

---

## Operational lenses

| Lens | Subindex | Related Project Insights | Intent |
|---|---|---|---|
| Memory and Headroom | [[Tokenomics/Memory_Headroom_Index|Open lens]] | `PI-006, PI-010, PI-014, PI-018` | Avoids context loss, root pollution, and forgotten learning. |
| Input and Retrieval | [[Tokenomics/Input_Retrieval_Index|Open lens]] | `PI-005, PI-012` | Reduces input noise and makes targeted retrieval more precise. |
| Output and Compaction | [[Tokenomics/Output_Compaction_Index|Open lens]] | `PI-003, PI-007, PI-009, PI-016` | Controls verbosity, cost, pruning, and documentary honesty. |
| Measurement and Telemetry | [[Tokenomics/Measurement_Telemetry_Index|Open lens]] | `PI-003, PI-013` | Makes the real savings visible, not just the intention to save. |
| Automation and Tooling | [[Tokenomics/Automation_Tooling_Index|Open lens]] | `PI-005, PI-006, PI-013` | Connects the doctrine with executable tooling and continuous observability. |

---

## Key Project Insights

| Insight | Summary |
|---|---|
| `PI-003` | Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call. [REMEDIATED Sprint 5: track_tokens.py wired to the D10 gate; visibility confirmed.] |
| `PI-005` | Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing. [NOT_APPLICABLE Sprint 10: analysis of 36 external repos showed LiteLLM is useful as an architectural reference but the provider abstraction layer is already covered by Cerberus gates; declarative integration, not executable.] |
| `PI-006` | Cerberus v0.3 – gate between intent and execution that enforces context discipline, observability, redaction, and state control. [ACTIVE Sprint 5-11: WARN to BLOCK in the APPROVED gate (recommendations only with FAILs); 12D domains (D1-D12); 386 adversarial tests; 17 synchronized satellites; verb_noun naming normalized; Golden Standard = pure knowledge (PI-015..PI-018 formalized).] |
| `PI-007` | Output governance (Cerberus diagnosis 2026-05-30) – the system had INPUT governance (quality gates) but not OUTPUT governance (orphan pruning), so it accumulated refactor residue: 250MB of backups, dead code, 5 plan docs, spectral scripts, divergent GLOBAL_LEARNING, stale base-set, IDs TK-043/44/45 declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk. Executable in PLAN.md P0 (orphan-hunt) / P1 (vulture/VC-118) / P5 (catalog=execution). |
| `PI-009` | Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked. [IMPLEMENTED Sprint 5: [RECOMMENDATIONS BY DOMAIN] suppressed from the APPROVED gate (non-blocking noise); it only appears when there are domain FAILs to guide the fix. Failing-first test validates both branches. Refactored _print_recommendations (C901 compliance).] |
| `PI-010` | Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue. |
| `PI-012` | Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress. |
| `PI-013` | Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem. |
| `PI-014` | Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools. |
| `PI-016` | DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage. |
| `PI-018` | Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge. |

---

## Adjacent crossings

| Node | Relation | Reason |
|---|---|---|
| `[[Project_Insights/PI-019|PI-019]]` | Satellite hygiene | Expands the discipline of editing and validation toward daily work with tools. |
| `[[Vices/VC-124|VC-124]]` | Mirror vice | Represents the error of deprecating without analysis or traceability. |

---

## Practical reading

1. If a problem consumes context, first check `Memory and Headroom`.
2. If the problem originates in the input, check `Input and Retrieval`.
3. If the cost is in the response, check `Output and Compaction`.
4. If there is no evidence of savings, check `Measurement and Telemetry`.
5. If the doctrine does not run by itself, check `Automation and Tooling`.

---
[[Tokenomics_Index|Back to Tokenomics Index]] | [[Project_Insights_Index|Go to Insights]] | [[Home|Home]]
