# BACKLOG — VibeCoding Golden Standard

**Single source of truth for Golden Standard debt and open work.**

> **Mandating rule (anti-atomization).** All Golden Standard debt — catalog drift, wiki
> dedup, separation from downstream enforcers, doc/count mismatches — MUST be tracked in
> this file before work begins. GitHub Issues may host discussion, but an item is not
> "tracked" until it appears here with an ID. If it is not here, it is not worked.
> This mirrors the downstream Cerberus "Technical-Debt Trinity" so both repos share one
> discipline. Counts and statuses below are validated against the YAML catalogs by CI.

Status legend: `OPEN` · `IN_PROGRESS` · `BLOCKED` (this file is future-only — closed
items move to `git log` / `AUDIT_TRAIL.md`; a guard rejects any `DONE` row, see
`validate_golden_standard_catalogs.py`).

<!-- CANONICAL-COUNTS (generated truth; asserted by validate_golden_standard_catalogs.py::validate_backlog_counts) -->
**Catalog counts (canonical, post-renumber `VC-001..086` / `VT-001..116` / `TK-001..034` / `PR-001..113`):** VC 86 / VT 116 / TK 34 / PR 113.
This line is the single source enforced against the YAML by CI.

---

## Live debt (OPEN / IN_PROGRESS only)

| ID | Severity | Item | Acceptance criteria | Status |
|----|----------|------|---------------------|--------|
| GS-071 | Low | 26 VC entries are DOC_ONLY (not falsifiable) | Promote remaining DOC_ONLY VC entries to PREVENTED via real detectors, or justify each as doctrinal. Metrics shows the DOC_ONLY count trending to a justified floor. Batch 2 (2026-06-18) promoted VC-002/010/018/024/036; 26 remain. | IN_PROGRESS |
| GS-075 | Low | Generator maintainability (audit 2026-06-16 item 11) | `generate_golden_audit.py` (~77KB) mixes audit-report and wiki generation. Split the two, add a documented fallback if it breaks. Accept: report and wiki generation are separable and independently testable. | OPEN |
| GS-076 | Low | Graph layer hardening (audit 2026-06-16 items 22/25/26) | `Wiki/Graph.md` count drift vs YAML; the validator checks wiki existence but not graph connectivity; the validation-debt table is static. Accept: a connectivity check lands in `validate_golden_standard_catalogs.py` and graph debt regenerates on commit. | OPEN |

> Audit recovery note: residual unresolved findings from the 2026-06-16 independent
> audit (preserved in git tag `pre-reset-2026-06-20`) are tracked above as
> GS-075/076/077/078 (and GS-071). All other audit items were verified RESOLVED
> against the live tree on 2026-06-20; their closure detail lives in `AUDIT_TRAIL.md`
> and `git log`. The BACKLOG jargon-scrub item (ex GS-074) is resolved by emptying the
> historical DONE rows from this file.

## Process / cross-repo

| ID | Severity | Item | Acceptance criteria | Status |
|----|----------|------|---------------------|--------|
| GS-010 | Medium | Adopt the corruption guard upstream-style | Mirror the Cerberus corruption/encoding guard as a GS-side pre-commit check. Accept: a guard rejects mojibake / truncation in the catalogs before commit. | OPEN |
