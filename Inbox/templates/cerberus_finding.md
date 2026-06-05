---
# Cerberus Finding — Inbox Template
# Copy this file to Inbox/cerberus/YYYY-MM-DD_<slug>.md
# Fill all required fields before depositing.
# Required fields are marked with ✅. Optional with ⚠️.
---

## Metadata

source: cerberus
cerberus_rule_id: CR-           # ✅ e.g. CR-042, or PENDING if not yet assigned
project_audited:                # ✅ Project name (anonymized is acceptable)
date_detected: YYYY-MM-DD       # ✅ ISO 8601

## Classification

proposed_domain:                # ✅ VC | VT | TK | PI
proposed_severity:              # ✅ critical | high | medium | low
refinement_target:              # ⚠️ Existing GS entry ID if this refines one (e.g. VC-312)
evidence_for:                   # ⚠️ Existing GS entry ID if this provides evidence (e.g. VC-200)
severity_challenge: false       # ⚠️ Set true if you believe an existing entry's severity is wrong

---

## Finding

### Symptom
<!-- What was observed during the audit? Be concrete and specific. -->
<!-- Bad: "the code was bad"  Good: "AuthService.login() returns 200 even on invalid credentials" -->


### Cause
<!-- Root cause. Not the symptom restated. -->
<!-- Bad: "the auth was broken"  Good: "JWT validation is skipped when X-Internal-Request header is present" -->


### Context / Example
<!-- ⚠️ Optional but strongly encouraged. Paste a minimal code snippet or log excerpt. -->
```
(paste code or log here)
```

### Proposed Mitigation
<!-- At least one concrete, actionable prevention step. -->
- 


### Evidence Artifact
<!-- ⚠️ Link to the Cerberus audit report, log file, or session transcript where this was detected. -->
evidence_artifact:

---

## Resolution (filled by curator, do not edit)

promoted_to:
wiki_article:
date_promoted:
curator:
