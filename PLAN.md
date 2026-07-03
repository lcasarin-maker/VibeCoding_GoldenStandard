# PLAN.md — Legacy Planning Landing Page

This file is retired. It previously tracked `GS-071/075/076/080/081` (task `GS-deuda-final`, started 2026-06-22).

Verified 2026-07-01 (GS-085): all five items are complete —
- GS-075: `--audit-only` / `--wiki-only` flags exist in `scripts/generate_golden_audit.py`.
- GS-076: `check_graph_connectivity()` exists in `scripts/validate_golden_standard_catalogs.py`.
- GS-080: `check_sp005()` exists in `scripts/audit.py`.
- GS-081: `knowledge/templates/` exists with all four templates; `check_sp007()` validates `priority:`/`effort:`.
- GS-071: the 13 listed DOC_ONLY entries (VC-007, 009, 012, 037, 042, 046, 058, 060, 062, 063, 064, 067, 068, 069) already carry the justification in their `action` field ("Sprint 3.4 triage" text) rather than a separate `justification_doc_only:` field — the underlying goal (documented, falsifiable justification per DOC_ONLY entry) is met.

Live state lives in `STATE.md`, `HANDOFF.md`, and `audit/AUDIT_TRAIL.md`. Live backlog is `tasks/backlog/`.
