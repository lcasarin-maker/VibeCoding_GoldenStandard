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

TESTING_VICES = {
    "VT-001": ("A test must assert general properties, not a single hardcoded return value that the implementation can trivially satisfy.", "static-ast", "D2", "audit_d2_completeness"),
    "VT-002": ("A placeholder body on an active path is not an implementation: completeness analysis rejects fake bodies that pass without doing the work.", "static-ast", "D2", "audit_d2_completeness"),
    "VT-003": ("A test must generalize beyond the one input it was written for; an assertion that only holds for a single hardcoded datum proves nothing.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-004": ("The expected value must come from an independent specification, not be copied into the production path or fixture where it stops being an independent observation.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-005": ("An assertion must be able to fail: a check that is always true is rejected as non-discriminating.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-006": ("A test that runs without any assertion verifies nothing; at least one discriminating assertion is mandatory.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-007": ("Asserting that a file or artifact merely exists is not a test; validate its effect or content.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-008": ("Validate the final state, not the presence of an approval message; matching success text is not verifying the outcome.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-009": ("A test must discriminate the subject's behavior, not restate a universal truth that holds regardless of the code.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-010": ("Test observable behavior, not internal implementation detail, so a behavior-preserving refactor keeps the test meaningful.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-011": ("The expected value (oracle) must track the current specification; an assertion compared against a stale expectation is invalid.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-012": ("Coverage means executed-and-verified: lines run without an oracle assertion do not constitute coverage.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-013": ("Coverage percentage is not a goal; what matters is the discriminating quality of the assertions, not a gamed number.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-014": ("A test must be judged against an external oracle, never approve itself in a circular loop.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-015": ("A test should localize the failure it detects; an over-broad test that cannot point to the cause has little diagnostic value.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-016": ("Invoke the real behavior the mandate requires; asserting that some text exists is ceremony.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-017": ("The recorded outcome must be derived from an actual verification, not a hardcoded success.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-018": ("Validate structured state, not free-text messages whose wording can silently flip the result.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-019": ("An error must surface as an explicit failure, not be encoded into data that looks valid.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-020": ("One hundred percent coverage is a consequence of good tests, never the goal; treating it as the target invites gaming.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-021": ("Every fixed defect must leave behind a discriminating regression test so the same error cannot silently reappear.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-022": ("Require boundary-value assertions and forbid broad catches that silence failures, so a green run cannot be ceremonial.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-023": ("A mock that always simulates success must be calibrated against a real integration, or it only tests itself.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-024": ("A fake that omits the hard cases gives false assurance; exercise the real system for those paths.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-025": ("A network stub drifts from reality; pin behavior with a live contract test.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-026": ("Test against an engine equivalent to production; a simplified database whose rules differ hides real failures.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-027": ("Exercise temporal boundaries; a permanently fixed clock never reveals date-edge failures.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-028": ("Assert statistical properties over the real distribution; fully controlled randomness explores nothing.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-029": ("Use a real resource for permission- and lock-sensitive paths that a fake filesystem cannot reproduce.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-030": ("Limit patching to the boundary; over-patching replaces the system under test with the test's own assumptions.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-031": ("Verify the external effect of a command, not a stub that merely prints success.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-032": ("Scan the full active domain; a partial mock-detection pass leaves untested code unguarded.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-033": ("Fix the cause in the subject under test; adding a layer so the judge stops failing adapts the judge, not the defect.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-034": ("Require observable behavior before approval; an evaluator that accepts an incomplete structure rubber-stamps a placeholder.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-035": ("An expected-failure marker is not evidence of health; a permanent xfail hides an ignored failure.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-036": ("A permanently skipped critical test invalidates the global result; skipping must not silently omit it.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-037": ("Verify that the test's branch actually executes; a condition that is never entered tests nothing.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-038": ("Tests must be independent; one that passes only because of another's leftover state is unreliable.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-039": ("Control time explicitly; a test whose result depends on the wall-clock hour or day is non-deterministic.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-040": ("An exception must surface, not be absorbed; swallowing it makes the failure disappear.", "static-ast", "D5", "audit_d5_angry_path"),
    "VT-041": ("Capture and observe error output; an unobserved error stream hides the failure signal.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-042": ("Log success only after the verification that justifies it, never before checking.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-043": ("The exit code must reflect the real state; an unconditional success exit produces a falsely green pipeline.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-044": ("Assert the return value; an ignored error result lets a failure pass unseen.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-045": ("Cover adverse cases, not just the ideal happy path.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-046": ("Generate input variations; a single magic datum chosen to avoid the bug never triggers it.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-047": ("Exercise realistic volume; a test on a tiny dataset misses failures that only appear at scale.", "runtime-test", "D10", "test_compress_1000_sessions_returns_structured_dict"),
    "VT-048": ("Cover empty, null, and zero boundary values, not only populated inputs.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-049": ("Include special characters and diverse real-world data that naive inputs never exercise.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-050": ("Cover calendar boundaries such as leap days and month/year edges; ideal dates hide date-arithmetic bugs.", "runtime-test", "D8", "test_non_leap_year_feb29_raises"),
    "VT-051": ("Critical CI failures must block; an informational-only pipeline lets failures through.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-052": ("Propagate errors strictly through the pipeline rather than ignoring them.", "static-ast", "D5", "audit_d5_angry_path"),
    "VT-053": ("Tests must run on the active path; tests living outside it never protect anything.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-054": ("Make risk-bearing tests mandatory; optional tests are not run and give no protection.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-055": ("A failure alert needs an owner; an unattended notification makes the failure invisible.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-056": ("Write a failing test before fixing the bug; a post-bug test that passes while the code is broken proves nothing.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-057": ("A deferred skip needs a hard deadline; an open-ended skip becomes permanent debt.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-058": ("Test the real feature-flag configuration; testing a divergent flag state hides production behavior.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-059": ("Run with a configuration equivalent to production; an environment variable that disables checks weakens the test.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-060": ("Test from a realistic, dirty state; over-cleaning setup creates conditions production never sees.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-061": ("Validate critical UI flows directly, not only visual deltas that miss functional breakage.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-062": ("Validate that code actually executes; a complete-but-dead file passes structural checks while doing nothing.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-063": ("Test the real public interface; documenting a flag the code does not support is a lie the tests must catch.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-064": ("Run the full active suite so an import error that silently disables tests is surfaced.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-065": ("Isolate each test's side effects so one cannot break the runner or other tests.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-066": ("Reconcile the test inventory so orphan files that are never discovered or run are surfaced.", "runtime-test", "D8", "test_infrastructure_checks"),
    "VT-067": ("Detect forwarding wrappers by structural analysis; a docstring must not mask a shim.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-068": ("Classify artifacts by type so backups are not miscounted as deprecated noise that contaminates the audit.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-069": ("A name must match behavior; a function whose name promises work its body never does is misleading.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-070": ("Validate that the real environment can start - runtime, dependencies, and minimum permissions - not just that the test passes.", "runtime-test", "D8", "test_setup_validation"),
    "VT-071": ("Test continuity from another actor's checkpoint; a handoff that cannot be resumed is broken.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-072": ("Verify the real reversal of a destructive change; a documented-but-unexecuted rollback is unproven.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-073": ("Maintain a suite of current consumers so a change that breaks an existing flow is caught.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-074": ("Test that a failure produces actionable diagnostic evidence, not silence.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-075": ("Audit the physical correspondence between test files on disk and tests actually discovered, so a green suite cannot hide inactive ones.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-076": ("Run across an environment matrix; a test that only works in one environment is not portable.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-077": ("Assert functional limits, not just a generous timeout under which slowness passes.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-078": ("Tests must be reproducible off one developer's machine, independent of a local installation.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-079": ("Test isolation by attempting controlled boundary violations, not by merely declaring the sandbox secure.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-080": ("Parametrize resources via injection or logical variables so tests do not couple to a physical address and break on migration.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-081": ("Tests benefit from independent review; an author validating only their own mental model confirms bias.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-082": ("Review the tests as part of the change; approving code without reviewing its tests is blind.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-083": ("Derive expected values from an independent specification, not an answer written so the test passes.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-084": ("Base approval on reproducible evidence, not a manually-set approved state treated as truth.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-085": ("Regenerate a golden snapshot only after semantic review; a stale golden legitimizes broken output.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-086": ("An expected failure must not count as green; normalizing it makes the failure permanent.", "static-ast", "D9", "audit_d9_test_purity"),
    "VT-087": ("Escalate a warning to a failure until its cause is resolved; a green suite carrying warnings tolerates rot.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-088": ("A health verdict accepts zero known errors; tolerating one normalizes it.", "static-ast", "D5", "audit_d5_angry_path"),
    "VT-089": ("Test the real interface with no simplifying wrapper that hides the real failure.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-090": ("Block placeholders on verified paths; a placeholder that satisfies the assertion fakes completion.", "static-ast", "D2", "audit_d2_completeness"),
    "VT-091": ("Every documented domain must have a live executor; a rule that exists but never runs is inert.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-092": ("Validate content and effect, not the mere presence of a section heading.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-093": ("Cross-check usage, calls, and tests; docstrings are not evidence of quality.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-094": ("Induce a real error to prove handling; matching a lexical keyword is not error handling.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-095": ("Run the suite of the audited subject; testing the protocol instead lets an untested project pass.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-096": ("Bind evidence to the version under test; a stale artifact must not satisfy a current check.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-097": ("Exercise the real components of the system, not an external library standing in for them.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-098": ("Report the domains actually exercised; a pass report claiming all while running few is a lie.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-099": ("Keep a single source of version truth; a dead fallback constant drifts from reality.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-100": ("Validate both positive and negative permission cases, not only the permitted actor.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-101": ("Test routing decisions with edge cases so tasks cannot silently reach the wrong flow.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-102": ("Every approval must revalidate active properties; accepting by name from a hardcoded list skips the behavior check.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-103": ("Separate generator, subject, and judge; an evaluator that already knows the expected answer cannot judge.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-104": ("Warnings count as failures until explicitly classified; leaving them outside the score hides risk.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-105": ("Parse the workflow and assert its validator and regenerator steps remain wired, so a pipeline cannot silently lose its verification.", "runtime-test", "D8", "test_audit_workflow_runs_validator_and_regenerator"),
    "VT-106": ("Periodically revalidate each exclusion so the ignore list cannot accumulate stale, unjustified entries.", "runtime-test", "D8", "test_setup_validation"),
    "VT-107": ("Validate the full active stack at startup - runtime, CLI tools, hooks, essential files, write permissions - and report exactly what is missing.", "runtime-test", "D8", "test_setup_validation"),
    "VT-108": ("Compare the formal declaration (name, domain count, version) against the real implementation and fail when they diverge.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-109": ("A simple static or structural validation should run directly and natively; wrapping it in a heavy test framework is middleman theater.", "runtime-test", "D8", "test_infrastructure_checks"),
    "VT-110": ("Consolidate governance and state metadata under a single hidden directory rather than scattering it across many.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-111": ("Every deferred classification must immediately open a debt-registry entry; a verbal deferral with no record loses the finding.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-112": ("A static gate must compare every top-level import against the dependency manifest so an unregistered dependency cannot drift in.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-113": ("A suite must empirically demonstrate it can fail against a controlled mutation; tests that stay green under any change are not falsifiable.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-114": ("A drift gate must compare checksums across satellite repositories and block when governance files diverge from the central core.", "static-ast", "D8", "audit_d8_test_coverage"),
    "VT-115": ("Normalize line endings to a single form before hashing so files identical on disk do not raise a false drift positive across platforms.", "runtime-test", "D8", "test_setup_validation"),
    "VT-116": ("Resolve symbols structurally through the AST so only a real definition node counts; a commented-out or string mention must not satisfy the check.", "runtime-test", "D8", "test_planted_def_comment_does_not_resolve"),
}

TABLES = {
    "coding_vices": CODING_VICES,
    "testing_vices": TESTING_VICES,
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
