#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hook commit-msg (VC-073, norma de continuidad agnóstica): bloquea el commit si
hay cambios en archivos de deuda viva pero BACKLOG.md no se actualizó.

Agnóstico: corre con cualquier `git commit` (Codex/Gemini/Claude). BACKLOG es
OBLIGATORIO para cambios en archivos de deuda: NO hay token de escape en el mensaje.
El único escape es la env var consciente CERBERUS_SKIP_BACKLOG=1 (paralelo a VC-072).
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_BACKLOG = "BACKLOG.md"
_REQUIRED = ("## Live debt", "## Known auditor limitations")
# Archivos de deuda viva que, si se modifican, requieren BACKLOG.md actualizado
_DEBT_FILES = {
    "dimensions/*.py",
    "scripts/*.py",
    "protocol_engine/*.py",
    ".agent_state.json",
    "SPEC.md",
}

logger = logging.getLogger("check_backlog_sync")


def _staged_files() -> list[str]:
    """Rutas staged (git diff --cached). [] si git falla."""
    try:
        out = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True,
            cwd=str(_ROOT),
            check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        logger.warning("git diff --cached falló: %s", exc)
        return []
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _matches_debt_file(filepath: str) -> bool:
    """Verifica si el archivo está en la lista de archivos de deuda."""
    from fnmatch import fnmatch
    for pattern in _DEBT_FILES:
        if fnmatch(filepath, pattern):
            return True
    return False


def check_backlog_sync(staged: list[str], backlog_text: str, msg: str) -> tuple[bool, str]:
    """PURA. (ok, motivo). Bloquea si hay cambio en deuda y BACKLOG.md no está actualizado."""
    if os.environ.get("CERBERUS_SKIP_BACKLOG") == "1":
        return True, "escape explícito (env CERBERUS_SKIP_BACKLOG)"

    # Detectar si hay cambios en archivos de deuda viva
    debt_changes = [f for f in staged if _matches_debt_file(f)]

    if not debt_changes:
        return True, "sin cambios en archivos de deuda"

    # Si hay cambios en deuda, BACKLOG.md debe estar updated
    if not any(Path(f).name == _BACKLOG for f in staged):
        return (
            False,
            f"{_BACKLOG} no actualizado en este commit ({len(debt_changes)} archivos de deuda modificados)",
        )

    # Verificar que BACKLOG tenga secciones obligatorias
    missing = [s for s in _REQUIRED if s not in backlog_text]
    if missing:
        return False, f"{_BACKLOG} sin secciones obligatorias: {', '.join(missing)}"

    return True, "backlog sincronizado"


def main() -> int:
    if len(sys.argv) <= 1 or sys.argv[1] in ("-h", "--help"):
        print(
            "ℹ️ [BACKLOG VC-073] uso: check_backlog_sync.py <archivo-mensaje-commit>; "
            "sin archivo = modo informativo (no bloquea).",
            file=sys.stderr,
        )
        return 0
    try:
        msg = Path(sys.argv[1]).read_text(encoding="utf-8")
    except OSError as exc:
        logger.warning("mensaje de commit ilegible %s: %s", sys.argv[1], exc)
        msg = ""
    bp = _ROOT / _BACKLOG
    # V3.2 migration: tasks/backlog/ replaces BACKLOG.md — no check needed
    if not bp.exists() and (_ROOT / "tasks" / "backlog").exists():
        print("✅ [BACKLOG VC-073] V3.2 tasks/backlog/ active — BACKLOG.md check skipped.", file=sys.stderr)
        sys.exit(0)
    text = bp.read_text(encoding="utf-8") if bp.exists() else ""
    ok, reason = check_backlog_sync(_staged_files(), text, msg)
    if ok:
        print(f"✅ [BACKLOG VC-073] {reason}", file=sys.stderr)
        return 0
    print(
        f"❌ [BACKLOG VC-073] BLOQUEADO — {reason}.\n"
        f"   Actualiza {_BACKLOG} (Live debt) y haz `git add {_BACKLOG}`.\n"
        f"   Escape consciente solo para fixes triviales: export CERBERUS_SKIP_BACKLOG=1.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
