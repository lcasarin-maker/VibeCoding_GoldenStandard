#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GS Wiki linter — validates Obsidian links and detects orphaned notes.

GS-11: independent wiki validation, not dependent on Cerberus cross-repo audit.
Checks [[internal]] and [markdown](links) for targets, identifies orphans.

Resolution mirrors Obsidian: targets may be a path relative to the vault
(``Domains/CD01``) or a bare note name resolved anywhere in the vault
(``CD01``). The vault includes Wiki/ recursively plus repo-root .md files.
"""

import sys
import re
from pathlib import Path
import logging

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_DIR = REPO_ROOT / "Wiki"
OBSIDIAN_LINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
KNOWN_ORPHANS = {"Home"}  # Home is the index
# IDs that refer to catalog items, not .md files — don't validate them as broken links
ID_PATTERNS = re.compile(r"^(VC|VT|PR|TK|CD)-\d+$|^arxiv|^vexp_|^index$")


def _is_catalog_id(target: str) -> bool:
    """Check if target is a known catalog ID or special reference.

    Args:
        target: normalized link target.

    Returns:
        True when the target names a YAML catalog entry, not a note.
    """
    return bool(ID_PATTERNS.match(target.upper()))


def _normalize_target(target: str) -> str:
    """Normalize a link target: strip .md suffix, anchors and whitespace.

    Keeps any directory component (``Domains/CD01``) so path-style links
    resolve exactly; bare names fall back to vault-wide stem lookup.

    Args:
        target: raw link target text.

    Returns:
        Normalized target, or "" for anchor-only links.
    """
    target = target.strip()
    if target.startswith("#"):  # anchor-only link
        return ""
    target = target.split("#")[0].strip()  # remove anchor
    if target.endswith(".md"):
        target = target[:-3]
    return target.replace("\\", "/")


class _Vault:
    """Index of every note reachable by Obsidian-style resolution.

    Example:
        vault = _Vault(WIKI_DIR, REPO_ROOT)
        vault.resolve("Domains/CD01")  # -> "CD01"
    """

    def __init__(self, wiki_dir: Path, repo_root: Path):
        """Index Wiki/ recursively plus repo-root .md files.

        Args:
            wiki_dir: the Wiki directory (vault core).
            repo_root: repo root; its top-level .md files are also linkable.
        """
        self.files = sorted(wiki_dir.rglob("*.md"))
        self.by_path = {
            str(f.relative_to(wiki_dir).with_suffix("")).replace("\\", "/"): f
            for f in self.files
        }
        self.by_stem: dict[str, list[Path]] = {}
        for f in self.files:
            self.by_stem.setdefault(f.stem, []).append(f)
        # Repo-root notes (README, CONCEPTUAL_FRAMEWORK, ...) are valid targets
        # but do not count as wiki notes for orphan purposes.
        for f in sorted(repo_root.glob("*.md")):
            self.by_stem.setdefault(f.stem, []).append(f)

    def resolve(self, target: str) -> str | None:
        """Resolve a normalized target to a note stem.

        Args:
            target: normalized link target (path-style or bare name).

        Returns:
            The resolved note stem, or None when the target does not exist.
        """
        if target in self.by_path:
            return self.by_path[target].stem
        stem = target.split("/")[-1]
        if stem in self.by_stem:
            return stem
        return None


def _find_orphans(vault: _Vault, incoming: dict[str, set]) -> list[str]:
    """Find wiki notes with no incoming links (excluding tolerated orphans).

    Args:
        vault: indexed vault.
        incoming: note stem -> set of notes linking to it.

    Returns:
        Sorted list of orphaned note stems.
    """
    orphans = []
    for f in vault.files:
        if f.stem in KNOWN_ORPHANS:
            continue
        if f.stem not in incoming:
            orphans.append(f.stem)
    return sorted(set(orphans))


def lint_wiki() -> list[str]:
    """Lint the Wiki tree. Returns a list of human-readable errors.

    Checks every [[wikilink]] and [markdown](link) in every note
    (recursively) against the vault index, then reports orphans.
    """
    if not WIKI_DIR.exists():
        return ["Wiki directory not found"]

    vault = _Vault(WIKI_DIR, REPO_ROOT)
    if not vault.files:
        return ["No .md files found in Wiki"]

    errors: list[str] = []
    incoming: dict[str, set] = {}

    for md_file in vault.files:
        content = md_file.read_text(encoding="utf-8")
        # Inline code is literal text, not links (e.g. `[[0,0,0]]` examples).
        content = re.sub(r"`[^`\n]*`", "", content)
        note_stem = md_file.stem

        for regex, label in ((OBSIDIAN_LINK_RE, "[[{t}]]"), (MARKDOWN_LINK_RE, "[{t}]")):
            for match in regex.finditer(content):
                raw = match.group(1)
                if regex is MARKDOWN_LINK_RE and raw.startswith(("http://", "https://")):
                    continue  # external link
                if regex is MARKDOWN_LINK_RE and "/" in raw:
                    # Path-style markdown link: resolve on the filesystem
                    # relative to the linking note (../output/report.md).
                    candidate = (md_file.parent / raw.split("#")[0]).resolve()
                    if candidate.exists():
                        continue
                target = _normalize_target(raw)
                if not target:
                    continue
                resolved = vault.resolve(target)
                if resolved is not None:
                    if resolved != note_stem:
                        incoming.setdefault(resolved, set()).add(note_stem)
                elif not _is_catalog_id(target.split("/")[-1]):
                    errors.append(
                        f"{note_stem}: broken link " + label.format(t=target)
                    )

    for orphan in _find_orphans(vault, incoming):
        errors.append(f"Orphaned note: {orphan} (no incoming links)")

    return errors


def main(argv=None) -> int:
    """CLI entry point. Returns 0 when the wiki is clean, 1 otherwise."""
    parser = __import__("argparse").ArgumentParser(description="Lint GS Wiki")
    parser.parse_args(argv or [])

    errors = lint_wiki()
    if not errors:
        print("✅ Wiki linter passed. Zero broken links, zero orphans.")
        return 0

    for error in errors:
        print(f"❌ {error}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
