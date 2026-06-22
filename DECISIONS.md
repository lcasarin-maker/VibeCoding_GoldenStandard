# DECISIONS — VibeCoding Golden Standard

Durable architectural decisions only. Not a session log.
Agents may Propose; only humans may Accept.

---

## DEC-001 — CD18 adopted as new GS canonical domain
**Date:** 2026-06-22 | **Status:** Accepted | **By:** Luis Casarin
Multi-Agent Project Governance (CD18) added to `config/canonical_domain_map.json`.
Rationale: GS had no domain covering structural invariants for multi-agent projects.
CD18 bridges GS's quality doctrine with the operational scaffold needed to run it.

## DEC-002 — SP catalog created (SP-001..009)
**Date:** 2026-06-22 | **Status:** Accepted | **By:** Luis Casarin
`golden_standard_structure_principles.yaml` created with 9 Structure Principles.
Rationale: CD18 rules needed a formal catalog entry type. SP mirrors existing VC/VT/TK/PR
format; status RULE_DEFINED until `scripts/audit.py` exists to enforce them automatically.

## DEC-003 — V3.2 canonical structure adopted for GS
**Date:** 2026-06-22 | **Status:** Accepted | **By:** Luis Casarin
GS migrates to CANONICAL_STRUCTURE V3.2 (defined in CC repo, to move to GS).
Rationale: GS is the authoritative home for the canonical structure standard.
CC and satellites will adopt this structure referencing GS as the source.

## DEC-004 — AGENT_CONSUMPTION.md and CODE_OF_CONDUCT.md to be absorbed
**Date:** 2026-06-22 | **Status:** Accepted | **By:** Luis Casarin
Both files will be absorbed into `.agents/AGENTS.md` (SP-001: single governance hub).
AGENT_CONSUMPTION.md content → AGENTS.md §0. CODE_OF_CONDUCT.md (human CoC, no
agent-specific content) → deleted without replacement. Deletion in Phase 3.

## DEC-005 — VC-088 added: Execution before plan
**Date:** 2026-06-22 | **Status:** Accepted | **By:** Luis Casarin
New VC entry documenting the "planless agent" antipattern. Triggered by this session:
SP catalog was written without a PLAN.md first. Detection: multi-file session with no
PLAN.md at start; PLAN.md present at session close (cleanup skipped).
