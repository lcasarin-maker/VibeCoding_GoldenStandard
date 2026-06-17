# Principles

The 113 principles are first-class doctrinal rules. They are governance knowledge, not mechanically detectable vices.

---

| ID | Title | Note |
|---|---|---|
| PR-001 | Unassumed incompetence | doctrinal |
| PR-002 | Blind trust | doctrinal |
| PR-003 | Demo as quality | doctrinal |
| PR-004 | Aesthetics as integrity | doctrinal |
| PR-005 | Non-human audit of the core | doctrinal |
| PR-006 | Operational optimism | doctrinal |
| PR-007 | Contaminated self-audit | doctrinal |
| PR-008 | Failure not turned into doctrine | doctrinal |
| PR-009 | Fake human test | doctrinal |
| PR-010 | "Looks good" as a metric | doctrinal |
| PR-011 | Free top score | doctrinal |
| PR-012 | Audit false positive | doctrinal |
| PR-013 | Agent as autonomous engineer | doctrinal |
| PR-014 | Blind fix | doctrinal |
| PR-015 | Patched symptom | doctrinal |
| PR-016 | Unreproduced bug | doctrinal |
| PR-017 | Speed over precision | doctrinal |
| PR-018 | Illusory productivity | doctrinal |
| PR-019 | Building without validation | doctrinal |
| PR-020 | Vague specification | doctrinal |
| PR-021 | Excessive assumptions | doctrinal |
| PR-022 | Sidequest | doctrinal |
| PR-023 | Closure pressure | doctrinal |
| PR-024 | Decisions without a why | doctrinal |
| PR-025 | Lost clarifications | doctrinal |
| PR-026 | Premature victory | doctrinal |
| PR-027 | Unaudited maintainability | doctrinal |
| PR-028 | Operational drift | doctrinal |
| PR-029 | Correction loops | doctrinal |
| PR-030 | Patches over patches | doctrinal |
| PR-031 | Production without a technical owner | doctrinal |
| PR-032 | Skipped pre-deprecation rescue | doctrinal |
| PR-033 | Non-binding state | doctrinal |
| PR-034 | Mixed audiences | doctrinal |
| PR-035 | Undirected update | doctrinal |
| PR-036 | Contextual saturation | doctrinal |
| PR-037 | Context rot | doctrinal |
| PR-038 | No prior checkpoint | doctrinal |
| PR-039 | Decentralized state | doctrinal |
| PR-040 | Concurrency without quarantine | doctrinal |
| PR-041 | Opaque routing | doctrinal |
| PR-042 | Textual memory merge | doctrinal |
| PR-043 | Architectural black box | doctrinal |
| PR-044 | Implicit policies | doctrinal |
| PR-045 | Normative conflicts | doctrinal |
| PR-046 | Module without biocontainment | doctrinal |
| PR-047 | Blind chunking | doctrinal |
| PR-048 | Critical code sliced up | doctrinal |
| PR-049 | Unverified integrations | doctrinal |
| PR-050 | Documentation hijack | doctrinal |
| PR-051 | Ignored regressive compatibility | doctrinal |
| PR-052 | Ornamental observability | doctrinal |
| PR-053 | Evasive wrapper | doctrinal |
| PR-054 | Error tolerated by policy | doctrinal |
| PR-055 | Skipped reconnaissance | doctrinal |
| PR-056 | Optimistic security | doctrinal |
| PR-057 | Mixed security | doctrinal |
| PR-058 | Late tests | doctrinal |
| PR-059 | Happy path only | doctrinal |
| PR-060 | No chaos | doctrinal |
| PR-061 | Non-functional ignored | doctrinal |
| PR-062 | Poor debug | doctrinal |
| PR-063 | UI without real use | doctrinal |
| PR-064 | Security boundary by convention | doctrinal |
| PR-065 | Lock Panic and Fast Syntactic Patching (Lock Panic Shortcut) | doctrinal |
| PR-066 | Reasoning Lock-In & AI Runaway loops (Chain-Pattern Interrupts) | doctrinal |
| PR-067 | Reprocessing stable context | doctrinal |
| PR-068 | Primitive context pruning | doctrinal |
| PR-069 | Excessive verbal output | doctrinal |
| PR-070 | Semantic pruning | doctrinal |
| PR-071 | Contextual retrieval | doctrinal |
| PR-072 | Structured delimiters | doctrinal |
| PR-073 | Full read by default | doctrinal |
| PR-074 | Whole file for a specific question | doctrinal |
| PR-075 | Narrated permissions | doctrinal |
| PR-076 | Hierarchical Dependency Skeleton | doctrinal |
| PR-077 | Batch processing | doctrinal |
| PR-078 | Capability cascade | doctrinal |
| PR-079 | Deptry – reconciliation of imports against declared dependencies to detect missing, unused, transitive, misplaced dev, and stdlib declared as dependencies. | doctrinal |
| PR-080 | Diagnostic assertions – when a test fails, the message must explain the discrepancy with actionable clarity. Real verified tools: pytest native assertion rewriting, pytest-clarity / pytest-icdiff for readable diffs, flake8-assertive for correct assertion methods. (Corrects a prior reference to a nonexistent package — see VC-061 hallucinated dependency.) | promotion candidate |
| PR-081 | Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call. | doctrinal |
| PR-082 | Trivy – multi-surface scanning (images, filesystem, git, VMs, Kubernetes) for CVEs, secrets, misconfigurations, SBOM, and licenses. | doctrinal |
| PR-083 | Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing. | doctrinal |
| PR-084 | Governance gate between intent and execution that enforces context discipline, observability, redaction, and state control. | doctrinal |
| PR-085 | Output governance – a system can have INPUT governance (quality gates) but lack OUTPUT governance (orphan pruning), accumulating refactor residue: backups, dead code, stale plan docs, spectral scripts, divergent learning logs, stale base-sets, and IDs declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk. | doctrinal |
| PR-086 | Batch of predictable authorizations – group permissions, clarifications, and decisions before a long run to avoid interruptions, rereads, and reactive work. | doctrinal |
| PR-087 | Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked. | doctrinal |
| PR-088 | Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue. | doctrinal |
| PR-089 | Descriptive names and simple topology – prefer scripts and modules that explain their purpose and flatten structure when it reduces cognitive friction. | doctrinal |
| PR-090 | Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress. | promotion candidate |
| PR-091 | Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem. | doctrinal |
| PR-092 | Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools. | doctrinal |
| PR-093 | Circularity ratchet – every new vice must break a real circular relationship and drain the baseline in batches; coverage that does not reduce the circle is still theater. | doctrinal |
| PR-094 | DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage. | doctrinal |
| PR-095 | Anti many-to-one coverage – a test that claims to cover N vices at once loses discrimination; each guard must isolate the failure it claims to protect against. | promotion candidate |
| PR-096 | Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge. | doctrinal |
| PR-097 | Execution and tooling hygiene – prefer simple commands, declarative edits, UTF-8, auditable evidence, and elevated permissions only as an exception; temporary helpers must disappear unless they are reusable and documented. | doctrinal |
| PR-098 | Confidence Tags (Graphify pattern) – every state claim in protocol documents must carry an explicit confidence level: VERIFIED (backed by terminal log or test), INFERRED (deduced from indirect evidence), ASSUMED (no evidence, reasonable supposition). Claims without a tag are treated as ASSUMED. Applies especially to protocol specs, audit logs, and architectural decision comments. Origin: safishamsi/graphify confidence tag system for knowledge graphs. | doctrinal |
| PR-099 | Semantic Wiki-Lint (Karpathy LLM Wiki pattern) – protocol documents must be audited periodically to detect: contradictions between sections, references to nonexistent files, mandates mentioned in one doc but absent in another, and inconsistent version claims. The Lint is not syntactic (that is handled by a syntactic catalog linter) but semantic: do two documents claim incompatible things about the same state? Origin: Karpathy LLM Wiki gist, Lint operation of the agent-maintained wiki framework. | promotion candidate |
| PR-100 | Operational uncertainty list – every session or protocol document must declare which subsystems, routes, or claims were not mechanically verified in that turn. The absence of a list equals incomplete verification. Origin: operational uncertainty discipline and anti-hallucination control. | doctrinal |
| PR-101 | Dual-session awareness – before touching shared sources, the agent must verify state and latest commits so as not to step on concurrent work. If there are external changes, impact is analyzed before editing. Origin: multi-agent coexistence discipline and serialized shared-source access. | doctrinal |
| PR-102 | Hub-based review – nodes with the highest fan-in or impact degree must be reviewed first when a catalog or index changes. The graph is not decorative: it prioritizes risk and orders the audit. Origin: hub-first review heuristic (graph fan-in prioritization). | doctrinal |
| PR-103 | Exportable retrospective – every session must close with a structured, parseable retrospective that is persisted to a durable ledger before a context reset (COMPACT/CLEAR). Chat is not reliable memory and new knowledge must survive the reset. Origin: structured-retrospective export and a durable ledger as a source of continuity. | doctrinal |
| PR-104 | Exhaustive preflight and no reopening scope post-execution – before executing any change, the agent must declare scope, foreseeable impacts, out-of-scope follow-ups, and the runner/loader that would be affected if the topology changes. If a new improvement emerges after executing, it is first recorded in the backlog; it is not offered as a post-execution suggestion. Origin: execution hygiene and the formal separation of audits between knowledge and consumption. | doctrinal |
| PR-105 | Serialization of Git operations – Git commands must be executed serially within automations and orchestrators to avoid index locks, state races, and inconsistent results. When coordination or concurrent tooling exists, the safe discipline is a single Git flow at a time with controlled retries, not opportunistic parallelism. Origin: global learning on race conditions and .git/index.lock locking. | doctrinal |
| PR-106 | Vibe Check (PV-Bhat/vibe-check-mcp-server, verified) – metacognition MCP server that curbs agent tunnel-vision and runaway loops via Chain-Pattern Interrupts; a direct implementation of the PR-066 mitigation. | doctrinal |
| PR-107 | vibecheck (yuvrajangadsingh/vibecheck, verified) – ESLint for AI slop: a local linter that detects code smells in AI-generated code (hardcoded secrets, eval, empty catch); evidence that the catalog vices are statically detectable. | doctrinal |
| PR-108 | viberails (refractionPOINT/viberails, verified) – AI Firewall that intercepts risky agent operations (Claude Code, Cursor, Gemini CLI) via hooks; an enforcement layer conceptually comparable to a policy-enforcement gate (unrelated to the homonym philips-software/cerberus). | doctrinal |
| PR-109 | ratelimit (tomasbasham/ratelimit, verified) – rate limiting decorator (@limits + sleep_and_retry) as a concrete control against PR-031 (quota as surprise) and the tokenomics debt (TK-034). | doctrinal |
| PR-110 | context7 (upstash/context7, verified) -- delivers up-to-date code documentation to LLMs to avoid calls to obsolete or nonexistent APIs; a direct mitigation of PR-044. | doctrinal |
| PR-111 | Persistent memory layer (byterover-cli / zilliztech claude-context-memsearch, verified) -- durable cross-session memory for agents; its discipline (source, date, reconciliation) mitigates PR-045. | doctrinal |
| PR-112 | serena (oraios/serena, verified) -- symbol-level (semantic) retrieval and editing so that recovered context is correct; mitigates VC-069 against blind chunking. | doctrinal |
| PR-113 | Auditing stochastic systems – when behavior depends on chance, sampling, retries, probabilistic routing, or non-deterministic generation, it is not evaluated with a single run nor with an exact value. The rule is to declare the target distribution, seed when applicable, sample size, acceptable thresholds, and repetition criterion; if the surface should be deterministic, the randomness is eliminated rather than disguised as controlled. Claims about stability or correctness must be reproducible across several runs, not just plausible in one. Origin: GS audit of stochastic systems; complements VT-028 on controlled randomness. | doctrinal |

---
[[Home|Back to Home]]
