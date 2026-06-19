# Cerberus ↔ Golden Standard Contract

> This document defines the **consumer-facing interface** between a downstream enforcement tool
> and the Golden Standard (the knowledge base).
>
> **Note:** Golden Standard does not require this consumer to exist, to be operational, or to be named
> "Cerberus" for GS to be valid. The contract is a reference implementation of consumption,
> not a dependency of GS.
>
> Both projects are independent. This contract is a boundary document, not a second source of truth.
> For the consumer's internal doctrine, `D:\AI\Cerberus\00 audit\00_CONSTITUCION_CERBERUS.md` wins.

---

## The Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                    Golden Standard                          │
│          (knowledge base — project-agnostic)                │
│                                                             │
│  VC-xxx  │  VT-xxx  │  TK-xxx  │  PI-xxx                   │
│  Coding  │  Testing │  Tokens  │  Insights                  │
│  Vices   │  Vices   │          │                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
            ┌──────────────┴──────────────┐
            │   consumes as normative      │   deposits findings via
            │   source (read-only)         │   Inbox/cerberus/ (write)
            ▼                             ▲
┌─────────────────────────────────────────────────────────────┐
│                    CoderCerberus                            │
│          (enforcement tool — project-specific)              │
│                                                             │
│  Audits real projects. Enforces rules derived from          │
│  Golden Standard entries.                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Direction 1: Cerberus Consumes Golden Standard

### How

Cerberus references Golden Standard as a **normative source**.
Recommended integration: separate repository read-only at the consumer boundary, with explicit sync or fetch steps.

Cerberus must not treat Golden Standard as a live submodule or internal snapshot.
If Cerberus needs a local mirror, it must be an explicitly managed read-only copy, not the source of truth.
If this contract ever conflicts with Cerberus's Constitution, the Constitution is authoritative for Cerberus behavior and this document must be updated to match.

### Rules for Cerberus Rules

Every rule implemented in Cerberus MUST:

1. **Reference a Golden Standard entry.** Each Cerberus rule includes a `golden_standard_ref` field:
   ```yaml
   # Example Cerberus rule
   - rule_id: CR-042
     title: "Untested UI flow detection"
     golden_standard_ref: VC-312    # ← required
     severity: high
     ...
   ```

2. **Not contradict the Golden Standard.** If Cerberus narrows or extends a principle, the delta must be documented in the rule itself.

3. **Flag missing coverage.** If Cerberus needs to implement a rule for a pattern not yet in Golden Standard, it MUST create an Inbox finding before implementing the rule (see Direction 2 below).
4. **Preflight the consumer impact.** If a change alters the audit topology, loader order, or runner path, the preflight must name the impacted Cerberus script, the file-order delta, and the validation step before the edit is considered ready.
5. **Reject stale external audit baselines.** This is the reusable GS-side principle behind Cerberus's external audit contract: an external verdict is only valid when it is tied to the active baseline being exercised. Findings based on retired `00 audit` artifacts, stale snapshots, or pre-purge states must be returned as `NEEDS_INFO`, not accepted as clean evidence.
6. **Require Cerberus-new functional proof.** GS keeps the abstract rule; Cerberus owns the procedural enforcement. “Passes tests” is not sufficient if the test harness or enforcement layer is retired, mismatched, or legacy. External audits must be re-targeted to the current Cerberus baseline and prove the actual functionality being claimed; otherwise the result is not a valid acceptance.
7. **Emit origin-rich findings.** Every consumer-facing warning or finding must include the exact origin of the signal (`path:line`, `catalog:id`, or an equivalent stable locus). Aggregate counts alone are not actionable and must be treated as incomplete evidence.

### What Cerberus May NOT Do

- Cerberus must not create rules that contradict a Golden Standard entry without first filing a `refine` request via Inbox.
- Cerberus must not implement project-specific overrides that would qualify as universal principles without contributing them back.
- Cerberus must not treat `DOC_ONLY` as `test_exempt` when the GS entry declares downstream verification as required.
- Cerberus must not accept “test passed” as proof of correctness when the test was run against a retired baseline, a legacy audit surface, or a different Cerberus generation; the verdict must be revalidated on the active baseline with functional evidence.

---

## Direction 2: Cerberus Feeds Golden Standard

### When to Deposit a Finding

Cerberus deposits a finding in `Inbox/cerberus/` when:

| Trigger | Action |
|---|---|
| Cerberus detects a pattern with no `VC-xxx`/`VT-xxx` coverage | Create Inbox finding before implementing the rule |
| An existing GS entry needs refinement based on audit evidence | Create Inbox finding with `refinement_target: <existing-ID>` |
| A GS entry's severity seems wrong based on real-world frequency | Create Inbox finding with `severity_challenge: true` |
| An audit produces hard evidence for a KNOWLEDGE-status entry | Create Inbox finding with `evidence_for: <existing-ID>` |
| An external audit claims cleanup, completeness, or repo hygiene | Require the active baseline plus fresh purge evidence; if either is missing, return `NEEDS_INFO` |
| An external audit only proves that old tests pass | Reject until it is re-run against the current Cerberus baseline and demonstrates the functionality being asserted |

### How to Deposit

1. Copy `Inbox/templates/cerberus_finding.md`
2. Fill all required fields (see template)
3. Save as `Inbox/cerberus/YYYY-MM-DD_<slug>.md`
4. Commit with message: `inbox: cerberus finding <slug>`

### Template Location

```
Inbox/templates/cerberus_finding.md
```

### Required Fields

| Field | Required | Notes |
|---|---|---|
| `source` | ✅ | Must be `cerberus` |
| `cerberus_rule_id` | ✅ | The CR-xxx ID (or `PENDING` if not yet assigned) |
| `project_audited` | ✅ | Anonymized project name is acceptable |
| `date_detected` | ✅ | ISO 8601 |
| `symptom` | ✅ | Observable behavior |
| `cause` | ✅ | Root cause |
| `proposed_domain` | ✅ | `VC`, `VT`, `TK`, or `PI` |
| `proposed_severity` | ✅ | `critical`, `high`, `medium`, `low` |
| `mitigation_proposal` | ✅ | At least one concrete action |
| `evidence_artifact` | ⚠️ | Link to audit log/report if available |
| `refinement_target` | ⚠️ | Existing GS entry ID if this refines one |
| `evidence_for` | ⚠️ | Existing GS entry ID if this provides evidence |
| `origin` | ⚠️ | Exact locus that produced the finding (`path:line`, `catalog:id`, or equivalent) |

---

## SLA and Processing

| Stage | Timeline |
|---|---|
| Finding deposited in `Inbox/cerberus/` | Immediately, no review needed |
| Finding reviewed by curator | Within 7 days |
| Finding promoted to catalog | Within 14 days |
| Finding rejected (duplicate/invalid) | Within 7 days, with rationale |

---

## Traceability Requirements

### In Golden Standard (for Cerberus-sourced entries)

```yaml
- id: VC-701
  source: cerberus
  source_reference: "CR-042"     # The Cerberus rule that triggered this
  ...
```

### In Cerberus (for all rules)

```yaml
- rule_id: CR-042
  golden_standard_ref: VC-312    # The GS entry this rule enforces
  # If the GS entry didn't exist yet:
  # golden_standard_ref: PENDING:VC-701  # Filed in Inbox, awaiting promotion
  ...
```

---

## Versioning

The contract version is implicit in the Golden Standard repository.
When breaking changes to the contract are needed, they are announced via:
1. A new section in this document with a version header
2. A GitHub Issue tagged `contract-change`
3. A minimum 30-day notice period before enforcement

---

## Contact Points

| Role | Responsibility |
|---|---|
| Golden Standard curator | Reviewing Inbox findings, maintaining catalog |
| Cerberus DRI | Ensuring all Cerberus rules have GS references |
| Both | Resolving conflicts between enforcement and knowledge base |

---

*Last updated: 2026-06-05*  
*This contract is binding on both projects.*
