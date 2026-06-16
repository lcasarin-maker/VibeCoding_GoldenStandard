# Knowledge Sources — Golden Standard

> This document defines the **authorized sources** that feed the Golden Standard knowledge base,
> the contract each source must fulfill, and the SLA for processing their findings.

---

## Principle

The Golden Standard is **read by many, written by few**.

Knowledge enters through structured sources with defined contracts.
Knowledge is never added directly to the catalogs without passing through the Inbox.
Every entry in the catalog must be traceable to its source.

---

## Authorized Sources

### 1. CoderCerberus (Historical Source — Example Downstream Consumer)

**Type:** Automated auditor  
**Canonical name:** `cerberus`  
**Inbox subdirectory:** `Inbox/cerberus/`  
**Template:** [`Inbox/templates/cerberus_finding.md`](Inbox/templates/cerberus_finding.md)  
**Contract document:** [`CONSUMER_CONTRACT.md`](CONSUMER_CONTRACT.md)

> **Note:** GS accepts findings from any source that meets the validity contract below.  
> CoderCerberus is listed here because it was the original source of many entries,  
> not because GS depends on it.

**What it contributes:**
- Patterns detected during real-project audits that are not yet in the catalog
- Refinements to existing entries based on observed real-world frequency
- Evidence that a known vice is actively manifesting in production code

**SLA:** Findings are reviewed in the next curation session (minimum: weekly).

**Naming convention:**
```
Inbox/cerberus/YYYY-MM-DD_<cerberus-rule-id-or-slug>.md
```
Example: `Inbox/cerberus/2026-06-04_untested-ui-flow-detection.md`

---

### 2. Manual Sessions (DRI)

**Type:** Human developer / DRI (Directly Responsible Individual)  
**Canonical name:** `manual`  
**Inbox subdirectory:** `Inbox/manual/`  
**Template:** [`Inbox/templates/manual_finding.md`](Inbox/templates/manual_finding.md)

**What it contributes:**
- Observations from vibe coding sessions not covered by Cerberus rules
- Pattern recognition from code review or debugging
- Nuanced judgment that automated tools cannot yet capture

**SLA:** Processed at the discretion of the DRI, no strict SLA.

**Naming convention:**
```
Inbox/manual/YYYY-MM-DD_<slug>.md
```
Example: `Inbox/manual/2026-06-05_silently-broken-auth-flow.md`

---

### 3. External Contributions

**Type:** Community contributors (GitHub Issues / Pull Requests)  
**Canonical name:** `external`  
**Inbox subdirectory:** `Inbox/external/`  
**Template:** [`Inbox/templates/external_contribution.md`](Inbox/templates/external_contribution.md)

**What it contributes:**
- Vices observed in other teams, languages, or stacks
- Refinements and corrections to existing entries
- New domains not yet covered
- Only evidence anchored to the active baseline counts; findings derived from retired `00 audit` artifacts, stale snapshots, or pre-purge states must be rejected or returned for rework.

**SLA:** Reviewed within 14 days of submission.

**Naming convention:**
```
Inbox/external/YYYY-MM-DD_<github-issue-or-pr-number>_<slug>.md
```
Example: `Inbox/external/2026-07-01_gh-42_react-stale-closure-vice.md`

---

## What Makes a Valid Finding

A finding is valid for Inbox deposit if it has at minimum:

| Field | Required? | Notes |
|---|---|---|
| `source` | ✅ | Must match a canonical source name |
| `date_detected` | ✅ | ISO 8601 date |
| `symptom` | ✅ | Observable behavior that signals the problem |
| `cause` | ✅ | Root cause or mechanism |
| `proposed_domain` | ✅ | `VC`, `VT`, `TK`, or `PI` |
| `proposed_severity` | ✅ | `critical`, `high`, `medium`, `low` |
| `mitigation_proposal` | ✅ | At least one concrete prevention action |
| `evidence_artifact` | ⚠️ Optional | Link to log, report, or session transcript |

A finding without a `symptom`, `cause`, and `mitigation_proposal` **will not be promoted** to the catalog.

---

## Processing Lifecycle

```
Source detects / observes a pattern
         ↓
Deposit in Inbox/<source>/YYYY-MM-DD_<slug>.md
         ↓
Curator reviews: deduplicate, validate fields
         ↓
Map to YAML domain (VC/VT/TK/PI), assign next sequential ID
         ↓
Add entry to golden_standard_*.yaml (status: KNOWLEDGE)
         ↓
Create Wiki article in Wiki/Vices/
         ↓
Run generate_golden_audit.py — verify coverage
         ↓
Move Inbox file to deprecated/
```

See [`INGESTION_PROTOCOL.md`](INGESTION_PROTOCOL.md) for the full step-by-step execution guide.

---

## Source Traceability

Every YAML entry in the catalog includes a `source` field:

```yaml
- id: VC-701
  title: "Silent Auth Flow Bypass"
  source: cerberus          # ← canonical source name
  source_reference: "CR-088"  # ← source-internal ID (if applicable)
  date_added: "2026-06-05"
  ...
```

This ensures the catalog remains fully auditable — every piece of knowledge
has a traceable origin.

External submissions that claim repository cleanliness or audit completeness must also include fresh purge evidence for the active baseline they audited. If they cannot name that baseline, they are not ready for promotion.

Passing a legacy test suite is not enough. If the submission only proves that old checks still go green, the maintainer must re-run or re-aim the verification against the current Cerberus baseline and require functional evidence for the claim being made.

---

*Last updated: 2026-06-05*
