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


def load_project_insight_records() -> dict[str, dict[str, object]]:
    """Load structured project-insight records from the principles catalog."""
    path = _ROOT / "golden_standard_principles.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    items = data.get("items", [])
    records: dict[str, dict[str, object]] = {}
    if not isinstance(items, list):
        return records
    for item in items:
        if not isinstance(item, dict):
            continue
        k = str(item.get("id", ""))
        if not k.startswith("PR-"):
            continue
        record = dict(item)
        record["title"] = normalize_knowledge_text(
            record.get("title", record.get("text", ""))
        )
        record["doctrinal"] = bool(record.get("doctrinal", False))
        record["promotion_candidate"] = bool(record.get("promotion_candidate", False))
        records[k] = record
    return records


def get_principles() -> dict[str, str]:
    """Load principles as a normalized mapping of id -> text."""
    return {
        pi_id: record["title"]
        for pi_id, record in load_project_insight_records().items()
        if str(record.get("title", "")).strip()
    }


def get_canonical_domain_map() -> dict[str, dict[str, object]]:
    """Return the canonical GS domain map with metadata plus principle assignments."""
    json_path = _ROOT / "config" / "canonical_domain_map.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def domain_principle_rows(domain_record: dict[str, object]) -> list[dict[str, str]]:
    """Return the principle assignment rows for a canonical domain record."""
    rows = domain_record.get("principles", [])
    return rows if isinstance(rows, list) else []


def principle_to_domain_map() -> dict[str, str]:
    """Return a mapping of principle_id -> domain_id from canonical_domain_map."""
    domain_map = get_canonical_domain_map()
    mapping = {}
    for domain_id, record in domain_map.items():
        for principle in record.get("principles", []):
            if isinstance(principle, dict):
                pr_id = str(principle.get("insight_id", "")).strip()
                if pr_id:
                    mapping[pr_id] = domain_id
    return mapping


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


def build_principles_section() -> list[str]:
    """Build a markdown section for the canonical principles layer."""
    insight_records = load_project_insight_records()
    insights = get_principles()
    lines = [
        "## Principles",
        "",
        "These entries are preserved as project-agnostic doctrine and now consumed as first-class principles by GS users and downstream tools.",
        "",
        "| ID | Principle |",
        "|---|---|",
    ]
    for insight_id in sorted(insights):
        lines.append(f"| `{insight_id}` | {insights[insight_id]} |")
    lines.append("")
    return lines


def build_canonical_domains_section() -> list[str]:
    """Build a markdown section mapping principles to canonical domains."""
    recommendations = get_canonical_domain_map()
    lines = [
        "## Principle Recommendations by Canonical Domain",
        "",
        "These actions are the operational bridge between the principles and the canonical GS domains.",
        "",
        "| Domain | Title | Principle | Project | Action |",
        "|---|---|---|---|---|",
    ]
    for domain in sorted(recommendations):
        record = recommendations[domain]
        items = domain_principle_rows(record)
        title = str(record.get("title", "—")).strip()
        for item in items:
            if not isinstance(item, dict):
                continue
            lines.append(
                f"| `{domain}` | {title} | `{item['insight_id']}` | {item['project']} | {item['action']} |"
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
    proposed_count = audited_count + doc_only_count
    enforced_external_count = prevented_count
    enforced_local_count = remediated_count
    home_content = f"""# Golden Standard Wiki

Welcome to the Obsidian vault of the **Golden Standard** (GS). This knowledge base represents the pure doctrine of engineering, vice mitigation, and tokenomics accumulated by the project.

---

## Quick Access

- 📂 **[[Vices_Index|Engineering Vices Index]]**: Central catalog of code and test anomalies (`VC`, `TV`).
- 📘 **[[Principles|Principles Index]]**: First-class doctrinal rules, each kept as a linked principle instead of duplicated prose.
- 🧭 **[[Domains/README|Canonical Domains Index]]**: The canonical GS domain taxonomy, with graph-aware navigation from doctrine to enforcement surfaces.
- 🕸️ **[[Graph|GS Graph Map]]**: Hubs, intentional orphans, candidate orphans, and local vault impact.
- 📘 **[Golden Standard Conceptual Framework](../CONCEPTUAL_FRAMEWORK.md)**: Epistemological doctrine, levels, and design foundations.
- 🧼 **[Repository Hygiene Chapter](../CONCEPTUAL_FRAMEWORK.md#6-Repository-and-Execution-Hygiene)**: Canonical standard for cleanup, naming, clean root, and organization evidence.
- ⚠️ **[[Vices/VC-056|Hasty deprecation]]**: Mirror vice that avoids moving to `deprecated/` without analysis.
- 💠 **[[Tokenomics_Index|Tokenomics Index]]**: Separate catalog of efficiency, headroom, and context management (`TK`).
- 🗺️ **[[Tokenomics_Map|Tokenomics Map]]**: Bridge between the `TK` lens and the principles that shape efficient context use.
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
| Principles | `PR-xxx` | {pi_count} | [[Principles|Open index]] |

---

## Operational Reading

| Reading | Entries | Meaning |
|---|---:|---|
| `PROPOSED` | {proposed_count} | The entry is documented or audited, but no enforcing implementation exists in the catalog flow. |
| `ENFORCED_EXTERNAL` | {enforced_external_count} | The guard exists in a downstream enforcing project. |
| `ENFORCED_LOCAL` | {enforced_local_count} | The guard or remediation is enforced in this repository. |
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
3. Promote to YAML + Wiki only after deduplicating and mapping the canonical domain.
4. Recompile with `python generate_golden_audit.py`.

---
*Vault auto-generated by the `generate_golden_audit.py` compiler on {date.today().isoformat()}.*"""
    (wiki_dir / "Home.md").write_text(home_content, encoding="utf-8")




def write_principles_index(wiki_dir: Path, records: dict[str, dict[str, object]]):
    """Write a single consolidated Principles index with all doctrinal entries."""
    rows = []
    for pr_id in sorted(records):
        record = records[pr_id]
        note = "promotion candidate" if record.get("promotion_candidate") else "doctrinal"
        title = record.get("title", "—")
        rows.append(f"| {pr_id} | {title} | {note} |")

    content = f"""# Principles

The {len(records)} principles are first-class governance rules. Some are doctrinal, some are operational, but all are treated as reusable knowledge instead of ad-hoc commentary.

---

| ID | Title | Note |
|---|---|---|
{chr(10).join(rows)}

---

## Canonical Domains

These principles are operationalized through the separate [[Domains/README|Canonical Domains Index]], where each domain declares its boundary, graph role, and linked doctrine.

---
[[Home|Back to Home]]
"""
    (wiki_dir / "Principles.md").write_text(content, encoding="utf-8")


def write_domains_index_md(wiki_dir: Path, recommendations: dict):
    """Write the canonical GS domain index."""
    rows = []
    for domain in sorted(recommendations):
        record = recommendations[domain]
        items = domain_principle_rows(record)
        unique_principles = sorted(
            {
                str(item.get("insight_id", "")).strip()
                for item in items
                if isinstance(item, dict) and str(item.get("insight_id", "")).strip()
            }
        )
        project_names = sorted(
            {
                str(item.get("project", "")).strip()
                for item in items
                if isinstance(item, dict) and str(item.get("project", "")).strip()
            }
        )
        title = str(record.get("title", "—")).strip()
        legacy = ", ".join(f"`{value}`" for value in record.get("legacy_gs_lenses", [])) or "—"
        sample = ", ".join(f"`{pid}`" for pid in unique_principles[:4])
        if len(unique_principles) > 4:
            sample += f" +{len(unique_principles) - 4} more"
        rows.append(
            f"| [[Domains/{domain}|{domain}]] | {title or '—'} | {len(unique_principles)} | {sample or '—'} | {legacy} |"
        )

    if not rows:
        rows = ["| — | — | 0 | — | — |"]

    content = f"""# Canonical Domains Index

This index is the canonical cognitive entrypoint for GS. Each domain page is a graph-aware semantic hub: it declares what the domain covers, what it excludes, which legacy GS lenses fed it, and which principles currently operationalize it.

---

| Domain | Title | Principles | Sample Principles | Legacy GS lenses |
|---|---|---:|---|---|
{chr(10).join(rows)}

---
[[Principles|Principles Index]] | [[Graph|GS Graph Map]] | [[Home|Back to Home]]
"""
    (wiki_dir / "Domains" / "README.md").write_text(content, encoding="utf-8")


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
    """Write a bridge page that links tokenomics lenses with principles."""
    bridge_rows = [
        (
            "Memory and Headroom",
            "[[Tokenomics/Memory_Headroom_Index|Open lens]]",
            "PR-084, PR-088, PR-092, PR-096",
            "Avoids context loss, root pollution, and forgotten learning.",
        ),
        (
            "Input and Retrieval",
            "[[Tokenomics/Input_Retrieval_Index|Open lens]]",
            "PR-083, PR-090",
            "Reduces input noise and makes targeted retrieval more precise.",
        ),
        (
            "Output and Compaction",
            "[[Tokenomics/Output_Compaction_Index|Open lens]]",
            "PR-081, PR-085, PR-087, PR-094",
            "Controls verbosity, cost, pruning, and documentary honesty.",
        ),
        (
            "Measurement and Telemetry",
            "[[Tokenomics/Measurement_Telemetry_Index|Open lens]]",
            "PR-081, PR-091",
            "Makes the real savings visible, not just the intention to save.",
        ),
        (
            "Automation and Tooling",
            "[[Tokenomics/Automation_Tooling_Index|Open lens]]",
            "PR-083, PR-084, PR-091",
            "Connects the doctrine with executable tooling and continuous observability.",
        ),
    ]

    insight_pairs = []
    for insight_id in ["PR-081", "PR-083", "PR-084", "PR-085", "PR-087", "PR-088", "PR-090", "PR-091", "PR-092", "PR-094", "PR-096"]:
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

This map serves as a bridge between the `TK` category and the GS principles layer. It does not repeat the catalog: it shows how to read it and which principles it crosses.

## What it is for

- Navigate relations between context vices, token savings, and operational discipline.
- Identify which principles reinforce each tokenomics lens.
- Detect gaps where doctrine exists, but a supporting artifact or clear telemetry is still missing.

---

## Operational lenses

| Lens | Subindex | Related Principles | Intent |
|---|---|---|---|
{lens_rows}

---

## Key Principles

| Principle | Summary |
|---|---|
{insight_rows}

---

## Adjacent crossings

| Node | Relation | Reason |
|---|---|---|
| `[[Principles|PR-097]]` | Principle hygiene | Expands the discipline of editing and validation toward daily work with tools. |
| `[[Vices/VC-056|VC-056]]` | Mirror vice | Represents the error of deprecating without analysis or traceability. |

---

## Practical reading

1. If a problem consumes context, first check `Memory and Headroom`.
2. If the problem originates in the input, check `Input and Retrieval`.
3. If the cost is in the response, check `Output and Compaction`.
4. If there is no evidence of savings, check `Measurement and Telemetry`.
5. If the doctrine does not run by itself, check `Automation and Tooling`.

---
[[Tokenomics_Index|Back to Tokenomics Index]] | [[Principles|Go to Principles]] | [[Home|Home]]
"""
    (wiki_dir / "Tokenomics_Map.md").write_text(map_content, encoding="utf-8")


def _tokenomics_subindex_group(item_id: str, title: str) -> str:
    """Map a tokenomics entry to a thematic subindex."""
    if item_id.startswith("PR-067") or item_id in {"TK-001", "TK-002", "TK-003", "TK-004", "TK-005", "TK-006", "TK-007", "TK-008", "TK-021", "TK-022", "TK-023", "TK-024", "TK-025", "PR-077"}:
        return "memory_headroom"
    if item_id.startswith("PR-068") or item_id in {"PR-070", "PR-071", "PR-072", "PR-070", "PR-073", "PR-074", "PR-072", "TK-012", "PR-076"}:
        return "input_retrieval"
    if item_id.startswith("PR-069") or item_id in {"TK-013", "PR-073", "PR-074", "PR-075", "TK-018", "TK-020", "PR-077", "PR-078", "TK-026", "TK-027", "TK-033"}:
        return "output_compaction"
    if item_id in {"TK-016", "PR-076", "TK-028", "TK-031", "TK-032"}:
        return "measurement_telemetry"
    if item_id in {"PR-071", "PR-075", "PR-078"}:
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

> Index page only: this file organizes TK entries and does not count as a TK entry itself.

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


# Editorial classification removed; all principles are now in a single index.


def entry_depth(item: dict) -> str:
    """Classify an entry by depth: deep, doctrinal, or stub.

    - 'deep'      : ships paired bad/good examples (a concrete, falsifiable vice).
    - 'doctrinal' : explicitly flagged as a behavioral/epistemic principle with no
                    static signature; a stub by design, not by neglect. Fabricating
                    code for these would be theater, so we never do.
    - 'stub'      : enrichable but not yet enriched (real depth debt).
    """
    # Aliases removed; all entries are real
    if str(item.get("example_bad", "")).strip() and str(item.get("example_good", "")).strip():
        return "deep"
    if item.get("doctrinal"):
        return "doctrinal"
    return "stub"


def depth_badge(item: dict) -> str:
    """Human-readable badge for an entry's depth classification."""
    # No aliases; all entries are real
    return {"deep": "🟢 Deep", "doctrinal": "⚪ Doctrinal"}.get(entry_depth(item), "🟡 Stub")


def evidence_slug(source: str) -> str:
    """Convert an evidence source string into a filesystem-safe slug."""
    import re
    slug = re.sub(r'[^\w\s.-]', '', source.lower())
    slug = re.sub(r'[\s.:]+', '_', slug)
    slug = slug.strip('_')
    # Truncate very long slugs
    if len(slug) > 80:
        slug = slug[:80]
    return slug


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
                slug = evidence_slug(source)
                source_link = f"[[Evidence/{slug}|{source}]]"
                lines.append(f"- **{source_link}** — {claim}" if claim else f"- **{source_link}**")
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
        tag_list = ", ".join(f"`{tag}`" for tag in item["tags"]) if item.get("tags") else "`untagged`"
        depth_sections = build_depth_sections(item)
        detector = str(item.get("detector", "")).strip()
        detector_row = (
            f"\n| **Local detector** | 🛡️ [[Detectors/{detector}|{detector}]] (tested against the examples in CI) |"
            if detector else ""
        )
        
        # Build related domains from PR mentions in vice text
        pr_to_domain = principle_to_domain_map()
        vice_text = " ".join([str(item.get(k, "")) for k in ["title", "symptom", "cause", "solution", "action"]])
        pr_mentions = set(re.findall(r"PR-\d{3}", vice_text))
        related_domains = sorted({pr_to_domain.get(pr, "") for pr in pr_mentions if pr_to_domain.get(pr, "")})
        domain_section = (
            "\n".join(f"- [[Domains/{d}|{d}]]" for d in related_domains)
            if related_domains
            else "*No domain assignments detected.*"
        )
        
        # Consumer usage layer: Cerberus dimensions that enforce this vice
        _cerberus_map_path = _ROOT / "config" / "cerberus_dimensions.json"
        cerberus_dimensions = {}
        if _cerberus_map_path.exists():
            with open(_cerberus_map_path, "r", encoding="utf-8") as f:
                cerberus_dimensions = json.load(f)
        enforced_by = cerberus_dimensions.get(flaw_id, [])
        enforced_section = (
            "\n".join(f"- {d}" for d in sorted(enforced_by))
            if enforced_by
            else "*No Cerberus enforcement detected.*"
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
| **Validation Mechanism** | `{_display_mechanism(item)}` |

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
- [[Principles|PR-097]]
- [[Tokenomics_Map|Tokenomics Map]]
- [[Home|Home]]

---

### Related Domains
{domain_section}

---

### Enforced by (Cerberus Dimensions)
{enforced_section}

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
| **Validation Mechanism** | `{_display_mechanism(item)}` |

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
    """Format mapping lines for principles."""
    if not mappings:
        return ["*No active domain assignments.*"]
    return [
        f"*   **[[Domains/{domain}|{domain}]]** (Project: *{proj}*): {act}"
        for domain, proj, act in sorted(mappings)
    ]




def write_audit_domains(wiki_dir: Path, recommendations: dict):
    """Create canonical domain overview files mapping domains to principles."""
    for domain in sorted(recommendations):
        record = recommendations[domain]
        items = domain_principle_rows(record)
        linked_items = [
            f"*   **[[Principles|{rec['insight_id']}]]** (Project: *{rec['project']}*): {rec['action']}"
            for rec in items
        ]
        title = str(record.get("title", "—")).strip()
        summary = str(record.get("summary", "—")).strip()
        covers = record.get("covers", [])
        excludes = record.get("excludes", [])
        legacy = record.get("legacy_gs_lenses", [])
        graph_role = str(record.get("graph_role", "")).strip()
        cover_lines = "\n".join(f"- {item}" for item in covers) if covers else "- No coverage declared."
        exclude_lines = "\n".join(f"- {item}" for item in excludes) if excludes else "- No explicit exclusions declared."
        legacy_text = ", ".join(f"`{item}`" for item in legacy) if legacy else "None"

        domain_content = f"""# {domain} — {title}

{summary}

---

## Graph Role

{graph_role or "Canonical domain hub that bridges doctrine, graph navigation, and downstream enforcement semantics."}

---

## Covers

{cover_lines}

---

## Explicitly Excludes

{exclude_lines}

---

## Legacy GS inputs

{legacy_text}

---

### Linked Principles

{"\n".join(linked_items)}

---
[[Domains/README|Canonical Domains Index]] | [[Graph|GS Graph Map]] | [[Home|Back to Home]]
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
    if rel_path == "Wiki/Principles.md":
        return "principle-index"
    if rel_path.startswith("Wiki/Domains/"):
        return "domain"
    if rel_path.startswith("Wiki/Concepts/"):
        return "concept"
    if rel_path.startswith("Wiki/"):
        return "wiki"
    return "doc"


def infer_graph_relation(
    source_path: Path, target_path: Path, source_id: str, target_id: str, link_kind: str
) -> tuple[str, float]:
    """Infer a semantic relation label and confidence for a graph edge."""
    if link_kind == "mention":
        return "mentions", 0.75

    source_kind = classify_graph_node(source_path)
    target_kind = classify_graph_node(target_path)

    if source_id == "Home":
        return "entrypoint", 0.95
    if source_id == "Tokenomics_Map":
        return "bridges", 0.95
    if source_id == "Principles" and target_kind == "domain":
        return "routes_to_domains", 0.95
    if source_id == "Principles" and target_kind == "wiki":
        return "indexes", 0.9
    if source_kind == "domain" and target_kind == "principle-index":
        return "operationalizes_domain", 0.95
    if source_kind == "vice" and target_kind == "principle-index":
        return "governed_by", 0.9
    if source_kind == "tokenomics" and target_kind == "principle-index":
        return "thematic_bridge", 0.9
    if source_kind == "tokenomics" and target_kind == "tokenomics":
        return "subindex", 0.9
    if source_kind == "wiki" and target_kind in {"vice", "tokenomics", "principle-index", "domain"}:
        return "catalogs", 0.95
    if source_kind in {"vice", "tokenomics", "principle-index", "domain"} and target_kind == "wiki":
        return "returns_to_index", 0.95
    if source_kind in {"root", "contributing", "code-of-conduct", "conceptual-framework"}:
        return "references", 0.9
    if source_kind == "inbox":
        return "template_or_intake", 0.8
    return "references", 0.85


def collect_graph_sources() -> list[Path]:
    """Return the live Markdown sources that should participate in the GS graph."""
    sources = [
        _ROOT / "README.md",
        _ROOT / "CONTRIBUTING.md",
        _ROOT / "CONCEPTUAL_FRAMEWORK.md",
        _ROOT / "CODE_OF_CONDUCT.md",
    ]

    for relative_dir in ["Wiki"]:
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


def _git_timestamps(path: Path) -> tuple[str | None, str | None]:
    """Return (created, promoted) ISO timestamps from git log for *path*."""
    try:
        import subprocess
        # First commit (created)
        created_result = subprocess.run(
            ["git", "log", "--follow", "--format=%aI", "--", str(path)],
            capture_output=True,
            text=True,
            cwd=_ROOT,
        )
        if created_result.returncode == 0 and created_result.stdout.strip():
            lines = created_result.stdout.strip().splitlines()
            created = lines[-1] if lines else None
        else:
            created = None
        # Last commit (promoted)
        promoted_result = subprocess.run(
            ["git", "log", "-1", "--format=%aI", "--", str(path)],
            capture_output=True,
            text=True,
            cwd=_ROOT,
        )
        if promoted_result.returncode == 0 and promoted_result.stdout.strip():
            promoted = promoted_result.stdout.strip().splitlines()[0]
        else:
            promoted = None
        return created, promoted
    except Exception:
        return None, None


def build_gs_graph() -> dict:
    """Build a deterministic knowledge graph from the live Markdown surface."""
    sources = collect_graph_sources()
    known_nodes = {canonical_graph_node_id(path) for path in sources}
    paths_by_id = {canonical_graph_node_id(path): path for path in sources}

    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    edge_keys: set[tuple[str, str, str, str]] = set()

    def add_edge(source: str, target: str, kind: str) -> None:
        if source == target:
            return
        source_path = paths_by_id[source]
        target_path = paths_by_id[target]
        relation, confidence = infer_graph_relation(source_path, target_path, source, target, kind)
        key = (source, target, kind, relation)
        if key in edge_keys:
            return
        edge_keys.add(key)
        edges.append(
            {
                "source": source,
                "target": target,
                "kind": kind,
                "relation": relation,
                "confidence": confidence,
            }
        )

    for path in sources:
        node_id = canonical_graph_node_id(path)
        content = path.read_text(encoding="utf-8")
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else path.stem
        created, promoted = _git_timestamps(path)
        nodes[node_id] = {
            "id": node_id,
            "path": path.relative_to(_ROOT).as_posix(),
            "title": title,
            "kind": classify_graph_node(path),
            "created": created,
            "promoted": promoted,
            "outgoing": [],
            "incoming": [],
            "outgoing_edges": [],
            "incoming_edges": [],
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
        nodes[edge["source"]]["outgoing_edges"].append(
            {
                "target": edge["target"],
                "kind": edge["kind"],
                "relation": edge["relation"],
                "confidence": edge["confidence"],
            }
        )
        nodes[edge["target"]]["incoming_edges"].append(
            {
                "source": edge["source"],
                "kind": edge["kind"],
                "relation": edge["relation"],
                "confidence": edge["confidence"],
            }
        )

    for node in nodes.values():
        node["outgoing"] = sorted(set(node["outgoing"]))
        node["incoming"] = sorted(set(node["incoming"]))
        node["outgoing_edges"] = sorted(
            node["outgoing_edges"],
            key=lambda item: (item["target"], item["relation"], item["kind"]),
        )
        node["incoming_edges"] = sorted(
            node["incoming_edges"],
            key=lambda item: (item["source"], item["relation"], item["kind"]),
        )
        node["in_degree"] = len(node["incoming"])
        node["out_degree"] = len(node["outgoing"])
        node["degree"] = node["in_degree"] + node["out_degree"]
        connected_types = {
            nodes[item["target"]]["kind"] for item in node["outgoing_edges"]
        } | {
            nodes[item["source"]]["kind"] for item in node["incoming_edges"]
        }
        relation_types = {
            item["relation"] for item in node["outgoing_edges"]
        } | {
            item["relation"] for item in node["incoming_edges"]
        }
        node["connected_types"] = sorted(connected_types)
        node["relation_types"] = sorted(relation_types)
        node["semantic_reach"] = len(node["connected_types"])
        node["relation_diversity"] = len(node["relation_types"])
        node["hub_score"] = (
            node["degree"]
            + (node["semantic_reach"] * 3)
            + (node["relation_diversity"] * 2)
        )

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
        and node["kind"] in {"wiki", "vice", "domain", "concept", "inbox", "root", "tokenomics", "principle-index"}
        and not is_intentional_graph_orphan(_ROOT / node["path"])
    ]
    orphan_candidates.sort(key=lambda node: (node["kind"], node["path"]))

    hubs = sorted(nodes.values(), key=lambda node: (-node["degree"], -node["in_degree"], node["path"]))
    bridges = sorted(
        [
            node
            for node in nodes.values()
            if len(node["connected_types"]) > 1
        ],
        key=lambda node: (-len(node["connected_types"]), -node["degree"], node["path"]),
    )
    edge_kind_counts = Counter(edge["kind"] for edge in edges)
    relation_counts = Counter(edge["relation"] for edge in edges)
    reciprocal_pairs = {
        tuple(sorted((edge["source"], edge["target"])))
        for edge in edges
        if edge["source"] != edge["target"]
        and any(
            reverse["source"] == edge["target"] and reverse["target"] == edge["source"]
            for reverse in edges
        )
    }
    avg_confidence = round(sum(edge["confidence"] for edge in edges) / len(edges), 3) if edges else 0.0
    intentional_orphan_review = []
    for node in intentional_orphans:
        rel_path = node["path"]
        recommendation = "keep_isolated"
        rationale = "Template fixtures should not pollute the main doctrine graph."
        if rel_path.startswith("Inbox/templates/"):
            recommendation = "index_anchor_only"
            rationale = "Templates belong in the graph through the template index, not as free-floating doctrine."
        intentional_orphan_review.append(
            {
                "id": node["id"],
                "path": node["path"],
                "kind": node["kind"],
                "recommendation": recommendation,
                "rationale": rationale,
            }
        )

    return {
        "generated_on": date.today().isoformat(),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "nodes": sorted(nodes.values(), key=lambda node: node["path"]),
        "edges": sorted(
            edges,
            key=lambda edge: (edge["source"], edge["target"], edge["relation"], edge["kind"]),
        ),
        "summary": {
            "edge_kinds": dict(sorted(edge_kind_counts.items())),
            "relation_counts": dict(sorted(relation_counts.items())),
            "reciprocal_pairs": len(reciprocal_pairs),
            "average_edge_confidence": avg_confidence,
            "intentional_orphans": intentional_orphans[:25],
            "intentional_orphan_review": intentional_orphan_review[:25],
            "orphan_candidates": orphan_candidates[:25],
            "hubs": hubs[:15],
            "bridges": bridges[:15],
        },
    }


def write_graph_artifacts(mapped_database: dict[str, dict] | None = None) -> None:
    """Persist the graph JSON plus a Markdown summary inside the wiki."""
    graph = build_gs_graph()
    node_by_stem = {Path(node["path"]).stem: node for node in graph["nodes"]}
    if mapped_database:
        for node in graph["nodes"]:
            flaw_id = Path(node["path"]).stem
            item = mapped_database.get(flaw_id)
            if item:
                node["status"] = item["status"]
                node["downstream_verification"] = item.get("downstream_verification", "none")
    # P2/P3: Enrich graph with severity, weight, cluster, and temporal data
    if mapped_database:
        # Severity-weighted edges
        severity_weight = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
        for edge in graph["edges"]:
            source_node = next((n for n in graph["nodes"] if n["id"] == edge["source"]), None)
            if source_node:
                item = mapped_database.get(Path(source_node["path"]).stem)
                if item:
                    edge["weight"] = round(severity_weight.get(str(item.get("severity", "medium")).strip(), 0.5), 2)
        
        # Add severity to vice nodes
        for node in graph["nodes"]:
            flaw_id = Path(node["path"]).stem
            item = mapped_database.get(flaw_id)
            if item:
                node["severity"] = str(item.get("severity", "medium")).strip()
        
        # Anti-pattern clusters: group vices by shared keywords in title+symptom
        import re
        vice_texts = {}
        for flaw_id, item in mapped_database.items():
            if item["category"] in {"Vibe Coding", "Testing & Evaluation"}:
                text = f"{item['title']} {item['symptom']}".lower()
                vice_texts[flaw_id] = set(re.findall(r'\b\w{5,}\b', text))
        
        cluster_map = {}
        cluster_id = 0
        for flaw_id, words in vice_texts.items():
            assigned = None
            for existing_id, existing_words in list(cluster_map.items()):
                if len(words & existing_words) >= 2:
                    assigned = existing_id
                    cluster_map[existing_id] = words | existing_words
                    break
            if assigned is None:
                cluster_id += 1
                assigned = f"cluster_{cluster_id}"
                cluster_map[assigned] = words
            for node in graph["nodes"]:
                if Path(node["path"]).stem == flaw_id:
                    node["cluster"] = assigned
    
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
    for node in graph["summary"]["bridges"]:
        bridge_rows.append(
            f"| [[{node['id']}]] | `{node['kind']}` | {', '.join(f'`{kind}`' for kind in node.get('connected_types', [])) or '—'} | "
            f"{', '.join(f'`{rel}`' for rel in node.get('relation_types', [])) or '—'} | {len(node['outgoing'])} |"
        )
    if not bridge_rows:
        bridge_rows = ["| — | — | — | — | 0 |"]

    semantic_relation_rows = "\n".join(
        f"| `{relation}` | {count} |"
        for relation, count in sorted(
            graph["summary"].get("relation_counts", {}).items(),
            key=lambda item: (-item[1], item[0]),
        )
    )
    if not semantic_relation_rows:
        semantic_relation_rows = "| — | 0 |"

    orphan_review_rows = "\n".join(
        f"| [[{node['id']}]] | `{node['recommendation']}` | {node['rationale']} |"
        for node in graph["summary"].get("intentional_orphan_review", [])
    )
    if not orphan_review_rows:
        orphan_review_rows = "| — | — | No intentional orphan review needed. |"

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
            for label in ("deep", "stub", "doctrinal")
        )

    validation_debt_rows = []
    cognitive_priority_rows = []
    validation_debt_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_none_summary = "| — | 0 | 0 | 0 |"
    downstream_verification_rows = ["| — | — | — | — |"]
    if mapped_database:
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        severity_weight = {"critical": 40, "high": 25, "medium": 10, "low": 5}
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
        doc_only_priorities = []
        for item in doc_only_items:
            node = node_by_stem.get(item["id"])
            if not node:
                continue
            downstream_required = str(item.get("downstream_verification", "none")).strip() == "required"
            score = (
                severity_weight.get(str(item.get("severity", "medium")), 10)
                + node["hub_score"]
                + (12 if downstream_required else 0)
            )
            signals = [
                f"deg={node['degree']}",
                f"types={node['semantic_reach']}",
                f"rels={node['relation_diversity']}",
            ]
            if downstream_required:
                signals.append("consumer-check")
            doc_only_priorities.append(
                {
                    "id": item["id"],
                    "title": item["title"],
                    "category": item["category"],
                    "severity": item["severity"],
                    "score": score,
                    "signals": ", ".join(signals),
                }
            )
        cognitive_priority_rows = [
            f"| `{item['id']}` | {item['title']} | `{item['severity']}` | `{item['score']}` | {item['signals']} |"
            for item in sorted(
                doc_only_priorities,
                key=lambda item: (-item["score"], severity_order.get(str(item["severity"]), 2), item["id"]),
            )[:12]
        ]
    if not validation_debt_rows:
        validation_debt_rows = ["| — | — | — | — | — |"]
    if not cognitive_priority_rows:
        cognitive_priority_rows = ["| — | — | — | 0 | No active DOC_ONLY priority debt. |"]
    if not downstream_verification_rows:
        downstream_verification_rows = ["| — | — | — | — |"]

    graph_md = f"""# GS Graph

Local vault map automatically generated by `generate_golden_audit.py`.

This graph combines Obsidian links, relative Markdown links, and explicit ID mentions (`VC-xxx`, `VT-xxx`, `TK-xxx`, `PR-xxx`).

---

## Snapshot

| Metric | Value |
|---|---:|
| Nodes | {graph["node_count"]} |
| Edges | {graph["edge_count"]} |
| Reciprocal pairs | {graph["summary"].get("reciprocal_pairs", 0)} |
| Average edge confidence | {graph["summary"].get("average_edge_confidence", 0.0)} |
| Intentional orphans | {len(graph["summary"]["intentional_orphans"])} |
| Candidate orphans | {len(graph["summary"]["orphan_candidates"])} |
| Hubs | {len(graph["summary"]["hubs"])} |

---

## Semantic Layer

The graph now distinguishes link syntax from relation meaning. `kind` records how the connection was found; `relation` records why the connection matters cognitively.

| Relation | Edges |
|---|---:|
{semantic_relation_rows}

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

## Cognitive Priority

This ranking combines severity with graph centrality, semantic reach, and downstream verification pressure so we can separate low-visibility doctrine from debt that sits on active navigation paths.

| ID | Title | Severity | Score | Why it matters |
|---|---|---|---:|---|
{chr(10).join(cognitive_priority_rows)}

---

## Depth Debt

Each entry is classified by depth: `deep` (ships bad/good examples and a detection recipe — a falsifiable vice), `doctrinal` (a behavioral/epistemic principle with no static signature; a stub by design, no code is fabricated for it), and `stub` (enrichable but not yet with examples — real debt).

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

## Intentional Orphan Review

This table questions whether a so-called intentional orphan is truly intentional or simply under-indexed.

| Node | Recommendation | Rationale |
|---|---|---|
{orphan_review_rows}

---

## Candidate Orphans

Pages within the live GS surface that receive no inbound links. If any is important, it should be linked from a main index or map.

| Node | Type | In | Out | Inbound | Outbound |
|---|---|---:|---:|---|---|
{orphan_rows}

---

## Bridges

Nodes that link to more than one page type. They are useful for navigating impact across domains.

| Node | Type | Reached types | Relations | Outbound |
|---|---|---|---|---:|
{chr(10).join(bridge_rows)}

---

## Cognitive Signals

- `Reciprocal pairs` estimates how much of the graph supports bidirectional navigation instead of one-way dumping.
- `Candidate orphans` point to live knowledge that exists but is not discoverable from a canonical entrypoint.
- `Relation` density shows whether GS is only linking pages or actually expressing reusable meaning.

---

## Quick Use

1. Open `[[Home]]` to enter the vault.
2. Open `[[Domains/README]]` if you want to traverse doctrine through canonical domains.
3. Open this map to see hubs, domain bridges, semantic relations, and graph priority surfaces.
4. Use the `golden_standard_graph.json` JSON if you want to automate impact analysis.

---
[[Home|Back to Home]]
"""
    GRAPH_MARKDOWN.write_text(graph_md, encoding="utf-8")
    print(f"Successfully generated Golden Standard graph at {GRAPH_OUTPUT} and {GRAPH_MARKDOWN}")




def write_evidence_pages(wiki_dir: Path, mapped_database: dict):
    """Create evidence citation nodes for every unique source in the catalog."""
    evidence_dir = wiki_dir / "Evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all evidence sources and their associated vices
    sources: dict[str, dict] = {}
    for flaw_id, item in mapped_database.items():
        evidence = item.get("evidence", [])
        if not isinstance(evidence, list):
            continue
        for ref in evidence:
            if not isinstance(ref, dict):
                continue
            source = str(ref.get("source", "")).strip()
            claim = str(ref.get("claim", "")).strip()
            if not source:
                continue
            if source not in sources:
                sources[source] = {"claims": set(), "vices": set()}
            if claim:
                sources[source]["claims"].add(claim)
            sources[source]["vices"].add(flaw_id)
    
    for source, data in sorted(sources.items()):
        slug = evidence_slug(source)
        claims = sorted(data["claims"])[:5]  # Top 5 claims
        vices = sorted(data["vices"])[:10]  # Top 10 vices
        vice_links = "\n".join(f"- [[Vices/{vid}|{vid}]]" for vid in vices)
        claim_lines = "\n".join(f"- {c}" for c in claims)
        
        content = f"""# {source}

> Citable evidence source referenced by {len(data["vices"])} entries in the Golden Standard catalog.

## Claims

{claim_lines}

## Referenced by

{vice_links}

---
[[Home|Back to Home]]
"""
        (evidence_dir / f"{slug}.md").write_text(content, encoding="utf-8")


def write_detector_pages(wiki_dir: Path, mapped_database: dict):
    """Create detector nodes for every vice with a registered static detector."""
    detectors_dir = wiki_dir / "Detectors"
    detectors_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all detectors and their associated vices
    detectors: dict[str, set[str]] = {}
    for flaw_id, item in mapped_database.items():
        detector = str(item.get("detector", "")).strip()
        if not detector:
            continue
        if detector not in detectors:
            detectors[detector] = set()
        detectors[detector].add(flaw_id)
    
    for detector, vices in sorted(detectors.items()):
        vice_links = "\n".join(f"- [[Vices/{vid}|{vid}]]" for vid in sorted(vices))
        content = f"""# {detector}

> Static detector registered in `scripts/detectors.py`. Tested in CI against the catalog's own `example_bad` / `example_good` corpus.

## Enforces

{vice_links}

---
[[Home|Back to Home]]
"""
        (detectors_dir / f"{detector}.md").write_text(content, encoding="utf-8")


def generate_obsidian_wiki(mapped_database: dict, wiki_dir: Path):
    """Generate a structured, cross-linked Obsidian vault from Compiled Golden Standard data."""
    clean_wiki_directory(wiki_dir)

    for folder in ["Domains", "Vices", "Tokenomics"]:
        (wiki_dir / folder).mkdir(parents=True, exist_ok=True)

    insights = get_principles()
    insight_records = load_project_insight_records()
    recommendations = get_canonical_domain_map()

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
    write_principles_index(wiki_dir, insight_records)
    write_domains_index_md(wiki_dir, recommendations)
    write_tokenomics_map_md(wiki_dir, insights)
    write_atomic_vices(wiki_dir, mapped_database)
    write_atomic_tokenomics(wiki_dir, mapped_database)
    write_audit_domains(wiki_dir, recommendations)
    write_evidence_pages(wiki_dir, mapped_database)
    write_detector_pages(wiki_dir, mapped_database)
    write_graph_artifacts(mapped_database)

    print(f"Successfully generated Obsidian Wiki Vault at {wiki_dir}")


def _display_mechanism(item: dict) -> str:
    """Prefer the concrete downstream mechanism for display when an entry has been
    migrated (enforcement.<consumer>.mechanism); otherwise fall back to the agnostic
    validating_mechanism value. Display-only; does not alter the stored raw field."""
    enforcement = item.get("enforcement")
    if isinstance(enforcement, dict):
        cerberus = enforcement.get("cerberus")
        if isinstance(cerberus, dict):
            mechanism = str(cerberus.get("mechanism", "")).strip()
            if mechanism:
                return mechanism
    return str(item.get("validating_mechanism", "")).strip()


def extract_catalog_items(config: dict, mapped_database: dict):
    """Parse catalog configuration dict and populate mapped flaws."""
    if not isinstance(config, dict) or "items" not in config:
        return
    # Skip non-vice catalogs handled separately
    if config.get("catalog_name") == "principles":
        return
    for item in config["items"]:
        flaw_id = item["id"]
        # Aliases removed; all entries are real

        downstream_verification = str(item.get("downstream_verification", "")).strip()
        if not downstream_verification:
            downstream_verification = "required" if str(item.get("status", "")).strip() == "DOC_ONLY" else "none"
        mapped_entry = {
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
            "detector": str(item.get("detector", "")).strip(),
            "tier": str(item.get("tier", "extended")).strip(),
        }
        # carry the enforcement binding through only when present, so migrated entries
        # expose enforcement downstream while legacy entries leave the JSON untouched.
        if isinstance(item.get("enforcement"), dict):
            mapped_entry["enforcement"] = item["enforcement"]
        mapped_database[flaw_id] = mapped_entry


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
                f"| `{item['id']}` | {item['title']} | **{item['severity']}** | **{item['status']}** | `{item.get('downstream_verification', 'none')}` | {action_snippet} | `{_display_mechanism(item)}` |"
            )
        report_lines.append("")

    report_lines.extend(build_principles_section())
    report_lines.extend(build_canonical_domains_section())

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
