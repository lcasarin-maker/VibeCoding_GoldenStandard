# AUDIT TRAIL

## 2026-06-15

- GS-061 Stage 2 completed in GS: added an enforced PI->VC/VT promotion gate with a synthetic fail-first test, marked all 35 project insights `doctrinal: true`, tagged `PI-002`, `PI-012`, `PI-017`, and `PI-021` as promotion candidates, regenerated the wiki with a new `Principles` index, and verified the CC consumer loader still ingests the structured catalog cleanly.
- GS-064 anti-duplication cleanup: removed the re-inlined promotion-gate copy from `validate_project_insights()` so the production flow now calls the tested helper directly; verified with `validate_golden_standard_catalogs.py --check-wiki`, `tests/test_project_insight_promotion_gate.py`, `scripts/metrics.py`, and the full pytest suite.
- GS-034 agnostic framing pass: regenerated the 12 domain pages as `Operational Lens 1..12`, removed the Cerberus-specific public framing, and kept the domain codes only as stable routing labels for the PI links.
- GS-036 dedup audit: scanned the vice wiki and found exactly 2 merged entries (`VC-028`, `VC-077`) with 0 duplicate titles in the 270-page vice set.
- GS-037 enum reading cleanup: rewrote the human-facing status reading in README, CONTRIBUTING, and generated Home.md to the self-describing enum (`PROPOSED` / `ENFORCED_EXTERNAL` / `ENFORCED_LOCAL`), then aligned the validator to the new output.
