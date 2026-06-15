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
| GS-031 | High | README + badge counts are stale vs YAML | README/About say 126 VC / 115 VT / 46 TK / 27 PI / **314 total**; local YAML has **154 / 116 / 47 / 35 = 352**. README claims counts are "source of truth, validated in CI" — so either CI count-check is not running or local is unpushed. Reconcile and push; verify `scripts/metrics.py` + `generate_golden_audit.py` regenerate badges. | OPEN |
| GS-032 | Medium | Detector count mismatch | About says "15 enforced by static detectors"; `golden_standard_metrics.json` reports `local_detectors: 16` / `registered_detectors: 16`. Pick the true number from `scripts/detectors.py` and make README/About/badge agree. | OPEN |
| GS-033 | High | CC-specific docs inside agnostic repo | Root carries `CODERCERBERUS_MARCO_CONCEPTUAL.md` (a Cerberus conceptual doc) and—pre-rename—`CERBERUS_CONTRACT.md`. A staged rename `CERBERUS_CONTRACT.md -> CONSUMER_CONTRACT.md` exists locally but is uncommitted/unpushed. Remove CC identity docs from GS; keep only the agnostic consumer contract. | OPEN |
| GS-034 | High | Wiki `Domains/D1..D12` break agnosticism | `Wiki/Domains/` documents Cerberus's 12 enforcement domains inside the agent-agnostic KB. Decide: move to Cerberus, or re-author as agnostic principles without the Dxx (Cerberus-specific) framing. | OPEN |
| GS-035 | Medium | Tokenomics wiki vs catalog drift | `Wiki/Tokenomics` has 52 pages vs 47 `TK-` catalog entries (5 non-entry pages: indexes/maps/overviews or potential dupes). Reconcile so every data point is a described, deduplicated entry or an explicitly-labeled index. | OPEN |
| GS-036 | Medium | Deep Wiki dedup pass (Vices) | 270 Vice articles (= 154 VC + 116 VT). Run overlap/duplicate detection and a per-entry descriptiveness check using `generate_golden_audit.py` + `golden_standard_graph.json`. | OPEN |
| GS-037 | Medium | Status enum hardening | Replace the ambiguous `DOC_ONLY` / `PREVENTED` reading with a self-describing enum (`ENFORCED_LOCAL` / `ENFORCED_EXTERNAL` / `PROPOSED`). Tracked upstream as GitHub issue #4. | OPEN |
| GS-061 | High | PI -> VC/VT promotion gate | Verify `project_insights` promotion: a Project Insight that acquires a static signature (an `example_bad` + detector) must graduate to an enforceable `VC/VT` entry; PIs that stay behavioral remain `doctrinal`. Confirm the gate is enforced, not just listed. | OPEN |

## Process / cross-repo

| ID | Severity | Item | Notes | Status |
|----|----------|------|-------|--------|
| GS-010 | Medium | Adopt the corruption guard upstream-style | Mirror Cerberus `scripts/check_no_corruption.py` (reject NUL bytes + unparseable sources) in GS CI, so a bad write to a YAML/MD catalog fails fast rather than shipping a truncated catalog. | OPEN |
| GS-020 | Low | Confirm `Inbox/cerberus/` is the only sanctioned CC->GS coupling | CC feeds GS via `Inbox/cerberus/` + `INGESTION_PROTOCOL.md` + `CONSUMER_CONTRACT.md`. Document this as the minimal interface; everything else is incidental and removable. | OPEN |

---

*Created 2026-06-14 by adversarial audit. IDs align with `D:\AI\AUDIT_2026-06-14_Cerberus_GS_adversarial.md`. This file is the GS counterpart to Cerberus `BACKLOG.md`.*
