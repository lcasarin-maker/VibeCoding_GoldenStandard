"""
inbox_deposit.py — Automated Inbox deposit for GS findings.

Agents and humans call this instead of writing directly to a catalog.
Creates a pre-filled finding file in Inbox/cerberus/ using the canonical template.

Usage:
    python scripts/inbox_deposit.py \\
        --slug "jwt-skip-on-internal-header" \\
        --domain VC \\
        --severity high \\
        --symptom "JWT validation skipped when X-Internal-Request header is present" \\
        --cause "Header check bypasses auth middleware" \\
        --mitigation "Remove X-Internal-Request bypass; use service accounts instead" \\
        --tags "security,auth,bypass"
"""

import argparse
import sys
import textwrap
from datetime import date
from pathlib import Path

GS_ROOT = Path(__file__).resolve().parent.parent
INBOX_DIR = GS_ROOT / "Inbox" / "cerberus"


def _validate_domain(value: str) -> str:
    allowed = {"VC", "VT", "TK", "PI", "PR", "SP"}
    v = value.upper()
    if v not in allowed:
        raise argparse.ArgumentTypeError(f"domain must be one of {sorted(allowed)}")
    return v


def _validate_severity(value: str) -> str:
    allowed = {"critical", "high", "medium", "low"}
    v = value.lower()
    if v not in allowed:
        raise argparse.ArgumentTypeError(f"severity must be one of {sorted(allowed)}")
    return v


def build_content(args, today: str) -> str:
    tags_block = "\n".join(f"  - {t.strip()}" for t in args.tags.split(",") if t.strip())
    mitigation_block = "\n".join(
        f"- {m.strip()}" for m in args.mitigation.split(";") if m.strip()
    )
    return textwrap.dedent(f"""\
        ---
        # Cerberus Finding — auto-deposited by inbox_deposit.py
        source: cerberus
        cerberus_rule_id: PENDING
        project_audited: {args.project}
        date_detected: {today}
        origin: {args.origin}

        ## Classification

        proposed_domain: {args.domain}
        proposed_severity: {args.severity}
        tags:
        {tags_block}

        ---

        ## Finding

        ### Symptom
        {args.symptom}

        ### Cause
        {args.cause}

        ### Context / Example
        ```
        (add code or log snippet here)
        ```

        ### Proposed Mitigation
        {mitigation_block}

        ### Evidence Artifact
        evidence_artifact: (add path or URL)

        ---

        ## Resolution (filled by curator, do not edit)

        promoted_to:
        wiki_article:
        date_promoted:
        curator:
    """)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deposit a finding into the GS Inbox")
    parser.add_argument("--slug", required=True, help="Short kebab-case identifier")
    parser.add_argument("--domain", required=True, type=_validate_domain)
    parser.add_argument("--severity", required=True, type=_validate_severity)
    parser.add_argument("--symptom", required=True)
    parser.add_argument("--cause", required=True)
    parser.add_argument("--mitigation", required=True, help="Semicolon-separated steps")
    parser.add_argument("--tags", required=True, help="Comma-separated tags (min 2)")
    parser.add_argument("--project", default="CoderCerberus")
    parser.add_argument("--origin", default="session-audit")

    args = parser.parse_args()

    tag_list = [t.strip() for t in args.tags.split(",") if t.strip()]
    if len(tag_list) < 2:
        print("[ERROR] At least 2 tags required.", file=sys.stderr)
        return 1

    today = date.today().isoformat()
    filename = f"{today}_{args.slug}.md"
    target = INBOX_DIR / filename

    if target.exists():
        print(f"[ERROR] File already exists: {target}", file=sys.stderr)
        return 1

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    target.write_text(build_content(args, today), encoding="utf-8")

    print(f"[OK] Deposited: {target}")
    print(f"     Next: fill 'Context / Example' and 'Evidence Artifact', then notify curator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
