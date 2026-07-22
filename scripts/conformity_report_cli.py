#!/usr/bin/env python3
"""
Conformity Report CLI: Generate weekly compliance reports for satellites.

Usage:
    python conformity_report_cli.py --satellite Aequitas_OS --output report.md
    python conformity_report_cli.py --help
"""

import sys
import io
from pathlib import Path

# Force UTF-8 output on Windows
if sys.platform == "win32" and "pytest" not in sys.modules:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

from generate_conformity_report import ConformityReportGenerator


def main():
    """Entry point for conformity report generation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate Golden Standard conformity report for satellite repos"
    )
    parser.add_argument(
        "--gs-path",
        type=Path,
        default=Path(__file__).parent.parent,
        help="Path to GoldenStandard repo (default: current repo)",
    )
    parser.add_argument(
        "--satellite",
        type=str,
        default="Aequitas_OS",
        help="Satellite name (default: Aequitas_OS)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output markdown file (default: print to stdout)",
    )
    parser.add_argument(
        "--json",
        type=Path,
        default=None,
        help="Also output JSON report to this file",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed enforcement metrics",
    )

    args = parser.parse_args()

    try:
        generator = ConformityReportGenerator(args.gs_path, args.satellite)

        # Generate markdown report
        print(f"Generating conformity report for {args.satellite}...")
        markdown = generator.generate_report(args.output)

        if args.output:
            print(f"✅ Report written to: {args.output}")
        else:
            # Print to stdout
            print("\n" + "=" * 70 + "\n")
            print(markdown)
            print("\n" + "=" * 70)

        # Generate JSON if requested
        if args.json:
            json_data = generator.generate_json(args.json)
            print(f"✅ JSON data written to: {args.json}")

        # Print metrics summary if verbose
        if args.verbose:
            print("\n[METRICS SUMMARY]")
            vice_status = generator._calculate_vice_status()
            metrics = generator._calculate_metrics(vice_status)
            print(f"  Enforcement Coverage: {metrics.enforcement_coverage:.1f}%")
            print(f"  Doctrine Alignment: {metrics.doctrine_alignment:.1f}%")
            print(f"  Total Vices: {metrics.total_vices}")
            print(f"  Enforced: {metrics.enforced_vices}")
            print(f"  Partial: {metrics.partial_vices}")
            print(f"  Proposed Only: {metrics.proposed_only_vices}")

        return 0

    except (FileNotFoundError, OSError, RuntimeError, TypeError, ValueError) as e:
        print(
            f"❌ Error generating report: {type(e).__name__}: {e}",
            file=sys.stderr,
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
