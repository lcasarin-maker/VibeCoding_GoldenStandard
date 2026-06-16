# BACKLOG — VibeCoding Golden Standard

**Single source of truth for Golden Standard debt and open work.**

> **Mandating rule (anti-atomization).** All Golden Standard debt — catalog drift, wiki
> dedup, separation from downstream enforcers, doc/count mismatches — MUST be tracked in
> this file before work begins. GitHub Issues may host discussion, but an item is not
> "tracked" until it appears here with an ID. If it is not here, it is not worked.
> This mirrors the downstream Cerberus "Technical-Debt Trinity" so both repos share one
> discipline. Counts and statuses below are validated against the YAML catalogs by CI.

Status legend: `OPEN` · `IN_PROGRESS` · `BLOCKED` · `DONE`

---

## Live debt

| ID | Severity | Item | Evidence / Notes | Status |
|----|----------|------|------------------|--------|
| GS-031 | High | README + badge counts are stale vs YAML | DONE 2026-06-15 (Eje 6): push AX-020 + AX-024 to remote. README:151 already correct: "317 vices + 35 insights (352 entries)" — 154 VC / 116 VT / 47 TK / 35 PI; `entries` badge intentionally = 317 (flaws only, documented in README). No badge regeneration needed. | DONE |
| GS-032 | Medium | Detector count mismatch | DONE 2026-06-15 (Eje 6): `detectors.py` has 16 real detectors (18 top-level defs − 2 private helpers). `badges/detectors.json` already = "16". Fixed GS About via `gh repo edit` 15→16. | DONE |
| GS-033 | High | CC-specific docs inside agnostic repo | DONE 2026-06-15 (Eje 6): pushed AX-023 commit (d2a1c9a in CC, committed in GS history) that removed `CODERCERBERUS_MARCO_CONCEPTUAL.md` and renamed `CERBERUS_CONTRACT.md` → `CONSUMER_CONTRACT.md`. Remote now clean. | DONE |
| GS-034 | High | Wiki `Domains/D1..D12` break agnosticism | `Wiki/Domains/` documents Cerberus's 12 enforcement domains inside the agent-agnostic KB. Decide: move to Cerberus, or re-author as agnostic principles without the Dxx (Cerberus-specific) framing. | OPEN |
| GS-035 | Medium | Tokenomics wiki vs catalog drift | `Wiki/Tokenomics` has 52 pages vs 47 `TK-` catalog entries (5 non-entry pages: indexes/maps/overviews or potential dupes). Reconcile so every data point is a described, deduplicated entry or an explicitly-labeled index. | DONE 2026-06-15: labeled the five subindex pages (`Automation_Tooling_Index`, `Input_Retrieval_Index`, `Measurement_Telemetry_Index`, `Memory_Headroom_Index`, `Output_Compaction_Index`) as index-only pages so they no longer masquerade as TK entries. |
| GS-035b | Low | TK-038/TK-042 duplicate action | After AX-020, `TK-038` (Full-state re-reading) and `TK-042` (Manifests without a size constraint) carry an identical `action` (the manifest size-gate, `D10`/`audit_d10_tokenomics`). Candidates for merge/alias; do not fuse yet — confirm they are not two distinct facets before collapsing. | DONE 2026-06-15: `TK-042` is now `alias_of: TK-038`. The duplicate is semantically the same action, and references remain in the wiki/graph, so deleting the ID would break consumers; alias preserves stability. |
| GS-035c | Low | TK-042 alias keeps full duplicate body | DONE 2026-06-15: `TK-042` now keeps only `id`, `title`, and `alias_of: TK-038` in `golden_standard_tokenomics.yaml`; the generator emits a redirect/stub page to the canonical `TK-038` entry, and the catalog validator accepts the alias without duplicated body fields. | DONE |
| GS-062 | Medium | `stub: 1` violates the repo's own `stubs = 0` contract | DONE 2026-06-15: the stub was `VC-082` (`Dependencies without a gate`). Root cause: AX-020 migration left it with `runtime-test`/mechanism metadata but stripped depth fields. Resolved by adding `example_bad`, `example_good`, `detection`, and real evidence from the YAML-importing GS scripts; `metrics.py` now reports `stub: 0`. | DONE |
| GS-036 | Medium | Deep Wiki dedup pass (Vices) | 270 Vice articles (= 154 VC + 116 VT). Run overlap/duplicate detection and a per-entry descriptiveness check using `generate_golden_audit.py` + `golden_standard_graph.json`. | OPEN |
| GS-037 | Medium | Status enum hardening | Replace the ambiguous `DOC_ONLY` / `PREVENTED` reading with a self-describing enum (`ENFORCED_LOCAL` / `ENFORCED_EXTERNAL` / `PROPOSED`). Tracked upstream as GitHub issue #4. | OPEN |
| GS-061 | High | PI -> VC/VT promotion gate | DONE 2026-06-15: enforced promotion gate added to `scripts/validate_golden_standard_catalogs.py` with a synthetic fixture test proving red/green behavior; all 35 PIs now declare `doctrinal: true`, four are marked `promotion_candidate: true`, the generated wiki gained `Wiki/Principles.md`, `generate_golden_audit.py`/regeneration succeeded, `validate_golden_standard_catalogs.py --check-wiki` passed, metrics remain `154 VC / 116 VT / 47 TK / 35 PI` with `stub: 0`, and the CC `test_project_insights_integration.py` consumer test passed against the structured catalog. | DONE |

## Process / cross-repo

| ID | Severity | Item | Notes | Status |
|----|----------|------|-------|--------|
| GS-010 | Medium | Adopt the corruption guard upstream-style | Mirror Cerberus `scripts/
