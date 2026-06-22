---
id: GS-010
title: Adopt corruption guard upstream-style (mojibake / truncation pre-commit)
status: backlog
priority: medium
created: 2026-06-10
---

## Goal
Mirror the Cerberus corruption/encoding guard as a GS-side pre-commit check.
Reject mojibake or truncated content in catalogs before commit.

## Acceptance criteria
- [ ] Pre-commit hook (or CI check) rejects mojibake in any YAML catalog
- [ ] Pre-commit hook rejects catalog files with 0 bytes or truncated YAML
- [ ] Guard is documented in AGENTS.md §1 or CONTRIBUTING.md

## Blockers
none
