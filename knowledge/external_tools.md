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
- **License:** unknown
- **Verdict:** backlog
- **Used in:** CC (pending install)
- **Origin session:** 2026-06-23
- **Rationale:** Native CC plugin (`/token-optimizer`). Audits 7 token waste signals, tracks cache preservation. Partially supersedes CACHE-001. Pending evaluation.

### [python-minifier](https://github.com/dflook/python-minifier)
- **Author/Org:** dflook
- **License:** MIT
- **Verdict:** backlog
- **Used in:** CC (pending evaluation)
- **Origin session:** 2026-06-23
- **Rationale:** Compresses Python source ~50% preserving semantics. Candidate for PreToolUse Read hook to minify Python files before they enter LLM context.

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
