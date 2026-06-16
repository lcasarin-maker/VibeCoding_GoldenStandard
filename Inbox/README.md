# Inbox — Golden Standard Knowledge Ingestion

This directory is the **intake mailbox** of the knowledge base.
Raw findings are deposited here before being curated and promoted to the catalog.

> **For the full ingestion protocol, see:** [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md)  
> **For authorized sources and their contracts, see:** [`KNOWLEDGE_SOURCES.md`](../KNOWLEDGE_SOURCES.md)

---

## Directory Structure

```
Inbox/
├── cerberus/      ← Findings from CoderCerberus audits
├── manual/        ← Findings from manual DRI sessions
├── external/      ← External contributions (triaged by maintainers)
└── templates/
    ├── cerberus_finding.md        ← Template for Cerberus findings
    ├── manual_finding.md          ← Template for manual findings
    └── external_contribution.md   ← Template for external contributions
```

### Notes per Folder

- [`cerberus/README.md`](cerberus/README.md) — what to deposit and how to name it.
- [`manual/README.md`](manual/README.md) — findings observed by the DRI.
- [`external/README.md`](external/README.md) — flow for external issues and PRs; only evidence anchored to the active baseline and with fresh purge if auditing cleanliness or completeness.
- [`templates/README.md`](templates/README.md) — quick reference for templates.

---

## How to Deposit a Finding (quick summary)

1. Copy the appropriate template from `Inbox/templates/`
2. Fill all required fields (marked with ✅ in the template)
3. Save the file in the correct subdirectory with the naming convention:
   ```
   YYYY-MM-DD_<slug>.md
   ```
4. Commit with the message: `inbox: <source> finding <slug>`

The curator will review the finding and promote it to the YAML catalog + Wiki following [`INGESTION_PROTOCOL.md`](../INGESTION_PROTOCOL.md).

### Depth Requirement (Definition of Done)

To prevent the catalog from filling again with declarative stubs, an entry **is not promoted** until it meets one of these two paths:

- **Falsifiable (`deep`)** — brings `example_bad`, `example_good`, a concrete `detection` recipe, and at least one `evidence`. If the signature is statically checkable, it must also register a detector in [`scripts/detectors.py`](../scripts/detectors.py) tested against its examples.
- **Doctrinal** — if it is a behavioral/epistemic principle with no static signature, it is marked `doctrinal: true` explicitly (stub by design, not by neglect). Fabricating example code for it is prohibited.

A finding that is neither `deep` nor explicitly `doctrinal` is a **stub** and stays in the Inbox until enriched. The `stubs` badge (in the README, calculated by [`scripts/metrics.py`](../scripts/metrics.py)) must remain at **0** in the curated catalog.

> Templates under `Inbox/templates/` are intentionally isolated. They are not live knowledge yet; they are molds for new findings.

---

## Ingestion Flow

```
Source (Cerberus / Manual / External)
        ↓
Deposit in Inbox/<source>/YYYY-MM-DD_<slug>.md
        ↓
Curator validates → deduplicates → maps domain
        ↓
Add entry to golden_standard_*.yaml (status: KNOWLEDGE)
        ↓
Create Wiki article in Wiki/Vices/
        ↓
Run generate_golden_audit.py
        ↓
Move file to deprecated/
```
