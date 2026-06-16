# Agent Consumption Guide — Golden Standard

> Read this first. Do not read the full Wiki (369 articles) — it is generated transclusions of the YAML and is token-inefficient for agent consumption.

## Minimal Reading Set (recommended)

1. **Identity & scope:** `README.md` (lines 1–50) + `CONCEPTUAL_FRAMEWORK.md` (lines 1–100)
2. **Schema:** `golden_standard.yaml` (9 lines) + `CONTRIBUTING.md` (Entry Format section)
3. **Catalogs:** Load only the domain(s) relevant to your task:
   - Vibe coding: `golden_standard_coding_vices.yaml` (154 entries)
   - Testing: `golden_standard_testing_vices.yaml` (116 entries)
   - Tokenomics: `golden_standard_tokenomics.yaml` (47 entries)
   - Insights: `golden_standard_project_insights.yaml` (35 entries)
4. **Metrics:** `golden_standard_metrics.json` (18 lines) — gives you the health snapshot.
5. **Index pages (if you need human-readable summaries):**
   - `Wiki/Vices_Index.md` (summary list)
   - `Wiki/Tokenomics_Index.md` (summary list)
   - `Wiki/Project_Insights_Index.md` (summary list)

## What NOT to read

- Do not read individual `Wiki/Vices/VC-xxx.md` or `Wiki/Vices/VT-xxx.md` articles unless you need the cross-link graph for a specific entry. They repeat the YAML verbatim.
- Do not read `deprecated/` — it is historical, not active knowledge.
- Do not read `generate_golden_audit.py` — it is an internal tool, not knowledge.
- Do not read `Inbox/` — it is raw intake, not curated knowledge.

## Total token budget (approximate)

- Full YAML catalogs: ~9,000 lines
- Index pages + docs: ~1,000 lines
- **Total efficient consumption: ~10,000 lines** vs ~15,000+ for the full Wiki.

## Quick reference: how to apply a rule

When you encounter a potential vice in generated code:
1. Search the relevant YAML catalog for the symptom or keyword.
2. Read the `detection` recipe and the `example_bad` / `example_good` pair.
3. If the entry is `deep` and has a `detector`, run it if available.
4. If the entry is `doctrinal`, apply the principle as a governance check, not as a static lint.
5. Always cite the `id` (e.g., `VC-003`) when you reference a rule, so the traceability is preserved.
