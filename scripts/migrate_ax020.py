#!/usr/bin/env python3
"""AX-020 schema migrator (option 2, strict-only-migrated).

Rewrites, per catalog entry, the agent-agnostic ``validating_mechanism`` type and
(where a real Cerberus mechanism enforces the vice) the optional
``enforcement.cerberus.{dimension, mechanism}`` binding, plus an agnostic ``action``
that names a principle/signature instead of a Cerberus dimension or function.

The migration is data-driven: TABLES below are the reviewable migration spec. Each
target entry is rewritten with an exact, fail-loud regex replacement scoped to that
entry's block; a missing entry or a non-unique match aborts the whole run (no silent
skips, no partial writes). The output file is written atomically (temp + os.replace).

Usage:  python scripts/migrate_ax020.py <coding_vices|testing_vices|tokenomics>
"""

from __future__ import annotations

import os
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATALOG_FILES = {
    "coding_vices": "golden_standard_coding_vices.yaml",
    "testing_vices": "golden_standard_testing_vices.yaml",
    "tokenomics": "golden_standard_tokenomics.yaml",
}


# Each value: (action, mechanism_type, dimension|None, mechanism|None).
# dimension/mechanism are set ONLY for entries enforced by a real Cerberus mechanism.
CODING_VICES = {
    # --- Cerberus runtime tests (pytest) ---
    "VC-003": ("Empirical proof is required before declaring success: closure fails when no structured evidence artifact backs the claim, forcing verification over optimism.", "runtime-test", "D5", "test_B7_evidence_files_are_valid_json"),
    "VC-017": ("Empirical proof is required before declaring success: closure fails when no structured evidence artifact backs the claim, forcing verification over optimism.", "runtime-test", "D5", "test_B7_evidence_files_are_valid_json"),
    "VC-062": ("State must stay consistent across concurrent sessions: a parity check fails when the protocol fingerprint diverges between two sessions.", "runtime-test", "D12", "test_F6_sync_binding_no_protocol_drift"),
    "VC-082": ("Every imported dependency must be declared in the manifest: a check fails when code imports a package that the dependency manifest does not list.", "runtime-test", "D11", "test_vc082_ghost_import_detected"),
    "VC-109": ("Filesystem paths must be portable: a scan fails when a hardcoded absolute path (drive letter or home directory) appears in scripts.", "runtime-test", "D6", "test_vc109_absolute_path_in_scripts"),
    "VC-115": ("Rules must not evaluate arbitrary expressions: dynamic execution of external strings is rejected in favor of a pre-registered dispatch of safe checks, closing a remote-code-execution path.", "runtime-test", "D7", "test_rule_security_rejects_arbitrary_check"),
    "VC-116": ("Dependency installation must never be automatic: an import-time guard must not trigger package installation; missing packages are surfaced for manual decision.", "runtime-test", "D11", "test_import_error_guard_does_not_pip_install"),
    "VC-117": ("Writes to critical state must be atomic: state is persisted via a temp-file-plus-atomic-replace path so a crash cannot leave a half-written, corrupted file.", "runtime-test", "D1", "test_critical_state_write_is_atomic"),
    "VC-121": ("Top-level function names must be unique across modules: a structural comparison fails when the same definition name is duplicated, surfacing redundant slop.", "runtime-test", "D3", "test_vc121_duplicate_function_names"),
    "VC-122": ("Scripts must not install packages at runtime: an automatic package install inside a script is blocked to prevent silent supply-chain contamination.", "runtime-test", "D11", "test_vc122_no_pip_install_in_scripts"),
    "VC-123": ("Staging must be deliberate: indiscriminate staging of all untracked files is rejected, requiring explicit human intent about what enters a commit.", "runtime-test", "D1", "test_vc123_no_git_add_all_in_scripts"),
    "VC-129": ("Declared dependencies must exist in the public registry: a lookup fails when a requirement resolves to not-found, catching hallucinated (slopsquatted) packages.", "runtime-test", "D11", "test_pypi_404_is_alucinated_dependency"),
    "VC-152": ("Edit the canonical source or its generator first: hand-patching a derived artifact to mask drift is rejected; derived files must be regenerated from source.", "runtime-test", "D1", "test_canonical_source_first_no_sink_patch"),
    "VC-153": ("Doctrine lands before enforcement: the rule must exist in the canonical knowledge base first, with downstream consumers following only after regeneration proves it.", "runtime-test", "D12", "test_doctrine_before_enforcement_resolves_refs"),
    "VC-154": ("Doctrine lands before enforcement: the rule must exist in the canonical knowledge base first, with downstream consumers following only after regeneration proves it.", "runtime-test", "D12", "test_doctrine_before_enforcement_resolves_refs"),
    # --- Cerberus static AST audits ---
    "VC-092": ("An audit may only be reported as total when its mandatory phases ran: completeness analysis fails when required prior-phase evidence is absent, so a partial pass cannot be called total.", "static-ast", "D2", "audit_d2_completeness"),
    "VC-118": ("A replacement is a single source of truth: the superseded unit is deleted and the new one carries no inheritance, shim, fallback, or dual test sentinel back to it; static analysis flags compatibility forwarders left in active code.", "static-ast", "D1", "D1Integrity"),
    "VC-142": ("Agent instructions must be tamper-resistant: static analysis flags directives that attempt to override or hijack the agent's governing prompt.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-143": ("The system prompt must not leak: static analysis flags triggers that would exfiltrate or echo the governing prompt into output.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-144": ("Data must not be exfiltrated: static analysis flags network patterns that would send protected data to unauthorized destinations.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-145": ("Privileges must not silently escalate: static analysis flags indicators of unauthorized privilege escalation.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-146": ("Agency must stay bounded: static analysis requires confirmation gates around high-impact actions, rejecting excessive autonomous reach.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-147": ("Persistent memory must not be poisoned: static analysis requires sanitization of memory write operations.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-148": ("Tool calls must be constrained: static analysis enforces parameter limits and rejects unsafe tool chaining.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-149": ("Agents must not establish unauthorized persistence: static analysis flags persistence indicators of rogue behavior.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-150": ("Tool access must follow least privilege: static analysis maps declared capabilities to the manifest and flags over-broad grants.", "static-ast", "D15", "D15AgentSecurity"),
    "VC-151": ("Tool descriptions must be trustworthy: static analysis scans for unicode homoglyphs and poisoned tool-description content.", "static-ast", "D15", "D15AgentSecurity"),
    # --- Cerberus runtime guards (hooks/scripts) ---
    "VC-124": ("Deprecation requires prior analysis: moving code into a deprecated area is blocked unless a justifying log entry exists, and coverage of that log is verified.", "runtime-test", "D1", "check_deprecation_log"),
    "VC-140": ("Handoff continuity is mandatory: a commit with substantive changes is blocked when the handoff record was not updated or is missing its required sections; an explicit token allows a conscious skip.", "runtime-test", "D1", "check_handoff_freshness"),
    "VC-141": ("No orphan changes: a commit is blocked when, after staging, the working tree still holds undecided modified or untracked files; idempotent writes and a canonical auto-stage whitelist neutralize artifact churn, and an explicit env escape exists.", "runtime-test", "D1", "check_clean_worktree"),
    # --- Golden Standard self-validation (no Cerberus binding) ---
    "VC-021": ("Closure is all-or-nothing: the catalog validator keeps canonical surfaces, link graph, and coverage counts aligned, so a partial close fails the gate.", "runtime-test", None, None),
    "VC-027": ("The plan must be externalized: topology validation requires the inbox surface to be published, linked from the home page, and backed by an ingestion protocol and templates.", "runtime-test", None, None),
    "VC-030": ("Generated surfaces must track their source: regenerating audit artifacts and re-checking topology prevents home, graph, and index pages from drifting away from the catalogs.", "runtime-test", None, None),
    "VC-037": ("Regeneration must precede validation: a fresh rebuild of the vault is forced before checks, so blind replacement cannot masquerade as a finished state.", "runtime-test", None, None),
    "VC-048": ("Knowledge must be modular: topology validation requires separate canonical surfaces for vices, tokenomics, insights, and the graph rather than one monolithic page.", "runtime-test", None, None),
    "VC-063": ("Documentation must not lie: link-integrity and count-parity validation fail when docs drift away from the generated state.", "runtime-test", None, None),
    "VC-069": ("Dependencies must be mapped: the graph and link validator require canonical surfaces to be linked and resolvable rather than assumed.", "runtime-test", None, None),
    "VC-090": ("Memory must be loadable on entry: topology validation requires the canonical memory surfaces to be linked from the home page.", "runtime-test", None, None),
    "VC-091": ("Missing files must fail loud: broken-link validation fails when a referenced markdown or wiki target does not resolve on disk.", "runtime-test", None, None),
    "VC-104": ("Infrastructure is a first-class surface: the audit workflow is a visible, validated file that must run both the generator and the catalog validator, so infra cannot be silently ignored.", "runtime-test", None, None),
    "VC-105": ("Components must be complete: topology validation checks the canonical home, vices, tokenomics, graph, and inbox surfaces, so a missing component fails the gate.", "runtime-test", None, None),
    "VC-106": ("Setup must be real, not phantom: inbox topology validation requires the ingestion protocol, knowledge-sources contract, and templates to exist before new findings are accepted.", "runtime-test", None, None),
    "VC-110": ("Quotas must be visible up front: topology validation requires the tokenomics index to expose its subindices and map before the category is treated as complete.", "runtime-test", None, None),
    "VC-114": ("Findings need a remediation path: inbox topology validation enforces the ingestion path, templates, and protocol docs required to act on a finding.", "runtime-test", None, None),
    "VC-125": ("Lessons must be externalized before closure: regeneration plus coverage and retrospective-export checks require every new lesson to reach the catalog or wiki, so closure without a structured export stays incomplete.", "runtime-test", None, None),
    # --- Downstream/local static detector (not yet a Cerberus dimension) ---
    "VC-138": ("Generated code must be secure by default: a static-signature detector, exercised against the catalog examples, flags insecure default patterns.", "static-regex", None, None),
    # --- Doctrinal principles (no executable binding) ---
    "VC-067": ("Policies must be explicit, not implicit: governing rules are declared in the canonical rule set rather than left to convention.", "doctrinal", None, None),
    "VC-108": ("Security boundaries must be enforced by gates, not convention: a boundary asserted only in prose, without an executable gate behind it, is not a boundary.", "doctrinal", None, None),
}

TABLES = {
    "coding_vices": CODING_VICES,
}

# Capture the action field plus the FULL validating_mechanism value (which may fold
# across continuation lines), stopping at the next 4-space-indented field (lookahead).
ACTION_VM_RE = re.compile(
    r"^[ ]{4}action:.*?\n[ ]{4}validating_mechanism:.*?\n(?=[ ]{4}\w)",
    re.S | re.M,
)


def build_block(action: str, vm: str, dim: str | None, mech: str | None) -> str:
    block = "    action: |\n"
    block += f"      {action}\n"
    block += f"    validating_mechanism: {vm}\n"
    if dim and mech:
        block += "    enforcement:\n"
        block += "      cerberus:\n"
        block += f"        dimension: {dim}\n"
        block += f"        mechanism: {mech}\n"
    return block


def split_entries(text: str) -> list[tuple[str, int, int]]:
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if line.startswith("  - id: ")]
    bounds = []
    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)
        entry_id = lines[start][len("  - id: "):].strip()
        bounds.append((entry_id, start, end))
    return bounds


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in CATALOG_FILES:
        print(f"usage: {sys.argv[0]} <{'|'.join(CATALOG_FILES)}>", file=sys.stderr)
        return 2
    catalog = sys.argv[1]
    table = TABLES.get(catalog)
    if not table:
        print(f"ERROR: no migration table defined for {catalog}.", file=sys.stderr)
        return 2

    path = ROOT / CATALOG_FILES[catalog]
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    bounds = {eid: (s, e) for eid, s, e in split_entries(text)}

    missing = [eid for eid in table if eid not in bounds]
    if missing:
        print(f"ERROR: ids not found in {catalog}: {', '.join(sorted(missing))}", file=sys.stderr)
        return 1

    out_lines = list(lines)
    applied = 0
    for entry_id, spec in table.items():
        start, end = bounds[entry_id]
        block_text = "\n".join(lines[start:end]) + "\n"
        new_block, nsubs = ACTION_VM_RE.subn(build_block(*spec), block_text, count=1)
        if nsubs != 1:
            print(f"ERROR: {entry_id}: expected 1 action/validating_mechanism match, got {nsubs}.", file=sys.stderr)
            return 1
        replacement = new_block.rstrip("\n").split("\n")
        out_lines[start:end] = replacement
        # recompute bounds shift: rebuild after each edit to keep indices correct
        rebuilt = "\n".join(out_lines)
        bounds = {eid: (s, e) for eid, s, e in split_entries(rebuilt)}
        lines = rebuilt.split("\n")
        out_lines = list(lines)
        applied += 1

    new_text = "\n".join(out_lines)
    fd, tmp = tempfile.mkstemp(dir=str(ROOT), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(new_text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise

    print(f"AX-020: migrated {applied} entries in {catalog}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
