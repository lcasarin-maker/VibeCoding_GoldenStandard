#!/usr/bin/env python3
"""Prove each local detector fires on its vice's example_bad and stays silent on example_good.

This is the contract that makes a detector real: it must discriminate the catalog's own
cataloged pair. Run in CI alongside catalog validation. Exits non-zero on any false
negative (missed the bad example) or false positive (fired on the good example).
"""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from detectors import DETECTORS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
CATALOGS = (
    "golden_standard_coding_vices.yaml",
    "golden_standard_testing_vices.yaml",
    "golden_standard_tokenomics.yaml",
)


def load_entries() -> dict:
    entries = {}
    for catalog in CATALOGS:
        data = yaml.safe_load((ROOT / catalog).read_text(encoding="utf-8"))
        for item in data.get("items", []):
            entries[str(item.get("id", "")).strip()] = item
    return entries


def main() -> int:
    entries = load_entries()
    errors: list[str] = []

    for vice_id, detector in DETECTORS.items():
        item = entries.get(vice_id)
        if item is None:
            errors.append(f"{vice_id}: detector maps to an unknown catalog id.")
            continue
        bad = str(item.get("example_bad", "")).strip()
        good = str(item.get("example_good", "")).strip()
        if not bad or not good:
            errors.append(f"{vice_id}: entry lacks example_bad/example_good to prove against.")
            continue
        if not detector(bad):
            errors.append(f"{vice_id}: detector did NOT fire on example_bad (false negative).")
        if detector(good):
            errors.append(f"{vice_id}: detector FIRED on example_good (false positive).")
        # The entry should advertise the detector so the wiki shows it is enforced locally.
        declared = str(item.get("detector", "")).strip()
        if declared and declared != detector.__name__:
            errors.append(f"{vice_id}: declared detector '{declared}' != registered '{detector.__name__}'.")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"All {len(DETECTORS)} local detectors proven against the catalog corpus "
          f"(fire on example_bad, silent on example_good).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
