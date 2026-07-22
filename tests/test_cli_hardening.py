from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

import scripts.conformity_report_cli as conformity_cli
import scripts.generate_golden_audit as golden_audit_cli
import scripts.split_golden_standard_catalogs as split_catalogs


def test_conformity_report_cli_returns_one_on_generator_error(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        conformity_cli,
        "ConformityReportGenerator",
        lambda *args, **kwargs: (_ for _ in ()).throw(ValueError("boom")),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["conformity_report_cli.py", "--gs-path", str(tmp_path)],
    )

    assert conformity_cli.main() == 1
    err = capsys.readouterr().err
    assert "ValueError" in err
    assert "boom" in err


def test_generate_golden_audit_returns_one_on_known_error(monkeypatch, capsys):
    def boom(argv=None):  # noqa: ARG001
        raise OSError("generator boom")

    monkeypatch.setattr(golden_audit_cli, "generate_main", boom)

    assert golden_audit_cli.main([]) == 1
    err = capsys.readouterr().err
    assert "OSError" in err
    assert "generator boom" in err


def test_split_catalogs_returns_one_on_source_read_error(monkeypatch, capsys):
    monkeypatch.setattr(
        split_catalogs,
        "_load_source_lines",
        lambda: (_ for _ in ()).throw(ValueError("bad source")),
    )

    assert split_catalogs.main() == 1
    out = capsys.readouterr().out
    assert "Fallo inesperado" in out
    assert "bad source" in out
