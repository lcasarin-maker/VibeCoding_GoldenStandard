---
name: obsidian-markdown
description: Edit the Golden Standard Wiki as an Obsidian-style Markdown vault. Use when creating or updating files under Wiki/ with wikilinks, aliases, index pages, or generated catalog note conventions.
source: https://github.com/kepano/obsidian-skills/tree/main/skills/obsidian-markdown
license: MIT
---

# GS Obsidian Markdown Skill

Use this skill for hand-authored edits under `Wiki/`. The GS Wiki is an
Obsidian-style vault, but its catalog pages are generated from YAML and must
not be freely reshaped by an agent.

## Rules

1. Preserve exact catalog filenames:
   - `Wiki/Vices/VC-XXX.md`
   - `Wiki/Vices/VT-XXX.md`
   - `Wiki/Tokenomics/TK-XXX.md`
   - `Wiki/Principles/PR-XXX.md` or the generated principles index when no per-page note exists.
2. Use Obsidian wikilinks for internal vault links:
   - `[[Vices/VC-021|VC-021]]`
   - `[[Tokenomics/TK-031|TK-031]]`
   - `[[Evidence/mypy_documentation|mypy documentation]]`
3. Keep aliases explicit. Do not rely on fuzzy display text when a canonical ID exists.
4. Do not add YAML frontmatter to generated catalog pages unless the generator already emits it.
5. Do not rename generated Wiki pages manually. Update the source YAML and regenerate instead.
6. Standard Markdown links are for external URLs or repo-relative non-vault files.
7. After edits, run:
   - `python scripts/validate_golden_standard_catalogs.py --check-wiki`
   - the relevant graph/alignment check from the consuming repo when the edit changes links.

## Safe Edit Pattern

1. Identify whether the target page is generated from YAML or hand-authored.
2. If generated, edit the YAML source first and regenerate the Wiki.
3. If hand-authored, edit the Markdown directly while preserving existing link style.
4. Verify that every new `[[wikilink]]` resolves to an existing page.
5. Keep navigation links back to `[[Home|Home]]`, the relevant index, or map page.
