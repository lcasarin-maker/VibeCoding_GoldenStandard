# knowledge/ — Protocol & Sources

GS-specific governance documents for knowledge intake and consumer contracts.
This folder holds **operational protocols**, not catalog content. The catalogs are at root.

## Contents

- [`CANONICAL_STRUCTURE.md`](CANONICAL_STRUCTURE.md) — **authoritative V3.2 repo structure standard** for CC, GS, and satellites (moved from CC 2026-06-22)
- [`INGESTION_PROTOCOL.md`](INGESTION_PROTOCOL.md) — quality gate: how raw findings become catalog entries
- [`KNOWLEDGE_SOURCES.md`](KNOWLEDGE_SOURCES.md) — authorized sources and their contracts
- [`CONSUMER_CONTRACT.md`](CONSUMER_CONTRACT.md) — boundary contract for downstream consumers of GS

## How knowledge flows

```
Inbox/   →  INGESTION_PROTOCOL.md  →  YAML catalogs (root)  →  Wiki/
(raw)         (quality gate)            (curated)               (navigation)
```

Hypotheses live in `Inbox/`. Promoted findings go into the YAML catalogs.
There is no intermediate holding area — if it is not in the catalog, it is not GS knowledge.
