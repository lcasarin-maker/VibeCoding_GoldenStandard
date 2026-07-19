# STATE — VibeCoding Golden Standard
**Last updated:** 2026-07-19 (GS-13 Conformity Report Generator implemented; contract freshness gate added; falsifiability report linked; remote CI green / Semgrep effectiveness gate) | **Agent:** Codex

---

## Catalog health

| Catalog | Entries | Open debt | Notes |
|---------|---------|-----------|-------|
| VC (coding vices) | 94 | none | VC-012 REMEDIATED; VC-084/VC-086 ratchet justifications recorded; VC-093/VC-094 added 2026-07-13 (unjustified nosemgrep suppression GS-05; BOM-in-config Semgrep rule) |
| VT (testing vices) | 116 | none | VT-043 PREVENTED by Semgrep rule with positive/negative fixtures |
| TK (tokenomics) | 34 | none | |
| PR (principles) | 121 | none | PR-118-121 added 2026-06-26; decoupled from CC-internal IDs 2026-07-01 |
| SP (structure principles) | 10 | none | 8 checks in audit.py (SP-001/003/004/005/006/007/009/010) |
| AV (adversarial vectors) | 104 | G-01 open | All 104 entries are `status: DOC_ONLY` with an identical boilerplate `doc_only_justification` (passes gs_lint.py's shallow len/substring check, not a real per-entry falseability classification) — see PLAN_MIGRACION_ATOM.md §6 G-01 |
| CD (canonical domains) | 18 | none | |

Counts verified directly against live YAML catalogs on 2026-07-14 (`grep -cE '^- id:' *.yaml`; not carried forward from a prior snapshot — the 2026-07-02 VC=93 count was stale, corrected to 94, and AV was missing from this table entirely). See `tasks/backlog/` for current open items — do not assume "backlog empty" without checking that folder first.

## Migration status

| Phase | Status | Remaining |
|-------|--------|-----------|
| Phase 1 — Scaffold | DONE | — |
| Phase 2 — Migrate content | DONE | — |
| Phase 3 — Absorb governance files | DONE | — |
| Phase 4 — Verify + commit | DONE | — |

## Open backlog

<!-- sección generada — no editar a mano -->

_Sección generada desde `tasks/backlog/` por `scripts/check_backlog_sync.py`; no editar a mano._

_No backlog items currently live under `tasks/backlog/`._

<!-- fin de sección generada — no editar a mano -->

## CI status

31/31 tests passing locally with warnings treated as errors; remote CI matrix runs on Python 3.10, 3.11, 3.12, and 3.13. `audit.py` reports 8/8 SP checks green. Semgrep: 12 rules, 12 positive matches, 0 negative matches, plus the preregistered effectiveness gate reports 0.0% max false-negative rate and 0 false positives over the known-vice corpus. `gs_lint.py` ratchet clean with zero soft warnings and zero `legacy review` catalog entries; 35 local detectors are proven; Wiki/Detectors has one canonical file per ID. GS-AUD-001…007 are closed in the adversarial-audit closure record. Contract freshness now uses a machine-readable boundary contract so validator surfaces cannot drift silently, and the falsifiability report is now linked from the wiki hub.
