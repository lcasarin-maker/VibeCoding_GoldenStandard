# AUDIT TRAIL

## 2026-06-30

| Session | Agent | Summary |
|---------|-------|---------|
| 2026-06-30-001 | Claude | Reconciled the GS catalog contract with the live YAML tree: validator now tolerates the legacy mechanism/downstream labels already present, the README counts were refreshed, and the catalog drift follow-up was closed with a regression test. |

## 2026-06-22

| Session | Agent | Summary |
|---------|-------|---------|
| [2026-06-22-001](sessions/2026-06-22-001.md) | Claude | V3.2 canonical structure migration (Phase 1-4): scaffold + content migration + governance absorption + SP/CD18/VC-088 catalog additions. 29 files changed. CI green. |
| [2026-06-22-002](sessions/2026-06-22-002.md) | Claude | GS root cleanup: knowledge/ consolidation (3 files moved, 3 ghosts deleted), SP-010 added. CI green. |
| 2026-06-22-003 | Claude | Sprint B+D: badges/→docs/badges/, generate_golden_audit.py→scripts/, JSON outputs→output/. Fixed _ROOT (.parent.parent), status_counts SP exclusion, validator SP orphan check. 3 commits, 10 tests green. |

## 2026-06-21

- GS-078 (B2 cerberus decouple) CLOSED on the GS side. The 219 `enforcement.cerberus.{dimension,mechanism}` blocks were lifted out of the three agnostic catalogs into `config/cerberus_enforcement.json` (mirroring the existing `config/cerberus_dimensions.json` overlay). Strip was a verified deletion-only line surgery (ruamel round-trip reflows the block scalars, so no YAML-library rewrite was used): every surviving line is byte-identical, item counts unchanged, and the only removed lines match the `enforcement:/cerberus:/dimension:/mechanism:` pattern. The generator now re-injects `enforcement.cerberus` from the overlay into the downstream `golden_standard_audit.json` and reads the overlay in `_display_mechanism`, so the consumer DB is **byte-identical to HEAD** (0 value diffs, 0 enforcement diffs) — CC consumers that read the generated DB are unaffected. Found and absorbed a latent bug: VC-027 carried a duplicate `enforcement` block (`D2/audit_d2_completeness` then `D17/validate`); `yaml.safe_load` already took the last, so the overlay correctly captured the effective `D17/validate` and the dead block is gone. `grep -c cerberus: golden_standard_*.yaml` = 0; validator + detectors green. CC-side `federated_linter` rewiring lands in the Cerberus repo.

- GS-077 (B1 detector parity) CLOSED. Root cause was a measurement bug in `metrics.py`: it resolved a catalog `detector:` ref by parsing the number out of the function name (`vc087_...` -> `VC-087`) and checking it against the registry keys, but the registry maps id -> function whose `__name__` need not match the id (e.g. `DETECTORS["VC-032"] == vc087_blanket_filterwarnings`). So 5 real detectors were counted as dangling and `local`=23 vs `registered`=27. Fixed `metrics.py` to resolve a ref by registered function name. Then closed the genuine gaps: 4 catalog entries (VC-002/018/024/027) advertised detectors that were not wired — registered the 3 existing-and-discriminating overloads (`vc005_untracked_prototype`, `vc061_constant_stub`, `vc070_blind_shell_edit`) and repointed VC-027 from the nonexistent `audit_d2_completeness` to the existing, discriminating `vc078_placeholder`. Result: `local == registered == 31`, `unregistered_detector_refs == []`, badge reads 31. Added a parity gate in `scripts/test_detectors.py` (already run in CI) that fails if `local != registered` or any ref is unregistered; proven failing-first (unregistering one detector returns exit 1). Regenerated all artifacts (report/audit.json/graph/metrics/badges/wiki); `validate_golden_standard_catalogs.py --check-wiki` green.

## 2026-06-15

- GS-061 Stage 2 completed in GS: added an enforced PI->VC/VT promotion gate with a synthetic fail-first test, marked all 35 project insights `doctrinal: true`, tagged `PI-002`, `PI-012`, `PI-017`, and `PI-021` as promotion candidates, regenerated the wiki with a new `Principles` index, and verified the CC consumer loader still ingests the structured catalog cleanly.
- GS-064 anti-duplication cleanup: removed the re-inlined promotion-gate copy from `validate_project_insights()` so the production flow now calls the tested helper directly; verified with `validate_golden_standard_catalogs.py --check-wiki`, `tests/test_project_insight_promotion_gate.py`, `scripts/metrics.py`, and the full pytest suite.
- GS-034 agnostic framing pass: regenerated the 12 domain pages as `Operational Lens 1..12`, removed the Cerberus-specific public framing, and kept the domain codes only as stable routing labels for the PI links.
- GS-036 dedup audit: scanned the vice wiki and found exactly 2 merged entries (`VC-028`, `VC-077`) with 0 duplicate titles in the 270-page vice set.
- GS-037 enum reading cleanup: rewrote the human-facing status reading in README, CONTRIBUTING, and generated Home.md to the self-describing enum (`PROPOSED` / `ENFORCED_EXTERNAL` / `ENFORCED_LOCAL`), then aligned the validator to the new output.

## SYNC [2026-06-30T15:40:00]
**Archivos integrados:** knowledge/external_tools.md
**Acción:** agent-learning-kit moved from backlog to adopted after the CC trajectory/evidence eval harness was wired, tested, and exposed through the CLI smoke path.

## SYNC [2026-06-30T16:05:00]
**Archivos integrados:** knowledge/external_tools.md
**Acción:** Probe was evaluated directly against the Cerberus repo, but the comparison favored retaining `semble`; the external-tools ledger now marks Probe rejected.

## SYNC [2026-06-30T16:20:00]
**Archivos integrados:** knowledge/external_tools.md
**Acción:** Claude Context was evaluated through the official MCP package help output, but rejected for the current workspace because provider credentials and Milvus configuration are absent; the external-tools ledger now records that decision.
