# STATE — VibeCoding Golden Standard
**Last updated:** 2026-07-11 (GS debt closure) | **Agent:** Codex

---

## Catalog health

| Catalog | Entries | Open debt | Notes |
|---------|---------|-----------|-------|
| VC (coding vices) | 92 | none | VC-012 REMEDIATED; VC-084/VC-086 ratchet justifications recorded |
| VT (testing vices) | 116 | none | VT-043 PREVENTED by Semgrep rule with positive/negative fixtures |
| TK (tokenomics) | 34 | none | |
| PR (principles) | 121 | none | PR-118-121 added 2026-06-26; decoupled from CC-internal IDs 2026-07-01 |
| SP (structure principles) | 10 | none | 8 checks in audit.py (SP-001/003/004/005/006/007/009/010) |
| CD (canonical domains) | 18 | none | |

Counts verified directly against live YAML catalogs on 2026-07-02 (not carried forward from a prior snapshot). See `tasks/backlog/` for current open items — do not assume "backlog empty" without checking that folder first.

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

26/26 tests passing on Python 3.11 and 3.13; CI matrix is Python 3.10–3.13. `audit.py` reports 8/8 SP checks green. Semgrep: 7 rules, 7 positive matches, 0 negative matches. `gs_lint.py` ratchet clean; Wiki/Detectors has one canonical file per ID. GS-AUD-001…007 are closed in the adversarial-audit closure record; residual AUDITED catalog entries are tracked inventory, not open backlog debt.
