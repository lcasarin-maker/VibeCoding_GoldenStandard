# Independent Adversarial Audit Report — Golden Standard

**Date:** 2026-06-16  
**Auditor:** Independent agent, adversarial mode  
**Scope:** Golden Standard repository (`D:\AI\VibeCoding_GoldenStandard`)  
**Mandate:** Verify directly against live repository. Do not trust status files, changelogs, badges, or previous audits.  

---

## A. Executive Summary

Golden Standard (GS) is a **real, substantial, and largely coherent** knowledge base of 352 cataloged entries (154 vibe-coding vices, 116 testing vices, 47 tokenomics principles, 35 project insights) with a hybrid architecture of YAML catalogs, generated wiki, and machine-readable graph exports. It has genuine value as an agent-agnostic, project-agnostic rule repository.

However, the audit found **material contamination, structural inconsistencies, and truth inflation** that weaken its claim to be a pure, independent standard:

| Finding | Severity |
|---|---|
| **CoderCerberus contamination in active files** | High |
| **Spanish text in active documentation** | High |
| **Broken link to `CERBERUS_CONTRACT.md`** | Medium |
| **Project-specific jargon in canonical backlog** | Medium |
| **Spanish badge labels** | Medium |
| **Status claims are aspirational without independent verification** | Medium |
| **Ingestion Protocol shows stale schema** | Medium |
| **Deprecated area contains 600+ lines of Spanish planning docs** | Low |
| **Wiki entries are largely template-generated and thin** | Low |
| **Graph metrics have minor count discrepancies** | Low |

**Verdict:** GS works as a real knowledge base but does **not** fully work as an independent standard. It tells the truth about entry counts and detector counts, but it inflates the meaning of `PREVENTED` status, contains active references to a downstream enforcer it claims not to depend on, and violates its own English-only and purity rules in several active files. **Remediation is required before GS can credibly claim agnostic independence.**

---

## B. Live Inventory

### Repository Structure (verified from `find`)

```
VibeCoding_GoldenStandard/
├── README.md                              ← Live, verified counts
├── CONCEPTUAL_FRAMEWORK.md               ← Doctrine, references Cerberus lineage
├── CONTRIBUTING.md                        ← Rules, but references issue #4 (unverifiable)
├── CODE_OF_CONDUCT.md                     ← Standard
├── CONSUMER_CONTRACT.md                   ← Boundary doc with Cerberus; extensive refs
├── INGESTION_PROTOCOL.md                  ← Shows stale schema (no depth fields)
├── KNOWLEDGE_SOURCES.md                   ← Lists Cerberus as "Primary Source"; broken link
├── BACKLOG.md                            ← Debt ledger; project jargon contamination
├── AUDIT_TRAIL.md                         ← 9 lines; recent claims
├── LICENSE                               ← MIT
│
├── golden_standard.yaml                   ← Master index (4 catalogs listed) ✓
├── golden_standard_coding_vices.yaml      ← 154 entries, 4075 lines ✓
├── golden_standard_testing_vices.yaml     ← 116 entries, 3736 lines ✓
├── golden_standard_tokenomics.yaml        ← 47 entries, 1373 lines ✓
├── golden_standard_project_insights.yaml  ← 35 entries, 199 lines ✓
│
├── golden_standard_metrics.json           ← Generated; 0 stubs, 16 detectors ✓
├── golden_standard_graph.json             ← Generated; 388 nodes, 1946 edges
├── golden_standard_audit.json             ← Generated coverage map
├── golden_standard_audit_report.md        ← Generated; 438 lines
│
├── generate_golden_audit.py               ← 77KB; hardcoded Cerberus dimension mappings
├── scripts/
│   ├── detectors.py                       ← 16 real detectors, tested ✓
│   ├── test_detectors.py                  ← Proves detectors against catalog ✓
│   ├── metrics.py                         ← Generates badges; Spanish labels in badges
│   ├── validate_golden_standard_catalogs.py ← 752 lines; validates schema + wiki sync
│   ├── migrate_ax020.py                   ← Project-specific migration script
│   └── harden_metadata.ps1                ← PowerShell helper; purpose unclear
│
├── tests/
│   ├── test_infrastructure.py             ← Infrastructure tests
│   └── test_project_insight_promotion_gate.py ← Synthetic promotion gate test
│
├── Wiki/
│   ├── Home.md                            ← Generated; "TV" typo for "VT"
│   ├── Vices_Index.md                     ← Generated; 282 lines
│   ├── Tokenomics_Index.md                ← Generated; still lists TK-F01..F03
│   ├── Project_Insights_Index.md         ← 65 lines; categorized
│   ├── Principles.md                      ← Generated; 35 PI ledger
│   ├── Graph.md                           ← Generated; 159 lines
│   ├── Tokenomics_Map.md                  ← 61 lines; bridge doc
│   ├── Concepts/Conceptual_Framework.md   ← Duplicates root doctrine
│   ├── Domains/D1..D12.md                 ← 12 thin routing pages; Cerberus refs
│   ├── Vices/VC-001..VC-154.md           ← 154 wiki pages
│   ├── Vices/VT-001..VT-116.md           ← 116 wiki pages
│   ├── Tokenomics/TK-001..TK-044.md      ← 44 pages + 5 subindex pages + 3 F-pages
│   └── Project_Insights/PI-001..PI-035.md ← 35 pages
│
├── Inbox/
│   ├── README.md                          ← **IN SPANISH** — violates English-only rule
│   ├── cerberus/README.md                 ← References Cerberus
│   ├── manual/README.md                   ← Standard
│   ├── external/README.md                 ← Standard
│   └── templates/                         ← 3 templates + README
│
├── badges/                                ← 6 JSON badge files
│   ├── entries.json, deep.json, evidence.json, detectors.json, stubs.json, ai-native.json
│   └── evidence.json & detectors.json have Spanish labels ("con evidencia", "detectores locales")
│
├── deprecated/
│   ├── README.md                          ← English, clean
│   ├── knowledge_snapshots/               ← Historical Cerberus framework doc
│   ├── planning/                          ← 5 Spanish docs (GS_remediation_plan, SCOPE_AUDIT,
│   │                                          NORMALIZATION_MANDATE, NORMALIZATION_SUMMARY,
│   │                                          CONCEPTUAL_FRAMEWORK_AUDIT_PLAN, AUDIT_EXECUTION_GUIDE)
│   │                                      ← 600+ lines of Spanish, Cerberus-specific planning
│   └── wiki_phases/                       ← 4 completion docs (historical)
│
├── .github/
│   ├── workflows/audit.yml                ← CI workflow
│   ├── ISSUE_TEMPLATE/                    ← 2 templates
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .gitattributes, .gitignore            ← Standard
├── .claude/settings.local.json           ← IDE config; should be gitignored
├── .protocol/                            ← Empty or near-empty directory
├── __pycache__/                          ← Python cache in repo
├── .pytest_cache/                        ← Pytest cache in repo
├── .ruff_cache/                          ← Ruff cache in repo
```

### Classification of Suspicious Files/Folders

| File/Folder | Status | Action | Reason |
|---|---|---|---|
| `Inbox/README.md` | **Active** | **Rewrite** | Entire file is Spanish; violates repo's English-only rule |
| `KNOWLEDGE_SOURCES.md` | **Active** | **Edit** | Broken link to `CERBERUS_CONTRACT.md`; rename to `CONSUMER_CONTRACT.md` |
| `BACKLOG.md` | **Active** | **Edit** | Contains project-specific jargon: "Eje 6", "AX-020", "AX-023", "AX-024" |
| `badges/evidence.json` | **Active** | **Edit** | Label is "con evidencia" (Spanish) |
| `badges/detectors.json` | **Active** | **Edit** | Label is "detectores locales" (Spanish) |
| `scripts/migrate_ax020.py` | **Active** | **Move to deprecated/** | Project-specific migration script; no longer needed for daily operation |
| `scripts/harden_metadata.ps1` | **Active** | **Investigate** | Purpose unclear; may be dead code |
| `.claude/settings.local.json` | **Active** | **Add to .gitignore** | IDE-specific settings should not be in repo |
| `.protocol/` | **Active** | **Investigate** | Empty or near-empty; why is it in active tree? |
| `__pycache__/`, `.pytest_cache/`, `.ruff_cache/` | **Active** | **Add to .gitignore** | Cache directories should not be tracked |
| `Wiki/Home.md` | **Active** | **Edit** | Says "TV" instead of "VT" for Testing & Evaluation |
| `Wiki/Tokenomics_Index.md` | **Active** | **Edit** | Still lists `TK-F01..F03` which were supposed to be normalized to `TK-001..003` per deprecated planning docs |
| `deprecated/planning/*.md` | **Deprecated** | **Keep** | Historical reference, but contains Spanish text and false claims (e.g., "32 stubs created") that don't match current tree |
| `generate_golden_audit.py` | **Active** | **Investigate** | 77KB; contains hardcoded Cerberus dimension mappings; may be overly complex |
| `Wiki/Domains/D1..D12.md` | **Active** | **Edit** | Contain "Project: *cerberus*" references; should be agnostic or use generic labels |
| `Wiki/Concepts/Conceptual_Framework.md` | **Active** | **Merge or Deduplicate** | Duplicates `CONCEPTUAL_FRAMEWORK.md` at root; risk of drift |

---

## C. Truth Audit

### Material Claims and Their Truth Status

| Claim | Source | Classification | Evidence |
|---|---|---|---|
| "154 VC / 116 VT / 47 TK / 35 PI entries" | README, YAML, wiki | **True** | `grep -c "^\s*- id:"` matches on all 4 catalogs. `grep -c "^\s*PI-"` on project_insights = 35. |
| "317 vices + 35 insights = 352 entries" | README line 151 | **True** | 154+116+47=317 vices. 317+35=352. Verified. |
| "16 local detectors" | README badge, metrics.json | **True** | `scripts/detectors.py` DETECTORS registry has exactly 16 entries. Verified. |
| "stubs = 0" | README badge, metrics.json | **True** | `metrics.py` logic: `stub` = entries without `example_bad`/`example_good` AND without `doctrinal:true`. All 70 doctrinal VC entries have the flag. Verified. |
| "100% Clean Status" in audit report | `golden_standard_audit_report.md` | **Partially true** | The report shows 100% coverage mapping, but "coverage" here means "every catalog entry has a wiki article" — not that every entry is enforced or validated. The 100% is a structural coverage metric, not an operational quality metric. |
| "PREVENTED" status means enforcement exists | Catalog entries, README | **Aspirational** | `PREVENTED` means "a guard exists in a downstream enforcing project (e.g. Cerberus)" but GS itself does not verify this. README line 161 explicitly states: "This knowledge-base repo does not itself run those guards." The status is therefore a claim about an external system, not a verified property of GS. |
| "0 stubs" badge | `badges/stubs.json` | **True** | Verified by metrics.py logic. |
| "77% deep" badge | `badges/deep.json` | **True** | 244 deep / 317 total = 77%. Verified by metrics.py. |
| "PROPOSED: 205, ENFORCED_EXTERNAL: 99, ENFORCED_LOCAL: 13" | `Wiki/Home.md` line 53-56 | **Partially true** | Counts are close to actual YAML status counts but not exact. Actual: DOC_ONLY+AUDITED = 101+0+12 + 7+88+0 = 208 (not 205). PREVENTED = 45+22+31 = 98 (not 99). REMEDIATED = 3+6+3 = 12 (not 13). Minor drift. |
| "All 35 PIs declare `doctrinal: true`" | BACKLOG.md GS-061 | **True** | `grep "doctrinal: true" golden_standard_project_insights.yaml` = 35 matches. Verified. |
| "4 promotion candidates" | BACKLOG.md GS-061 | **True** | `grep "promotion_candidate: true"` = 4 matches (PI-002, PI-012, PI-017, PI-021). Verified. |
| "Wiki `Domains/D1..D12` regenerated as agnostic" | BACKLOG.md GS-034 | **False** | Live inspection shows D1.md, D8.md, and others still contain "Project: *cerberus*" references. They are thin routing pages, not truly agnostic. |
| "Remote now clean" (CC-specific docs removed) | BACKLOG.md GS-033 | **Partially true** | `CODERCERBERUS_MARCO_CONCEPTUAL.md` was removed, but `CONSUMER_CONTRACT.md` still exists and contains extensive Cerberus references. Also `KNOWLEDGE_SOURCES.md` still lists Cerberus as the primary source. |
| "Tokenomics normalized: TK-F01→TK-001, etc." | deprecated/NORMALIZATION_SUMMARY.md | **False** | The live `Wiki/Tokenomics_Index.md` and `golden_standard_tokenomics.yaml` still contain `TK-F01`, `TK-F02`, `TK-F03` entries. The normalization was planned but not fully executed in the live catalog. |
| "32 stubs created" | deprecated/NORMALIZATION_SUMMARY.md | **False** | The current tree has no `Patterns/` or `Principles/` directories. These stubs were never created in the live tree or were removed. The claim is a historical artifact that doesn't match reality. |
| "Badge counts validated against YAML by CI" | BACKLOG.md line 10 | **True** | `.github/workflows/audit.yml` exists and `scripts/metrics.py` + `validate_golden_standard_catalogs.py` provide the machinery. CI badge links in README are live. |
| "CERBERUS_CONTRACT.md" contract document | `KNOWLEDGE_SOURCES.md` line 26 | **False** | The file was renamed to `CONSUMER_CONTRACT.md`. The link is broken. |
| "All documentation in English" | `CONTRIBUTING.md` line 84 | **False** | `Inbox/README.md` is entirely in Spanish. |

### Fake Completion / Inflated Status Risks

1. **`PREVENTED` status inflation**: 98 entries claim `PREVENTED` status, but GS has no independent way to verify that the downstream enforcer actually catches these patterns. The README itself admits this (line 161). The status is essentially a **trust claim** about Cerberus, not a GS-verified property.
2. **Deprecated planning docs claim completion that never materialized**: `NORMALIZATION_SUMMARY.md` claims "32 stubs created" and "TK numbering normalized" but the live tree contradicts both. These are historical false claims preserved in `deprecated/`.
3. **Domain agnosticism claims**: BACKLOG says D1-D12 were "regenerated as agnostic lenses" but live inspection shows Cerberus references remain.
4. **"Remote now clean" claim**: GS-033 claims CC-specific docs were removed, but the repo still contains `CONSUMER_CONTRACT.md` (a boundary doc about Cerberus), `KNOWLEDGE_SOURCES.md` (lists Cerberus as primary), and numerous wiki entries that reference Cerberus dimensions.

---

## D. Identity, Scope, and Sources of Truth

### What GS Is

- An **open, agent-agnostic, project-agnostic knowledge base** of antipatterns, rules, and quality principles for AI-assisted software development.
- A **normative catalog** with structured entries (ID, severity, status, tags, examples, detection, evidence, mitigation).
- A **hybrid architecture**: YAML catalogs (machine-readable) + Wiki articles (human-readable) + Graph exports (navigable) + Metrics (badges).
- A **documentation-first standard**: it documents what to avoid and how to detect it, but does not itself enforce.

### What GS Is Not

- **Not a linter** or automatic enforcement tool. Only 16 entries have local static detectors.
- **Not a CI pipeline**. It has CI for self-validation, but it does not audit external projects.
- **Not tied to a single programming language**. Examples are mostly Python, but principles are stated as universal.
- **Not independent of its lineage** (yet). Active files still reference CoderCerberus as primary source and use its dimension framework.

### The Problem GS Solves

The "vibe coding" problem: AI-assisted development generates code that looks correct but is structurally flawed, tests that are ceremonial, and debt that accumulates silently. GS captures these failure patterns so they can be recognized and prevented across projects and agents.

### What Belongs in GS

- Universal antipatterns observable in AI-assisted development (VC, VT).
- Token-efficiency principles that apply to any AI agent (TK).
- Cross-cutting lessons extracted from real projects (PI).
- Detection recipes, evidence references, and mitigation strategies.
- Doctrinal principles that are behavioral/epistemic and have no static signature.

### What Does NOT Belong in GS

- Project-specific tool configurations (e.g., Cerberus-specific dimensions, rules, tests).
- Language-specific linter implementations (detectors.py is fine as a demonstrative sample, but a full linter belongs elsewhere).
- Agent-specific instruction files (e.g., CLAUDE.md, GEMINI.md) — these are bindings, not universal knowledge.
- Historical planning documents that claim completed work that didn't materialize.
- Non-English documentation in the active tree.

### Canonical Sources of Truth

| Aspect | Canonical Source | Issues |
|---|---|---|
| **Catalog list** | `golden_standard.yaml` | Clean, minimal, accurate. |
| **Rule content** | `golden_standard_*_vices.yaml` | Schema is consistent (v3.0). Good. |
| **PI content** | `golden_standard_project_insights.yaml` | **Different schema** (flat mapping vs list). Inconsistent. |
| **Human-readable form** | `Wiki/` tree | Generated by `generate_golden_audit.py`. Thin, mostly template-driven. |
| **Backlog / debt** | `BACKLOG.md` | Contaminated with project jargon. Single source of truth claim is valid. |
| **Deprecated material** | `deprecated/` | Contains false claims about completed work. |
| **Identity / purpose** | `README.md` + `CONCEPTUAL_FRAMEWORK.md` | Both are accurate but `CONCEPTUAL_FRAMEWORK.md` references Cerberus lineage. |
| **Graph / relationships** | `golden_standard_graph.json` + `Wiki/Graph.md` | Generated, useful for navigation, but count drift exists. |

### Competing / Conflicting Sources

1. **`CONCEPTUAL_FRAMEWORK.md` (root) vs `Wiki/Concepts/Conceptual_Framework.md`**: These are duplicate documents. Risk of drift if one is updated and the other isn't.
2. **`README.md` status enum vs YAML stored statuses**: README uses `PROPOSED`/`ENFORCED_EXTERNAL`/`ENFORCED_LOCAL` while YAML stores `DOC_ONLY`/`AUDITED`/`PREVENTED`/`REMEDIATED`. The mapping is documented but adds cognitive overhead.
3. **`INGESTION_PROTOCOL.md` vs `CONTRIBUTING.md`**: The protocol shows an old schema (no `downstream_verification`, no depth fields, no `doctrinal` flag) while CONTRIBUTING.md shows the current schema. Contradiction for new contributors.
4. **`BACKLOG.md` vs GitHub Issues**: BACKLOG claims to be the "single source of truth" for debt, but the GitHub issue templates reference discussions that may live only in Issues.

---

## E. Structural Architecture

### Rule Taxonomy

GS uses a 4-domain taxonomy with stable IDs:
- **VC-xxx**: Vibe Coding Vices (154 entries)
- **VT-xxx**: Testing Vices (116 entries)
- **TK-xxx**: Tokenomics (47 entries, including TK-F01..F03 legacy IDs)
- **PI-xxx**: Project Insights (35 entries)

**Assessment:** The taxonomy is **sound**. Stable IDs, sequential numbering, clear domain separation. The only anomaly is `TK-F01..F03` which were supposed to be normalized to `TK-001..003` per a deprecated plan, but the live catalog still carries the F-prefix. This is **not a functional bug** but it is a **hygiene debt**.

### Status Model

The YAML stores 4 statuses: `DOC_ONLY`, `AUDITED`, `PREVENTED`, `REMEDIATED`.
The human-readable wiki maps these to: `PROPOSED`, `ENFORCED_EXTERNAL`, `ENFORCED_LOCAL`.

**Assessment:** The dual-layer status system is **confusing** and creates a risk of misinterpretation. The README admits `PREVENTED` does not mean "prevented in GS" but "prevented in a downstream consumer." This is honest documentation, but the status name itself is misleading. `DOC_ONLY` is also ambiguous — it means "documented, no gate yet" but could be read as "test exempt" (which the README explicitly says it is not).

### Depth Model

Entries are classified as:
- `deep`: has `example_bad` + `example_good` + `detection` + `evidence`
- `doctrinal`: has `doctrinal: true`, no static signature
- `alias`: points to another entry (`alias_of`)
- `stub`: missing depth (target: 0)

**Assessment:** The depth model is **excellent** and the `stubs: 0` target is a strong quality signal. However, 70 of 154 VC entries are `doctrinal` (45.5%). This means nearly half the coding vices cannot be automatically detected. For a knowledge base that wants to enable "disciplined vibe coding without dirty code," this is a significant gap. The testing vices are 100% deep, which is the strongest catalog.

### Graph Layer

The graph exports 388 nodes, 1946 edges, 15 hubs, 3 intentional orphans, 0 candidate orphans.

**Assessment:** The graph is **genuinely useful**, not decorative. It identifies hubs (high-impact pages), orphans (unconnected entries), and validation debt. However, the generated `Wiki/Graph.md` has minor count discrepancies vs the actual YAML (e.g., 205 vs 208 PROPOSED). The graph is also **passive** — it reports structure but does not enforce connectivity rules at contribution time (the validator checks wiki existence, but not graph connectivity).

### Wiki / Documentation

The wiki has 369 articles (154 VC + 116 VT + 47 TK + 35 PI + 12 Domains + 5 Tokenomics subindices + indexes).

**Assessment:** The wiki is **necessary but thin**. Most vice articles follow a strict template that echoes the YAML fields without adding analytical depth. The wiki adds value through cross-links (Relations section) and the index pages, but the individual articles are largely **transclusions** of the YAML. For a human reader, the YAML + index pages might be more efficient than reading 270 individual vice pages.

### Backlog and Technical Debt

`BACKLOG.md` tracks debt with IDs (GS-xxx). The live debt section shows all items as `DONE` as of 2026-06-15.

**Assessment:** The backlog is **clean but potentially stale**. If all items are DONE, there should be no open debt — but this audit found new debt (Spanish text, broken links, Cerberus contamination) that is not tracked. The backlog's "single source of truth" claim is only valid if it is actively maintained. Currently it appears to be a historical completion log rather than a living debt register.

### Deprecated Material

`deprecated/` contains 14 files across 4 subdirectories. The planning docs are in Spanish and contain claims that were never executed (32 stubs, TK normalization).

**Assessment:** The deprecated area is **appropriate for historical reference** but should not contain false claims about completed work. The Spanish documents in `deprecated/planning/` are acceptable as historical artifacts (they document the project's origins), but they should be clearly labeled as "historical, not authoritative." The `deprecated/README.md` does this well.

---

## F. Rule Quality, Validity, and Usability

### Overall Assessment

| Catalog | Clarity | Usefulness | Enforceability | Depth | Verdict |
|---|---|---|---|---|---|
| **VT (Testing)** | High | High | High | 100% deep | **Strongest catalog** |
| **TK (Tokenomics)** | Medium-High | Medium | Medium | 46 deep, 12 DOC_ONLY | **Good, some thin** |
| **VC (Coding)** | Medium | Medium | Low | 82 deep, 70 doctrinal | **Weakest catalog** |
| **PI (Insights)** | Medium | Medium | N/A | All doctrinal | **Doctrinal by design** |

### VC Catalog Issues

1. **Too many doctrinal entries (70/154 = 45%)**: These are behavioral principles (e.g., "Unassumed incompetence", "Blind trust", "Demo as quality") that cannot be automatically detected. They are valid as governance principles, but as "vices" they are hard to act on. An agent reading "Unassumed incompetence" knows it should validate output, but has no concrete signal to detect when it's failing.
2. **Many entries have the same severity and status**: 101 entries are `DOC_ONLY` + `medium`. This creates a **flattened risk profile** where genuinely critical issues (e.g., `VC-127` Prompt Injection, `critical`) are mixed with style concerns (e.g., `VC-051` Contextual saturation, `medium`). The index is readable, but the YAML could benefit from sub-categorization or risk tagging.
3. **Thin symptom/cause fields**: Some entries have single-line symptoms (e.g., `VC-082` "Risks are added" as symptom, "Uncontrolled supply chain" as cause). These are too vague to be actionable without reading the full article.
4. **Cerberus dimension contamination**: The `enforcement.cerberus.dimension` and `enforcement.cerberus.mechanism` fields tie VC entries to a specific downstream tool. This is fine for traceability but creates a **dependency smell** in an agnostic repo.

### VT Catalog Strengths

The testing vices are the **strongest catalog**:
- All 116 entries are `deep` (example_bad + example_good + detection + evidence).
- 0 doctrinal entries. 0 stubs.
- Detection recipes are concrete (AST patterns, regexes, structural checks).
- Evidence cites real papers (e.g., `arxiv:2602.00409`).
- 22 entries are `PREVENTED` with local or downstream enforcement.

### TK Catalog Issues

1. **Legacy IDs persist**: `TK-F01`, `TK-F02`, `TK-F03` still exist. The deprecated normalization plan claimed they would be renamed to `TK-001..003`, but this was not executed.
2. **12 entries are `DOC_ONLY`**: These are behavioral principles about token usage (e.g., `TK-009` Semantic pruning, `TK-010` Contextual retrieval). Like the VC doctrinal entries, they are valid but not auto-detectable.
3. **The `TK-042` alias is correct**: `TK-042` is an alias of `TK-038`. This is a good pattern for handling duplicates without breaking references.

### PI Catalog Issues

1. **All 35 entries are `doctrinal`**: This is by design, but it means the PI catalog is entirely **prose guidance** with no concrete detection recipes.
2. **4 entries are "promotion candidates"**: PI-002, PI-012, PI-017, PI-021. These are flagged as candidates for promotion to VC/VT status, but the promotion criteria are vague ("if they acquire a static signature").
3. **Some PI entries reference tools** (e.g., PI-001 Deptry, PI-004 Trivy). These are useful but **risk becoming dated** if the tools change or become obsolete. The `verified` tags on PI-028..PI-034 are good but will require maintenance.

### Contradictions and Duplications

1. **No duplicate vices found**: The deduplication audit (GS-036) found exactly 2 merged entries (`VC-028`, `VC-077`). The alias pattern is clean.
2. **No logical contradictions found** between rules. The catalogs are consistent in their philosophy.
3. **One naming inconsistency**: The wiki uses `TV` in `Home.md` ("Engineering Vices Index: Central catalog of code and test anomalies (`VC`, `TV`)") but the actual domain code is `VT`. This is a typo.

---

## G. Repository Hygiene

### English-Only Rule Violations

The repository has an explicit English-only rule (CONTRIBUTING.md line 84: "Technical identifiers ASCII-only... prose may keep normal human language, including accents"). However, the following active files violate this:

| File | Violation | Severity |
|---|---|---|
| `Inbox/README.md` | **Entire file is Spanish** | High |
| `badges/evidence.json` | Label: "con evidencia" | Medium |
| `badges/detectors.json` | Label: "detectores locales" | Medium |
| `BACKLOG.md` | Contains "Eje 6" (Spanish for "Axis 6") | Medium |
| `deprecated/planning/*.md` | All 5 docs are Spanish | Low (deprecated, but in active repo) |

### Broken References

| File | Broken Reference | Fix |
|---|---|---|
| `KNOWLEDGE_SOURCES.md` line 26 | `CERBERUS_CONTRACT.md` | Rename to `CONSUMER_CONTRACT.md` |
| `Wiki/Home.md` line 43 | `TV` for Testing Vices | Should be `VT` |
| `Wiki/Tokenomics_Index.md` | Lists `TK-F01..F03` as if they are normalized | Either normalize them or document the legacy ID |

### Dead / Unnecessary Files in Active Tree

| File | Assessment | Action |
|---|---|---|
| `scripts/migrate_ax020.py` | One-time migration script for the AX-020 schema change. No longer needed. | Move to `deprecated/scripts/` or delete |
| `scripts/harden_metadata.ps1` | Purpose unclear. If it is a one-time hardening script, it should be documented or removed. | Document purpose or remove |
| `.claude/settings.local.json` | IDE configuration. Not part of the knowledge base. | Add to `.gitignore` and remove from repo |
| `.protocol/` | Appears empty or contains ephemeral files. | Verify contents; remove if empty |
| `__pycache__/` | Python bytecode cache. | Add to `.gitignore` and remove |
| `.pytest_cache/` | Pytest cache. | Add to `.gitignore` and remove |
| `.ruff_cache/` | Ruff linter cache. | Add to `.gitignore` and remove |

### Generated Artifacts Drift

The `generate_golden_audit.py` script is 77KB and contains hardcoded mappings to Cerberus dimensions (e.g., `D1`, `D2`, ... `D12`). The script generates:
- `golden_standard_audit_report.md`
- `golden_standard_audit.json`
- `Wiki/Graph.md`
- `Wiki/Home.md`
- `Wiki/Vices_Index.md`
- `Wiki/Principles.md`

**Assessment:** The generator is **functional but overweight**. 77KB for a report generator is excessive. It hardcodes Cerberus-specific dimensions, which means the generator itself is not agnostic. This creates a **circular dependency**: the agnostic knowledge base is generated by a tool that knows about Cerberus.

### Duplicate Doctrine

`CONCEPTUAL_FRAMEWORK.md` exists at the root and is duplicated (with slight variations) in `Wiki/Concepts/Conceptual_Framework.md`. This is a **drift risk**. Any update to the root file must be manually synced to the wiki copy.

---

## H. Fitness-for-Purpose

### Objective Assessment

The objective is: *"Create an agnostic Golden Standard that captures reusable knowledge, rules, anti-patterns, and governance principles to enable disciplined vibe coding without dirty code, fake passes, hidden debt, uncontrolled token waste, or lost learning across projects."*

| Criterion | Assessment |
|---|---|
| **Agnostic** | Partially. The catalogs are agnostic, but active docs (KNOWLEDGE_SOURCES, BACKLOG, CONSUMER_CONTRACT) reference Cerberus. The generator hardcodes Cerberus dimensions. |
| **Reusable** | Yes. The YAML schema is portable. The rules are implementation-neutral. |
| **Prevents dirty code** | Partially. 100% of testing vices are actionable. Only 53% of coding vices are deep (the rest are doctrinal). |
| **Prevents fake passes** | Yes. The testing vices catalog is excellent at this. |
| **Prevents hidden debt** | Partially. The tokenomics and PI catalogs address this, but many entries are doctrinal (not auto-detectable). |
| **Prevents token waste** | Partially. The tokenomics catalog is good, but the wiki itself is large (369 articles) and an agent consuming the full wiki would waste tokens. The YAML catalogs are the efficient interface. |
| **Survives across projects** | Yes. The stable IDs and schema make this portable. |

### Is the Structure Right?

**Yes, with reservations.** The YAML+Wiki+JSON hybrid is the right architecture for a knowledge base that must serve both humans and machines. However:

1. **YAML is the right interface for agents**, not the wiki. The wiki is too verbose and token-heavy for agent consumption. There should be a clear "Agent Consumption Guide" that tells agents to read the YAML catalogs, not the wiki.
2. **The wiki is too thin** to justify its size. Most articles are template transclusions. Consider reducing the wiki to: index pages, deep doctrinal articles, and cross-cutting concepts. Let the YAML be the source of truth for individual vice details.
3. **The graph is useful but passive** — it should be integrated into the validator to block new orphan entries.
4. **The generator is too complex** — a simpler Python script that reads YAML and emits markdown would be more maintainable than 77KB of hardcoded logic.

### Is It Overbuilt / Underbuilt / Misbuilt?

- **Overbuilt**: The wiki (369 articles, mostly templates). The generator (77KB). The graph (1946 edges, but many are just "back to index" links).
- **Underbuilt**: Agent consumption guide. Enforcement layer (only 16 detectors). Sub-categorization within VC (154 entries with no taxonomy beyond the domain list).
- **Misbuilt**: The dual status enum (YAML vs human-readable). The PI schema (flat mapping vs list). The Cerberus dimension mappings in the agnostic repo.

### Token Efficiency

Reading the full wiki (369 articles × average 40 lines) would consume ~15,000 lines of context. An agent should instead consume:
- `golden_standard.yaml` (9 lines)
- `golden_standard_metrics.json` (18 lines)
- The relevant YAML catalog(s) (~1000-4000 lines each)
- The index pages (~100 lines each)

**Total efficient consumption: ~5,000-10,000 lines** depending on which catalogs are relevant.

GS should add an **AGENT_CONSUMPTION.md** file that explicitly tells agents which files to read and in what order, to prevent token waste from reading the full wiki.

---

## I. Unified Remediation Plan

### Urgent Cleanup (Do First)

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 1 | **High** | `Inbox/README.md` | Rewrite entirely in English. Keep the same structure and content. | Active file complies with English-only rule. | Visual inspection. |
| 2 | **High** | `KNOWLEDGE_SOURCES.md` line 26 | Fix broken link: `CERBERUS_CONTRACT.md` → `CONSUMER_CONTRACT.md` | Link resolves. | Click/read test. |
| 3 | **High** | `Wiki/Home.md` line 43 | Fix typo: `TV` → `VT` | Domain code is consistent. | Grep for `TV-` in wiki. |
| 4 | **Medium** | `badges/evidence.json` + `badges/detectors.json` | Change Spanish labels to English: "with evidence", "local detectors" | Badges comply with English-only rule. | Read JSON files. |
| 5 | **Medium** | `BACKLOG.md` | Scrub project-specific jargon: replace "Eje 6" with "Phase 6" or "Batch 6"; replace "AX-020/023/024" with human-readable descriptions or links to commits. | Backlog is readable without insider knowledge. | Readability check. |
| 6 | **Medium** | `.gitignore` | Add: `.claude/`, `__pycache__/`, `.pytest_cache/`, `.ruff_cache/`, `.protocol/` | Cache and IDE files are excluded from repo. | `git status` shows them untracked. |
| 7 | **Medium** | `scripts/migrate_ax020.py` | Move to `deprecated/scripts/` or delete if no longer needed. | Active tree contains only live tools. | File does not exist in `scripts/`. |
| 8 | **Medium** | `Wiki/Concepts/Conceptual_Framework.md` | Either delete and link to root `CONCEPTUAL_FRAMEWORK.md`, or add a machine-generated header warning that it is a copy. | Eliminate drift risk between duplicate doctrine files. | Only one authoritative copy exists. |

### Structural Redesign

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 9 | **Medium** | `INGESTION_PROTOCOL.md` | Update the Step 4 YAML template to match the current schema (v3.0): add `downstream_verification`, `tier`, `doctrinal`, `example_bad`, `example_good`, `detection`, `evidence`, `detector`. Remove stale fields like `operativity_status`, `source_reference`. | New contributors see the correct schema. | Compare with `CONTRIBUTING.md` and live YAML. |
| 10 | **Medium** | `golden_standard_project_insights.yaml` | Restructure from flat mapping to list format (matching VC/VT/TK schema) for consistency. | All 4 catalogs use the same schema shape. | Validator passes without special PI handling. |
| 11 | **Low** | `generate_golden_audit.py` | Audit and refactor: reduce hardcoded Cerberus dimension mappings; extract dimension mapping to a separate config file if needed. | Generator is agnostic or its dependencies are explicit. | Code review of generator. |
| 12 | **Low** | `Wiki/Domains/D1..D12.md` | Remove or genericize "Project: *cerberus*" references. Use generic labels like "Project: *example-consumer*" or "Downstream enforcement reference". | Domain pages are truly agnostic. | Grep `cerberus` in `Wiki/Domains/`. |
| 13 | **Low** | `Wiki/Tokenomics_Index.md` | Either normalize `TK-F01..F03` to `TK-001..003` (requires renumbering TK-001..027) or add an explicit note that F-prefixes are legacy IDs preserved for stability. | Index accurately reflects the catalog state. | Read index and catalog. |
| 14 | **Low** | `CONSUMER_CONTRACT.md` | Add a header note: "This document defines the boundary with a downstream consumer. Golden Standard does not require this consumer to exist or to be operational for GS to be valid." | The contract is framed as optional, not essential. | Read the header. |
| 15 | **Low** | Create `AGENT_CONSUMPTION.md` | Document the minimal file set an agent should read to understand GS efficiently: `golden_standard.yaml` → relevant catalog(s) → `CONCEPTUAL_FRAMEWORK.md` → index pages. Warn against reading the full wiki. | Agents consume GS efficiently without token waste. | File exists and is clear. |

### Source-of-Truth Consolidation

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 16 | **Medium** | `BACKLOG.md` | Create a new `OPEN` debt item for the findings of this audit (Spanish text, broken link, Cerberus contamination, stale INGESTION_PROTOCOL). If the backlog claims to be the single source of truth for debt, it must contain current debt. | Backlog is a living register, not a historical completion log. | Read backlog; see open items. |
| 17 | **Low** | `README.md` status explanation | Clarify that `PREVENTED` is a claim about downstream enforcement, not a GS-verified property. Add a note: "GS does not independently verify that downstream enforcers are operational." | Readers understand the limitation of status claims. | Read README status section. |
| 18 | **Low** | `KNOWLEDGE_SOURCES.md` | Change Cerberus from "Primary Source" to "Historical Source" or "Example Downstream Consumer". Add a note that GS accepts findings from any source that meets the contract. | GS does not appear dependent on Cerberus for its identity. | Read the source hierarchy. |

### Rule Validity Fixes

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 19 | **Low** | `golden_standard_coding_vices.yaml` | Review the 70 `doctrinal` VC entries. For each, assess whether it could be made falsifiable with a concrete detection recipe. If not, keep `doctrinal`. If yes, add `example_bad`/`example_good`/`detection` and convert to `deep`. | More VC entries are actionable. | Metrics shows `deep` > 90% for VC. |
| 20 | **Low** | `Wiki/Vices/VC-082.md` | Expand the thin symptom/cause fields. "Risks are added" / "Uncontrolled supply chain" are too vague. | Entry is more actionable. | Read the article. |
| 21 | **Low** | `golden_standard_tokenomics.yaml` | Add `downstream_verification` to all entries that currently lack it. | All TK entries have explicit verification metadata. | `grep` for missing field. |

### Documentation / Wiki Fixes

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 22 | **Low** | `Wiki/Graph.md` | Fix count discrepancies: PROPOSED should be 208 (not 205), ENFORCED_EXTERNAL should be 98 (not 99), ENFORCED_LOCAL should be 12 (not 13). Or add a note that counts are approximate. | Graph counts match YAML reality. | Compare with `grep` counts. |
| 23 | **Low** | `deprecated/planning/NORMALIZATION_SUMMARY.md` | Add a header warning: "This document contains claims that were not executed in the live tree (e.g., 32 stubs, TK normalization). It is preserved for historical context only." | Readers are not misled by stale claims. | Read the header. |
| 24 | **Low** | `Wiki/Project_Insights/PI-006.md`, `PI-007.md`, etc. | Remove or genericize "Project: *cerberus*" references in domain mappings. | PI pages are agnostic. | Grep `cerberus` in PI pages. |

### Graph / Wiki Fixes

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 25 | **Low** | `scripts/validate_golden_standard_catalogs.py` | Add a graph-connectivity check: new entries must link to at least one index, map, or related concept page. | Zero accidental orphans in future contributions. | Run validator on a test entry with no links. |
| 26 | **Low** | `Wiki/Graph.md` | Make the validation debt table dynamic rather than a static snapshot. Or regenerate it on every commit. | Graph debt is always current. | Check CI for graph regeneration. |

### Backlog / Debt Consolidation

| # | Priority | File / Area | Action | Expected Result | Validation |
|---|---|---|---|---|---|
| 27 | **High** | `BACKLOG.md` | Add the following open items from this audit:
- GS-065: Spanish text in active files (Inbox/README, badges)
- GS-066: Broken link to CERBERUS_CONTRACT.md
- GS-067: Cerberus contamination in active docs (KNOWLEDGE_SOURCES, Domains, PI pages)
- GS-068: INGESTION_PROTOCOL shows stale schema
- GS-069: Generator hardcodes Cerberus dimensions
- GS-070: Duplicate doctrine files (CONCEPTUAL_FRAMEWORK root + wiki)
- GS-071: 70 VC entries are doctrinal (not falsifiable) — assess promotion to deep
- GS-072: TV/VT typo in Wiki/Home.md
- GS-073: Cache directories tracked in repo | Debt is tracked and visible. | Read backlog. |

---

## J. Open Questions

These questions cannot be resolved by inspecting the repository alone:

1. **Does any downstream consumer actually enforce the 98 `PREVENTED` entries?** GS claims these are enforced in Cerberus, but there is no independent verification mechanism within GS. If Cerberus is non-operational or has changed its rule set, the `PREVENTED` status becomes a false claim.

2. **Are the Cerberus D1-D12 dimension mappings still accurate?** The generator and wiki map vices to Cerberus dimensions (e.g., `D2` = completeness, `D8` = test coverage, `D10` = tokenomics). If Cerberus has restructured its dimensions, these mappings are stale.

3. **What is the intended audience for the graph layer?** The graph exports `golden_standard_graph.json` and `Wiki/Graph.md`, but there is no documented consumer. Is it for human navigation, for Obsidian, or for a future automated tool? Without a defined consumer, the graph is at risk of becoming decorative.

4. **Is `generate_golden_audit.py` (77KB) maintainable?** The script is large, hardcodes many mappings, and mixes report generation with wiki generation. If the generator fails, the entire wiki and audit report become stale. There is no documented fallback if the generator breaks.

5. **Should the `deprecated/` area be pruned?** It contains 14 files, some of which are 600+ lines of Spanish planning documents. These are historical artifacts, but they bloat the repository and contain claims that contradict the live tree. Should there be a retention policy for deprecated material?

---

*End of Independent Adversarial Audit — Golden Standard*
