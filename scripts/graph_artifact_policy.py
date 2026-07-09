"""Policy helpers for generated GS graph artifacts.

The graph JSON and the human-facing wiki graph page are generated evidence
artifacts. This module records a small local receipt whenever the canonical
generator refreshes them, so local audits can distinguish a fresh regeneration
from a manual patch.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

GRAPH_ARTIFACTS = frozenset(
    {
        "output/golden_standard_graph.json",
        "Wiki/Graph.md",
    }
)
GRAPH_RECEIPT_REL = ".protocol/metadata/golden_standard_graph_receipt.json"


def normalize_repo_path(path: str | Path, root: Path | None = None) -> str:
    """Return a slash-separated repo-relative path when possible."""

    root_path = root.resolve() if root is not None else None
    raw = Path(path)
    resolved_rel: Path | None = None
    if root_path is not None:
        try:
            resolved_rel = raw.resolve().relative_to(root_path)
        except OSError:
            resolved_rel = None
        except ValueError:
            resolved_rel = None
    if resolved_rel is not None:
        return resolved_rel.as_posix()
    return str(path).strip().replace("\\", "/")


def is_graph_artifact(path: str | Path, root: Path | None = None) -> bool:
    """Return True when a path points to a generated GS graph artifact."""

    return normalize_repo_path(path, root) in GRAPH_ARTIFACTS


def receipt_path(root: Path) -> Path:
    """Return the local receipt path for graph regeneration evidence."""

    return root / GRAPH_RECEIPT_REL


def recommended_regeneration_command() -> str:
    """Return the canonical command that refreshes GS graph artifacts."""

    return "python scripts/generate_golden_audit.py"


def record_graph_regeneration(
    root: Path, command: str, outputs: Iterable[str | Path]
) -> Path | None:
    """Write a local receipt for a successful GS graph regeneration run."""

    root = root.resolve()
    normalized_outputs = [
        normalize_repo_path(path, root) for path in outputs if is_graph_artifact(path, root)
    ]
    if not normalized_outputs:
        return None

    receipt = receipt_path(root)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    output_hashes = {
        rel: _sha256_file(root / rel) for rel in sorted(set(normalized_outputs))
    }
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "command": command,
        "outputs": sorted(set(normalized_outputs)),
        "output_hashes": output_hashes,
    }
    receipt.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return receipt


def has_fresh_graph_receipt(root: Path, rel: str) -> bool:
    """Return True when a local receipt proves the artifact was regenerated."""

    root = root.resolve()
    rel = normalize_repo_path(rel)
    if rel not in GRAPH_ARTIFACTS:
        return False

    receipt = receipt_path(root)
    artifact = root / rel
    if not receipt.is_file() or not artifact.exists():
        return False

    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False

    outputs = {
        normalize_repo_path(item)
        for item in payload.get("outputs", [])
        if isinstance(item, str)
    }
    if rel not in outputs:
        return False
    output_hashes = payload.get("output_hashes")
    if not isinstance(output_hashes, dict):
        return False
    expected_hash = output_hashes.get(rel)
    if not isinstance(expected_hash, str) or not expected_hash:
        return False
    return expected_hash == _sha256_file(artifact)


def collect_git_paths(root: Path, staged: bool = False) -> list[str] | None:
    """Return changed git paths or None when git status cannot be read."""

    cmd = ["git", "diff", "--name-only", "--diff-filter=ACMR"]
    if staged:
        cmd.insert(2, "--cached")
    else:
        cmd = ["git", "status", "--porcelain=v1", "--untracked-files=all"]
    try:
        result = subprocess.run(
            cmd,
            cwd=str(root),
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    if staged:
        return sorted(
            {
                line.strip().replace("\\", "/")
                for line in result.stdout.splitlines()
                if line.strip()
            }
        )

    files: set[str] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = line[3:] if len(line) > 3 else line
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if path.strip():
            files.add(path.strip().replace("\\", "/"))
    return sorted(files)


def audit_graph_artifact_receipts(
    root: Path, files: Iterable[str] | None = None
) -> list[dict[str, str]]:
    """Return dirty GS graph artifacts lacking a fresh regeneration receipt."""

    root = root.resolve()
    candidate_files = collect_git_paths(root) if files is None else list(files)
    if candidate_files is None:
        return [
            {
                "path": ".",
                "command": "",
                "message": "Cannot read git state for GS graph-artifact verification.",
            }
        ]

    findings: list[dict[str, str]] = []
    seen: set[str] = set()
    for rel in candidate_files:
        normalized = normalize_repo_path(rel)
        if normalized in seen or normalized not in GRAPH_ARTIFACTS:
            continue
        seen.add(normalized)
        if has_fresh_graph_receipt(root, normalized):
            continue
        findings.append(
            {
                "path": normalized,
                "command": recommended_regeneration_command(),
                "message": (
                    "Generated GS graph artifact changed without a fresh regeneration receipt."
                ),
            }
        )
    return findings


def format_graph_artifact_audit_errors(
    root: Path, files: Iterable[str] | None = None
) -> list[str]:
    """Format dirty GS graph-artifact findings for audit output."""

    findings = audit_graph_artifact_receipts(root, files)
    return [
        (
            f"GS-GRAPH: {finding['path']} changed without regeneration evidence. "
            f"Run `{finding['command']}` instead of patching the artifact manually."
        )
        for finding in findings
    ]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()
