"""Block commits that add likely credentials to Git's staged snapshot."""

from __future__ import annotations

import re
import subprocess
import sys


PATTERNS = {
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "provider token": re.compile(r"\b(?:sk-proj-|ghp_|github_pat_|AKIA)[A-Za-z0-9_-]{16,}"),
    "assigned secret": re.compile(
        r"(?i)^\s*(?:api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"]([^'\"]{12,})"
    ),
}

PLACEHOLDER_VALUES = (
    "test-",
    "example",
    "supersecret",
    "hunter2",
    "changeme",
    "dummy",
)


def staged_files() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z"],
        check=True,
        capture_output=True,
    )
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def staged_text(path: str) -> str:
    result = subprocess.run(["git", "show", f":{path}"], capture_output=True)
    if result.returncode or b"\0" in result.stdout[:8192]:
        return ""
    return result.stdout.decode("utf-8", errors="ignore")


def main() -> int:
    findings: list[str] = []
    for path in staged_files():
        if path.startswith(("tests/", "Wiki/", "output/", "docs/")):
            continue
        for line_number, line in enumerate(staged_text(path).splitlines(), 1):
            for label, pattern in PATTERNS.items():
                match = pattern.search(line)
                if match and label == "assigned secret" and any(
                    value.lower().startswith(PLACEHOLDER_VALUES)
                    for value in (match.group(1),)
                ):
                    continue
                if match:
                    findings.append(f"{path}:{line_number}: {label}")
    if findings:
        print("SECRET-SCAN BLOCKED: possible credentials in staged content", file=sys.stderr)
        print("\n".join(findings), file=sys.stderr)
        return 1
    print("SECRET-SCAN PASS: 0 findings in staged content")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
