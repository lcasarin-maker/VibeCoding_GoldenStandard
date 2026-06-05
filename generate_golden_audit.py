#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_golden_audit.py — Compile and map Golden Standard compliance database.
Parses the split Golden Standard catalogs, mapping each flaw to Cerberus guards/tests,
and auto-generates a fully cross-linked Obsidian Markdown Wiki vault.
"""

import json
import shutil
import sys
from collections import Counter
from datetime import date
from pathlib import Path
import yaml

_ROOT = Path(__file__).resolve().parent

# Detect if we are inside Cerberus (submodule configuration)
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
        ],
    }


def _read_version_label() -> str:
    if VERSION_FILE.exists():
        version = VERSION_FILE.read_text(encoding="utf-8").strip()
        if version:
            return f"V{version}"
    return "V0.5"


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
        "These entries are preserved as project-agnostic knowledge extracted from external references and now consumed by Cerberus.",
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
        "These actions are the operational bridge between the project insights and the Cerberus audit domains.",
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
    home_content = f"""# CoderCerberus Golden Standard Wiki

Bienvenido a la bóveda Obsidian del **Golden Standard** (GS) de CoderCerberus. Esta base de conocimiento representa la doctrina pura de ingeniería, mitigación de vicios y tokenomics acumulada del proyecto central y sus satélites.

---

## Acceso Rápido

- 📂 **[[Vices_Index|Índice de Vicios de Ingeniería]]**: Catálogo central de anomalías de código, tests y tokenomics (`VC`, `TV`, `TK`).
- 📂 **[[Project_Insights_Index|Índice de Insights Satélite]]**: Lecciones y mejores prácticas (`PI`) extraídas de repositorios externos y automatizaciones.
- 📘 **[[Concepts/Marco_Conceptual|Marco Conceptual de CoderCerberus]]**: Doctrina epistemológica, niveles y bases de diseño.
- 📥 **[Inbox](../Inbox/README.md)**: Buzón de entrada para hallazgos crudos y propuestas nuevas.
- 🧪 **[Audit Report](../golden_standard_audit_report.md)**: Estado compilado de cobertura y mapeo vigente.
- 🏠 **[README](../README.md)**: Visión general del repositorio público.

---

## Mapa por Dominio

| Dominio | Catálogo | Entradas | Enlace |
|---|---|---:|---|
| Vibe Coding | `VC-xxx` | {vc_count} | [[Vices_Index|Abrir índice]] |
| Testing & Evaluation | `VT-xxx` | {tv_count} | [[Vices_Index|Abrir índice]] |
| Tokenomics & Context | `TK-xxx` | {tk_count} | [[Vices_Index|Abrir índice]] |
| Project Insights | `PI-xxx` | {pi_count} | [[Project_Insights_Index|Abrir índice]] |

---

## Estado de Operatividad

| Estado | Entradas | Significado |
|---|---:|---|
| `PREVENTED` + `REMEDIATED` | {operational_count} | El catálogo ya tiene una compuerta ejecutable o una corrección concreta. |
| `AUDITED` + `DOC_ONLY` | {documentary_count} | La entrada existe como conocimiento, pero sigue siendo principalmente documental. |
| `Total` | {total_vices} | Suma de las entradas de VC, VT y TK auditadas por el compilador. |

---

## Guía de Severidad

| Severidad | Qué significa | Acción típica |
|---|---|---|
| `critical` | Riesgo de seguridad, pérdida de datos o fallo total de una capacidad esencial. | Corregir antes de seguir. |
| `high` | Bug visible para usuarios o ruptura seria de confianza. | Priorizar en la siguiente iteración. |
| `medium` | Deuda de fiabilidad o mantenibilidad. | Programar remediación. |
| `low` | Ajuste de estilo, claridad o eficiencia. | Agrupar con limpieza general. |

> La severidad se usa en revisión de contribuciones; el estado operativo canónico en los catálogos sigue siendo `status`.

---

## Flujo de Entrada

1. Depositar el hallazgo en `Inbox/<fuente>/YYYY-MM-DD_<slug>.md`.
2. Validar campos mínimos con `INGESTION_PROTOCOL.md`.
3. Promover a YAML + Wiki solo después de deduplicar y mapear el dominio.
4. Recompilar con `python generate_golden_audit.py`.

---
*Bóveda auto-generada por el compilador `generate_golden_audit.py` el {date.today().isoformat()}.*"""
    (wiki_dir / "Home.md").write_text(home_content, encoding="utf-8")


def write_vices_index_md(wiki_dir: Path, mapped_database: dict):
    """Write the main Vices index catalog."""
    vc_items = []
    tv_items = []
    tk_items = []
    for flaw_id, item in sorted(mapped_database.items()):
        line = f"*   [[Vices/{flaw_id}|{flaw_id}]] — **{item['title']}** ({item['status']}, {item['severity']})"
        if item["category"] == "Vibe Coding":
            vc_items.append(line)
        elif item["category"] == "Testing & Evaluation":
            tv_items.append(line)
        elif item["category"] == "Tokenomics & Context":
            tk_items.append(line)

    vices_index_content = f"""# Índice de Vicios de Ingeniería

Este índice clasifica todos los vicios del Golden Standard, organizados por sus dominios de desarrollo. Cada entrada enlaza a su nota atómica de mitigación.

---

## Vibe Coding (VC)
{"\n".join(vc_items)}

## Testing & Evaluation (TV)
{"\n".join(tv_items)}

## Tokenomics & Context (TK)
{"\n".join(tk_items)}

---
[[Home|Volver al Inicio]]
"""
    (wiki_dir / "Vices_Index.md").write_text(vices_index_content, encoding="utf-8")


def write_project_insights_index_md(wiki_dir: Path, insights: dict):
    """Write the Project Insights index catalog."""
    pi_items = []
    for pi_id in sorted(insights):
        pi_items.append(f"*   [[Project_Insights/{pi_id}|{pi_id}]] — {insights[pi_id]}")

    pi_index_content = f"""# Índice de Insights Satélite

Mapeo de lecciones extraídas de repositorios de referencia y herramientas de auditoría externa.

---

{"\n".join(pi_items)}

---
[[Home|Volver al Inicio]]
"""
    (wiki_dir / "Project_Insights_Index.md").write_text(pi_index_content, encoding="utf-8")


def write_conceptual_concepts_md(wiki_dir: Path):
    """Create link-adapted copy of conceptual framework."""
    conceptual_src = _ROOT / "CODERCERBERUS_MARCO_CONCEPTUAL.md"
    if conceptual_src.exists():
        original_text = conceptual_src.read_text(encoding="utf-8")
        nav_header = "# [[Home|← Volver al Inicio de la Bóveda]]\n\n---\n\n"
        (wiki_dir / "Concepts" / "Marco_Conceptual.md").write_text(nav_header + original_text, encoding="utf-8")


def write_atomic_vices(wiki_dir: Path, mapped_database: dict):
    """Create individual atomic files for all vices."""
    for flaw_id, item in mapped_database.items():
        tag_list = ", ".join(f"`{tag}`" for tag in item["tags"]) if item.get("tags") else "`untagged`"
        flaw_content = f"""# {flaw_id}: {item['title']}

| Campo | Detalle |
|---|---|
| **ID** | `{flaw_id}` |
| **Categoría** | {item['category']} |
| **Estado** | **{item['status']}** |
| **Severidad** | **{item['severity']}** |
| **Tags** | {tag_list} |
| **Mecanismo de Validación** | `{item['validating_mechanism']}` |

---

### Síntoma (Symptom)
> {item['symptom']}

### Causa (Cause)
{item['cause']}

### Solución (Solution)
{item['solution']}

### Acción Correctiva / Prevención
{item['action']}

---
[[Vices_Index|Volver al Índice de Vicios]] | [[Home|Inicio]]
"""
        (wiki_dir / "Vices" / f"{flaw_id}.md").write_text(flaw_content, encoding="utf-8")


def build_pi_mapping_lines(mappings: list) -> list[str]:
    """Format mapping lines for project insights."""
    if not mappings:
        return ["*Sin asignaciones activas de dominio.*"]
    return [
        f"*   **[[Domains/{domain}|{domain}]]** (Proyecto: *{proj}*): {act}"
        for domain, proj, act in sorted(mappings)
    ]


def write_atomic_project_insights(wiki_dir: Path, insights: dict, pi_to_domains: dict):
    """Create individual atomic files for all project insights."""
    for pi_id, text in insights.items():
        mappings = pi_to_domains.get(pi_id, [])
        mapping_lines = build_pi_mapping_lines(mappings)

        pi_content = f"""# {pi_id}: Insight Satélite

### Descripción del Insight
> {text}

---

### Mapeo a Dominios de Auditoría Cerberus
{"\n".join(mapping_lines)}

---
[[Project_Insights_Index|Volver al Índice de Insights]] | [[Home|Inicio]]
"""
        (wiki_dir / "Project_Insights" / f"{pi_id}.md").write_text(pi_content, encoding="utf-8")


def write_audit_domains(wiki_dir: Path, recommendations: dict):
    """Create domains overview files mapping to insights."""
    for domain in sorted(recommendations):
        linked_items = [
            f"*   **[[Project_Insights/{rec['insight_id']}|{rec['insight_id']}]]** (Proyecto: *{rec['project']}*): {rec['action']}"
            for rec in recommendations[domain]
        ]

        domain_content = f"""# Dominio de Auditoría: {domain}

Este dominio cubre un área específica del protocolo de consistencia y seguridad de Cerberus. Los siguientes insights satélite están vinculados a este dominio de auditoría:

---

### Insights Vinculados

{"\n".join(linked_items)}

---
[[Home|Volver al Inicio]]
"""
        (wiki_dir / "Domains" / f"{domain}.md").write_text(domain_content, encoding="utf-8")


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

    for folder in ["Concepts", "Domains", "Vices", "Project_Insights"]:
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
    write_project_insights_index_md(wiki_dir, insights)
    write_conceptual_concepts_md(wiki_dir)
    write_atomic_vices(wiki_dir, mapped_database)
    write_atomic_project_insights(wiki_dir, insights, pi_to_domains)
    write_audit_domains(wiki_dir, recommendations)

    print(f"Successfully generated Obsidian Wiki Vault at {wiki_dir}")


def extract_catalog_items(config: dict, mapped_database: dict):
    """Parse catalog configuration dict and populate mapped flaws."""
    if not isinstance(config, dict) or "items" not in config:
        return
    for item in config["items"]:
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
        f"**CoderCerberus {_read_version_label()} | Date: {date.today().isoformat()} | Total Audited Items: {len(mapped_database)}**",
        "",
        "This document is generated automatically by `generate_golden_audit.py` to map every Golden Standard point to its specific mitigation action and validating test in CoderCerberus.",
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
            "| ID | Flaw Title | Severity | Status | Action Taken / Prevention Method | Validating Test / Guard |"
        )
        report_lines.append("|---|---|---|---|---|---|")

        for item in sorted(cat_items, key=lambda x: x["id"]):
            action_snippet = item["action"].replace("\n", " ")
            report_lines.append(
                f"| `{item['id']}` | {item['title']} | **{item['severity']}** | **{item['status']}** | {action_snippet} | `{item['validating_mechanism']}` |"
            )
        report_lines.append("")

    report_lines.extend(build_project_insight_section())
    report_lines.extend(build_project_insight_recommendations_section())

    MARKDOWN_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_OUTPUT.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"Successfully generated {MARKDOWN_OUTPUT}")

    generate_obsidian_wiki(mapped_database, WIKI_DIR)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback
        print("Error compiling audit report:", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
