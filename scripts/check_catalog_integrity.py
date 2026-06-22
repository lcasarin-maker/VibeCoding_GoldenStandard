"""GS-010: Corruption guard for YAML catalogs.

Rejects:
- Zero-byte or empty files
- Files not decodeable as UTF-8
- Files with UTF-8 replacement chars (U+FFFD) indicating mojibake
- Files where yaml.safe_load fails (truncated or malformed YAML)

Exit 0 = all clean. Exit 1 = at least one catalog is corrupt.
"""

import sys
import yaml
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_CATALOGS = list(_ROOT.glob("golden_standard_*.yaml"))


def check(path: Path) -> list[str]:
    errors: list[str] = []

    raw = path.read_bytes()
    if len(raw) == 0:
        errors.append(f"{path.name}: zero bytes")
        return errors

    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        errors.append(f"{path.name}: UTF-8 decode error — {e}")
        return errors

    if "�" in text:
        errors.append(f"{path.name}: contains U+FFFD replacement char (mojibake)")

    try:
        yaml.safe_load(text)
    except yaml.YAMLError as e:
        errors.append(f"{path.name}: YAML parse error — {e}")

    return errors


def main() -> int:
    if not _CATALOGS:
        print("ERROR: no golden_standard_*.yaml found", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for catalog in sorted(_CATALOGS):
        all_errors.extend(check(catalog))

    if all_errors:
        for err in all_errors:
            print(f"CORRUPT: {err}", file=sys.stderr)
        return 1

    print(f"Catalog integrity OK ({len(_CATALOGS)} files checked)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
