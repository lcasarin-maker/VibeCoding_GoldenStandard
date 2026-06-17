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
| Memory and Headroom | [[Tokenomics/Memory_Headroom_Index|Open lens]] | `PR-084, PR-088, PR-092, PR-096` | Avoids context loss, root pollution, and forgotten learning. |
| Input and Retrieval | [[Tokenomics/Input_Retrieval_Index|Open lens]] | `PR-083, PR-090` | Reduces input noise and makes targeted retrieval more precise. |
| Output and Compaction | [[Tokenomics/Output_Compaction_Index|Open lens]] | `PR-081, PR-085, PR-087, PR-094` | Controls verbosity, cost, pruning, and documentary honesty. |
| Measurement and Telemetry | [[Tokenomics/Measurement_Telemetry_Index|Open lens]] | `PR-081, PR-091` | Makes the real savings visible, not just the intention to save. |
| Automation and Tooling | [[Tokenomics/Automation_Tooling_Index|Open lens]] | `PR-083, PR-084, PR-091` | Connects the doctrine with executable tooling and continuous observability. |

---

## Key Project Insights

| Insight | Summary |
|---|---|
| `PR-081` | Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call. |
| `PR-083` | Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing. |
| `PR-084` | Governance gate between intent and execution that enforces context discipline, observability, redaction, and state control. |
| `PR-085` | Output governance – a system can have INPUT governance (quality gates) but lack OUTPUT governance (orphan pruning), accumulating refactor residue: backups, dead code, stale plan docs, spectral scripts, divergent learning logs, stale base-sets, and IDs declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk. |
| `PR-087` | Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked. |
| `PR-088` | Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue. |
| `PR-090` | Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress. |
| `PR-091` | Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem. |
| `PR-092` | Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools. |
| `PR-094` | DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage. |
| `PR-096` | Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge. |

---

## Adjacent crossings

| Node | Relation | Reason |
|---|---|---|
| `[[Project_Insights/PR-097|PR-097]]` | Satellite hygiene | Expands the discipline of editing and validation toward daily work with tools. |
| `[[Vices/VC-056|VC-056]]` | Mirror vice | Represents the error of deprecating without analysis or traceability. |

---

## Practical reading

1. If a problem consumes context, first check `Memory and Headroom`.
2. If the problem originates in the input, check `Input and Retrieval`.
3. If the cost is in the response, check `Output and Compaction`.
4. If there is no evidence of savings, check `Measurement and Telemetry`.
5. If the doctrine does not run by itself, check `Automation and Tooling`.

---
[[Tokenomics_Index|Back to Tokenomics Index]] | [[Project_Insights_Index|Go to Insights]] | [[Home|Home]]
