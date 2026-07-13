"""Contrato con el consumidor real (GS-06): reimplementa localmente la
resolucion minima que usa protocol_engine/knowledge_loader.py de Cerberus
(manifest -> catalogs: {nombre: ruta} -> cada archivo tiene items: [...]),
SIN importar codigo de Cerberus -- los repos son independientes por diseño
(ver knowledge/CONSUMER_CONTRACT.md). Si este test se rompe, el loader real
de Cerberus tambien se romperia al leer este catalogo.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "golden_standard.yaml"


def _load_manifest() -> dict:
    return yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))


def test_manifest_exists_and_has_catalogs_mapping():
    assert MANIFEST_PATH.is_file(), "golden_standard.yaml es el manifest que resuelve el root del consumidor"
    manifest = _load_manifest()
    assert isinstance(manifest.get("catalogs"), dict) and manifest["catalogs"]


def test_every_referenced_catalog_file_resolves_and_has_items_list():
    manifest = _load_manifest()
    for catalog_name, relative_path in manifest["catalogs"].items():
        catalog_path = (ROOT / str(relative_path)).resolve()
        assert catalog_path.is_file(), f"{catalog_name} -> {relative_path} no existe (rompe get_golden_catalog_paths)"
        data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), f"{catalog_name}: el archivo debe parsear a un mapping"
        assert isinstance(data.get("items"), list), (
            f"{catalog_name}: falta 'items' como lista -- "
            "load_golden_standard_catalogs()/load_golden_standard() de Cerberus lo asume"
        )


def test_every_item_has_the_fields_the_consumer_contract_reads():
    """id/title/status son los campos minimos que gs_lint.py YA exige
    (check_missing_required_fields) y que cualquier consumidor razonable
    necesita para mostrar/filtrar una entrada."""
    manifest = _load_manifest()
    for catalog_name, relative_path in manifest["catalogs"].items():
        catalog_path = (ROOT / str(relative_path)).resolve()
        data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
        for item in data["items"]:
            for field in ("id", "title", "status"):
                assert item.get(field), f"{catalog_name}/{item.get('id', '?')}: falta {field!r}"


def test_format_version_is_well_formed_for_drift_detection():
    """format_version es una cadena de deteccion de drift (no semver
    validado -- HANDOFF.md 2026-07-03 lo documenta explicitamente como
    limitacion conocida). Este test solo exige que tenga forma MAJOR.MINOR
    numerica, para que un consumidor pueda al menos comparar "cambio" vs
    "sin cambio" de forma determinista. Definir que constituye un cambio
    BREAKING queda fuera de alcance: es una decision de producto, no un
    gate mecanico que se pueda inventar sin el criterio de ambos repos."""
    manifest = _load_manifest()
    version = str(manifest.get("format_version", ""))
    assert re.fullmatch(r"\d+\.\d+", version), f"format_version {version!r} no tiene forma MAJOR.MINOR"
