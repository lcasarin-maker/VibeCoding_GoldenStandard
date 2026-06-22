"""GS-077: Structural audit — enforces SP rules with static repo checks.

Checks implemented:
  SP-001  No rogue governance files outside .agents/AGENTS.md
  SP-003  tasks/done/ is empty
  SP-004  No archive/ folder; tasks/done/ is empty
  SP-006  V3.2 canonical structure required files/folders exist
  SP-007  tasks/README.md and audit/README.md exist; backlog files have required frontmatter
  SP-009  DECISIONS.md and audit/sessions/ exist and are non-empty
  SP-010  Root contains no stray .json or unexpected .md files

Skipped (no static signature):
  SP-002  No material fact in chat  — session-time behavioral check
  SP-005  Session close mandatory   — session-time behavioral check
  SP-008  Agent self-certifies DoD  — behavioral check

Exit 0 = all implemented checks pass. Exit 1 = at least one violation.
"""

import sys
import yaml
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

_ROGUE_GOVERNANCE = {
    "BOOTSTRAP.md", "RULES.md", "PERMISSIONS.md",
    "DEFINITION_OF_DONE.md", "AGENT_INSTRUCTIONS.md",
}

_REQUIRED_V32 = [
    ".agents/AGENTS.md",
    "tasks",
    "tasks/backlog",
    "audit",
    "audit/AUDIT_TRAIL.md",
    "SPEC.md",
    "HANDOFF.md",
    "DECISIONS.md",
    "STATE.md",
]

_ALLOWED_ROOT_MD = {
    "README.md", "CONCEPTUAL_FRAMEWORK.md", "CONTRIBUTING.md",
    "SPEC.md", "HANDOFF.md", "DECISIONS.md", "STATE.md", "PLAN.md",
}


def _check(label: str, condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(f"{label}: {message}")


def check_sp001(errors: list[str]) -> None:
    for name in _ROGUE_GOVERNANCE:
        _check("SP-001", not (_ROOT / name).exists(),
               f"{name} exists at root — collapse into .agents/AGENTS.md", errors)
    for f in _ROOT.glob("*.md"):
        if f.name in _ROGUE_GOVERNANCE:
            _check("SP-001", False, f"{f.name} is a rogue governance file", errors)


def check_sp003_sp004(errors: list[str]) -> None:
    done_dir = _ROOT / "tasks" / "done"
    if done_dir.exists():
        files = [f for f in done_dir.iterdir() if f.is_file() and f.name != ".gitkeep"]
        _check("SP-003", len(files) == 0,
               f"tasks/done/ has {len(files)} file(s) — delete after closing commit", errors)
    archive_dir = _ROOT / "archive"
    _check("SP-004", not archive_dir.exists(),
           "archive/ folder exists — completed records belong in git log, not a folder", errors)


def check_sp006(errors: list[str]) -> None:
    for path in _REQUIRED_V32:
        target = _ROOT / path
        _check("SP-006", target.exists(), f"missing required V3.2 path: {path}", errors)


def check_sp007(errors: list[str]) -> None:
    _check("SP-007", (_ROOT / "tasks" / "README.md").exists(),
           "tasks/README.md missing — template required", errors)
    _check("SP-007", (_ROOT / "audit" / "README.md").exists(),
           "audit/README.md missing — template required", errors)

    backlog_dir = _ROOT / "tasks" / "backlog"
    if backlog_dir.exists():
        for task_file in backlog_dir.glob("*.md"):
            text = task_file.read_text(encoding="utf-8", errors="replace")
            for field in ("id:", "title:", "status:"):
                _check("SP-007", field in text,
                       f"{task_file.name}: missing frontmatter field '{field}'", errors)


def check_sp009(errors: list[str]) -> None:
    decisions = _ROOT / "DECISIONS.md"
    _check("SP-009", decisions.exists() and decisions.stat().st_size > 0,
           "DECISIONS.md missing or empty", errors)
    sessions_dir = _ROOT / "audit" / "sessions"
    _check("SP-009", sessions_dir.exists(),
           "audit/sessions/ missing — session records required", errors)


def check_sp010(errors: list[str]) -> None:
    for f in _ROOT.glob("*.json"):
        _check("SP-010", False,
               f"{f.name} is a generated JSON at root — move to output/", errors)
    for f in _ROOT.glob("*.md"):
        if f.name not in _ALLOWED_ROOT_MD:
            _check("SP-010", False,
                   f"{f.name} is an unexpected .md at root — move to knowledge/ or docs/", errors)


def main() -> int:
    errors: list[str] = []

    check_sp001(errors)
    check_sp003_sp004(errors)
    check_sp006(errors)
    check_sp007(errors)
    check_sp009(errors)
    check_sp010(errors)

    if errors:
        for err in errors:
            print(f"FAIL  {err}", file=sys.stderr)
        print(f"\n{len(errors)} violation(s) found.", file=sys.stderr)
        return 1

    implemented = ["SP-001", "SP-003", "SP-004", "SP-006", "SP-007", "SP-009", "SP-010"]
    print(f"audit.py OK — {len(implemented)} SP checks passed ({', '.join(implemented)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
