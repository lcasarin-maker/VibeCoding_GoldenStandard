#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Split the canonical Golden Standard into catalog YAML fragments.

This script operates on the Golden Standard repository.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

def setup_windows_utf8() -> None:
    if sys.platform == "win32":
        try:
            if hasattr(sys.stdout, "reconfigure"):
                sys.stdout.reconfigure(encoding="utf-8", errors="ignore")
            if hasattr(sys.stderr, "reconfigure"):
                sys.stderr.reconfigure(encoding="utf-8", errors="ignore")
        except (AttributeError, OSError, ValueError):
            pass

setup_windows_utf8()

GOLDEN_ROOT = Path(__file__).resolve().parent.parent
SOURCE = GOLDEN_ROOT / "golden_standard.yaml"


def _load_source_lines() -> list[str]:
    if not SOURCE.is_file():
        raise FileNotFoundError(f"Golden Standard source not found: {SOURCE}")
    return SOURCE.read_text(encoding="utf-8").splitlines(keepends=True)


def _slice(lines: list[str], start: int, end: int | None) -> str:
    return "".join(lines[start:end])


def _find_index(lines: list[str], prefix: str) -> int:
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return index
    raise KeyError(f"Could not find section starting with {prefix!r}")


def _is_manifest(lines: list[str]) -> bool:
    return any(line.startswith("catalogs:") for line in lines)


def main() -> int:
    import logging

    logger = logging.getLogger(__name__)
    try:
        lines = _load_source_lines()
    except FileNotFoundError as exc:
        logger.error("GS source not found: %s", exc)
        print(f"[ERROR] Golden Standard no encontrado: {exc}")
        return 1
    except Exception as exc:
        logger.error("Error inesperado al cargar GS: %s", exc, exc_info=True)
        print(f"[ERROR] Fallo inesperado: {exc}")
        return 1
    try:
        if _is_manifest(lines):
            fragments = [
                GOLDEN_ROOT / "golden_standard_tokenomics.yaml",
                GOLDEN_ROOT / "golden_standard_testing_vices.yaml",
                GOLDEN_ROOT / "golden_standard_coding_vices.yaml",
                GOLDEN_ROOT / "golden_standard_principles.yaml",
            ]
            missing = [
                str(p.relative_to(GOLDEN_ROOT)) for p in fragments if not p.is_file()
            ]
            if missing:
                raise FileNotFoundError(
                    f"Manifest split pero fragmentos faltantes: {missing}"
                )
            print(f"Golden Standard catalogs already split at {GOLDEN_ROOT}")
            return 0

        tokenomics_idx = _find_index(lines, "tokenomics:")
        testing_idx = _find_index(lines, "testing_vices:")
        coding_idx = _find_index(lines, "coding_vices:")
        principles_idx = _find_index(lines, "principles:")
        coding_details_idx = _find_index(lines, "coding_vices_details:")

        fragments = {
            "golden_standard_tokenomics.yaml": _slice(
                lines, tokenomics_idx, testing_idx
            ),
            "golden_standard_testing_vices.yaml": _slice(
                lines, testing_idx, coding_idx
            ),
            "golden_standard_coding_vices.yaml": _slice(
                lines, coding_idx, principles_idx
            )
            + _slice(lines, coding_details_idx, None),
            "golden_standard_principles.yaml": _slice(
                lines, principles_idx, coding_details_idx
            ),
        }

        for filename, content in fragments.items():
            if not content.strip():
                raise ValueError(f"Fragmento generado vacío: {filename}")
            (GOLDEN_ROOT / filename).write_text(content, encoding="utf-8")
    except (FileNotFoundError, KeyError, ValueError) as exc:
        logger.error("Error al procesar catálogos GS: %s", exc)
        print(f"[ERROR] Fallo al procesar catálogos: {exc}")
        return 1

    SOURCE.write_text(
        "format_version: 2\n"
        "description: Golden Standard canonical manifest. Data lives in split catalogs; this file indexes them.\n"
        "catalogs:\n"
        "  tokenomics: golden_standard_tokenomics.yaml\n"
        "  testing_vices: golden_standard_testing_vices.yaml\n"
        "  coding_vices: golden_standard_coding_vices.yaml\n"
        "  principles: golden_standard_principles.yaml\n",
        encoding="utf-8",
    )
    print(f"Golden Standard split complete at {GOLDEN_ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
