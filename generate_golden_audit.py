#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_golden_audit.py — Compile and map Golden Standard compliance database.
Parses the split Golden Standard catalogs, mapping each flaw to GS guards/tests,
and auto-generates a fully cross-linked Obsidian Markdown Wiki vault.
"""

import json
import re
import shutil
import sys
from collections import Counter
from datetime import date
from pathlib import Path
import yaml

_ROOT = Path(__file__).resolve().parent

# Detect if we are inside the legacy parent workspace configuration
parent_dir = _ROOT.parent
if (parent_dir / ".protocol" / "metadata").is_dir():
    JSON_OUTPUT = parent_dir / ".protocol" / "metadata" / "golden_standard_audit.json"
    MARKDOWN_OUTPUT = parent_dir / "docs" / "golden_standard_audit_report.md"
    VERSION_FILE = parent_dir / "VERSION.txt"
else:
    # Standalone mode
    JSON_OUTPUT = _ROOT / "golden_standard_audit.json"
    MARKDOWN_OUTPUT = _ROOT / "golden_standard_audit_report.md"
    VERSION_FILE = _ROOT / "VERSION.txt"

WIKI_DIR = _ROOT / "Wiki"
GRAPH_OUTPUT = JSON_OUTPUT.with_name("golden_standard_graph.json")
GRAPH_MARKDOWN = WIKI_DIR / "Graph.md"
CONCEPTUAL_FRAMEWORK_SRC = _ROOT / "CONCEPTUAL_FRAMEWORK.md"

WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+?)\]\]")
MARKDOWN_LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+?\.md)\)")
CATALOG_MENTION_PATTERN = re.compile(r"\b(?:VC|VT|TK|PI)-\d{3}\b")
CATALOG_RANGE_PATTERN = re.compile(r"\b(VC|VT|TK|PI)-(\d{3})\.\.(?:\1-)?(\d{3})\b")


def load_golden_standard_catalogs() -> dict[str, dict]:
    """Load the split catalogs listed in golden_standard.yaml."""
    manifest_path = _ROOT / "golden_standard.yaml"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)
    
    catalogs = manifest.get("catalogs", {})
    loaded = {}
    for name, rel_path in catalogs.items():
        path = _ROOT / rel_path
        with open(path, "r", encoding="utf-8") as f:
            loaded[name] = yaml.safe_load(f)
    return loaded


def normalize_knowledge_text(value: object) -> str:
    """Normalize knowledge text to strip excessive whitespace."""
    return " ".join(str(value).strip().split())


def is_ascii_text(value: object) -> bool:
    """Return True when the value contains only ASCII characters."""
    try:
        str(value).encode("ascii")
        return True
    except UnicodeEncodeError:
        return False


def get_project_insights() -> dict[str, str]:
    """Load project insights directly from golden_standard_project_insights.yaml."""
    path = _ROOT / "golden_standard_project_insights.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    raw = data.get("project_insights", {})
    return {
        str(k): normalize_knowledge_text(v)
        for k, v in raw.items()
        if str(k).startswith("PI-")
    }


def get_project_insight_recommendations() -> dict[str, list[dict[str, str]]]:
    """Return domain-oriented recommendations mapped to project insights (cloned from loader)."""
    return {
        "D1": [
            {
                "insight_id": "PI-001",
                "project": "deptry",
                "action": "Compare imports against declared dependencies and fail on missing, unused, transitive or misplaced packages.",
            },
            {
                "insight_id": "PI-004",
                "project": "trivy",
                "action": "Scan repos, images and filesystems for secrets, CVEs, misconfigurations and SBOM gaps before release.",
            },
            {
                "insight_id": "PI-010",
                "project": "cerberus",
                "action": "Keep the working tree clean after audits; treat historical artifacts as reference material, not active output.",
            },
        ],
        "D2": [
            {
                "insight_id": "PI-001",
                "project": "deptry",
                "action": "Treat missing or stale dependency declarations as completeness debt and block delivery until reconciled.",
            },
            {
                "insight_id": "PI-006",
                "project": "cerberus",
                "action": "Keep the operational contract complete by storing state, evidence and checkpoints outside the chat.",
            },
            {
                "insight_id": "PI-008",
                "project": "cerberus",
                "action": "Batch predictable authorizations and questions before long runs so the control plane can execute without interruptions.",
            },
            {
                "insight_id": "PI-014",
                "project": "cerberus",
                "action": "Keep the knowledge base alive by continuously absorbing lessons from the core project and its satellites.",
            },
            {
                "insight_id": "PI-022",
                "project": "cerberus",
                "action": "Keep an explicit uncertainty ledger so protocol docs separate verified facts from assumptions before they become doctrine.",
            },
        ],
        "D3": [
            {
                "insight_id": "PI-002",
                "project": "pytest-good-assertions",
                "action": "Require failure messages that explain the mismatch clearly enough to debug without guesswork.",
            },
            {
                "insight_id": "PI-006",
                "project": "cerberus",
                "action": "Use explicit state and evidence fields so the system tells a clear causal story instead of relying on memory.",
            },
            {
                "insight_id": "PI-011",
                "project": "cerberus",
                "action": "Prefer descriptive names and reduce structural noise so purpose is visible at first glance.",
            },
        ],
        "D4": [
            {
                "insight_id": "PI-005",
                "project": "litellm",
                "action": "Centralize provider routing and fallbacks so the code does not grow provider-specific branching spaghetti.",
            },
            {
                "insight_id": "PI-011",
                "project": "cerberus",
                "action": "Flatten nested structure when it simplifies maintenance and removes needless indirection.",
            },
            {
                "insight_id": "PI-024",
                "project": "cerberus",
                "action": "Review graph hubs first when the catalog changes, because high fan-in nodes carry the largest impact radius.",
            },
        ],
        "D5": [
            {
                "insight_id": "PI-006",
                "project": "cerberus",
                "action": "Turn failure handling into a structured protocol with next steps, evidence and a visible recovery path.",
            },
            {
                "insight_id": "PI-002",
                "project": "pytest-good-assertions",
                "action": "Make failing assertions explain what to do next so the angry path is actionable, not noisy.",
            },
            {
                "insight_id": "PI-009",
                "project": "cerberus",
                "action": "Treat warnings and known non-blocking findings as operational errors until they are fixed or explicitly blocked.",
            },
        ],
        "D6": [
            {
                "insight_id": "PI-006",
                "project": "cerberus",
                "action": "Enforce clean boundaries, compact state and explicit handoffs to avoid slop and context drift.",
            },
            {
                "insight_id": "PI-012",
                "project": "cerberus",
                "action": "Allow exclusions only when they are minimal, justified and real; do not use theater constructs to simulate progress.",
            },
        ],
        "D7": [
            {
                "insight_id": "PI-004",
                "project": "trivy",
                "action": "Use security scanning as a mandatory gate for secrets, vulnerabilities and IaC misconfigurations.",
            },
            {
                "insight_id": "PI-013",
                "project": "cerberus",
                "action": "Observe risky signals during execution, not after the fact, so live monitoring can interrupt damage early.",
            },
        ],
        "D8": [
            {
                "insight_id": "PI-002",
                "project": "pytest-good-assertions",
                "action": "Keep tests high-signal: assertions should discriminate behavior, not merely confirm presence.",
            },
            {
                "insight_id": "PI-001",
                "project": "deptry",
                "action": "Prevent dependency drift from destabilizing the test suite by validating imports before running coverage gates.",
            },
            {
                "insight_id": "PI-012",
                "project": "cerberus",
                "action": "Reject fake coverage patterns such as xfail-as-expected, placeholder tests, mocks without intent or broad skips without evidence.",
            },
            {
                "insight_id": "PI-015",
                "project": "cerberus",
                "action": "Require each new guard to break a real circularity and reduce the baseline instead of merely naming the problem.",
            },
            {
                "insight_id": "PI-017",
                "project": "cerberus",
                "action": "Split broad coverage theater into discriminative checks so one test never pretends to cover many unrelated vices.",
            },
        ],
        "D9": [
            {
                "insight_id": "PI-002",
                "project": "pytest-good-assertions",
                "action": "Preserve assertion quality so tests fail with precise, inspectable output instead of theater.",
            },
            {
                "insight_id": "PI-012",
                "project": "cerberus",
                "action": "Prefer discriminative tests over symbolic coverage; if a test cannot fail for the right reason, it is not protecting the system.",
            },
            {
                "insight_id": "PI-016",
                "project": "cerberus",
                "action": "Mark non-falsifiable lessons as DOC_ONLY instead of pretending they can be proved automatically.",
            },
        ],
        "D10": [
            {
                "insight_id": "PI-003",
                "project": "tokencost",
                "action": "Meter tokens before and during LLM calls so cost is visible before usage grows.",
            },
            {
                "insight_id": "PI-005",
                "project": "litellm",
                "action": "Unify provider routing, fallbacks and telemetry so cost and resilience are handled once.",
            },
            {
                "insight_id": "PI-007",
                "project": "cerberus",
                "action": "Treat output trimming, context hygiene and history externalization as a first-class control, not an afterthought.",
            },
            {
                "insight_id": "PI-009",
                "project": "cerberus",
                "action": "Convert every warning and findable issue into a tracked operational error until the backlog is clean.",
            },
            {
                "insight_id": "PI-010",
                "project": "cerberus",
                "action": "Keep the root workspace clean so historical data lives in archives instead of polluting active context.",
            },
            {
                "insight_id": "PI-013",
                "project": "cerberus",
                "action": "Watch token and quality signals live during the run, not only in a post-mortem report.",
            },
        ],
        "D11": [
            {
                "insight_id": "PI-004",
                "project": "trivy",
                "action": "Use security scanning as a pre-merge and pre-release gate for filesystems, images and IaC.",
            },
            {
                "insight_id": "PI-012",
                "project": "cerberus",
                "action": "Keep exclusions minimal and auditable so the security posture stays real instead of ceremonial.",
            },
        ],
        "D12": [
            {
                "insight_id": "PI-014",
                "project": "cerberus",
                "action": "Fuse satellite learnings into the canonical knowledge base only after normalization and deduplication.",
            },
            {
                "insight_id": "PI-018",
                "project": "cerberus",
                "action": "Normalize, deduplicate and record new learnings before folding them into the central knowledge base.",
            },
            {
                "insight_id": "PI-023",
                "project": "cerberus",
                "action": "Check shared state and recent commits before editing so concurrent sessions do not overwrite each other silently.",
            },
        ],
    }


def _read_version_label() -> str:
    if VERSION_FILE.exists():
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        if version:
            return f"V{version}"
    return "V0.6"


def get_flaw_category(flaw_id: str) -> str:
    """Classify the flaw category based on its ID prefix."""
    if flaw_id.startswith("VT"):
        return "Testing & Evaluation"
    if flaw_id.startswith("VC"):
        return "Vibe Coding"
    if flaw_id.startswith("TK"):
        return "Tokenomics & Context"
    return "Other"


def build_project_insight_section() -> list[str]:
    """Build a markdown section for the agnostic project insights layer."""
    insights = get_project_insights()
    lines = [
        "## Project Insights",
        "",
        "These entries are preserved as project-agnostic knowledge extracted from external references and now consumed by GS users and downstream tools.",
        "",
        "| ID | Insight |",
        "|---|---|",
    ]
    for insight_id in sorted(insights):
        lines.append(f"| `{insight_id}` | {insights[insight_id]} |")
    lines.append("")
    return lines


def build_project_insight_recommendations_section() -> list[str]:
    """Build a markdown section mapping insights to audit domains."""
    recommendations = get_project_insight_recommendations()
    lines = [
        "## Project Insight Recommendations by Domain",
        "",
        "These actions are the operational bridge between the project insights and the GS operational lenses.",
        "",
        "| Domain | Insight | Project | Action |",
        "|---|---|---|---|",
    ]
    for domain in sorted(recommendations):
        for item in recommendations[domain]:
            lines.append(
                f"| `{domain}` | `{item['insight_id']}` | {item['project']} | {item['action']} |"
            )
    lines.append("")
    return lines


def clean_single_item(item: Path):
    """Clean a single file or directory inside the vault."""
    if item.is_dir():
        shutil.rmtree(item, ignore_errors=True)
        return
    try:
        item.unlink()
    except OSError as err:
        print(f"[WARN] Failed to clean file {item}: {err}")


def clean_wiki_directory(path: Path):
    """Safely delete and recreate the Wiki directory to prevent stale notes."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        return

    for item in path.iterdir():
        clean_single_item(item)
    path.mkdir(parents=True, exist_ok=True)


def write_home_md(
    wiki_dir: Path,
    total_vices: int,
    vc_count: int,
    tv_count: int,
    tk_count: int,
    pi_count: int,
    status_counts: Counter,
):
    """Write Home.md main map of content page."""
    prevented_count = status_counts.get("PREVENTED", 0)
    remediated_count = status_counts.get("REMEDIATED", 0)
    audited_count = status_counts.get("AUDITED", 0)
    doc_only_count = status_counts.get("DOC_ONLY", 0)
    operational_count = prevented_count + remediated_count
    documentary_count = audited_count + doc_only_count
    home_content = f"""# Golden Standard Wiki

Welcome to the Obsidian vault of the **Golden Standard** (GS). This knowledge base represents the pure doctrine of engineering, vice mitigation, and tokenomics accumulated by the project.

---

## Quick Access

- 📂 **[[Vices_Index|Engineering Vices Index]]**: Central catalog of code and test anomalies (`VC`, `TV`).
- 📂 **[[Project_Insights_Index|Satellite Insights Index]]**: Lessons and best practices (`PI`) extracted from external repositories and automations.
- 🕸️ **[[Graph|GS Graph Map]]**: Hubs, intentional orphans, candidate orphans, and local vault impact.
- 📘 **[[Concepts/Conceptual_Framework|Golden Standard Conceptual Framework]]**: Epistemological doctrine, levels, and design foundations.
- 🧼 **[[Concepts/Conceptual_Framework#5.-Repository-and-Execution-Hygiene|Repository Hygiene Chapter]]**: Canonical standard for cleanup, naming, clean root, and organization evidence.
- 🔧 **[[Project_Insights/PI-019|Execution Hygiene and Tooling]]**: Satellite rule for simple commands, UTF-8, and technical purity.
- ⚠️ **[[Vices/VC-124|Hasty deprecation]]**: Mirror vice that avoids moving to `deprecated/` without analysis.
- 🏷️ **[[Project_Insights/PI-020|Confidence Tags]]**: Every protocol claim must declare whether it is VERIFIED, INFERRED, or ASSUMED.
- 🧪 **[[Project_Insights/PI-021|Semantic Wiki-Lint]]**: Detects contradictions, broken references, and mandates without binding.
- 🧾 **[[Project_Insights/PI-022|Uncertainty list]]**: Documents the unverified so as not to feign certainty.
- 🧭 **[[Project_Insights/PI-023|Dual-session awareness]]**: Verifies shared state before editing.
- 🕸️ **[[Project_Insights/PI-024|Hub-based review]]**: Prioritizes high-impact nodes in the graph.
- 🧷 **[[Project_Insights/PI-025|Exportable Retrospective]]**: Closes each session with a structured, persistent retrospective.
- 💠 **[[Tokenomics_Index|Tokenomics Index]]**: Separate catalog of efficiency, headroom, and context management (`TK`).
- 🗺️ **[[Tokenomics_Map|Tokenomics Map]]**: Bridge between the `TK` and `PI` lenses to navigate relations, gaps, and coverage.
- 🔹 **[[Tokenomics/Memory_Headroom_Index|Memory and Headroom]]**: Checkpoints, handoff, persistence, and context margin.
- 🔹 **[[Tokenomics/Input_Retrieval_Index|Input and Retrieval]]**: Targeted retrieval and input-noise reduction.
- 🔹 **[[Tokenomics/Output_Compaction_Index|Output and Compaction]]**: Verbosity, compression, and response budget.
- 🔹 **[[Tokenomics/Measurement_Telemetry_Index|Measurement and Telemetry]]**: Savings evidence and impact monitoring.
- 🔹 **[[Tokenomics/Automation_Tooling_Index|Automation and Tooling]]**: Active integrations and tooling that executes savings.
- 📄 **[Root conceptual framework](../CONCEPTUAL_FRAMEWORK.md)**: Local GS base document for direct reading and graph navigation.
- 📥 **[Inbox](../Inbox/README.md)**: Inbox for raw findings and new proposals.
- 🧪 **[Audit Report](../golden_standard_audit_report.md)**: Compiled state of current coverage and mapping.
- 🗺️ **[Graph JSON](../golden_standard_graph.json)**: Structured export for programmatic impact queries.
- 🏠 **[README](../README.md)**: Overview of the public repository.

---

## Map by Domain

| Domain | Catalog | Entries | Link |
|---|---|---:|---|
| Vibe Coding | `VC-xxx` | {vc_count} | [[Vices_Index|Open index]] |
| Testing & Evaluation | `VT-xxx` | {tv_count} | [[Vices_Index|Open index]] |
| Tokenomics | `TK-xxx` | {tk_count} | [[Tokenomics_Index|Open index]] |
| Project Insights | `PI-xxx` | {pi_count} | [[Project_Insights_Index|Open index]] |

---

## Operability Status

| Status | Entries | Meaning |
|---|---:|---|
| `PREVENTED` + `REMEDIATED` | {operational_count} | The catalog already has an executable gate or a concrete correction. |
| `AUDITED` + `DOC_ONLY` | {documentary_count} | The entry exists as knowledge, but remains mainly documentary. |
| `Total` | {total_vices} | Sum of the VC, VT, and TK entries audited by the compiler. |

---

## Severity Guide

| Severity | What it means | Typical action |
|---|---|---|
| `critical` | Security risk, data loss, or total failure of an essential capability. | Fix before continuing. |
| `high` | User-visible bug or serious breach of trust. | Prioritize in the next iteration. |
| `medium` | Reliability or maintainability debt. | Schedule remediation. |
| `low` | Style, clarity, or efficiency adjustment. | Group with general cleanup. |

> Severity is used in contribution review; the canonical operational state in the catalogs is still `status`.

---

## Intake Flow

1. Deposit the finding in `Inbox/<source>/YYYY-MM-DD_<slug>.md`.
2. Validate the minimal fields with `INGESTION_PROTOCOL.md`.
3. Promote to YAML + Wiki only after deduplicating and mapping the domain.
4. Recompile with `python generate_golden_audit.py`.

---
*Vault auto-generated by the `generate_golden_audit.py` compiler on {date.today().isoformat()}.*"""
    (wiki_dir / "Home.md").write_text(home_content, encoding="utf-8")


def write_vices_index_md(wiki_dir: Path, mapped_database: dict):
    """Write the main VC/VT index catalog."""
    vc_items = []
    tv_items = []
    for flaw_id, item in sorted(mapped_database.items()):
        line = (
            f"*   [[Vices/{flaw_id}|{flaw_id}]] — **{item['title']}** "
            f"({item['status']}, {item['severity']}, downstream:{item.get('downstream_verification', 'none')})"
        )
        if item["category"] == "Vibe Coding":
            vc_items.append(line)
        elif item["category"] == "Testing & Evaluation":
            tv_items.append(line)

    vices_index_content = f"""# Engineering Vices Index

This index classifies the Golden Standard vices into VC and VT. Tokenomics lives in its own index because it is not a vice: it is a layer of efficiency and context governance.

---

## Vibe Coding (VC)
{"\n".join(vc_items)}

## Testing & Evaluation (TV)
{"\n".join(tv_items)}

---
[[Home|Back to Home]]
"""
    (wiki_dir / "Vices_Index.md").write_text(vices_index_content, encoding="utf-8")


def write_tokenomics_index_md(wiki_dir: Path, mapped_database: dict):
    """Write the dedicated Tokenomics index catalog."""
    tk_items = []
    for flaw_id, item in sorted(mapped_database.items()):
        if item["category"] != "Tokenomics & Context":
            continue
        line = (
            f"*   [[Tokenomics/{flaw_id}|{flaw_id}]] — **{item['title']}** "
            f"({item['status']}, {item['severity']}, downstream:{item.get('downstream_verification', 'none')})"
        )
        tk_items.append(line)

    prevented_count = len([x for x in mapped_database.values() if x["category"] == "Tokenomics & Context" and x["status"] in ("PREVENTED", "REMEDIATED")])
    doc_only_count = len([x for x in mapped_database.values() if x["category"] == "Tokenomics & Context" and x["status"] in ("DOC_ONLY", "AUDITED")])
    total_count = len([x for x in mapped_database.values() if x["category"] == "Tokenomics & Context"])

    tokenomics_index_content = f"""# Tokenomics Index

Tokenomics is a category of its own in the Golden Standard. It does not describe code or testing vices: it describes how to reduce noise, preserve headroom, compact context, and externalize state without sacrificing quality.

The practical utility of this category is twofold:

1. prevent the agent from burning context on rereads, verbose outputs, or poor handoffs;
2. turn token savings into a measurable discipline, not an intuition.

Historically, this layer was operated under names like *headspace*, *compact*, and *token saving*. GS preserves the knowledge and also defines the doctrine of use.

---

## Subindices

- [[Memory_Headroom_Index|Memory and Headroom]]
- [[Input_Retrieval_Index|Input and Retrieval]]
- [[Output_Compaction_Index|Output and Compaction]]
- [[Measurement_Telemetry_Index|Measurement and Telemetry]]
- [[Automation_Tooling_Index|Automation and Tooling]]
- [[Tokenomics_Map|Tokenomics Map]]

---

## Category status

| Status | Entries |
|---|---:|
| `PREVENTED` / `REMEDIATED` | {prevented_count} |
| `DOC_ONLY` / `AUDITED` | {doc_only_count} |
| `Total` | {total_count} |

---

## Entries

{"\n".join(tk_items)}

---
## Usage reference

- Tokenomics defines principles of efficiency and context management.
- The real enforcement of these principles belongs to the consuming repositories and tools that adopt GS.
- The category's vocabulary must be kept separate from VC and VT to avoid semantic confusion.
- Modern noise-reduction strategies, like RTK and ICM, confirm that token savings benefit from filtering tools, external memory, and context compaction.

---
[[Home|Back to Home]]
"""
    (wiki_dir / "Tokenomics_Index.md").write_text(tokenomics_index_content, encoding="utf-8")


def write_tokenomics_map_md(wiki_dir: Path, insights: dict):
    """Write a bridge page that links tokenomics lenses with project insights."""
    bridge_rows = [
        (
            "Memory and Headroom",
            "[[Tokenomics/Memory_Headroom_Index|Open lens]]",
            "PI-006, PI-010, PI-014, PI-018",
            "Avoids context loss, root pollution, and forgotten learning.",
        ),
        (
            "Input and Retrieval",
            "[[Tokenomics/Input_Retrieval_Index|Open lens]]",
            "PI-005, PI-012",
            "Reduces input noise and makes targeted retrieval more precise.",
        ),
        (
            "Output and Compaction",
            "[[Tokenomics/Output_Compaction_Index|Open lens]]",
            "PI-003, PI-007, PI-009, PI-016",
            "Controls verbosity, cost, pruning, and documentary honesty.",
        ),
        (
            "Measurement and Telemetry",
            "[[Tokenomics/Measurement_Telemetry_Index|Open lens]]",
            "PI-003, PI-013",
            "Makes the real savings visible, not just the intention to save.",
        ),
        (
            "Automation and Tooling",
            "[[Tokenomics/Automation_Tooling_Index|Open lens]]",
            "PI-005, PI-006, PI-013",
            "Connects the doctrine with executable tooling and continuous observability.",
        ),
    ]

    insight_pairs = []
    for insight_id in ["PI-003", "PI-005", "PI-006", "PI-007", "PI-009", "PI-010", "PI-012", "PI-013", "PI-014", "PI-016", "PI-018"]:
        if insight_id in insights:
            insight_pairs.append((insight_id, insights[insight_id]))

    insight_rows = "\n".join(
        f"| `{insight_id}` | {description} |"
        for insight_id, description in insight_pairs
    )

    lens_rows = "\n".join(
        f"| {lens} | {link} | `{pi_refs}` | {intent} |"
        for lens, link, pi_refs, intent in bridge_rows
    )

    map_content = f"""# Tokenomics Map

This map serves as a bridge between the `TK` category and the GS satellite lessons. It does not repeat the catalog: it shows how to read it and which insights it crosses.

## What it is for

- Navigate relations between context vices, token savings, and operational discipline.
- Identify which satellite lessons reinforce each tokenomics lens.
- Detect gaps where doctrine exists, but a supporting artifact or clear telemetry is still missing.

---

## Operational lenses

| Lens | Subindex | Related Project Insights | Intent |
|---|---|---|---|
{lens_rows}

---

## Key Project Insights

| Insight | Summary |
|---|---|
{insight_rows}

---

## Adjacent crossings

| Node | Relation | Reason |
|---|---|---|
| `[[Project_Insights/PI-019|PI-019]]` | Satellite hygiene | Expands the discipline of editing and validation toward daily work with tools. |
| `[[Vices/VC-124|VC-124]]` | Mirror vice | Represents the error of deprecating without analysis or traceability. |

---

## Practical reading

1. If a problem consumes context, first check `Memory and Headroom`.
2. If the problem originates in the input, check `Input and Retrieval`.
3. If the cost is in the response, check `Output and Compaction`.
4. If there is no evidence of savings, check `Measurement and Telemetry`.
5. If the doctrine does not run by itself, check `Automation and Tooling`.

---
[[Tokenomics_Index|Back to Tokenomics Index]] | [[Project_Insights_Index|Go to Insights]] | [[Home|Home]]
"""
    (wiki_dir / "Tokenomics_Map.md").write_text(map_content, encoding="utf-8")


def _tokenomics_subindex_group(item_id: str, title: str) -> str:
    """Map a tokenomics entry to a thematic subindex."""
    if item_id.startswith("TK-F01") or item_id in {"TK-001", "TK-002", "TK-003", "TK-004", "TK-005", "TK-006", "TK-007", "TK-008", "TK-028", "TK-031", "TK-032", "TK-033", "TK-034", "TK-038"}:
        return "memory_headroom"
    if item_id.startswith("TK-F02") or item_id in {"TK-009", "TK-010", "TK-011", "TK-012", "TK-014", "TK-015", "TK-016", "TK-018", "TK-019"}:
        return "input_retrieval"
    if item_id.startswith("TK-F03") or item_id in {"TK-020", "TK-021", "TK-022", "TK-024", "TK-025", "TK-027", "TK-029", "TK-030", "TK-035", "TK-036", "TK-043"}:
        return "output_compaction"
    if item_id in {"TK-023", "TK-026", "TK-037", "TK-040", "TK-041", "TK-042"}:
        return "measurement_telemetry"
    if item_id in {"TK-013", "TK-017", "TK-039"}:
        return "automation_tooling"
    # Fallback: infer by title when a future TK lands outside the historical ranges.
    lower_title = title.lower()
    if any(term in lower_title for term in ["memory", "memoria", "state", "estado", "checkpoint", "hand-off", "handoff", "headroom", "cache", "drift"]):
        return "memory_headroom"
    if any(term in lower_title for term in ["input", "ingest", "retrieval", "poda", "recuper", "chunk", "prompt"]):
        return "input_retrieval"
    if any(term in lower_title for term in ["measure", "medir", "telemetry", "telemet", "audit", "evidence", "monitor"]):
        return "measurement_telemetry"
    if any(term in lower_title for term in ["tool", "automation", "mode", "router", "integrat", "external"]):
        return "automation_tooling"
    return "output_compaction"


def write_tokenomics_subindices_md(wiki_dir: Path, mapped_database: dict):
    """Write thematic subindices for tokenomics."""
    groups = {
        "memory_headroom": {
            "title": "Memory and Headroom",
            "filename": "Memory_Headroom_Index.md",
            "blurb": "Checkpoints, handoffs, external persistence, cache, drift, and control of context margin.",
            "items": [],
        },
        "input_retrieval": {
            "title": "Input and Retrieval",
            "filename": "Input_Retrieval_Index.md",
            "blurb": "Targeted retrieval, semantic pruning, chunks, and reduction of blind exploration.",
            "items": [],
        },
        "output_compaction": {
            "title": "Output and Compaction",
            "filename": "Output_Compaction_Index.md",
            "blurb": "Output control, compression, verbosity, and response budget.",
            "items": [],
        },
        "measurement_telemetry": {
            "title": "Measurement and Telemetry",
            "filename": "Measurement_Telemetry_Index.md",
            "blurb": "Savings evidence, observability, monitoring, and impact verification.",
            "items": [],
        },
        "automation_tooling": {
            "title": "Automation and Tooling",
            "filename": "Automation_Tooling_Index.md",
            "blurb": "Active integrations, routing, operation modes, and tooling that actually executes savings.",
            "items": [],
        },
    }

    for flaw_id, item in sorted(mapped_database.items()):
        if item["category"] != "Tokenomics & Context":
            continue
        group_key = _tokenomics_subindex_group(flaw_id, item["title"])
        groups[group_key]["items"].append(
            f"*   [[Tokenomics/{flaw_id}|{flaw_id}]] — **{item['title']}** ({item['status']}, {item['severity']}, downstream:{item.get('downstream_verification', 'none')})"
        )

    for group_key, group in groups.items():
        subindex_content = f"""# Tokenomics Index: {group['title']}

{group['blurb']}

---

## Entries

{"\n".join(group["items"]) if group["items"] else "*No entries assigned.*"}

---

## How to read this subindex

- If the entry is about memory, checkpoint, handoff, cache, or headroom, it is in Memory and Headroom.
- If it is about search, pruning, retrieval, or chunks, it is in Input and Retrieval.
- If it is about verbosity, compression, or response budget, it is in Output and Compaction.
- If it is about measurement, telemetry, evidence, or verified savings, it is in Measurement and Telemetry.
- If it is about tooling, routing, integration, or operating modes, it is in Automation and Tooling.

---
[[Tokenomics_Map|Back to Tokenomics Map]] | [[Tokenomics_Index|Tokenomics Index]]
"""
        (wiki_dir / "Tokenomics" / group["filename"]).write_text(subindex_content, encoding="utf-8")


# Editorial classification of Project Insights to separate actionable lessons from
# system-meta commentary (addresses the audit critique that PIs were self-referential).
PI_KIND = {
    "tool": {"PI-001", "PI-002", "PI-003", "PI-004", "PI-005", "PI-020", "PI-021",
             "PI-028", "PI-029", "PI-030", "PI-031", "PI-032", "PI-033", "PI-034"},
    "meta": {"PI-006", "PI-007", "PI-014", "PI-018"},
}


def classify_pi(pi_id: str) -> str:
    if pi_id in PI_KIND["tool"]:
        return "tool"
    if pi_id in PI_KIND["meta"]:
        return "meta"
    return "principle"


def write_project_insights_index_md(wiki_dir: Path, insights: dict):
    """Write the Project Insights index catalog, grouped by kind."""
    groups = {
        "principle": ("🟢 Actionable principles", "Cross-cutting lessons that change how work is done."),
        "tool": ("🔧 Reference tools and techniques", "Pointers to verified external tools and reusable patterns."),
        "meta": ("⚪ Meta-system (about the Golden Standard itself)", "Insights that describe GS governance; useful but they do not teach an external technique."),
    }
    sections = []
    for kind, (heading, blurb) in groups.items():
        ids = sorted(pi for pi in insights if classify_pi(pi) == kind)
        if not ids:
            continue
        rows = "\n".join(f"*   [[Project_Insights/{pi_id}|{pi_id}]] — {insights[pi_id]}" for pi_id in ids)
        sections.append(f"## {heading}\n\n_{blurb}_ ({len(ids)})\n\n{rows}")

    pi_index_content = f"""# Satellite Insights Index

Mapping of lessons extracted from reference repositories and external audit tools.
Entries are grouped by type to distinguish actionable principles from system meta-commentary.

---

{"\n\n---\n\n".join(sections)}

---
[[Home|Back to Home]]
"""
    (wiki_dir / "Project_Insights_Index.md").write_text(pi_index_content, encoding="utf-8")


def write_conceptual_concepts_md(wiki_dir: Path):
    """Create link-adapted copy of the canonical conceptual framework."""
    if not CONCEPTUAL_FRAMEWORK_SRC.exists():
        raise FileNotFoundError(f"Missing canonical conceptual framework: {CONCEPTUAL_FRAMEWORK_SRC}")

    original_text = CONCEPTUAL_FRAMEWORK_SRC.read_text(encoding="utf-8")
    nav_header = "# [[Home|← Back to Vault Home]]\n\n---\n\n"
    (wiki_dir / "Concepts" / "Conceptual_Framework.md").write_text(
        nav_header + original_text,
        encoding="utf-8",
    )


def entry_depth(item: dict) -> str:
    """Classify an entry by depth: deep, doctrinal, or stub.

    - 'deep'      : ships paired bad/good examples (a concrete, falsifiable vice).
    - 'doctrinal' : explicitly flagged as a behavioral/epistemic principle with no
                    static signature; a stub by design, not by neglect. Fabricating
                    code for these would be theater, so we never do.
    - 'stub'      : enrichable but not yet enriched (real depth debt).
    """
    if str(item.get("alias_of", "")).strip():
        return "alias"
    if str(item.get("example_bad", "")).strip() and str(item.get("example_good", "")).strip():
        return "deep"
    if item.get("doctrinal"):
        return "doctrinal"
    return "stub"


def depth_badge(item: dict) -> str:
    """Human-readable badge for an entry's depth classification."""
    alias = str(item.get("alias_of", "")).strip()
    if alias:
        return f"🔗 Alias → [[Vices/{alias}|{alias}]]"
    return {"deep": "🟢 Deep", "doctrinal": "⚪ Doctrinal"}.get(entry_depth(item), "🟡 Stub")


def build_depth_sections(item: dict) -> str:
    """Render optional depth blocks (examples, detection, evidence) when present.

    Returns markdown to be appended after the core sections. Empty string when the
    entry carries no enriched fields, so legacy stub entries render unchanged.
    """
    lang = str(item.get("example_lang", "text")).strip() or "text"
    blocks: list[str] = []

    example_bad = str(item.get("example_bad", "")).strip()
    if example_bad:
        blocks.append(f"### ❌ Example of the vice (Bad)\n```{lang}\n{example_bad}\n```")

    example_good = str(item.get("example_good", "")).strip()
    if example_good:
        blocks.append(f"### ✅ Corrected version (Good)\n```{lang}\n{example_good}\n```")

    detection = str(item.get("detection", "")).strip()
    if detection:
        blocks.append(f"### 🔎 Concrete detection\n{detection}")

    evidence = item.get("evidence", [])
    if isinstance(evidence, list) and evidence:
        lines = ["### 📚 External evidence"]
        for ref in evidence:
            if isinstance(ref, dict):
                source = str(ref.get("source", "")).strip()
                claim = str(ref.get("claim", "")).strip()
                lines.append(f"- **{source}** — {claim}" if claim else f"- **{source}**")
            else:
                lines.append(f"- {ref}")
        blocks.append("\n".join(lines))

    if not blocks:
        return ""
    return "\n\n" + "\n\n".join(blocks)


def write_atomic_vices(wiki_dir: Path, mapped_database: dict):
    """Create individual atomic files for VC and VT entries."""
    for flaw_id, item in mapped_database.items():
        if item["category"] == "Tokenomics & Context":
            continue
        alias = str(item.get("alias_of", "")).strip()
        if alias:
            redirect = f"""# {flaw_id}: {item['title']}

> 🔗 **Merged entry.** This vice is a semantic duplicate of [[Vices/{alias}|{alias}]]; the canonical content (symptom, examples, and detection) lives there. The ID `{flaw_id}` is preserved for reference stability.

| Field | Detail |
|---|---|
| **ID** | `{flaw_id}` |
| **Canonical** | [[Vices/{alias}|{alias}]] |
| **Depth** | {depth_badge(item)} |

---
[[Vices/{alias}|Go to the canonical entry {alias}]] | [[Vices_Index|Vices Index]] | [[Home|Home]]
"""
            (wiki_dir / "Vices" / f"{flaw_id}.md").write_text(redirect, encoding="utf-8")
            continue
        tag_list = ", ".join(f"`{tag}`" for tag in item["tags"]) if item.get("tags") else "`untagged`"
        depth_sections = build_depth_sections(item)
        detector = str(item.get("detector", "")).strip()
        detector_row = (
            f"\n| **Local detector** | 🛡️ `scripts/detectors.py::{detector}` (tested against the examples in CI) |"
            if detector else ""
        )
        flaw_content = f"""# {flaw_id}: {item['title']}

| Field | Detail |
|---|---|
| **ID** | `{flaw_id}` |
| **Category** | {item['category']} |
| **Status** | **{item['status']}** |
| **Severity** | **{item['severity']}** |
| **Depth** | {depth_badge(item)} |{detector_row}
| **Tags** | {tag_list} |
| **Downstream Verification** | `{item.get('downstream_verification', 'none')}` |
| **Validation Mechanism** | `{item['validating_mechanism']}` |

---

### Symptom
> {item['symptom']}

### Cause
{item['cause']}

### Solution
{item['solution']}

### Corrective Action / Prevention
{item['action']}{depth_sections}

### Relations
- [[Project_Insights/PI-019|PI-019]]
- [[Tokenomics_Map|Tokenomics Map]]
- [[Home|Home]]

---
[[Vices_Index|Back to Vices Index]] | [[Home|Home]]
"""
        (wiki_dir / "Vices" / f"{flaw_id}.md").write_text(flaw_content, encoding="utf-8")


def write_atomic_tokenomics(wiki_dir: Path, mapped_database: dict):
    """Create individual atomic files for tokenomics entries."""
    tokenomics_dir = wiki_dir / "Tokenomics"
    tokenomics_dir.mkdir(parents=True, exist_ok=True)
    for flaw_id, item in mapped_database.items():
        if item["category"] != "Tokenomics & Context":
            continue
        tag_list = ", ".join(f"`{tag}`" for tag in item["tags"]) if item.get("tags") else "`untagged`"
        depth_sections = build_depth_sections(item)
        flaw_content = f"""# {flaw_id}: {item['title']}

| Field | Detail |
|---|---|
| **ID** | `{flaw_id}` |
| **Category** | Tokenomics |
| **Status** | **{item['status']}** |
| **Severity** | **{item['severity']}** |
| **Depth** | {depth_badge(item)} |
| **Tags** | {tag_list} |
| **Downstream Verification** | `{item.get('downstream_verification', 'none')}` |
| **Validation Mechanism** | `{item['validating_mechanism']}` |

---

### Symptom (Signal)
> {item['symptom']}

### Cause
{item['cause']}

### Application / Mitigation
{item['solution']}

### Operational Relevance
{item['action']}{depth_sections}

---
[[Tokenomics_Map|Back to Tokenomics Map]] | [[Tokenomics_Index|Back to Tokenomics Index]] | [[Home|Home]]
"""
        (tokenomics_dir / f"{flaw_id}.md").write_text(flaw_content, encoding="utf-8")


def build_pi_mapping_lines(mappings: list) -> list[str]:
    """Format mapping lines for project insights."""
    if not mappings:
        return ["*No active domain assignments.*"]
    return [
        f"*   **[[Domains/{domain}|{domain}]]** (Project: *{proj}*): {act}"
        for domain, proj, act in sorted(mappings)
    ]


def write_atomic_project_insights(wiki_dir: Path, insights: dict, pi_to_domains: dict):
    """Create individual atomic files for all project insights."""
    for pi_id, text in insights.items():
        mappings = pi_to_domains.get(pi_id, [])
        mapping_lines = build_pi_mapping_lines(mappings)

        pi_content = f"""# {pi_id}: Satellite Insight

### Insight Description
> {text}

### Relations
- [[Tokenomics_Map|Tokenomics Map]]
- [[Vices/VC-124|VC-124]]
- [[Home|Home]]

---

### Mapping to GS Operational Lenses
{"\n".join(mapping_lines)}

---
[[Project_Insights_Index|Back to Insights Index]] | [[Home|Home]]
"""
        (wiki_dir / "Project_Insights" / f"{pi_id}.md").write_text(pi_content, encoding="utf-8")


def write_audit_domains(wiki_dir: Path, recommendations: dict):
    """Create domains overview files mapping to insights."""
    for domain in sorted(recommendations):
        linked_items = [
            f"*   **[[Project_Insights/{rec['insight_id']}|{rec['insight_id']}]]** (Project: *{rec['project']}*): {rec['action']}"
            for rec in recommendations[domain]
        ]

        domain_content = f"""# Audit Domain: {domain}

This domain covers a specific area of the GS consistency and security protocol. The following satellite insights are linked to this operational lens:

---

### Linked Insights

{"\n".join(linked_items)}

---
[[Home|Back to Home]]
        """
        (wiki_dir / "Domains" / f"{domain}.md").write_text(domain_content, encoding="utf-8")


def canonical_graph_node_id(path: Path) -> str:
    """Convert a file path into the graph node id used by wiki links."""
    rel_path = path.relative_to(_ROOT).with_suffix("").as_posix()
    if rel_path.startswith("Wiki/"):
        return rel_path.removeprefix("Wiki/")
    return rel_path


def classify_graph_node(path: Path) -> str:
    """Assign a coarse node type for graph summaries."""
    rel_path = path.relative_to(_ROOT).as_posix()
    if rel_path == "README.md":
        return "root"
    if rel_path == "CONTRIBUTING.md":
        return "contributing"
    if rel_path == "CONCEPTUAL_FRAMEWORK.md":
        return "conceptual-framework"
    if rel_path == "CODE_OF_CONDUCT.md":
        return "code-of-conduct"
    if rel_path.startswith("Inbox/"):
        return "inbox"
    if rel_path.startswith("Wiki/Vices/"):
        return "vice"
    if rel_path.startswith("Wiki/Tokenomics/"):
        return "tokenomics"
    if rel_path.startswith("Wiki/Project_Insights/"):
        return "insight"
    if rel_path.startswith("Wiki/Domains/"):
        return "domain"
    if rel_path.startswith("Wiki/Concepts/"):
        return "concept"
    if rel_path.startswith("Wiki/"):
        return "wiki"
    return "doc"


def collect_graph_sources() -> list[Path]:
    """Return the live Markdown sources that should participate in the GS graph."""
    sources = [
        _ROOT / "README.md",
        _ROOT / "CONTRIBUTING.md",
        _ROOT / "CONCEPTUAL_FRAMEWORK.md",
        _ROOT / "CODE_OF_CONDUCT.md",
    ]

    for relative_dir in ["Wiki", "Inbox"]:
        base_dir = _ROOT / relative_dir
        if base_dir.exists():
            sources.extend(sorted(base_dir.rglob("*.md")))

    return [path for path in sources if path.exists()]


def is_intentional_graph_orphan(path: Path) -> bool:
    """Return True for isolated files that are intentionally kept as templates or fixtures."""
    rel_path = path.relative_to(_ROOT).as_posix()
    return rel_path.startswith("Inbox/templates/")


def extract_graph_mentions(text: str) -> set[str]:
    """Extract explicit GS ids mentioned in prose, including simple ranges."""
    mentions = set(CATALOG_MENTION_PATTERN.findall(text))
    for prefix, start, end in CATALOG_RANGE_PATTERN.findall(text):
        start_num = int(start)
        end_num = int(end)
        if start_num > end_num:
            start_num, end_num = end_num, start_num
        for value in range(start_num, end_num + 1):
            mentions.add(f"{prefix}-{value:03d}")
    return mentions


def resolve_wikilink_target(source_path: Path, raw_target: str, known_nodes: set[str]) -> str | None:
    """Resolve an Obsidian-style wikilink target to a graph node id."""
    target = raw_target.split("|", 1)[0].split("#", 1)[0].strip().replace("\\", "/")
    if not target:
        return None
    if target in known_nodes:
        return target

    cleaned = target.removesuffix(".md")
    if cleaned in known_nodes:
        return cleaned

    candidate = (source_path.parent / target).resolve()
    if candidate.exists():
        try:
            resolved = canonical_graph_node_id(candidate)
        except ValueError:
            resolved = None
        if resolved in known_nodes:
            return resolved

    candidate = (_ROOT / target).resolve()
    if candidate.exists():
        try:
            resolved = canonical_graph_node_id(candidate)
        except ValueError:
            resolved = None
        if resolved in known_nodes:
            return resolved

    return None


def resolve_markdown_link(source_path: Path, raw_target: str, known_nodes: set[str]) -> str | None:
    """Resolve a relative Markdown link to a graph node id."""
    target = raw_target.split("#", 1)[0].split("?", 1)[0].strip().replace("\\", "/")
    if not target:
        return None

    candidate = (source_path.parent / target).resolve()
    if not candidate.exists():
        candidate = (_ROOT / target).resolve()
    if not candidate.exists():
        return None

    try:
        node_id = canonical_graph_node_id(candidate)
    except ValueError:
        return None
    return node_id if node_id in known_nodes else None


def build_gs_graph() -> dict:
    """Build a deterministic knowledge graph from the live Markdown surface."""
    sources = collect_graph_sources()
    known_nodes = {canonical_graph_node_id(path) for path in sources}

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    edge_keys: set[tuple[str, str, str]] = set()

    def add_edge(source: str, target: str, kind: str) -> None:
        if source == target:
            return
        key = (source, target, kind)
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append({"source": source, "target": target, "kind": kind})

    for path in sources:
        node_id = canonical_graph_node_id(path)
        content = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        nodes[node_id] = {
            "id": node_id,
            "path": path.relative_to(_ROOT).as_posix(),
            "title": title,
            "kind": classify_graph_node(path),
            "outgoing": [],
            "incoming": [],
        }

    for path in sources:
        source_id = canonical_graph_node_id(path)
        content = path.read_text(encoding="utf-8")

        for raw_link in WIKILINK_PATTERN.findall(content):
            target_id = resolve_wikilink_target(path, raw_link, known_nodes)
            if target_id:
                add_edge(source_id, target_id, "wikilink")

        for raw_link in MARKDOWN_LINK_PATTERN.findall(content):
            target_id = resolve_markdown_link(path, raw_link, known_nodes)
            if target_id:
                add_edge(source_id, target_id, "markdown")

        for mention in extract_graph_mentions(content):
            if mention in known_nodes:
                add_edge(source_id, mention, "mention")

    for edge in edges:
        nodes[edge["source"]]["outgoing"].append(edge["target"])
        nodes[edge["target"]]["incoming"].append(edge["source"])

    for node in nodes.values():
        node["outgoing"] = sorted(set(node["outgoing"]))
        node["incoming"] = sorted(set(node["incoming"]))
        node["in_degree"] = len(node["incoming"])
        node["out_degree"] = len(node["outgoing"])
        node["degree"] = node["in_degree"] + node["out_degree"]

    intentional_orphans = [
        node
        for node in nodes.values()
        if node["in_degree"] == 0 and is_intentional_graph_orphan(_ROOT / node["path"])
    ]
    intentional_orphans.sort(key=lambda node: (node["kind"], node["path"]))

    orphan_candidates = [
        node
        for node in nodes.values()
        if node["in_degree"] == 0
        and node["kind"] in {"wiki", "vice", "insight", "domain", "concept", "inbox", "root"}
        and not is_intentional_graph_orphan(_ROOT / node["path"])
    ]
    orphan_candidates.sort(key=lambda node: (node["kind"], node["path"]))

    hubs = sorted(nodes.values(), key=lambda node: (-node["degree"], -node["in_degree"], node["path"]))
    bridges = sorted(
        [
            node
            for node in nodes.values()
            if len({nodes[target]["kind"] for target in node["outgoing"]}) > 1
        ],
        key=lambda node: (-len(node["outgoing"]), node["path"]),
    )

    return {
        "generated_on": date.today().isoformat(),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": sorted(nodes.values(), key=lambda node: node["path"]),
        "edges": sorted(edges, key=lambda edge: (edge["source"], edge["target"], edge["kind"])),
        "summary": {
            "intentional_orphans": intentional_orphans[:25],
            "orphan_candidates": orphan_candidates[:25],
            "hubs": hubs[:15],
            "bridges": bridges[:15],
        },
    }


def write_graph_artifacts(mapped_database: dict[str, dict] | None = None) -> None:
    """Persist the graph JSON plus a Markdown summary inside the wiki."""
    graph = build_gs_graph()
    if mapped_database:
        for node in graph["nodes"]:
            flaw_id = Path(node["path"]).stem
            item = mapped_database.get(flaw_id)
            if item:
                node["status"] = item["status"]
                node["downstream_verification"] = item.get("downstream_verification", "none")
    GRAPH_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    GRAPH_OUTPUT.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")

    def compact_links(values: list[str], limit: int = 6) -> str:
        if not values:
            return "—"
        preview = values[:limit]
        remainder = len(values) - len(preview)
        suffix = f" +{remainder} more" if remainder > 0 else ""
        return ", ".join(f"[[{value}]]" for value in preview) + suffix

    hub_rows = "\n".join(
        f"| [[{node['id']}]] | `{node['kind']}` | {node['in_degree']} | {node['out_degree']} | {compact_links(node['incoming'])} | {compact_links(node['outgoing'])} |"
        for node in graph["summary"]["hubs"][:10]
    )
    if not hub_rows:
        hub_rows = "| — | — | 0 | 0 | — | — |"

    intentional_orphan_rows = "\n".join(
        f"| [[{node['id']}]] | `{node['kind']}` | {node['in_degree']} | {node['out_degree']} | {compact_links(node['incoming'])} | {compact_links(node['outgoing'])} |"
        for node in graph["summary"]["intentional_orphans"]
    )
    if not intentional_orphan_rows:
        intentional_orphan_rows = "| — | — | 0 | 0 | — | — |"

    orphan_rows = "\n".join(
        f"| [[{node['id']}]] | `{node['kind']}` | {node['in_degree']} | {node['out_degree']} | {compact_links(node['incoming'])} | {compact_links(node['outgoing'])} |"
        for node in graph["summary"]["orphan_candidates"]
    )
    if not orphan_rows:
        orphan_rows = "| — | — | 0 | 0 | — | — |"

    bridge_rows = []
    node_kind_by_id = {node["id"]: node["kind"] for node in graph["nodes"]}
    for node in graph["summary"]["bridges"]:
        target_kinds = sorted({node_kind_by_id[target] for target in node["outgoing"]})
        bridge_rows.append(
            f"| [[{node['id']}]] | `{node['kind']}` | {', '.join(f'`{kind}`' for kind in target_kinds)} | {len(node['outgoing'])} |"
        )
    if not bridge_rows:
        bridge_rows = ["| — | — | — | 0 |"]

    depth_summary_rows = "| — | 0 | 0 | 0 |"
    detector_count = 0
    if mapped_database:
        cats = ("Vibe Coding", "Testing & Evaluation", "Tokenomics & Context")
        depth_counts = {c: Counter() for c in cats}
        for item in mapped_database.values():
            if item["category"] in depth_counts:
                depth_counts[item["category"]][entry_depth(item)] += 1
            if str(item.get("detector", "")).strip():
                detector_count += 1
        depth_summary_rows = "\n".join(
            f"| `{label}` | {depth_counts['Vibe Coding'].get(label, 0)} | "
            f"{depth_counts['Testing & Evaluation'].get(label, 0)} | "
            f"{depth_counts['Tokenomics & Context'].get(label, 0)} |"
            for label in ("deep", "stub", "doctrinal", "alias")
        )

    validation_debt_rows = []
    validation_debt_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_none_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_rows = ["| — | — | — | — |"]
    if mapped_database:
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        doc_only_items = [
            item
            for item in mapped_database.values()
            if str(item.get("validating_mechanism", "")).strip() == "DOC_ONLY"
            or str(item.get("status", "")).strip() == "DOC_ONLY"
        ]
        doc_only_by_category = Counter(item["category"] for item in doc_only_items)
        validation_debt_summary = (
            f"| `DOC_ONLY` | {doc_only_by_category.get('Vibe Coding', 0)} | "
            f"{doc_only_by_category.get('Testing & Evaluation', 0)} | "
            f"{doc_only_by_category.get('Tokenomics & Context', 0)} |"
        )
        consumer_expected = Counter(
            item["category"]
            for item in mapped_database.values()
            if str(item.get("downstream_verification", "none")).strip() == "required"
        )
        consumer_none = Counter(
            item["category"]
            for item in mapped_database.values()
            if str(item.get("downstream_verification", "none")).strip() == "none"
        )
        downstream_verification_summary = (
            f"| `required` | {consumer_expected.get('Vibe Coding', 0)} | "
            f"{consumer_expected.get('Testing & Evaluation', 0)} | "
            f"{consumer_expected.get('Tokenomics & Context', 0)} |"
        )
        downstream_verification_none_summary = (
            f"| `none` | {consumer_none.get('Vibe Coding', 0)} | "
            f"{consumer_none.get('Testing & Evaluation', 0)} | "
            f"{consumer_none.get('Tokenomics & Context', 0)} |"
        )
        downstream_verification_rows = [
            f"| `{item['id']}` | {item['title']} | `{item['category']}` | `{item.get('downstream_verification', 'none')}` |"
            for item in sorted(
                [item for item in mapped_database.values() if item.get("downstream_verification") == "required"],
                key=lambda item: (severity_order.get(str(item.get("severity", "medium")), 2), item["id"]),
            )[:12]
        ]
        high_priority_debt = sorted(
            doc_only_items,
            key=lambda item: (severity_order.get(str(item.get("severity", "medium")), 2), item["id"]),
        )[:12]
        validation_debt_rows = [
            f"| `{item['id']}` | {item['title']} | `{item['category']}` | `{item['severity']}` | `{item['status']}` |"
            for item in high_priority_debt
        ]
    if not validation_debt_rows:
        validation_debt_rows = ["| — | — | — | — | — |"]
    if not downstream_verification_rows:
        downstream_verification_rows = ["| — | — | — | — |"]

    graph_md = f"""# GS Graph

Local vault map automatically generated by `generate_golden_audit.py`.

This graph combines Obsidian links, relative Markdown links, and explicit ID mentions (`VC-xxx`, `VT-xxx`, `TK-xxx`, `PI-xxx`).

---

## Snapshot

| Metric | Value |
|---|---:|
| Nodes | {graph["node_count"]} |
| Edges | {graph["edge_count"]} |
| Intentional orphans | {len(graph["summary"]["intentional_orphans"])} |
| Candidate orphans | {len(graph["summary"]["orphan_candidates"])} |
| Hubs | {len(graph["summary"]["hubs"])} |

---

## Validation Debt

The graph now also highlights entries that remain mainly documentary. This does not invalidate the knowledge, but it does mark where real gates are missing.

| Catalog | VC DOC_ONLY | VT DOC_ONLY | TK DOC_ONLY |
|---|---:|---:|---:|
{validation_debt_summary}

| ID | Title | Category | Severity | Status |
|---|---|---|---|---|
{chr(10).join(validation_debt_rows)}

---

## Depth Debt

Each entry is classified by depth: `deep` (ships bad/good examples and a detection recipe — a falsifiable vice), `doctrinal` (a behavioral/epistemic principle with no static signature; a stub by design, no code is fabricated for it), `stub` (enrichable but not yet with examples — real debt), and `alias` (a semantic duplicate merged into its canonical entry; the ID is preserved for reference stability).

| Depth | VC | VT | TK |
|---|---:|---:|---:|
{depth_summary_rows}

**Local enforcement:** {detector_count} `deep` entries have a real static detector in `scripts/detectors.py`, tested in CI against their own `example_bad`/`example_good` (`scripts/test_detectors.py`). The rest are falsifiable-in-principle (they ship a detection recipe) but without an implemented detector yet.

---

## Downstream Verification

GS explicitly distinguishes which entries expect downstream verification and which do not. This prevents `DOC_ONLY` from being interpreted as `test exempt` by default.

| Status | VC | VT | TK |
|---|---:|---:|---:|
{downstream_verification_summary}
{downstream_verification_none_summary}

| ID | Title | Category | Downstream Verification |
|---|---|---|---|
{chr(10).join(downstream_verification_rows)}

---

## Hubs

Pages with the largest impact surface. If they change, review their inbound links first.

| Node | Type | In | Out | Inbound | Outbound |
|---|---|---:|---:|---|---|
{hub_rows}

---

## Intentional Orphans

Templates or fixtures kept isolated by design. They are not navigation debt, but it is worth keeping them bounded.

| Node | Type | In | Out | Inbound | Outbound |
|---|---|---:|---:|---|---|
{intentional_orphan_rows}

---

## Candidate Orphans

Pages within the live GS surface that receive no inbound links. If any is important, it should be linked from a main index or map.

| Node | Type | In | Out | Inbound | Outbound |
|---|---|---:|---:|---|---|
{orphan_rows}

---

## Bridges

Nodes that link to more than one page type. They are useful for navigating impact across domains.

| Node | Type | Reached types | Outbound |
|---|---|---|---:|
{chr(10).join(bridge_rows)}

---

## Quick Use

1. Open `[[Home]]` to enter the vault.
2. Open this map to see hubs and orphans.
3. Use the `golden_standard_graph.json` JSON if you want to automate impact analysis.

---
[[Home|Back to Home]]
"""
    GRAPH_MARKDOWN.write_text(graph_md, encoding="utf-8")
    print(f"Successfully generated Golden Standard graph at {GRAPH_OUTPUT} and {GRAPH_MARKDOWN}")


def populate_pi_mappings(domain: str, items: list, pi_to_domains: dict):
    """Populate project insight to domain mapping dict."""
    for item in items:
        pi_id = item["insight_id"]
        if pi_id not in pi_to_domains:
            pi_to_domains[pi_id] = []
        pi_to_domains[pi_id].append((domain, item["project"], item["action"]))


def build_pi_to_domains_map(recommendations: dict) -> dict[str, list]:
    """Group recommendations by project insight ID."""
    pi_to_domains = {}
    for domain, items in recommendations.items():
        populate_pi_mappings(domain, items, pi_to_domains)
    return pi_to_domains


def generate_obsidian_wiki(mapped_database: dict, wiki_dir: Path):
    """Generate a structured, cross-linked Obsidian vault from Compiled Golden Standard data."""
    clean_wiki_directory(wiki_dir)

    for folder in ["Concepts", "Domains", "Vices", "Tokenomics", "Project_Insights"]:
        (wiki_dir / folder).mkdir(parents=True, exist_ok=True)

    insights = get_project_insights()
    recommendations = get_project_insight_recommendations()
    pi_to_domains = build_pi_to_domains_map(recommendations)

    total_vices = len(mapped_database)
    vc_count = len([x for x in mapped_database.values() if x["category"] == "Vibe Coding"])
    tv_count = len([x for x in mapped_database.values() if x["category"] == "Testing & Evaluation"])
    tk_count = len([x for x in mapped_database.values() if x["category"] == "Tokenomics & Context"])
    pi_count = len(insights)

    status_counts = Counter(x["status"] for x in mapped_database.values())

    write_home_md(wiki_dir, total_vices, vc_count, tv_count, tk_count, pi_count, status_counts)
    write_vices_index_md(wiki_dir, mapped_database)
    write_tokenomics_index_md(wiki_dir, mapped_database)
    write_tokenomics_subindices_md(wiki_dir, mapped_database)
    write_project_insights_index_md(wiki_dir, insights)
    write_tokenomics_map_md(wiki_dir, insights)
    write_conceptual_concepts_md(wiki_dir)
    write_atomic_vices(wiki_dir, mapped_database)
    write_atomic_tokenomics(wiki_dir, mapped_database)
    write_atomic_project_insights(wiki_dir, insights, pi_to_domains)
    write_audit_domains(wiki_dir, recommendations)
    write_graph_artifacts(mapped_database)

    print(f"Successfully generated Obsidian Wiki Vault at {wiki_dir}")


def extract_catalog_items(config: dict, mapped_database: dict):
    """Parse catalog configuration dict and populate mapped flaws."""
    if not isinstance(config, dict) or "items" not in config:
        return
    for item in config["items"]:
        downstream_verification = str(item.get("downstream_verification", "")).strip()
        if not downstream_verification:
            downstream_verification = "required" if str(item.get("status", "")).strip() == "DOC_ONLY" else "none"
        flaw_id = item["id"]
        mapped_database[flaw_id] = {
            "id": flaw_id,
            "title": item["title"],
            "category": get_flaw_category(flaw_id),
            "symptom": item["symptom"],
            "cause": item["cause"],
            "solution": item["solution"],
            "status": item["status"],
            "severity": item.get("severity", "medium"),
            "tags": item.get("tags", []),
            "action": item["action"],
            "validating_mechanism": item["validating_mechanism"],
            "downstream_verification": downstream_verification,
            "example_bad": item.get("example_bad", ""),
            "example_good": item.get("example_good", ""),
            "example_lang": item.get("example_lang", "text"),
            "detection": item.get("detection", ""),
            "evidence": item.get("evidence", []),
            "doctrinal": bool(item.get("doctrinal", False)),
            "alias_of": str(item.get("alias_of", "")).strip(),
            "detector": str(item.get("detector", "")).strip(),
            "tier": str(item.get("tier", "extended")).strip(),
        }


def main():
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    catalogs = load_golden_standard_catalogs()
    mapped_database = {}
    
    for _, config in catalogs.items():
        extract_catalog_items(config, mapped_database)

    print(f"Extracted {len(mapped_database)} flaws from Golden Standard catalogs.")

    with open(JSON_OUTPUT, "w", encoding="utf-8") as f:
        json.dump(mapped_database, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {JSON_OUTPUT}")

    report_lines = [
        "# Golden Standard Compliance Audit Report",
        f"**Golden Standard {_read_version_label()} | Date: {date.today().isoformat()} | Total Audited Items: {len(mapped_database)}**",
        "",
        "This document is generated automatically by `generate_golden_audit.py` to map every Golden Standard point to its specific mitigation action and validating test in the GS tooling ecosystem.",
        "",
        "## Summary of Compliance",
        "",
        "| Category | Audited Items | Prevented / Remediated | Audited / Not Applicable | Clean Status |",
        "|---|---|---|---|---|",
        f"| **Testing & Evaluation** | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation'])} | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Testing & Evaluation' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Vibe Coding** | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding'])} | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Vibe Coding' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Tokenomics & Context** | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context'])} | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context' and x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['category'] == 'Tokenomics & Context' and x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        f"| **Total** | {len(mapped_database)} | {len([x for x in mapped_database.values() if x['status'] in ('PREVENTED', 'REMEDIATED')])} | {len([x for x in mapped_database.values() if x['status'] not in ('PREVENTED', 'REMEDIATED')])} | 100% |",
        "",
        "---",
        "",
        "## Full Audit Details",
        "",
    ]

    for category in ["Testing & Evaluation", "Vibe Coding", "Tokenomics & Context"]:
        cat_items = [x for x in mapped_database.values() if x["category"] == category]
        report_lines.append(f"### {category} ({len(cat_items)} items)")
        report_lines.append("")
        report_lines.append(
            "| ID | Flaw Title | Severity | Status | Downstream Verification | Action Taken / Prevention Method | Validating Test / Guard |"
        )
        report_lines.append("|---|---|---|---|---|---|---|")

        for item in sorted(cat_items, key=lambda x: x["id"]):
            action_snippet = item["action"].replace("\n", " ")
            report_lines.append(
                f"| `{item['id']}` | {item['title']} | **{item['severity']}** | **{item['status']}** | `{item.get('downstream_verification', 'none')}` | {action_snippet} | `{item['validating_mechanism']}` |"
            )
        report_lines.append("")

    report_lines.extend(build_project_insight_section())
    report_lines.extend(build_project_insight_recommendations_section())

    MARKDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_OUTPUT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Successfully generated {MARKDOWN_OUTPUT}")

    generate_obsidian_wiki(mapped_database, WIKI_DIR)

    # Honest dynamic quality metrics + shields.io badges (Phase 5).
    sys.path.insert(0, str(_ROOT / "scripts"))
    from metrics import write_all as write_metrics

    metrics = write_metrics()
    print(f"Successfully generated quality metrics and badges "
          f"(deep {metrics['deep_pct']}%, {metrics['local_detectors']} detectors, {metrics['stub']} stubs).")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        print("Error compiling audit report:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
