from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = yaml.safe_load(
    (ROOT / "knowledge" / "CONSUMER_CONTRACT.yaml").read_text(encoding="utf-8")
)


def _validator_surfaces() -> list[Path]:
    return [ROOT / rel for rel in CONTRACT.get("validator_surfaces", []) if (ROOT / rel).exists()]


def test_validator_surfaces_do_not_retain_historical_aliases() -> None:
    findings: list[str] = []
    banned_tokens = [str(item).casefold() for item in CONTRACT.get("banned_tokens", [])]
    exceptions = {
        str(item)
        for item in CONTRACT.get("exception_files", [])
    }

    for path in _validator_surfaces():
        rel = path.relative_to(ROOT).as_posix()
        if rel in exceptions:
            continue

        lowered = path.read_text(encoding="utf-8").casefold()
        offenders = [token for token in banned_tokens if token in lowered]
        if offenders:
            findings.append(f"{rel}: {', '.join(sorted(offenders))}")

    assert not findings, (
        "Historical aliases must not survive in validator surfaces: "
        + "; ".join(findings)
    )
