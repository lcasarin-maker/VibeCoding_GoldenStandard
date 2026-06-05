# Ingestion Protocol — Golden Standard

> The canonical, executable guide for promoting a finding from the Inbox into the Golden Standard catalog.
> This document is authoritative. The `Inbox/README.md` is a summary that references this document.

---

## Overview

The Ingestion Protocol is the **quality gate** between raw observations and codified knowledge.
Its job is to ensure that only well-formed, deduplicated, actionable knowledge enters the catalog.

```
Raw finding (Inbox/)
      ↓
Step 1: Validate fields
      ↓
Step 2: Deduplicate
      ↓
Step 3: Map to domain and assign ID
      ↓
Step 4: Add YAML entry (status: KNOWLEDGE)
      ↓
Step 5: Create Wiki article
      ↓
Step 6: Run audit script
      ↓
Step 7: Close the finding
```

---

## Who Runs This

The **curator** — either the DRI (human) or an AI agent acting as curator — is responsible
for executing this protocol. The curator must have read access to all YAML catalogs and write
access to the repository.

---

## Step 1 — Validate the Finding

Open the file in `Inbox/<source>/` and verify it contains at minimum:

- [ ] `source` — matches a canonical name in `KNOWLEDGE_SOURCES.md`
- [ ] `date_detected` — valid ISO 8601 date
- [ ] `symptom` — concrete, observable behavior
- [ ] `cause` — root cause, not just the symptom restated
- [ ] `proposed_domain` — one of: `VC`, `VT`, `TK`, `PI`
- [ ] `proposed_severity` — one of: `critical`, `high`, `medium`, `low`
- [ ] `mitigation_proposal` — at least one actionable prevention step

If any required field is missing: **return the finding to the source** with a note.
Do not proceed.

---

## Step 2 — Deduplicate

Search the existing catalogs for the pattern described:

```bash
# Quick scan of coding vices
grep -i "<keyword>" golden_standard_coding_vices.yaml

# Quick scan of testing vices
grep -i "<keyword>" golden_standard_testing_vices.yaml
```

**If an existing entry covers the finding:**
- If the finding adds new evidence or nuance → update the existing entry's `evidence_notes` field
- If the finding is a duplicate with no new information → discard, move to `deprecated/`
- In both cases, note the existing entry ID in the Inbox file before closing

**If no existing entry covers the finding:**
- Proceed to Step 3

---

## Step 3 — Map to Domain and Assign ID

### Determine the Domain

| Domain | Code | Catalog file | When to use |
|---|---|---|---|
| Vibe Coding Vice | `VC` | `golden_standard_coding_vices.yaml` | AI-assisted dev antipatterns |
| Testing Vice | `VT` | `golden_standard_testing_vices.yaml` | Test quality failures |
| Tokenomics | `TK` | `golden_standard_tokenomics.yaml` | AI token usage inefficiencies |
| Project Insight | `PI` | `golden_standard_project_insights.yaml` | Cross-cutting lessons |

### Assign the Next Sequential ID

Open the target YAML file and find the last entry. Increment by 1.

```bash
# Find the last ID in the coding vices catalog
grep "^- id:" golden_standard_coding_vices.yaml | tail -1
```

Record the new ID (e.g., `VC-701`).

---

## Step 4 — Add the YAML Entry

Open the target catalog file and append the new entry in canonical format:

```yaml
- id: VC-701                          # Assigned in Step 3
  title: "Short descriptive title"
  description: >
    Full description of the vice, its context, and why it is harmful.
  severity: high                      # critical | high | medium | low
  domain: architecture                # Choose appropriate subdomain
  source: cerberus                    # Canonical source name
  source_reference: "CR-088"          # Source-internal ID (optional)
  date_added: "2026-06-05"
  status: KNOWLEDGE                   # Always starts at KNOWLEDGE
  symptom: >
    What you observe when this vice is present.
  cause: >
    Root cause or mechanism.
  detection_criteria:
    - "Concrete thing to look for in code"
    - "Another detection signal"
  mitigation:
    - "Concrete prevention action"
    - "Another prevention action"
  evidence_notes: ""                  # Leave empty until evidence is generated
  operativity_status: KNOWLEDGE
```

Save the file.

---

## Step 5 — Create the Wiki Article

Create a new Markdown file at:
```
Wiki/Vices/<ID>.md
```

Use this template:

```markdown
# <ID> — <Title>

**Severity:** <severity>  
**Domain:** <domain>  
**Status:** KNOWLEDGE  
**Source:** <source> (<source_reference if applicable>)  
**Date Added:** YYYY-MM-DD  

---

## Description

<Full description from YAML>

## Symptom

<What you observe>

## Cause

<Root cause>

## Detection Criteria

- <criterion 1>
- <criterion 2>

## Mitigation

- <action 1>
- <action 2>

## Evidence

*No evidence generated yet. Status: KNOWLEDGE.*

---

*See also: [back to Vices Index](../Vices_Index.md)*
```

---

## Step 6 — Run the Audit Script

```bash
python generate_golden_audit.py
```

Verify:
- [ ] The new entry appears in the audit output
- [ ] The Wiki article is detected and linked
- [ ] No errors in YAML parsing

---

## Step 7 — Close the Finding

1. Add a closing note to the Inbox file:
   ```
   ## Resolution
   Promoted to: <ID> (<YAML file>)
   Wiki article: Wiki/Vices/<ID>.md
   Date promoted: YYYY-MM-DD
   Curator: <name or agent>
   ```
2. Move the Inbox file to `deprecated/`:
   ```bash
   git mv Inbox/<source>/<filename>.md deprecated/<filename>.md
   ```
3. Commit with message:
   ```
   knowledge: promote <ID> from Inbox
   
   Source: <source>
   Finding: <slug>
   Domain: <VC|VT|TK|PI>
   ```

---

## File Naming Conventions

| Location | Convention | Example |
|---|---|---|
| `Inbox/cerberus/` | `YYYY-MM-DD_<slug>.md` | `2026-06-04_silent-auth-bypass.md` |
| `Inbox/manual/` | `YYYY-MM-DD_<slug>.md` | `2026-06-05_ghost-service-layer.md` |
| `Inbox/external/` | `YYYY-MM-DD_gh<issue>_<slug>.md` | `2026-07-01_gh42_react-closure.md` |

---

## Commit Convention

All knowledge commits follow this format:

```
knowledge: <action> <ID>

<Optional body explaining rationale>

Source: <canonical source name>
```

Actions:
- `promote` — new entry from Inbox
- `refine` — update to existing entry
- `deprecate` — entry marked as superseded
- `elevate` — status progression (KNOWLEDGE → RULE_DEFINED → etc.)

---

*Last updated: 2026-06-05*  
*Authoritative document — do not modify the protocol without curator consensus.*
