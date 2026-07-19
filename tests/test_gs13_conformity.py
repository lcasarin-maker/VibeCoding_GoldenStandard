"""
Tests for GS-13 Conformity Report Generator.

Verifies:
- Catalogs actually load (non-empty; empty catalogs must be a hard error)
- Vice status derives from catalog fields, never assumed
- Metrics computation over the real 300+ item corpus
- Report generation (markdown and JSON)
- Real CLI invocation via subprocess
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_conformity_report import (
    ConformityMetrics,
    ConformityReportGenerator,
    ViceStatus,
)


@pytest.fixture
def gs_path():
    """Path to GoldenStandard repo."""
    return Path(__file__).parent.parent


class TestConformityReportGenerator:
    """Test suite for ConformityReportGenerator."""

    def test_initialization(self, gs_path):
        """Generator initializes and loads every catalog non-empty."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Aequitas_OS")

        assert generator.satellite_name == "Aequitas_OS"
        assert generator.gs_path == gs_path
        assert generator.audit_date is not None

    def test_load_vices(self, gs_path):
        """Coding vices catalog loads its real items (94+ as of 2026-07)."""
        generator = ConformityReportGenerator(gs_path)
        assert len(generator.vices) >= 90
        assert all(k.startswith("VC-") for k in generator.vices)

    def test_load_principles(self, gs_path):
        """Principles catalog loads its real items (122+ as of 2026-07)."""
        generator = ConformityReportGenerator(gs_path)
        assert len(generator.principles) >= 120
        assert "PR-122" in generator.principles  # Canonical Correction

    def test_load_testing_vices(self, gs_path):
        """Testing vices catalog loads its real items (116+ as of 2026-07)."""
        generator = ConformityReportGenerator(gs_path)
        assert len(generator.testing_vices) >= 110

    def test_missing_catalog_is_hard_error(self, gs_path):
        """An empty/missing catalog must raise, not silently report 0 items."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises((FileNotFoundError, ValueError)):
                ConformityReportGenerator(Path(tmpdir))

    def test_vice_status_dataclass(self):
        """ViceStatus dataclass holds derived fields."""
        status = ViceStatus(
            vice_id="VC-001",
            vice_type="VC",
            name="Mutable Default Arguments",
            status="ENFORCED",
            enforcing_rules=["static-ast"],
            coverage=1.0,
            evidence="def func(x=[]):",
        )

        assert status.vice_id == "VC-001"
        assert status.status == "ENFORCED"
        assert status.coverage == 1.0

    def test_calculate_vice_status_derives_from_catalog(self, gs_path):
        """Statuses come from the catalog's own status field, not assumptions."""
        generator = ConformityReportGenerator(gs_path)
        vice_status = generator._calculate_vice_status()

        assert len(vice_status) >= 320  # 94 VC + 116 TV + 122 PR

        for vice_id, status in vice_status.items():
            assert isinstance(status, ViceStatus)
            assert status.vice_type in ("VC", "TV", "PR")
            raw = generator.catalogs[status.vice_type][vice_id]
            if raw["status"] == "PREVENTED":
                assert status.status == "ENFORCED" and status.coverage == 1.0
            elif raw["status"] == "REMEDIATED":
                assert status.status == "REMEDIATED"
            else:
                assert status.status == "DOC_ONLY" and status.coverage == 0.0

    def test_calculate_metrics(self, gs_path):
        """Metrics reflect the real catalog composition."""
        generator = ConformityReportGenerator(gs_path)
        vice_status = generator._calculate_vice_status()
        metrics = generator._calculate_metrics(vice_status)

        assert isinstance(metrics, ConformityMetrics)
        assert metrics.total_vices == len(vice_status)
        assert 0 < metrics.enforcement_coverage < 100
        assert metrics.enforced_vices + metrics.partial_vices + metrics.proposed_only_vices == metrics.total_vices
        # PREVENTED items exist in every catalog snapshot we ship.
        assert metrics.enforced_vices >= 90
        # DOC_ONLY items require human judgment.
        assert metrics.manual_reviews == metrics.proposed_only_vices

    def test_doctrine_alignment_counts_justified_doc_only(self, gs_path):
        """Alignment > coverage because justified DOC_ONLY items count as aligned."""
        generator = ConformityReportGenerator(gs_path)
        vice_status = generator._calculate_vice_status()
        metrics = generator._calculate_metrics(vice_status)

        assert metrics.doctrine_alignment >= metrics.enforcement_coverage

    def test_generate_report_markdown(self, gs_path):
        """Markdown report contains the real sections and satellite name."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Test_Satellite")
        markdown = generator.generate_report()

        assert "Golden Standard Conformity Report" in markdown
        assert "Test_Satellite" in markdown
        assert "Executive Summary" in markdown
        assert "Enforcement Coverage" in markdown
        assert "Recommendations" in markdown

    def test_generate_report_to_file(self, gs_path):
        """Markdown report writes to file identically to the returned string."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "conformity_report.md"
            generator = ConformityReportGenerator(gs_path)
            markdown = generator.generate_report(output_path)

            assert output_path.exists()
            assert output_path.read_text(encoding="utf-8") == markdown

    def test_generate_json(self, gs_path):
        """JSON report carries metrics and the full vice list."""
        generator = ConformityReportGenerator(gs_path)
        data = json.loads(generator.generate_json())

        assert "metrics" in data
        assert "vices" in data
        assert data["metrics"]["total_vices"] == len(data["vices"])
        assert len(data["vices"]) >= 320

    def test_generate_json_to_file(self, gs_path):
        """JSON report writes valid JSON to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "conformity_report.json"
            generator = ConformityReportGenerator(gs_path)
            generator.generate_json(output_path)

            data = json.loads(output_path.read_text(encoding="utf-8"))
            assert "metrics" in data
            assert "vices" in data

    def test_metrics_calculation_edge_cases(self, gs_path):
        """Empty status map yields zeroed metrics without division errors."""
        generator = ConformityReportGenerator(gs_path)
        metrics = generator._calculate_metrics({})

        assert metrics.enforcement_coverage == 0
        assert metrics.total_vices == 0

    def test_report_structure(self, gs_path):
        """Complete report structure: all sections present."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Aequitas_OS")
        markdown = generator.generate_report()

        expected_sections = [
            "# Golden Standard Conformity Report",
            "## Executive Summary",
            "## 1. Coding Vices (VC-*)",
            "## 2. Testing Vices (TV-*)",
            "## 3. Principles (PR-*)",
            "## 4. Active Enforcement Mechanisms",
            "## 5. Recommendations",
            "## 6. Conformity Audit Trail",
        ]

        for section in expected_sections:
            assert section in markdown, f"Missing section: {section}"

        assert "| Metric | Value |" in markdown


class TestConformityReportCLI:
    """Test CLI functionality end-to-end (real subprocess)."""

    def test_cli_writes_report_and_json(self, gs_path):
        """CLI produces markdown + JSON files and exits 0."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_md = Path(tmpdir) / "report.md"
            out_json = Path(tmpdir) / "report.json"
            result = subprocess.run(
                [
                    sys.executable,
                    str(gs_path / "scripts" / "generate_conformity_report.py"),
                    "--gs-path", str(gs_path),
                    "--satellite", "CLI_Test",
                    "--output", str(out_md),
                    "--json", str(out_json),
                ],
                capture_output=True,
                text=True,
                timeout=120,
            )
            assert result.returncode == 0, result.stderr
            assert out_md.exists()
            assert "CLI_Test" in out_md.read_text(encoding="utf-8")
            data = json.loads(out_json.read_text(encoding="utf-8"))
            assert data["metrics"]["satellite_name"] == "CLI_Test"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
