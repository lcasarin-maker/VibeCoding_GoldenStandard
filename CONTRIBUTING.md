# Contributing to the Golden Standard

Thank you for helping make this knowledge base better. Every real failure you've seen, every lesson learned, every antipattern encountered — that's exactly what belongs here.

---

## Types of Contributions

### 1. New Vice Entry (most common)
You've encountered a failure pattern in AI-assisted development that isn't in the catalog.

**Format:**
- A new entry in `golden_standard_coding_vices.yaml` or `golden_standard_testing_vices.yaml`
- A corresponding Wiki article in `Wiki/Vices/VC-xxx.md` or `Wiki/Vices/VT-xxx.md`

### 2. Improving an Existing Entry
An existing entry is incomplete, imprecise, or missing detection criteria.

### 3. Promoting an Entry's Operativity Status
An entry is documented (`KNOWLEDGE`) but you've written an executable rule, test, or evidence generator for it.

### 4. New Knowledge Area
You believe a whole new domain belongs in the Golden Standard (beyond vibe coding, testing, and tokenomics).

### 5. Bug in the Audit Script
The `generate_golden_audit.py` script has errors or misses coverage.

---

## Entry Format

### For YAML Catalogs

Each entry in the YAML files follows this structure:

```yaml
- id: "VC-XXX"
  title: "Short descriptive name (not dramatic)"
  description: |
    What the vice is. What causes it. Why it's harmful.
  severity: "critical|high|medium|low"
  detection_criteria:
    - "How to detect it automatically"
    - "What to look for in code review"
  mitigation:
    - "How to prevent it"
    - "How to fix it when found"
  operativity_status: "KNOWLEDGE|RULE_DEFINED|TEST_ASSOCIATED|EVIDENCE_GENERATED|OPERATIONAL|BLOCKING"
  tags:
    - "relevant-tag"
  examples:
    bad: |
      # What the bad code looks like
    good: |
      # What the correct code looks like
```

### For Wiki Articles

Each Wiki article (`Wiki/Vices/VC-xxx.md`) follows this structure:

```markdown
# VC-xxx — Title

**Severity:** Critical / High / Medium / Low
**Domain:** Vibe Coding / Testing / Tokenomics
**Status:** KNOWLEDGE / OPERATIONAL / BLOCKING

## Description
What this vice is and why it matters.

## Why It Happens
The root cause in AI-assisted development contexts.

## Detection
How to identify this vice in a codebase.

## Examples

### ❌ Bad
```code
# Example of the vice
```

### ✅ Good
```code
# Correct approach
```

## Mitigation
How to prevent or fix it.

## Related Vices
- [VC-xxx — Related vice](VC-xxx.md)
```

---

## ID Numbering

- **VC-xxx** = Coding vices (start from the current max ID + 1)
- **VT-xxx** = Testing vices (start from the current max ID + 1)

Check the current max IDs in:
- `golden_standard_coding_vices.yaml` (look for the highest VC-xxx)
- `golden_standard_testing_vices.yaml` (look for the highest VT-xxx)

---

## Process

### Small contributions (single entry fix, typo, clarity)
→ Open a PR directly. No issue needed.

### New entries
1. Check the [Inbox/](../Inbox/) folder for similar proposals
2. Check the YAML to avoid duplicates
3. Open an Issue using the **"New Vice"** template
4. After discussion, submit a PR with:
   - YAML entry in the appropriate catalog
   - Wiki article at `Wiki/Vices/[ID].md`

### New knowledge areas
→ Open an Issue for discussion first. New domains require broader consensus.

---

## Quality Standards

**Names:** Simple and descriptive. Not dramatic.
- ✅ `"Missing input validation in generated endpoints"`
- ❌ `"The Ultimate AI Doom Pattern of Infinite Regret"`

**Descriptions:** Concrete and specific.
- ✅ Describe what actually happens, with real examples
- ❌ Abstract definitions that could mean anything

**Severity:** Honest.
- `critical` = Can cause data loss, security breach, or complete feature failure
- `high` = Causes bugs that reach users
- `medium` = Causes maintainability or reliability issues
- `low` = Style or efficiency concern

**Examples:** Real code, not pseudocode.

---

## Code of Conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

---

## Questions?

Open an Issue with the label `question`. There are no dumb questions — especially if the answer should probably be in the docs.
