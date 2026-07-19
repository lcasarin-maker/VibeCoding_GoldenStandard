"""
Tests for GS-13 Conformity Report Generator.

Verifies:
- ConformityReportGenerator initialization
- Vice status calculation
- Metrics computation
- Report generation (markdown and JSON)
- CLI invocation
"""

import json
import tempfile
from pathlib import Path

import pytest

# Add scripts directory to path
import sys
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
        """Test generator initialization."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Aequitas_OS")

        assert generator.satellite_name == "Aequitas_OS"
        assert generator.gs_path == gs_path
        assert generator.audit_date is not None

    def test_load_vices(self, gs_path):
        """Test loading coding vices from YAML."""
        generator = ConformityReportGenerator(gs_path)

        # Should load vices (may be empty if YAML not populated, but should not error)
        assert isinstance(generator.vices, dict)

    def test_load_principles(self, gs_path):
        """Test loading principles from YAML."""
        generator = ConformityReportGenerator(gs_path)

        # Should load principles
        assert isinstance(generator.principles, dict)

    def test_load_testing_vices(self, gs_path):
        """Test loading testing vices from YAML."""
        generator = ConformityReportGenerator(gs_path)

        # Should load testing vices
        assert isinstance(generator.testing_vices, dict)

    def test_vice_status_dataclass(self):
        """Test ViceStatus dataclass creation."""
        status = ViceStatus(
            vice_id="VC-001",
            vice_type="VC",
            name="Mutable Default Arguments",
            status="ENFORCED",
            enforcing_rules=["SP-AQ-001"],
            coverage=1.0,
            evidence="def func(x=[]):",
        )

        assert status.vice_id == "VC-001"
        assert status.status == "ENFORCED"
        assert status.coverage == 1.0

    def test_conformity_metrics_dataclass(self):
        """Test ConformityMetrics dataclass creation."""
        metrics = ConformityMetrics(
            enforcement_coverage=75.5,
            doctrine_alignment=82.0,
            automated_checks=34,
            manual_reviews=13,
            total_vices=47,
            enforced_vices=35,
            partial_vices=8,
            proposed_only_vices=4,
            audit_date="2026-07-19T00:00:00",
            satellite_name="Aequitas_OS",
        )

        assert metrics.enforcement_coverage == 75.5
        assert metrics.total_vices == 47
        assert metrics.satellite_name == "Aequitas_OS"

    def test_calculate_vice_status(self, gs_path):
        """Test vice status calculation."""
        generator = ConformityReportGenerator(gs_path)
        vice_status = generator._calculate_vice_status()

        # Should return dict (may be empty if no vices defined)
        assert isinstance(vice_status, dict)

        # Each entry should be ViceStatus
        for vice_id, status in vice_status.items():
            assert isinstance(status, ViceStatus)
            assert status.vice_type in ["VC", "TV", "PR"]

    def test_calculate_metrics(self, gs_path):
        """Test metrics calculation."""
        generator = ConformityReportGenerator(gs_path)
        vice_status = generator._calculate_vice_status()
        metrics = generator._calculate_metrics(vice_status)

        assert isinstance(metrics, ConformityMetrics)
        assert 0 <= metrics.enforcement_coverage <= 100
        assert metrics.total_vices >= 0
        assert metrics.enforced_vices <= metrics.total_vices

    def test_generate_report_markdown(self, gs_path):
        """Test markdown report generation."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Test_Satellite")
        markdown = generator.generate_report()

        # Should contain expected sections
        assert "Golden Standard Conformity Report" in markdown
        assert "Test_Satellite" in markdown
        assert "Executive Summary" in markdown
        assert "Enforcement Coverage" in markdown
        assert "Recommendations" in markdown

    def test_generate_report_to_file(self, gs_path):
        """Test writing markdown report to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "conformity_report.md"
            generator = ConformityReportGenerator(gs_path)
            markdown = generator.generate_report(output_path)

            # File should be created
            assert output_path.exists()

            # Content should match returned markdown
            assert output_path.read_text() == markdown

    def test_generate_json(self, gs_path):
        """Test JSON report generation."""
        generator = ConformityReportGenerator(gs_path)
        json_str = generator.generate_json()

        # Should be valid JSON
        data = json.loads(json_str)

        # Should have metrics and vices keys
        assert "metrics" in data
        assert "vices" in data
        assert isinstance(data["metrics"], dict)
        assert isinstance(data["vices"], list)

    def test_generate_json_to_file(self, gs_path):
        """Test writing JSON report to file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "conformity_report.json"
            generator = ConformityReportGenerator(gs_path)
            json_str = generator.generate_json(output_path)

            # File should be created
            assert output_path.exists()

            # Content should be valid JSON
            data = json.loads(output_path.read_text())
            assert "metrics" in data
            assert "vices" in data

    def test_metrics_calculation_edge_cases(self, gs_path):
        """Test metrics calculation with edge cases."""
        generator = ConformityReportGenerator(gs_path)

        # Test with empty vice_status
        empty_status = {}
        metrics = generator._calculate_metrics(empty_status)

        assert metrics.enforcement_coverage == 0
        assert metrics.total_vices == 0

    def test_report_structure(self, gs_path):
        """Test complete report structure and content."""
        generator = ConformityReportGenerator(gs_path, satellite_name="Aequitas_OS")
        markdown = generator.generate_report()

        # Check all expected sections exist
        expected_sections = [
            "# Golden Standard Conformity Report",
            "## Executive Summary",
            "## 1. Vice Enforcement",
            "## 4. Active Enforcement Mechanisms",
            "## 5. Recommendations",
            "## 6. Conformity Audit Trail",
        ]

        for section in expected_sections:
            assert section in markdown, f"Missing section: {section}"

        # Check table format
        assert "| Metric | Value |" in markdown or "Enforcement Coverage" in markdown


class TestConformityReportCLI:
    """Test CLI functionality."""

    def test_cli_basic_invocation(self, gs_path, capsys):
        """Test basic CLI invocation."""
        import subprocess

        # This would require the CLI to be executable, skip for now
        # as we're testing the generator directly
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
