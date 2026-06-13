# Tokenomics Index

Tokenomics is a category of its own in the Golden Standard. It does not describe code or testing vices: it describes how to reduce noise, preserve headroom, compact context, and externalize state without sacrificing quality.

The practical utility of this category is twofold:

1. prevent the agent from burning context on rereads, verbose outputs, or poor handoffs;
2. turn token savings into a measurable discipline, not an intuition.

Historically, this layer was operated under names like *headspace*, *compact*, and *token saving*. GS preserves the knowledge and also defines the doctrine of use.

---

## Subindices

- [[Memory_Headroom_Index|Memory and Headroom]]
- [[Input_Retrieval_Index|Input and Retrieval]]
- [[Output_Compaction_Index|Output and Compaction]]
- [[Measurement_Telemetry_Index|Measurement and Telemetry]]
- [[Automation_Tooling_Index|Automation and Tooling]]
- [[Tokenomics_Map|Tokenomics Map]]

---

## Category status

| Status | Entries |
|---|---:|
| `PREVENTED` / `REMEDIATED` | 35 |
| `DOC_ONLY` / `AUDITED` | 12 |
| `Total` | 47 |

---

## Entries

*   [[Tokenomics/TK-001|TK-001]] — **Missing checkpoint** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-002|TK-002]] — **Chat memory as the primary source** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-003|TK-003]] — **Project switch without closure** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-004|TK-004]] — **Re-explained setup** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-005|TK-005]] — **Prose-heavy handoff** (PREVENTED, medium, downstream:none)
*   [[Tokenomics/TK-006|TK-006]] — **Manual history merge** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-007|TK-007]] — **Duplicated source of truth** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-008|TK-008]] — **Empirical memory segregation** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-009|TK-009]] — **Semantic pruning** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-010|TK-010]] — **Contextual retrieval** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-011|TK-011]] — **Structured delimiters** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-012|TK-012]] — **Exploration tax** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-013|TK-013]] — **Bloated tool schemas** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-014|TK-014]] — **Full read by default** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-015|TK-015]] — **Whole file for a specific question** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-016|TK-016]] — **Giant multi-objective prompt** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-017|TK-017]] — **Narrated permissions** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-018|TK-018]] — **Backlog mixed with the objective** (PREVENTED, medium, downstream:none)
*   [[Tokenomics/TK-019|TK-019]] — **Hierarchical Dependency Skeleton** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-020|TK-020]] — **Output constraint** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-021|TK-021]] — **Prefilling** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-022|TK-022]] — **Example optimization** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-023|TK-023]] — **Raw logs** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-024|TK-024]] — **Summary without density** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-025|TK-025]] — **Verbose audit output** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-026|TK-026]] — **Noisy observability** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-027|TK-027]] — **Lexical Compression of Diagnostics** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-028|TK-028]] — **Stable context caching** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-029|TK-029]] — **Batch processing** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-030|TK-030]] — **Capability cascade** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-031|TK-031]] — **Context compaction** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-032|TK-032]] — **Cache cliff** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-033|TK-033]] — **No headroom** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-034|TK-034]] — **Invisible rollback cost** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-035|TK-035]] — **Thinking with the execution tool** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-036|TK-036]] — **Response without a mode** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-037|TK-037]] — **Forgettable manual monitoring** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-038|TK-038]] — **Full-state re-reading** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-039|TK-039]] — **Non-integrated external tools** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-040|TK-040]] — **Promised savings not measured** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-041|TK-041]] — **Invisible quotas** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-042|TK-042]] — **Manifests without a size constraint** (REMEDIATED, medium, downstream:none)
*   [[Tokenomics/TK-043|TK-043]] — **Entropy without pruning — input governance without output governance** (PREVENTED, low, downstream:none)
*   [[Tokenomics/TK-044|TK-044]] — **Accumulated tokenomics debt (Cost Compounding)** (PREVENTED, medium, downstream:none)
*   [[Tokenomics/TK-F01|TK-F01]] — **Reprocessing stable context** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-F02|TK-F02]] — **Primitive context pruning** (DOC_ONLY, low, downstream:required)
*   [[Tokenomics/TK-F03|TK-F03]] — **Excessive verbal output** (DOC_ONLY, low, downstream:required)

---
## Usage reference

- Tokenomics defines principles of efficiency and context management.
- The real enforcement of these principles belongs to the consuming repositories and tools that adopt GS.
- The category's vocabulary must be kept separate from VC and VT to avoid semantic confusion.
- Modern noise-reduction strategies, like RTK and ICM, confirm that token savings benefit from filtering tools, external memory, and context compaction.

---
[[Home|Back to Home]]
