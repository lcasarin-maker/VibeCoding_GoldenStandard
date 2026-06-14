# Satellite Insights Index

Mapping of lessons extracted from reference repositories and external audit tools.
Entries are grouped by type to distinguish actionable principles from system meta-commentary.

---

## 🟢 Actionable principles

_Cross-cutting lessons that change how work is done._ (17)

*   [[Project_Insights/PI-008|PI-008]] — Batch of predictable authorizations – group permissions, clarifications, and decisions before a long run to avoid interruptions, rereads, and reactive work.
*   [[Project_Insights/PI-009|PI-009]] — Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked.
*   [[Project_Insights/PI-010|PI-010]] — Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue.
*   [[Project_Insights/PI-011|PI-011]] — Descriptive names and simple topology – prefer scripts and modules that explain their purpose and flatten structure when it reduces cognitive friction.
*   [[Project_Insights/PI-012|PI-012]] — Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress.
*   [[Project_Insights/PI-013|PI-013]] — Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem.
*   [[Project_Insights/PI-015|PI-015]] — Circularity ratchet – every new vice must break a real circular relationship and drain the baseline in batches; coverage that does not reduce the circle is still theater.
*   [[Project_Insights/PI-016|PI-016]] — DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage.
*   [[Project_Insights/PI-017|PI-017]] — Anti many-to-one coverage – a test that claims to cover N vices at once loses discrimination; each guard must isolate the failure it claims to protect against.
*   [[Project_Insights/PI-019|PI-019]] — Execution and tooling hygiene – prefer simple commands, declarative edits, UTF-8, auditable evidence, and elevated permissions only as an exception; temporary helpers must disappear unless they are reusable and documented.
*   [[Project_Insights/PI-022|PI-022]] — Operational uncertainty list – every session or protocol document must declare which subsystems, routes, or claims were not mechanically verified in that turn. The absence of a list equals incomplete verification. Origin: operational uncertainty discipline and anti-hallucination control.
*   [[Project_Insights/PI-023|PI-023]] — Dual-session awareness – before touching shared sources, the agent must verify state and latest commits so as not to step on concurrent work. If there are external changes, impact is analyzed before editing. Origin: multi-agent coexistence discipline and serialized shared-source access.
*   [[Project_Insights/PI-024|PI-024]] — Hub-based review – nodes with the highest fan-in or impact degree must be reviewed first when a catalog or index changes. The graph is not decorative: it prioritizes risk and orders the audit. Origin: hub-first review heuristic (graph fan-in prioritization).
*   [[Project_Insights/PI-025|PI-025]] — Exportable retrospective – every session must close with a structured, parseable retrospective that is persisted to a durable ledger before a context reset (COMPACT/CLEAR). Chat is not reliable memory and new knowledge must survive the reset. Origin: structured-retrospective export and a durable ledger as a source of continuity.
*   [[Project_Insights/PI-026|PI-026]] — Exhaustive preflight and no reopening scope post-execution – before executing any change, the agent must declare scope, foreseeable impacts, out-of-scope follow-ups, and the runner/loader that would be affected if the topology changes. If a new improvement emerges after executing, it is first recorded in the backlog; it is not offered as a post-execution suggestion. Origin: execution hygiene and the formal separation of audits between knowledge and consumption.
*   [[Project_Insights/PI-027|PI-027]] — Serialization of Git operations – Git commands must be executed serially within automations and orchestrators to avoid index locks, state races, and inconsistent results. When coordination or concurrent tooling exists, the safe discipline is a single Git flow at a time with controlled retries, not opportunistic parallelism. Origin: global learning on race conditions and .git/index.lock locking.
*   [[Project_Insights/PI-035|PI-035]] — Auditing stochastic systems – when behavior depends on chance, sampling, retries, probabilistic routing, or non-deterministic generation, it is not evaluated with a single run nor with an exact value. The rule is to declare the target distribution, seed when applicable, sample size, acceptable thresholds, and repetition criterion; if the surface should be deterministic, the randomness is eliminated rather than disguised as controlled. Claims about stability or correctness must be reproducible across several runs, not just plausible in one. Origin: GS audit of stochastic systems; complements VT-028 on controlled randomness.

---

## 🔧 Reference tools and techniques

_Pointers to verified external tools and reusable patterns._ (14)

*   [[Project_Insights/PI-001|PI-001]] — Deptry – reconciliation of imports against declared dependencies to detect missing, unused, transitive, misplaced dev, and stdlib declared as dependencies.
*   [[Project_Insights/PI-002|PI-002]] — Diagnostic assertions – when a test fails, the message must explain the discrepancy with actionable clarity. Real verified tools: pytest native assertion rewriting, pytest-clarity / pytest-icdiff for readable diffs, flake8-assertive for correct assertion methods. (Corrects a prior reference to a nonexistent package — see VC-129 hallucinated dependency.)
*   [[Project_Insights/PI-003|PI-003]] — Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call.
*   [[Project_Insights/PI-004|PI-004]] — Trivy – multi-surface scanning (images, filesystem, git, VMs, Kubernetes) for CVEs, secrets, misconfigurations, SBOM, and licenses.
*   [[Project_Insights/PI-005|PI-005]] — Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing.
*   [[Project_Insights/PI-020|PI-020]] — Confidence Tags (Graphify pattern) – every state claim in protocol documents must carry an explicit confidence level: VERIFIED (backed by terminal log or test), INFERRED (deduced from indirect evidence), ASSUMED (no evidence, reasonable supposition). Claims without a tag are treated as ASSUMED. Applies especially to protocol specs, audit logs, and architectural decision comments. Origin: safishamsi/graphify confidence tag system for knowledge graphs.
*   [[Project_Insights/PI-021|PI-021]] — Semantic Wiki-Lint (Karpathy LLM Wiki pattern) – protocol documents must be audited periodically to detect: contradictions between sections, references to nonexistent files, mandates mentioned in one doc but absent in another, and inconsistent version claims. The Lint is not syntactic (that is handled by a syntactic catalog linter) but semantic: do two documents claim incompatible things about the same state? Origin: Karpathy LLM Wiki gist, Lint operation of the agent-maintained wiki framework.
*   [[Project_Insights/PI-028|PI-028]] — Vibe Check (PV-Bhat/vibe-check-mcp-server, verified) – metacognition MCP server that curbs agent tunnel-vision and runaway loops via Chain-Pattern Interrupts; a direct implementation of the VC-120 mitigation.
*   [[Project_Insights/PI-029|PI-029]] — vibecheck (yuvrajangadsingh/vibecheck, verified) – ESLint for AI slop: a local linter that detects code smells in AI-generated code (hardcoded secrets, eval, empty catch); evidence that the catalog vices are statically detectable.
*   [[Project_Insights/PI-030|PI-030]] — viberails (refractionPOINT/viberails, verified) – AI Firewall that intercepts risky agent operations (Claude Code, Cursor, Gemini CLI) via hooks; an enforcement layer conceptually comparable to a policy-enforcement gate (unrelated to the homonym philips-software/cerberus).
*   [[Project_Insights/PI-031|PI-031]] — ratelimit (tomasbasham/ratelimit, verified) – rate limiting decorator (@limits + sleep_and_retry) as a concrete control against VC-110 (quota as surprise) and the tokenomics debt (TK-044).
*   [[Project_Insights/PI-032|PI-032]] — context7 (upstash/context7, verified) -- delivers up-to-date code documentation to LLMs to avoid calls to obsolete or nonexistent APIs; a direct mitigation of VC-135.
*   [[Project_Insights/PI-033|PI-033]] — Persistent memory layer (byterover-cli / zilliztech claude-context-memsearch, verified) -- durable cross-session memory for agents; its discipline (source, date, reconciliation) mitigates VC-136.
*   [[Project_Insights/PI-034|PI-034]] — serena (oraios/serena, verified) -- symbol-level (semantic) retrieval and editing so that recovered context is correct; mitigates VC-137 against blind chunking.

---

## ⚪ Meta-system (about the Golden Standard itself)

_Insights that describe GS governance; useful but they do not teach an external technique._ (4)

*   [[Project_Insights/PI-006|PI-006]] — Governance gate between intent and execution that enforces context discipline, observability, redaction, and state control.
*   [[Project_Insights/PI-007|PI-007]] — Output governance – a system can have INPUT governance (quality gates) but lack OUTPUT governance (orphan pruning), accumulating refactor residue: backups, dead code, stale plan docs, spectral scripts, divergent learning logs, stale base-sets, and IDs declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk.
*   [[Project_Insights/PI-014|PI-014]] — Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools.
*   [[Project_Insights/PI-018|PI-018]] — Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge.

---
[[Home|Back to Home]]
