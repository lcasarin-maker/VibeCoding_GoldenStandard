from pathlib import Path

from gs_generator.engine import (
    MANUAL_NOTES_DIRNAME,
    clean_wiki_directory,
    write_manual_notes_roster,
)


def test_clean_wiki_directory_preserves_manual_notes_tree(tmp_path: Path):
    wiki_dir = tmp_path / "Wiki"
    manual_entry = wiki_dir / MANUAL_NOTES_DIRNAME / "entries" / "2026-07-19_note.md"
    manual_entry.parent.mkdir(parents=True, exist_ok=True)
    manual_entry.write_text("manual note", encoding="utf-8")
    stray = wiki_dir / "ephemeral.md"
    stray.parent.mkdir(parents=True, exist_ok=True)
    stray.write_text("remove me", encoding="utf-8")

    clean_wiki_directory(wiki_dir)

    assert manual_entry.exists()
    assert manual_entry.read_text(encoding="utf-8") == "manual note"
    assert not stray.exists()


def test_write_manual_notes_roster_lists_preserved_surfaces(tmp_path: Path):
    wiki_dir = tmp_path / "Wiki"
    (wiki_dir / MANUAL_NOTES_DIRNAME / "entries").mkdir(parents=True, exist_ok=True)

    write_manual_notes_roster(wiki_dir)

    roster = wiki_dir / MANUAL_NOTES_DIRNAME / "ROSTER.md"
    content = roster.read_text(encoding="utf-8")

    assert "Wiki/Home.md" in content
    assert "Wiki/Falsifiability_Report.md" in content
    assert "Wiki/.manual_notes/entries/*.md" in content
    assert "The compiler skips the `.manual_notes` directory" in content
