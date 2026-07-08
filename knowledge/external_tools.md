# External Tools Catalog

Single source of truth for all external tools evaluated, adopted, or rejected in this stack.
Updated per PR-115 — every entry requires: source URL, license, verdict, and origin session.

---

## FORMAT

```
### [Tool Name](url)
- **Author/Org:** ...
- **License:** ...
- **Verdict:** adopted | backlog | rejected
- **Used in:** CC | GS | both | none
- **Origin session:** YYYY-MM-DD
- **Rationale:** ...
```

---

## Token Optimization

### [RTK — Rust Token Killer](https://github.com/rtk-ai/rtk)
- **Author/Org:** rtk-ai
- **License:** MIT
- **Verdict:** adopted
- **Used in:** CC
- **Origin session:** 2026-06-21
- **Rationale:** Reduces bash command output 60-90% before it reaches LLM context. Wired via PreToolUse Bash hook (`scripts/rtk_rewrite_hook.py`) per PR-114 equivalent-effect substitution (Windows native hook unavailable).

### [headroom-ai](https://github.com/gglucass/headroom-desktop) / [headroomlabs](https://github.com/headroomlabs-ai/headroom)
- **Author/Org:** gglucass / headroomlabs-ai
- **License:** MIT (freemium)
- **Verdict:** backlog (partial)
- **Used in:** CC (installed, proxy disabled)
- **Origin session:** 2026-06-23
- **Rationale:** Proxy invalidates Anthropic prompt cache (cache-death risk). `headroom audit-reads` and `headroom diff` adopted without proxy (HEADROOM-001, HEADROOM-002). Desktop app macOS-only.

### [LLMLingua](https://github.com/microsoft/LLMLingua)
- **Author/Org:** Microsoft
- **License:** MIT
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-06-23
- **Rationale:** Requires local 7B LLM model to compress prompts. Overhead exceeds savings for code-agent workflows. Designed for RAG/text, not code.

### [token-optimizer](https://github.com/alexgreensh/token-optimizer)
- **Author/Org:** alexgreensh
- **License:** PolyForm Noncommercial 1.0.0 (non-commercial use only)
- **Verdict:** backlog (pending manual install)
- **Used in:** CC (pending install — git clone blocked by CC auto-mode classifier)
- **Origin session:** 2026-06-23
- **Rationale:** Native CC skill (`/token-optimizer`). Audits 7 token waste signals, tracks cache preservation. Install: `git clone https://github.com/alexgreensh/token-optimizer.git ~/.claude/token-optimizer && ln -s ~/.claude/token-optimizer/skills/token-optimizer ~/.claude/skills/token-optimizer`

### [caveman](https://github.com/JuliusBrussee/caveman)
- **Author/Org:** JuliusBrussee
- **License:** MIT
- **Verdict:** adopted
- **Used in:** both
- **Origin session:** 2026-06-26
- **Rationale:** Adds a compressed-response mode and a local skill/command hub for token-efficient replies while preserving technical detail. Integrated locally via `skills/caveman/caveman-compress.md`, `.claude/commands/caveman-compress.md`, and `.agents/skills/caveman-compress.md`.

### [Ollama](https://github.com/ollama/ollama)
- **Author/Org:** Ollama
- **License:** MIT
- **Verdict:** backlog (planned)
- **Used in:** CC
- **Origin session:** 2026-06-27
- **Rationale:** Local model runtime for the new workstation; provides a clean localhost serving layer for chat and embeddings while keeping the repo off cloud dependencies.

### [Open WebUI](https://github.com/open-webui/open-webui)
- **Author/Org:** Open WebUI Inc.
- **License:** BSD-3-Clause
- **Verdict:** backlog (planned)
- **Used in:** CC
- **Origin session:** 2026-06-27
- **Rationale:** Browser UI for local providers such as Ollama or OpenAI-compatible endpoints; useful as the human-facing surface once the workstation is provisioned.

### [LM Studio](https://lmstudio.ai/)
- **Author/Org:** Element Labs / LM Studio
- **License:** Proprietary (free for home and work use)
- **Verdict:** backlog (evaluated)
- **Used in:** CC
- **Origin session:** 2026-06-27
- **Rationale:** Alternative local desktop/server stack with localhost APIs and OpenAI-compatible endpoints; keep as an evaluated fallback if the Ollama + Open WebUI stack is insufficient.

### [semble](https://github.com/MinishLab/semble)
- **Author/Org:** MinishLab
- **License:** MIT
- **Verdict:** backlog (evaluated)
- **Used in:** CC
- **Origin session:** 2026-06-26
- **Rationale:** CPU-only semantic code search for agents; install and search smoke tests succeeded on Cerberus. Promising backend for D3/D8, but direct integration into the dimensions is still pending.

### [python-minifier](https://github.com/dflook/python-minifier)
- **Author/Org:** dflook
- **License:** MIT
- **Verdict:** partially adopted (hook created, NOT wired)
- **Used in:** CC (scripts/read_minifier_hook.py created but not wired in settings.json)
- **Origin session:** 2026-06-23
- **Rationale:** Compresses Python source ~50% preserving semantics. Hook created (EVAL-002) but NOT wired because CC's Read tool uses offset/limit by line — minified 1-line files break partial reads.

## MCP / Retrieval / Evaluation

### [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- **Author/Org:** Model Context Protocol a Series of LF Projects, LLC.
- **License:** MIT
- **Verdict:** adopted
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** Official SDK provides the standard MCP transport and FastMCP server/runtime primitives, which removes the need for a hand-rolled JSON shim and keeps the wrapper aligned with the current protocol tooling.

### [Context7](https://github.com/upstash/context7)
- **Author/Org:** Upstash
- **License:** MIT
- **Verdict:** adopted
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** `ctx7` successfully resolved `anthropic` to `/anthropics/anthropic-sdk-python`, `docs` returned current Anthropic SDK examples, and `ctx7 setup --mcp --claude --project --yes --stdio` wrote the project MCP configuration plus the matching Claude rule/skill. The upstream service remains managed, but the integration is now live and usable.

### [Probe](https://github.com/probelabs/probe)
- **Author/Org:** Probe Labs
- **License:** MIT
- **Verdict:** rejected
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** `npx -y @probelabs/probe@latest` worked against `D:\AI\Cerberus`, but representative hook-search queries did not materially beat `semble`, and the result list still surfaced noisy hidden `.secrets` samples. Cerberus keeps `semble` as the default local helper.

### [Serena](https://github.com/oraios/serena)
- **Author/Org:** Oraios AI
- **License:** MIT
- **Verdict:** backlog
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** Symbol-level retrieval/editing and MCP integration are a strong fit for future refactors, but the current Cerberus workflow still lacks a concrete adoption point beyond reference value.

### [agent-learning-kit](https://github.com/future-agi/agent-learning-kit)
- **Author/Org:** Future AGI
- **License:** Apache-2.0
- **Verdict:** adopted
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** The repo now has a deterministic trajectory/evidence gate (`scripts/agent_learning_kit_evals.py`) that grades inspect/edit/verify runs, fails edit-without-verify trajectories, and is smoke-tested through `scripts/protocol_cli.py agent-evals`.

### [Claude Context](https://github.com/zilliztech/claude-context)
- **Author/Org:** Zilliz
- **License:** MIT
- **Verdict:** rejected
- **Used in:** CC
- **Origin session:** 2026-06-30
- **Rationale:** `npx -y @zilliz/claude-context-mcp@latest --help` confirmed the package and its required provider/Milvus environment. Cerberus does not have an embedding-provider key or Milvus address/token configured, so no meaningful comparison against `semble` is possible in this workspace; the local helper remains the default.

### [LightRAG](https://github.com/HKUDS/LightRAG)
- **Author/Org:** HKUDS
- **License:** MIT
- **Verdict:** partially adopted (pattern only)
- **Used in:** CC
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-033 as a possible `semantic_layer.py` upgrade. The dependency/server was rejected because it requires LLM-driven entity/relation extraction, embedding configuration, LightRAG storage backends, and usually a REST API. Its `mix` retrieval pattern was adopted in CC as a deterministic composite route that returns graph, semantic, and literal evidence together without adding LightRAG as a runtime dependency.

### [Obsidian Skills](https://github.com/kepano/obsidian-skills)
- **Author/Org:** Steph Ango / Kepano
- **License:** MIT
- **Verdict:** partially adopted
- **Used in:** GS
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-034 against the GS Wiki vault. Adopted only the `obsidian-markdown` convention layer as a GS-specific skill under `skills/obsidian-markdown/SKILL.md`; rejected `obsidian-cli`, Bases, Canvas, and Defuddle for this workflow because GS edits are file-based and validated by catalog/wiki/graph checks, not by a running Obsidian app.

### [QMD](https://github.com/tobi/qmd)
- **Author/Org:** Tobi Lutke / tobi
- **License:** MIT
- **Verdict:** partially adopted (pattern only)
- **Used in:** CC
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-035 on a temporary copy of the GS Wiki. QMD's BM25 and typed `lex:` query behavior ranked canonical ID pages strongly, but vector/hybrid mode required GGUF model embedding and did not finish an intentionally bounded local run. Cerberus adopted the exact-ID ranking lesson in `_score_record` rather than adding QMD as a runtime backend.

### [Spec Kit](https://github.com/github/spec-kit)
- **Author/Org:** GitHub
- **License:** MIT
- **Verdict:** rejected for current scope
- **Used in:** none
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-036 as an additional front-door for genuinely large new features. Its spec/plan/tasks templates add useful rigor around prioritized user stories, independent tests, constitution checks, and execution phases, but CC already has B10 `PLAN.md` plus a feature spec template, and there was no real large feature in scope to pilot. GS canonical YAML/Wiki structure was explicitly left untouched.

### [GSD Core](https://github.com/open-gsd/gsd-core)
- **Author/Org:** Open GSD
- **License:** MIT
- **Verdict:** rejected for current scope
- **Used in:** none
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-036 alongside Spec Kit. The phase loop, fresh-context discipline, `.planning/` artifacts, and explicit verification are valuable patterns for large multi-phase builds, but installing GSD Core would add a Node/slash-command workflow and generated `.planning/` surface without a live feature to measure. No GS canon files were changed.

### [ruflo ADR plugin](https://github.com/ruvnet/ruflo/tree/main/plugins/ruflo-adr)
- **Author/Org:** ruvnet
- **License:** MIT
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated narrowly for CC-037. The ADR lifecycle, relationship vocabulary, index, and compliance-review idea are useful, but the plugin's actual contract depends on `@claude-flow/cli`, AgentDB namespaces (`adr-patterns`, `adr-edges`), and ruflo skill/command infrastructure. CC keeps durable decisions in `DECISIONS.md` and session state in `HANDOFF.md`, so adding the plugin would duplicate existing logs while importing the very platform surface this task excluded.

### [pxpipe](https://github.com/teamchong/pxpipe)
- **Author/Org:** teamchong
- **License:** MIT
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-07-04
- **Rationale:** Evaluated for CC-038 only on non-critical archived handoff context via npm `pxpipe-proxy@0.8.0` installed under `%TEMP%`. Local render measurements showed large token savings, but the blind visual gist check lost exact operational details and upstream documents lossy exact-string recall with silent confabulation risk. Not adopted for code, audit findings, evidence logging, IDs, hashes, or compliance outputs.

### [OpenWiki](https://github.com/langchain-ai/openwiki)
- **Author/Org:** LangChain AI
- **License:** MIT
- **Verdict:** partially adopted (wrapper/pattern only)
- **Used in:** Cerberus containment tooling
- **Origin session:** 2026-07-07
- **Rationale:** Evaluated for CC-040 against `openwiki@0.0.2`. Upstream docs/package declare an MIT Node >=20 CLI that writes `openwiki/`, may mutate top-level `AGENTS.md`/`CLAUDE.md`, and stores provider credentials in `~/.openwiki/.env`. CC installed it only under `%TEMP%`, ran sandboxed `--help`, `--dry-run --init --print`, and no-key `--init --print`; the real no-key run failed before generation with zero changed files. Runtime inspection confirmed `LocalShellBackend`, `openwiki/.last-update.json`, agent-prompt mutation instructions, and provider env handling. Direct unsupervised runs against CC are rejected and now shell-audited; only the contained sandbox-report pattern is adopted via `scripts/openwiki_sandbox.py`.

### [Agent Skills](https://github.com/addyosmani/agent-skills)
- **Author/Org:** Addy Osmani
- **License:** MIT
- **Verdict:** partially adopted (pattern only)
- **Used in:** GS
- **Origin session:** 2026-07-07
- **Rationale:** GS adopted the anti-rationalization table pattern as the optional `rationalizations` field in vice entries, with the field documented in `CONTRIBUTING.md` and demonstrated on VC-002. The full plugin/skill pack was not adopted; only the excuse/rebuttal schema pattern was reused with attribution.

---

## JavaScript Minifiers (evaluated, not adopted)

### [terser](https://github.com/terser/terser)
- **Author/Org:** terser-js (fork of uglify-es)
- **License:** BSD-2-Clause
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-06-23
- **Rationale:** JS only. CC stack is Python-first. Not applicable.

### [minify (coderaiser)](https://github.com/coderaiser/minify)
- **Author/Org:** coderaiser
- **License:** MIT
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-06-23
- **Rationale:** JS/CSS/HTML/img minifier. No Python support. Not applicable.

### [MinifyAll](https://github.com/Josee9988/MinifyAll)
- **Author/Org:** Josee9988
- **License:** GPL-3.0
- **Verdict:** rejected
- **Used in:** none
- **Origin session:** 2026-06-23
- **Rationale:** VS Code extension only. No CLI/hook integration. Not applicable.
