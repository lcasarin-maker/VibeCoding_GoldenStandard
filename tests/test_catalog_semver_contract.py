from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "tests" / "fixtures" / "cerberus_consumer_contract.yaml"
MANIFEST = ROOT / "golden_standard.yaml"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")


def _load(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _semver(value: object) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(str(value))
    assert match, f"{value!r} is not strict MAJOR.MINOR.PATCH SemVer"
    return tuple(int(part) for part in match.groups())


def test_fixture_itself_is_versioned_and_matches_manifest_surface():
    contract = _load(CONTRACT)
    manifest = _load(MANIFEST)
    _semver(contract["contract_version"])
    assert set(contract["required_catalogs"]) == set(manifest["catalogs"])


def test_manifest_semver_stays_inside_consumer_range():
    contract = _load(CONTRACT)["manifest_semver"]
    current = _semver(_load(MANIFEST)["format_version"])
    assert _semver(contract["minimum"]) <= current
    assert current < _semver(contract["maximum_exclusive"])


def test_every_catalog_uses_supported_semver_major_and_shape():
    contract = _load(CONTRACT)["catalog_schema"]
    manifest = _load(MANIFEST)
    required_top = set(contract["required_top_level"])
    required_fields = set(contract["required_item_fields"])

    for name, relative_path in manifest["catalogs"].items():
        data = _load(ROOT / relative_path)
        assert required_top <= set(data), f"{name}: incompatible top-level schema"
        assert _semver(data["format_version"])[0] == contract["supported_major"]
        ids = []
        for item in data["items"]:
            assert required_fields <= set(item), f"{name}/{item.get('id', '?')}: missing consumer field"
            ids.append(item["id"])
        assert len(ids) == len(set(ids)), f"{name}: duplicate ids break consumer indexing"


def test_contract_rejects_abbreviated_or_yaml_numeric_versions():
    for invalid in (2.1, "2.1", "v2.1.0", "02.1.0", "2.1.0-rc1"):
        try:
            _semver(invalid)
        except AssertionError:
            continue
        raise AssertionError(f"consumer contract accepted non-strict SemVer: {invalid!r}")
