---
# External Contribution — Inbox Template
# Copy this file to Inbox/external/YYYY-MM-DD_gh<issue>_<slug>.md
# Use when submitting a finding from outside the core team (GitHub Issue / PR).
# This file will be created by the maintainer when triaging an Issue/PR.
---

## Metadata

source: external
contributor:                    # ✅ GitHub handle or name
github_issue:                   # ⚠️ GitHub Issue number (if applicable)
github_pr:                      # ⚠️ GitHub PR number (if applicable)
audit_baseline:                 # ✅ Active Cerberus/GS baseline audited (commit, tag, or version)
verification_target:            # ✅ Current Cerberus generation / active enforcement baseline
date_detected: YYYY-MM-DD       # ✅ ISO 8601 (date contributor reported it)
date_triaged: YYYY-MM-DD        # ✅ ISO 8601 (date maintainer triaged it)
language_or_stack:              # ⚠️ If the finding is stack-specific, note it here
triaged_by:                     # ✅ Maintainer who triaged
purge_evidence:                 # ⚠️ Required when the submission claims cleanup/completeness/repo hygiene
functional_evidence:            # ⚠️ Required when the submission claims a behavior or guard actually works
legacy_artifacts_checked:       # ⚠️ yes/no + note if any retired artifacts were encountered

## Classification

proposed_domain:                # ✅ VC | VT | TK | PI
proposed_severity:              # ✅ critical | high | medium | low
tags:                           # ✅ At least two normalized tags
  - 
  - 
refinement_target:              # ⚠️ Existing GS entry ID if this refines one
evidence_for:                   # ⚠️ Existing GS entry ID if this provides evidence
triage_decision:                # ✅ ACCEPT | REJECT | NEEDS_INFO
rejection_reason:               # ✅ (required if REJECT)

## Hard Law

If the only proof is that an old or retired test suite still passes, the submission is not valid evidence.
The maintainer must retarget verification to the current Cerberus baseline and require functional evidence for the exact claim being made.
Legacy `00 audit` artifacts, stale snapshots, and pre-purge states are not acceptable as proof of correctness or repo health.

---

## Original Submission

<!-- Copy the relevant excerpt from the GitHub Issue or PR here. -->
<!-- Attribute to the contributor. -->

> Submitted by @<contributor>:
>
> (paste the original report here)

---

## Maintainer Analysis

### Symptom (extracted)
<!-- Restate the symptom in canonical form. -->


### Cause (extracted)
<!-- Root cause. -->


### Example
<!-- ⚠️ Optional: code snippet or example from the submission. -->
```
(paste example here)
```

### Proposed Mitigation
<!-- One or more concrete prevention actions. -->
- 


### Canonicalization Notes
<!-- ⚠️ Notes on how the original submission was adapted to GS canonical format. -->

---

## Resolution (filled by curator, do not edit)

promoted_to:
wiki_article:
date_promoted:
curator:
