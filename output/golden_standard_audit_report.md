# Golden Standard Compliance Audit Report
**Golden Standard V0.6 | Date: 2026-06-30 | Total Audited Items: 355**

This document is generated automatically by `scripts/generate_golden_audit.py` to map every Golden Standard point to its specific mitigation action and validating test in the GS tooling ecosystem.

## Summary of Compliance

| Category | Audited Items | Prevented / Remediated | Audited / Not Applicable | Clean Status |
|---|---|---|---|---|
| **Testing & Evaluation** | 116 | 28 | 88 | 100% |
| **Vibe Coding** | 91 | 68 | 23 | 100% |
| **Tokenomics & Context** | 34 | 33 | 1 | 100% |
| **Total** | 355 | 136 | 219 | 100% |

---

## Full Audit Details

### Testing & Evaluation (116 items)

| ID | Flaw Title | Severity | Status | Downstream Verification | Action Taken / Prevention Method | Validating Test / Guard |
|---|---|---|---|---|---|---|
| `VT-001` | Hardcoded return | **high** | **PREVENTED** | `none` | A test must assert general properties, not a single hardcoded return value that the implementation can trivially satisfy.  | `audit_d2_completeness` |
| `VT-002` | Permanent stub | **high** | **PREVENTED** | `none` | A placeholder body on an active path is not an implementation: completeness analysis rejects fake bodies that pass without doing the work.  | `audit_d2_completeness` |
| `VT-003` | Response by exact datum | **medium** | **AUDITED** | `none` | A test must generalize beyond the one input it was written for; an assertion that only holds for a single hardcoded datum proves nothing.  | `audit_d8_test_coverage` |
| `VT-004` | Copying the expected value | **medium** | **AUDITED** | `none` | The expected value must come from an independent specification, not be copied into the production path or fixture where it stops being an independent observation.  | `audit_d8_test_coverage` |
| `VT-005` | Trivial assert | **high** | **PREVENTED** | `none` | An assertion must be able to fail: a check that is always true is rejected as non-discriminating.  | `audit_d9_test_purity` |
| `VT-006` | Test without assert | **high** | **PREVENTED** | `none` | A test that runs without any assertion verifies nothing; at least one discriminating assertion is mandatory.  | `audit_d9_test_purity` |
| `VT-007` | Presence not correctness | **medium** | **AUDITED** | `none` | Asserting that a file or artifact merely exists is not a test; validate its effect or content.  | `audit_d8_test_coverage` |
| `VT-008` | Message not result | **medium** | **AUDITED** | `none` | Validate the final state, not the presence of an approval message; matching success text is not verifying the outcome.  | `audit_d8_test_coverage` |
| `VT-009` | Tautology | **high** | **PREVENTED** | `none` | A test must discriminate the subject's behavior, not restate a universal truth that holds regardless of the code.  | `audit_d9_test_purity` |
| `VT-010` | Implementation test | **medium** | **AUDITED** | `none` | Test observable behavior, not internal implementation detail, so a behavior-preserving refactor keeps the test meaningful.  | `audit_d8_test_coverage` |
| `VT-011` | Incorrect expected value | **medium** | **AUDITED** | `none` | The expected value (oracle) must track the current specification; an assertion compared against a stale expectation is invalid.  | `audit_d8_test_coverage` |
| `VT-012` | Coverage without asserts | **high** | **PREVENTED** | `none` | Coverage means executed-and-verified: lines run without an oracle assertion do not constitute coverage.  | `audit_d9_test_purity` |
| `VT-013` | Tests for percentage | **high** | **PREVENTED** | `none` | Coverage percentage is not a goal; what matters is the discriminating quality of the assertions, not a gamed number.  | `audit_d9_test_purity` |
| `VT-014` | Circular test | **medium** | **AUDITED** | `none` | A test must be judged against an external oracle, never approve itself in a circular loop.  | `audit_d8_test_coverage` |
| `VT-015` | Test too broad | **medium** | **AUDITED** | `none` | A test should localize the failure it detects; an over-broad test that cannot point to the cause has little diagnostic value.  | `audit_d8_test_coverage` |
| `VT-016` | Ceremonial textual assertion | **high** | **PREVENTED** | `none` | Invoke the real behavior the mandate requires; asserting that some text exists is ceremony.  | `audit_d9_test_purity` |
| `VT-017` | Hardcoded evidence | **medium** | **AUDITED** | `none` | The recorded outcome must be derived from an actual verification, not a hardcoded success.  | `audit_d8_test_coverage` |
| `VT-018` | Fragile string matching | **medium** | **AUDITED** | `none` | Validate structured state, not free-text messages whose wording can silently flip the result.  | `audit_d8_test_coverage` |
| `VT-019` | Valid error hash | **medium** | **AUDITED** | `none` | An error must surface as an explicit failure, not be encoded into data that looks valid.  | `audit_d8_test_coverage` |
| `VT-020` | One hundred percent as the goal | **medium** | **AUDITED** | `none` | One hundred percent coverage is a consequence of good tests, never the goal; treating it as the target invites gaming.  | `audit_d8_test_coverage` |
| `VT-021` | Regression without a sentinel | **medium** | **AUDITED** | `none` | Every fixed defect must leave behind a discriminating regression test so the same error cannot silently reappear.  | `audit_d8_test_coverage` |
| `VT-022` | Green ceremony and Tautological Assertions | **high** | **PREVENTED** | `none` | Require boundary-value assertions and forbid broad catches that silence failures, so a green run cannot be ceremonial.  | `audit_d9_test_purity` |
| `VT-023` | Complacent mock | **medium** | **AUDITED** | `none` | A mock that always simulates success must be calibrated against a real integration, or it only tests itself.  | `audit_d8_test_coverage` |
| `VT-024` | Incomplete fake | **medium** | **AUDITED** | `none` | A fake that omits the hard cases gives false assurance; exercise the real system for those paths.  | `audit_d8_test_coverage` |
| `VT-025` | Network stub | **medium** | **AUDITED** | `none` | A network stub drifts from reality; pin behavior with a live contract test.  | `audit_d8_test_coverage` |
| `VT-026` | Simplified database | **medium** | **AUDITED** | `none` | Test against an engine equivalent to production; a simplified database whose rules differ hides real failures.  | `audit_d8_test_coverage` |
| `VT-027` | Fixed clock | **medium** | **AUDITED** | `none` | Exercise temporal boundaries; a permanently fixed clock never reveals date-edge failures.  | `audit_d8_test_coverage` |
| `VT-028` | Controlled randomness | **medium** | **AUDITED** | `none` | Assert statistical properties over the real distribution; fully controlled randomness explores nothing.  | `audit_d8_test_coverage` |
| `VT-029` | Fake filesystem | **medium** | **AUDITED** | `none` | Use a real resource for permission- and lock-sensitive paths that a fake filesystem cannot reproduce.  | `audit_d8_test_coverage` |
| `VT-030` | Friendly monkey patch | **medium** | **AUDITED** | `none` | Limit patching to the boundary; over-patching replaces the system under test with the test's own assumptions.  | `audit_d8_test_coverage` |
| `VT-031` | Command stub | **medium** | **AUDITED** | `none` | Verify the external effect of a command, not a stub that merely prints success.  | `audit_d8_test_coverage` |
| `VT-032` | Partial mock scan | **medium** | **AUDITED** | `none` | Scan the full active domain; a partial mock-detection pass leaves untested code unguarded.  | `audit_d8_test_coverage` |
| `VT-033` | Wrapper as remediation | **medium** | **AUDITED** | `none` | Fix the cause in the subject under test; adding a layer so the judge stops failing adapts the judge, not the defect.  | `audit_d8_test_coverage` |
| `VT-034` | Approved placeholder | **medium** | **AUDITED** | `none` | Require observable behavior before approval; an evaluator that accepts an incomplete structure rubber-stamps a placeholder.  | `audit_d8_test_coverage` |
| `VT-035` | Permanent xfail | **high** | **PREVENTED** | `none` | An expected-failure marker is not evidence of health; a permanent xfail hides an ignored failure.  | `audit_d9_test_purity` |
| `VT-036` | Permanent skip | **high** | **PREVENTED** | `none` | A permanently skipped critical test invalidates the global result; skipping must not silently omit it.  | `audit_d9_test_purity` |
| `VT-037` | Impossible condition | **medium** | **AUDITED** | `none` | Verify that the test's branch actually executes; a condition that is never entered tests nothing.  | `audit_d8_test_coverage` |
| `VT-038` | Order dependency | **medium** | **AUDITED** | `none` | Tests must be independent; one that passes only because of another's leftover state is unreliable.  | `audit_d8_test_coverage` |
| `VT-039` | Temporal dependency | **medium** | **AUDITED** | `none` | Control time explicitly; a test whose result depends on the wall-clock hour or day is non-deterministic.  | `audit_d8_test_coverage` |
| `VT-040` | Absorbed exception | **high** | **PREVENTED** | `none` | An exception must surface, not be absorbed; swallowing it makes the failure disappear.  | `audit_d5_angry_path` |
| `VT-041` | Ignored error output | **medium** | **AUDITED** | `none` | Capture and observe error output; an unobserved error stream hides the failure signal.  | `audit_d8_test_coverage` |
| `VT-042` | False success log | **medium** | **AUDITED** | `none` | Log success only after the verification that justifies it, never before checking.  | `audit_d8_test_coverage` |
| `VT-043` | Unconditional successful exit | **medium** | **AUDITED** | `none` | The exit code must reflect the real state; an unconditional success exit produces a falsely green pipeline.  | `audit_d8_test_coverage` |
| `VT-044` | Ignored return | **medium** | **AUDITED** | `none` | Assert the return value; an ignored error result lets a failure pass unseen.  | `audit_d8_test_coverage` |
| `VT-045` | Single happy path | **medium** | **AUDITED** | `none` | Cover adverse cases, not just the ideal happy path.  | `audit_d8_test_coverage` |
| `VT-046` | Magic datum | **medium** | **AUDITED** | `none` | Generate input variations; a single magic datum chosen to avoid the bug never triggers it.  | `audit_d8_test_coverage` |
| `VT-047` | Small dataset | **high** | **PREVENTED** | `none` | Exercise realistic volume; a test on a tiny dataset misses failures that only appear at scale.  | `test_compress_1000_sessions_returns_structured_dict` |
| `VT-048` | No empty/null/zero | **medium** | **AUDITED** | `none` | Cover empty, null, and zero boundary values, not only populated inputs.  | `audit_d8_test_coverage` |
| `VT-049` | No special characters | **medium** | **AUDITED** | `none` | Include special characters and diverse real-world data that naive inputs never exercise.  | `audit_d8_test_coverage` |
| `VT-050` | No boundary dates | **high** | **PREVENTED** | `none` | Cover calendar boundaries such as leap days and month/year edges; ideal dates hide date-arithmetic bugs.  | `test_non_leap_year_feb29_raises` |
| `VT-051` | Informational CI | **medium** | **AUDITED** | `none` | Critical CI failures must block; an informational-only pipeline lets failures through.  | `audit_d8_test_coverage` |
| `VT-052` | Ignore errors | **high** | **PREVENTED** | `none` | Propagate errors strictly through the pipeline rather than ignoring them.  | `audit_d5_angry_path` |
| `VT-053` | Tests outside the active branch | **medium** | **AUDITED** | `none` | Tests must run on the active path; tests living outside it never protect anything.  | `audit_d8_test_coverage` |
| `VT-054` | Optional tests | **medium** | **AUDITED** | `none` | Make risk-bearing tests mandatory; optional tests are not run and give no protection.  | `audit_d8_test_coverage` |
| `VT-055` | Unattended notification | **medium** | **AUDITED** | `none` | A failure alert needs an owner; an unattended notification makes the failure invisible.  | `audit_d8_test_coverage` |
| `VT-056` | Complacent post-bug test | **medium** | **AUDITED** | `none` | Write a failing test before fixing the bug; a post-bug test that passes while the code is broken proves nothing.  | `audit_d8_test_coverage` |
| `VT-057` | Skip later | **high** | **PREVENTED** | `none` | A deferred skip needs a hard deadline; an open-ended skip becomes permanent debt.  | `audit_d9_test_purity` |
| `VT-058` | Divergent feature flag | **medium** | **AUDITED** | `none` | Test the real feature-flag configuration; testing a divergent flag state hides production behavior.  | `audit_d8_test_coverage` |
| `VT-059` | Variable alters validation | **medium** | **AUDITED** | `none` | Run with a configuration equivalent to production; an environment variable that disables checks weakens the test.  | `audit_d8_test_coverage` |
| `VT-060` | Setup cleans too much | **medium** | **AUDITED** | `none` | Test from a realistic, dirty state; over-cleaning setup creates conditions production never sees.  | `audit_d8_test_coverage` |
| `VT-061` | UI by delta | **medium** | **AUDITED** | `none` | Validate critical UI flows directly, not only visual deltas that miss functional breakage.  | `audit_d8_test_coverage` |
| `VT-062` | Full dead file | **medium** | **AUDITED** | `none` | Validate that code actually executes; a complete-but-dead file passes structural checks while doing nothing.  | `audit_d8_test_coverage` |
| `VT-063` | False documented interface | **medium** | **AUDITED** | `none` | Test the real public interface; documenting a flag the code does not support is a lie the tests must catch.  | `audit_d8_test_coverage` |
| `VT-064` | Invisible broken tests | **medium** | **AUDITED** | `none` | Run the full active suite so an import error that silently disables tests is surfaced.  | `audit_d8_test_coverage` |
| `VT-065` | Broken global capture | **medium** | **AUDITED** | `none` | Isolate each test's side effects so one cannot break the runner or other tests.  | `audit_d8_test_coverage` |
| `VT-066` | Orphan tests | **high** | **PREVENTED** | `none` | Reconcile the test inventory so orphan files that are never discovered or run are surfaced.  | `test_infrastructure_checks` |
| `VT-067` | False negative from docstring | **medium** | **AUDITED** | `none` | Detect forwarding wrappers by structural analysis; a docstring must not mask a shim.  | `audit_d8_test_coverage` |
| `VT-068` | Backups as deprecated | **medium** | **AUDITED** | `none` | Classify artifacts by type so backups are not miscounted as deprecated noise that contaminates the audit.  | `audit_d8_test_coverage` |
| `VT-069` | Misleading name | **medium** | **AUDITED** | `none` | A name must match behavior; a function whose name promises work its body never does is misleading.  | `audit_d8_test_coverage` |
| `VT-070` | Missing setup validation | **high** | **REMEDIATED** | `none` | Validate that the real environment can start - runtime, dependencies, and minimum permissions - not just that the test passes.  | `test_setup_validation` |
| `VT-071` | Non-resumable handoff | **medium** | **AUDITED** | `none` | Test continuity from another actor's checkpoint; a handoff that cannot be resumed is broken.  | `audit_d8_test_coverage` |
| `VT-072` | Documentary rollback | **medium** | **AUDITED** | `none` | Verify the real reversal of a destructive change; a documented-but-unexecuted rollback is unproven.  | `audit_d8_test_coverage` |
| `VT-073` | Compatibility not evaluated | **medium** | **AUDITED** | `none` | Maintain a suite of current consumers so a change that breaks an existing flow is caught.  | `audit_d8_test_coverage` |
| `VT-074` | Untested observability | **medium** | **AUDITED** | `none` | Test that a failure produces actionable diagnostic evidence, not silence.  | `audit_d8_test_coverage` |
| `VT-075` | Incomplete Test Discovery | **medium** | **AUDITED** | `none` | Audit the physical correspondence between test files on disk and tests actually discovered, so a green suite cannot hide inactive ones.  | `audit_d8_test_coverage` |
| `VT-076` | System dependency | **medium** | **AUDITED** | `none` | Run across an environment matrix; a test that only works in one environment is not portable.  | `audit_d8_test_coverage` |
| `VT-077` | Misleading timeout | **medium** | **AUDITED** | `none` | Assert functional limits, not just a generous timeout under which slowness passes.  | `audit_d8_test_coverage` |
| `VT-078` | Single local machine | **medium** | **AUDITED** | `none` | Tests must be reproducible off one developer's machine, independent of a local installation.  | `audit_d8_test_coverage` |
| `VT-079` | Unpenetrated sandbox | **medium** | **AUDITED** | `none` | Test isolation by attempting controlled boundary violations, not by merely declaring the sandbox secure.  | `audit_d8_test_coverage` |
| `VT-080` | Physical Address Coupling | **high** | **REMEDIATED** | `none` | Parametrize resources via injection or logical variables so tests do not couple to a physical address and break on migration.  | `audit_d9_test_purity` |
| `VT-081` | Author tests their own implementation | **medium** | **AUDITED** | `none` | Tests benefit from independent review; an author validating only their own mental model confirms bias.  | `audit_d8_test_coverage` |
| `VT-082` | Review without tests | **medium** | **AUDITED** | `none` | Review the tests as part of the change; approving code without reviewing its tests is blind.  | `audit_d8_test_coverage` |
| `VT-083` | Encoded expected value | **medium** | **AUDITED** | `none` | Derive expected values from an independent specification, not an answer written so the test passes.  | `audit_d8_test_coverage` |
| `VT-084` | Hardcoded approval | **medium** | **AUDITED** | `none` | Base approval on reproducible evidence, not a manually-set approved state treated as truth.  | `audit_d8_test_coverage` |
| `VT-085` | Complacent golden file | **medium** | **AUDITED** | `none` | Regenerate a golden snapshot only after semantic review; a stale golden legitimizes broken output.  | `audit_d8_test_coverage` |
| `VT-086` | Normalized expected failure | **high** | **PREVENTED** | `none` | An expected failure must not count as green; normalizing it makes the failure permanent.  | `audit_d9_test_purity` |
| `VT-087` | Tolerated warning | **medium** | **AUDITED** | `none` | Escalate a warning to a failure until its cause is resolved; a green suite carrying warnings tolerates rot.  | `audit_d8_test_coverage` |
| `VT-088` | Error tolerance | **high** | **PREVENTED** | `none` | A health verdict accepts zero known errors; tolerating one normalizes it.  | `audit_d5_angry_path` |
| `VT-089` | Convenience wrapper | **medium** | **AUDITED** | `none` | Test the real interface with no simplifying wrapper that hides the real failure.  | `audit_d8_test_coverage` |
| `VT-090` | Tested placeholder | **high** | **PREVENTED** | `none` | Block placeholders on verified paths; a placeholder that satisfies the assertion fakes completion.  | `audit_d2_completeness` |
| `VT-091` | Documented domain not implemented | **medium** | **AUDITED** | `none` | Every documented domain must have a live executor; a rule that exists but never runs is inert.  | `audit_d8_test_coverage` |
| `VT-092` | Section as compliance | **medium** | **AUDITED** | `none` | Validate content and effect, not the mere presence of a section heading.  | `audit_d8_test_coverage` |
| `VT-093` | Docstrings as quality | **medium** | **AUDITED** | `none` | Cross-check usage, calls, and tests; docstrings are not evidence of quality.  | `audit_d8_test_coverage` |
| `VT-094` | Handling by keyword | **medium** | **AUDITED** | `none` | Induce a real error to prove handling; matching a lexical keyword is not error handling.  | `audit_d8_test_coverage` |
| `VT-095` | Tests of the protocol, not the subject | **medium** | **AUDITED** | `none` | Run the suite of the audited subject; testing the protocol instead lets an untested project pass.  | `audit_d8_test_coverage` |
| `VT-096` | Stale evidence | **medium** | **AUDITED** | `none` | Bind evidence to the version under test; a stale artifact must not satisfy a current check.  | `audit_d8_test_coverage` |
| `VT-097` | Ceremonial chaos | **medium** | **AUDITED** | `none` | Exercise the real components of the system, not an external library standing in for them.  | `audit_d8_test_coverage` |
| `VT-098` | Lying passed report | **medium** | **AUDITED** | `none` | Report the domains actually exercised; a pass report claiming all while running few is a lie.  | `audit_d8_test_coverage` |
| `VT-099` | Dead version constant | **medium** | **AUDITED** | `none` | Keep a single source of version truth; a dead fallback constant drifts from reality.  | `audit_d8_test_coverage` |
| `VT-100` | Permissions not rigorous | **medium** | **AUDITED** | `none` | Validate both positive and negative permission cases, not only the permitted actor.  | `audit_d8_test_coverage` |
| `VT-101` | Unvalidated routing | **medium** | **AUDITED** | `none` | Test routing decisions with edge cases so tasks cannot silently reach the wrong flow.  | `audit_d8_test_coverage` |
| `VT-102` | Hardcoded approved list | **medium** | **AUDITED** | `none` | Every approval must revalidate active properties; accepting by name from a hardcoded list skips the behavior check.  | `audit_d8_test_coverage` |
| `VT-103` | Expected hardcoded in the evaluator | **medium** | **AUDITED** | `none` | Separate generator, subject, and judge; an evaluator that already knows the expected answer cannot judge.  | `audit_d8_test_coverage` |
| `VT-104` | Warnings outside the score | **medium** | **AUDITED** | `none` | Warnings count as failures until explicitly classified; leaving them outside the score hides risk.  | `audit_d8_test_coverage` |
| `VT-105` | No hook-existence test | **high** | **REMEDIATED** | `none` | Parse the workflow and assert its validator and regenerator steps remain wired, so a pipeline cannot silently lose its verification.  | `test_audit_workflow_runs_validator_and_regenerator` |
| `VT-106` | Unrevalidated exclusion | **high** | **REMEDIATED** | `none` | Periodically revalidate each exclusion so the ignore list cannot accumulate stale, unjustified entries.  | `test_setup_validation` |
| `VT-107` | Stack incompleto silencioso | **high** | **REMEDIATED** | `none` | Validate the full active stack at startup - runtime, CLI tools, hooks, essential files, write permissions - and report exactly what is missing.  | `test_setup_validation` |
| `VT-108` | Name disconnected from the domain | **medium** | **AUDITED** | `none` | Compare the formal declaration (name, domain count, version) against the real implementation and fail when they diverge.  | `audit_d8_test_coverage` |
| `VT-109` | Redundant Frameworks and Middleman Theater (Testing Bridge Theater) | **high** | **PREVENTED** | `none` | A simple static or structural validation should run directly and natively; wrapping it in a heavy test framework is middleman theater.  | `test_infrastructure_checks` |
| `VT-110` | Hidden-Directory Fragmentation (Dot-Directory Fragmentation) | **medium** | **AUDITED** | `none` | Consolidate governance and state metadata under a single hidden directory rather than scattering it across many.  | `audit_d8_test_coverage` |
| `VT-111` | Deferred Without Registration | **medium** | **AUDITED** | `none` | Every deferred classification must immediately open a debt-registry entry; a verbal deferral with no record loses the finding.  | `audit_d8_test_coverage` |
| `VT-112` | Ghost Dependency Drift | **medium** | **AUDITED** | `none` | A static gate must compare every top-level import against the dependency manifest so an unregistered dependency cannot drift in.  | `audit_d8_test_coverage` |
| `VT-113` | Lack of Mutation Testing (Lack of Test Mutation Validation) | **medium** | **AUDITED** | `none` | A suite must empirically demonstrate it can fail against a controlled mutation; tests that stay green under any change are not falsifiable.  | `audit_d8_test_coverage` |
| `VT-114` | Multi-Repository Sync Drift | **medium** | **AUDITED** | `none` | A drift gate must compare checksums across satellite repositories and block when governance files diverge from the central core.  | `audit_d8_test_coverage` |
| `VT-115` | False Drift Positive from Line Endings (CRLF/LF Hash Mismatch) | **high** | **REMEDIATED** | `none` | Normalize line endings to a single form before hashing so files identical on disk do not raise a false drift positive across platforms.  | `test_setup_validation` |
| `VT-116` | Decoy comment satisfies a text-based validator | **high** | **PREVENTED** | `none` | Resolve symbols structurally through the AST so only a real definition node counts; a commented-out or string mention must not satisfy the check.  | `test_planted_def_comment_does_not_resolve` |

### Vibe Coding (91 items)

| ID | Flaw Title | Severity | Status | Downstream Verification | Action Taken / Prevention Method | Validating Test / Guard |
|---|---|---|---|---|---|---|
| `VC-001` | Optimism without proof | **high** | **PREVENTED** | `none` | Empirical proof is required before declaring success: closure fails when no structured evidence artifact backs the claim, forcing verification over optimism.  | `test_B7_evidence_files_are_valid_json` |
| `VC-002` | Prototype turned into debt | **medium** | **PREVENTED** | `required` | Static detector `vc005_untracked_prototype` flags TODO/FIXME/HACK/prototype comments that lack owner, expiration, and ticket metadata. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-003` | Incomprehensible code | **medium** | **PREVENTED** | `required` | Static detector `vc003_incomprehensible_code` flags functions that are structurally complex and missing a docstring. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-004` | Stochastic Conversational Optimism without proof | **high** | **PREVENTED** | `none` | Empirical proof is required before declaring success: closure fails when no structured evidence artifact backs the claim, forcing verification over optimism.  | `test_B7_evidence_files_are_valid_json` |
| `VC-005` | Premature closure | **medium** | **PREVENTED** | `none` | Static detector `vc005_premature_closure` flags closures that ignore still-visible secondary failures. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-006` | Non-externalized plan | **medium** | **PREVENTED** | `none` | The plan must be externalized: topology validation requires the inbox surface to be published, linked from the home page, and backed by an ingestion protocol and templates.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-007` | Non-surgical scope | **medium** | **DOC_ONLY** | `required` | Behavioral/doctrinal vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_behavioral_compliance to DOC_ONLY. | `DOC_ONLY` |
| `VC-008` | State drift | **medium** | **PREVENTED** | `none` | Generated surfaces must track their source: regenerating audit artifacts and re-checking topology prevents home, graph, and index pages from drifting away from the catalogs.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-009` | Full rewrite | **medium** | **DOC_ONLY** | `required` | Full rewrite vs surgical edit: behavioral judgment vice (when a rewrite is justified). No static test discriminates intent, so this stays a manual-review DOC_ONLY entry. | `DOC_ONLY` |
| `VC-010` | No dry run | **medium** | **PREVENTED** | `required` | Static detector `vc036_destructive_without_dryrun` flags destructive operations that appear without a dry-run or simulation step in the same flow. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-011` | Blind regeneration | **medium** | **PREVENTED** | `none` | Regeneration must precede validation: a fresh rebuild of the vault is forced before checks, so blind replacement cannot masquerade as a finished state.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-012` | Invisible debt | **medium** | **REMEDIATED** | `required` | Behavioral/doctrinal vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_behavioral_compliance to DOC_ONLY. | `static-regex` |
| `VC-013` | Ambiguous handoff | **medium** | **PREVENTED** | `required` | Static detector `vc013_ambiguous_handoff` flags handoff notes that omit goal/state/evidence/blockers/next. | `static-regex` |
| `VC-014` | Monolithic memory | **medium** | **PREVENTED** | `none` | Knowledge must be modular: topology validation requires separate canonical surfaces for vices, tokenomics, insights, and the graph rather than one monolithic page.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-015` | Hallucinated integration | **medium** | **PREVENTED** | `required` | The agent imports or references a package, API, or module that does not exist in the declared dependency manifest or in the public package registry.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-016` | Broken version parity | **medium** | **PREVENTED** | `required` | Static detector `vc016_broken_version_parity` flags multiple distinct version literals on the same surface. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-017` | Deadlock without a heartbeat | **medium** | **PREVENTED** | `required` | Static detector `vc017_deadlock_without_heartbeat` flags blocking calls that appear without timeout or heartbeat support. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-018` | Stub as architecture | **medium** | **PREVENTED** | `required` | Static detector `vc061_constant_stub` flags production functions or classes whose body collapses to a stub such as pass, ellipsis, or a constant return. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-019` | State Concurrency Drift (Dual-Session Drift) | **high** | **PREVENTED** | `none` | State must stay consistent across concurrent sessions: a parity check fails when the protocol fingerprint diverges between two sessions.  | `test_F6_sync_binding_no_protocol_drift` |
| `VC-020` | Lying documentation | **medium** | **PREVENTED** | `none` | Documentation must not lie: link-integrity and count-parity validation fail when docs drift away from the generated state.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-021` | Late schema | **medium** | **PREVENTED** | `required` | Code accesses fields that are not declared in the schema or model, leading to runtime AttributeError and silent data corruption when the model changes.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-022` | Spatial blindness | **medium** | **DOC_ONLY** | `required` | UI code is generated without a structured layout system, producing a fragile visual hierarchy that breaks on different screen sizes and is unmaintainable.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-023` | Unmapped dependencies | **medium** | **PREVENTED** | `none` | Dependencies must be mapped: the graph and link validator require canonical surfaces to be linked and resolvable rather than assumed.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-024` | Blind shell manipulation | **medium** | **PREVENTED** | `required` | Static detector `vc070_blind_shell_edit` flags shell-based mutation of structured files; use a parser instead of sed/awk/grep-based edits. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-025` | I/O without validation | **medium** | **PREVENTED** | `required` | Static detector `vc025_io_without_validation` flags external input that reaches a sink without boundary validation. | `static-regex` |
| `VC-026` | Lax typing | **medium** | **PREVENTED** | `none` | Static AST analysis requires complete type annotations on public functions: every parameter and the return value must be typed, and an unconstrained `Any` in domain positions is rejected. The checked signature is the function definition's annotation set, independent of any specific tool.  | `audit_d6_anti_slop` |
| `VC-027` | Permanent placeholder | **medium** | **AUDITED** | `none` | Static AST analysis rejects incomplete implementations as a structural signature: empty function bodies, stub-only docstrings, and pass-only functions; tests whose bodies carry no active assertion are likewise rejected as non-discriminating. The check reads the parsed body, not any specific runner or placeholder literal.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-028` | Core dependent on unstable parts | **medium** | **PREVENTED** | `required` | Static detector `vc028_core_dependent_on_unstable_parts` flags core imports from experimental or unstable modules. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-029` | Uncritical copy-paste | **medium** | **PREVENTED** | `required` | Static detector `vc029_uncritical_copy_paste` flags duplicated non-trivial function bodies copied without consolidation. | `static-ast` |
| `VC-030` | Dependencies without a gate | **high** | **PREVENTED** | `none` | Every imported dependency must be declared in the manifest: a check fails when code imports a package that the dependency manifest does not list.  | `test_vc082_ghost_import_detected` |
| `VC-031` | Tolerated dead file | **medium** | **AUDITED** | `none` | Static integrity analysis enumerates every code file (excluding non-code by extension) and fails with "unregistered file (dead)" when a file is neither declared in the authorized inventory (whitelist) nor a legitimate test. The signature is presence-on-disk without any authorizing reference.  | `D1Integrity` |
| `VC-032` | Normalized warning | **medium** | **PREVENTED** | `none` | Static source analysis flags a blanket `filterwarnings("ignore")` that carries no justifying inline comment on production paths (tests excluded). The allowed pattern is a narrowly-scoped suppression accompanied by a specific reason comment; the rejected signature is the unqualified global suppression call.  | `audit_d6_anti_slop` |
| `VC-033` | Memory not loaded | **medium** | **PREVENTED** | `none` | Memory must be loadable on entry: topology validation requires the canonical memory surfaces to be linked from the home page.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-034` | Lazy file-not-found | **medium** | **PREVENTED** | `none` | Missing files must fail loud: broken-link validation fails when a referenced markdown or wiki target does not resolve on disk.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-035` | Partial audit called total | **medium** | **PREVENTED** | `none` | An audit may only be reported as total when its mandatory phases ran: completeness analysis fails when required prior-phase evidence is absent, so a partial pass cannot be called total.  | `audit_d2_completeness` |
| `VC-036` | Direct production access | **medium** | **PREVENTED** | `required` | Static detector `vc095_hardcoded_secret` flags production hosts or credentials in source; keep production access out of code and validate secrets scanning before merge. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-037` | Code without tests | **medium** | **DOC_ONLY** | `required` | Behavioral/doctrinal vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_behavioral_compliance to DOC_ONLY. | `d8_test_coverage.py` |
| `VC-038` | Optimistic config | **medium** | **PREVENTED** | `required` | Hardcoded configuration values that assume a perfect development environment will break in production where the environment differs.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-039` | Ignored infrastructure | **medium** | **PREVENTED** | `none` | Infrastructure is a first-class surface: the audit workflow is a visible, validated file that must run both the generator and the catalog validator, so infra cannot be silently ignored.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-040` | Component omission | **medium** | **PREVENTED** | `none` | Components must be complete: topology validation checks the canonical home, vices, tokenomics, graph, and inbox surfaces, so a missing component fails the gate.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-041` | Phantom setup | **medium** | **PREVENTED** | `none` | Setup must be real, not phantom: inbox topology validation requires the ingestion protocol, knowledge-sources contract, and templates to exist before new findings are accepted.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-042` | Implicit permission matrix | **medium** | **DOC_ONLY** | `required` | Behavioral/doctrinal vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_behavioral_compliance to DOC_ONLY. | `d15_agent_security.py` |
| `VC-043` | Environmental literal path | **high** | **PREVENTED** | `none` | Filesystem paths must be portable: a scan fails when a hardcoded absolute path (drive letter or home directory) appears in scripts.  | `test_vc109_absolute_path_in_scripts` |
| `VC-044` | Quota as surprise | **medium** | **PREVENTED** | `none` | Quotas must be visible up front: topology validation requires the tokenomics index to expose its subindices and map before the category is treated as complete.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-045` | Exclusion without prior audit | **medium** | **PREVENTED** | `none` | Static analysis verifies that every active exclusion rule in the ignore file is preceded by an explanatory comment justifying the exclusion in the same block; an unannotated exclusion entry is the rejected signature.  | `audit_d2_completeness` |
| `VC-046` | Propagation without adoption verification | **medium** | **DOC_ONLY** | `required` | Behavioral/doctrinal vice — not statically falsifiable in a generic way. Documented in the Golden Standard catalogs as governance knowledge; no automated test can discriminate this without human semantic judgment. Sprint 3.4 triage: reclassified from AUDITED/test_behavioral_compliance to DOC_ONLY. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-047` | Frozen nomenclature | **medium** | **PREVENTED** | `required` | Static detector `vc047_frozen_nomenclature` flags identifiers that still carry embedded version tokens. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-048` | Finding without a remediation plan | **medium** | **PREVENTED** | `none` | Findings need a remediation path: inbox topology validation enforces the ingestion path, templates, and protocol docs required to act on a finding.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-049` | Dynamic execution of external expressions | **high** | **REMEDIATED** | `none` | Rules must not evaluate arbitrary expressions: dynamic execution of external strings is rejected in favor of a pre-registered dispatch of safe checks, closing a remote-code-execution path.  | `test_rule_security_rejects_arbitrary_check` |
| `VC-050` | Automatic installation of unverified dependencies | **high** | **REMEDIATED** | `none` | Dependency installation must never be automatic: an import-time guard must not trigger package installation; missing packages are surfaced for manual decision.  | `test_import_error_guard_does_not_pip_install` |
| `VC-051` | Non-atomic destructive write of critical state | **high** | **REMEDIATED** | `none` | Writes to critical state must be atomic: state is persisted via a temp-file-plus-atomic-replace path so a crash cannot leave a half-written, corrupted file.  | `test_critical_state_write_is_atomic` |
| `VC-052` | Zombie Compatibility Theater | **high** | **PREVENTED** | `none` | A replacement is a single source of truth: the superseded unit is deleted and the new one carries no inheritance, shim, fallback, or dual test sentinel back to it; static analysis flags compatibility forwarders left in active code.  | `D1Integrity` |
| `VC-053` | Critical Redundancies and Repetitive AI-slop Patterns | **high** | **PREVENTED** | `none` | Top-level function names must be unique across modules: a structural comparison fails when the same definition name is duplicated, surfacing redundant slop.  | `test_vc121_duplicate_function_names` |
| `VC-054` | Supply-Chain Contamination via Silent Executions | **high** | **PREVENTED** | `none` | Scripts must not install packages at runtime: an automatic package install inside a script is blocked to prevent silent supply-chain contamination.  | `test_vc122_no_pip_install_in_scripts` |
| `VC-055` | Indiscriminate Staging of Untracked Directories (Unfiltered Git Staging) | **high** | **PREVENTED** | `none` | Staging must be deliberate: indiscriminate staging of all untracked files is rejected, requiring explicit human intent about what enters a commit.  | `test_vc123_no_git_add_all_in_scripts` |
| `VC-056` | Hasty Deprecation without Analysis (Hasty Deprecation) | **high** | **PREVENTED** | `none` | Deprecation requires prior analysis: moving code into a deprecated area is blocked unless a justifying log entry exists, and coverage of that log is verified.  | `check_deprecation_log.py` |
| `VC-057` | Non-externalized retrospective | **high** | **PREVENTED** | `none` | Lessons must be externalized before closure: regeneration plus coverage and retrospective-export checks require every new lesson to reach the catalog or wiki, so closure without a structured export stays incomplete.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-058` | Post-execution suggestion that reopens scope | **medium** | **DOC_ONLY** | `required` | CONTRIBUTING.md now requires a preflight with scope, impacts and out-of-scope follow-ups before execution; post-execution suggestions must be captured in backlog first. | `DOC_ONLY` |
| `VC-059` | Prompt injection in the agent loop (Prompt Injection) | **critical** | **PREVENTED** | `required` | Static detector `vc059_prompt_injection_in_agent_loop` flags instruction-channel concatenation with untrusted content. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-060` | Context Poisoning | **high** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Recipe: a verification step before persisting a fact, and re-anchoring in sources of truth when compacting.  | `d15_agent_security.py` |
| `VC-061` | Hallucinated dependency (slopsquatting) | **high** | **PREVENTED** | `none` | Declared dependencies must exist in the public registry: a lookup fails when a requirement resolves to not-found, catching hallucinated (slopsquatted) packages.  | `test_pypi_404_is_alucinated_dependency` |
| `VC-062` | Echo-Chamber Review | **medium** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Recipe: separate generator and reviewer (distinct model/version/context) or add an independent static gate.  | `DOC_ONLY` |
| `VC-063` | Architectural drift in long sessions (Architecture Drift) | **medium** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Recipe: persistent ADR + post-compaction re-anchoring + coherence check against active decisions.  | `d17_knowledge.py` |
| `VC-064` | Spec Ambiguity Cascade | **medium** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Recipe: confirm the interpretation at branch points before building on it.  | `DOC_ONLY` |
| `VC-065` | Unhandled tool-call failure in the agent loop | **high** | **PREVENTED** | `required` | Static detector `vc065_unhandled_tool_call_failure` flags tool calls whose result is consumed without verifying success. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-066` | Multi-agent coordination without a protocol | **high** | **PREVENTED** | `required` | Static detector `vc066_multi_agent_without_protocol` flags concurrent agent edits on the same state without lock or handoff. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-067` | Use of an obsolete or hallucinated API of a real library | **high** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Distinct from VC-061 (nonexistent package): here the package exists but the symbol does not. Mitigation: up-to-date docs via context7 (PR-110).  | `d11_dependency.py` |
| `VC-068` | Poisoned or stale persistent memory (cross-session) | **high** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Extends PR-042 (context poisoning) to DURABLE memory across sessions. Mitigation: memory layers like byterover / claude-context-memsearch (PR-111).  | `d15_agent_security.py` |
| `VC-069` | Retrieval (RAG) that feeds wrong context | **medium** | **DOC_ONLY** | `required` | Documented; enforcement downstream. Mitigation: symbol-level retrieval (serena) or code-search MCP (claude-context) (PR-112).  | `DOC_ONLY` |
| `VC-070` | Generated code insecure by default | **high** | **PREVENTED** | `none` | Generated code must be secure by default: a static-signature detector, exercised against the catalog examples, flags insecure default patterns.  | `scripts/validate_golden_standard_catalogs.py` |
| `VC-071` | Blind trust in LLM output (Insecure Output Handling) | **high** | **PREVENTED** | `required` | Static detector `vc071_blind_trust_in_llm_output` flags model output that reaches a dangerous sink without sanitization. | `scripts/validate_golden_standard_catalogs.py` |
| `VC-072` | Continuity gap between agents (orphan handoff) | **high** | **PREVENTED** | `none` | Handoff continuity is mandatory: a commit with substantive changes is blocked when the handoff record was not updated or is missing its required sections; an explicit token allows a conscious skip.  | `check_handoff_freshness` |
| `VC-073` | Orphan changes evaded (evasive partial commit) | **high** | **PREVENTED** | `none` | No orphan changes: a commit is blocked when, after staging, the working tree still holds undecided modified or untracked files; idempotent writes and a canonical auto-stage whitelist neutralize artifact churn, and an explicit env escape exists.  | `check_clean_worktree.py` |
| `VC-074` | Agent instruction hijack (Prompt Injection / P1-P2) | **high** | **PREVENTED** | `none` | Agent instructions must be tamper-resistant: static analysis flags directives that attempt to override or hijack the agent's governing prompt.  | `D15AgentSecurity` |
| `VC-075` | System prompt leakage (System Prompt Leakage / P6-P8) | **high** | **PREVENTED** | `none` | The system prompt must not leak: static analysis flags triggers that would exfiltrate or echo the governing prompt into output.  | `D15AgentSecurity` |
| `VC-076` | Unauthorized data exfiltration (Data Exfiltration / E1-E4) | **high** | **PREVENTED** | `none` | Data must not be exfiltrated: static analysis flags network patterns that would send protected data to unauthorized destinations.  | `D15AgentSecurity` |
| `VC-077` | Unjustified privilege escalation (Privilege Escalation / PE1-PE3) | **high** | **PREVENTED** | `none` | Privileges must not silently escalate: static analysis flags indicators of unauthorized privilege escalation.  | `D15AgentSecurity` |
| `VC-078` | Excessive and uncontrolled agency (Excessive Agency / EA1-EA4) | **high** | **PREVENTED** | `none` | Agency must stay bounded: static analysis requires confirmation gates around high-impact actions, rejecting excessive autonomous reach.  | `D15AgentSecurity` |
| `VC-079` | Persistent memory poisoning (Memory Poisoning / MP1-MP3) | **high** | **PREVENTED** | `none` | Persistent memory must not be poisoned: static analysis requires sanitization of memory write operations.  | `D15AgentSecurity` |
| `VC-080` | Insecure tool call or chaining (Tool Misuse / TM1-TM3) | **high** | **PREVENTED** | `none` | Tool calls must be constrained: static analysis enforces parameter limits and rejects unsafe tool chaining.  | `D15AgentSecurity` |
| `VC-081` | Unauthorized persistent behavior (Rogue Agent / RA1-RA2) | **high** | **PREVENTED** | `none` | Agents must not establish unauthorized persistence: static analysis flags persistence indicators of rogue behavior.  | `D15AgentSecurity` |
| `VC-082` | Least-privilege violation in MCP (MCP Least Privilege / LP1-LP4) | **high** | **PREVENTED** | `none` | Tool access must follow least privilege: static analysis maps declared capabilities to the manifest and flags over-broad grants.  | `D15AgentSecurity` |
| `VC-083` | Envenenamiento de descripciones de herramientas (MCP Tool Poisoning / TP1-TP4) | **high** | **PREVENTED** | `none` | Tool descriptions must be trustworthy: static analysis scans for unicode homoglyphs and poisoned tool-description content.  | `D15AgentSecurity` |
| `VC-084` | Canonical source first (no sink patching) | **high** | **AUDITED** | `none` | Edit the canonical source or its generator first: hand-patching a derived artifact to mask drift is rejected; derived files must be regenerated from source.  | `test_canonical_source_first_no_sink_patch` |
| `VC-085` | Doctrine before enforcement (source-first ordering) | **medium** | **AUDITED** | `none` | Doctrine lands before enforcement: the rule must exist in the canonical knowledge base first, with downstream consumers following only after regeneration proves it.  | `test_doctrine_before_enforcement_resolves_refs` |
| `VC-086` | No backlog entry, no work | **high** | **AUDITED** | `required` | Require a backlog entry before planning or execution; if it is not in the ledger, it does not get worked.  | `runtime-test` |
| `VC-087` | Self-polluting tooling (scratch written into the tracked working tree) | **high** | **PREVENTED** | `none` | No scratch in the tracked tree: a test or script that creates temp/probe/backup artifacts at a repo-relative path, or whose run leaves untracked non-ignored files, is rejected. Scratch goes to OS temp with guaranteed cleanup; unavoidable residue is gitignored. | `static-regex` |
| `VC-088` | Execution before plan (planless agent) | **high** | **DOC_ONLY** | `required` | Before touching any file in a task with more than one change: (1) create PLAN.md with numbered steps and acceptance criteria; (2) execute one step at a time; (3) validate each step against PLAN.md before proceeding; (4) delete PLAN.md in the closing commit once all steps are done. Absence of PLAN.md after close = evidence of completion. | `doctrinal` |
| `VC-089` | Addition when deletion suffices | **medium** | **DOC_ONLY** | `required` | Run the YAGNI check before writing: (1) does this need to exist at all? (2) does removing something existing solve it? Shortest working diff wins. Deletion over addition. Flag any PR where net line count is positive but the root problem was an unused code path.  | `d_complexity.py` |
| `VC-090` | Premature abstraction (YAGNI interface) | **medium** | **DOC_ONLY** | `required` | Before creating an interface, abstract class, factory, or plugin system: verify there are at least 2 concrete implementations today. One implementation = inline it. One config key with one value = hardcode it. One layer with one caller = delete the layer.  | `static-ast` |
| `VC-091` | Unnecessary dependency introduction | **medium** | **DOC_ONLY** | `required` | Resolution ladder before any new dependency: (1) does stdlib cover it? (2) does an already-installed package expose this? (3) does a native platform API cover it? Only after all three fail: add dep. Every new dep requires explicit justification in the PR why the ladder was exhausted.  | `d_complexity.py` |

### Tokenomics & Context (34 items)

| ID | Flaw Title | Severity | Status | Downstream Verification | Action Taken / Prevention Method | Validating Test / Guard |
|---|---|---|---|---|---|---|
| `TK-001` | Missing checkpoint | **low** | **PREVENTED** | `none` | Close each session with a durable checkpoint so a new session does not restart from zero; the canonical checkpoint guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-002` | Chat memory as the primary source | **low** | **PREVENTED** | `none` | Keep authoritative state outside the chat so switching threads does not lose it; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-003` | Project switch without closure | **low** | **PREVENTED** | `none` | Checkpoint before changing objective so contexts do not contaminate each other; the canonical checkpoint guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-004` | Re-explained setup | **low** | **PREVENTED** | `none` | Keep a minimal boot-and-health sheet so each session does not spend tokens rebuilding the environment; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-005` | Prose-heavy handoff | **medium** | **PREVENTED** | `none` | Session handoff state must use structured sections rather than free prose so it is machine-parseable; a test fails on unstructured handoff.  | `test_tk005_status_md_has_required_sections` |
| `TK-006` | Manual history merge | **low** | **PREVENTED** | `none` | Merge context by decisions and invariants rather than raw text so conflict resolution does not burn context; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-007` | Duplicated source of truth | **low** | **PREVENTED** | `none` | Consult one canonical core and archive copies as evidence so contradictory duplicates are not re-read; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-008` | Empirical memory segregation | **low** | **PREVENTED** | `none` | Separate stable guidelines into an immutable core and compact the transitional buffer so stable specs are not reprocessed; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-009` | Exploration tax | **low** | **PREVENTED** | `none` | Use indexes, maps, and targeted reading so many tokens are not spent before acting; the canonical input-and-retrieval guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-010` | Bloated tool schemas | **low** | **PREVENTED** | `none` | Load tools on demand so unused schemas do not consume context; the canonical input-and-retrieval guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-011` | Giant multi-objective prompt | **low** | **PREVENTED** | `none` | Pursue one concrete task per cycle so attention is not split across objectives; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-012` | Backlog mixed with the objective | **medium** | **PREVENTED** | `none` | The backlog must be externalized to a durable machine-readable store rather than living only in chat; a test verifies the external backlog artifact exists.  | `test_tk018_external_backlog_exists` |
| `TK-013` | Output constraint | **low** | **PREVENTED** | `none` | Define an output budget and format so responses are not long by default; the canonical output-and-compaction guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-014` | Prefilling | **low** | **PREVENTED** | `none` | Predefine the start and structure of responses so the format is not variable; the canonical output-and-compaction guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-015` | Example optimization | **low** | **PREVENTED** | `none` | Use minimal, diverse, dense examples so few-shot context is not redundant; the canonical input-and-retrieval guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-016` | Raw logs | **medium** | **REMEDIATED** | `none` | Long-running background loops and orchestrators must route output through a compression/throttling layer; static analysis flags scripts that do not wrap execution in an output compressor.  | `audit_d10_tokenomics` |
| `TK-017` | Summary without density | **low** | **PREVENTED** | `none` | Preserve critical facts, decisions, and next steps so compaction does not lose them; the canonical output-and-compaction guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-018` | Verbose audit output | **low** | **PREVENTED** | `none` | Report finding, evidence, and action so the signal is not lost in noise; the canonical output-and-compaction guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-019` | Noisy observability | **low** | **PREVENTED** | `none` | Log a causal summary and retain detail on demand so extensive logs do not push out the problem; the canonical measurement-and-telemetry guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-020` | Lexical Compression of Diagnostics | **low** | **PREVENTED** | `none` | Apply controlled lexical-redundancy filtering to execution traces so verbose, repetitive errors do not cost context; the canonical output-and-compaction guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-021` | Stable context caching | **low** | **PREVENTED** | `none` | Mark reusable blocks and avoid reloading them so stable context is not reprocessed; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-022` | Context compaction | **low** | **PREVENTED** | `none` | Summarize state and restart with continuity so a long session does not degrade; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-023` | Cache cliff | **low** | **PREVENTED** | `none` | Manage resumption and checkpoints so pauses do not invalidate the cache benefit; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-024` | No headroom | **low** | **PREVENTED** | `none` | Keep a context budget with a safety zone so context does not collapse silently; the canonical memory-and-headroom guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-025` | Invisible rollback cost | **low** | **PREVENTED** | `none` | Record the cost of fix/revert loops so it does not silently consume the session; the canonical measurement-and-telemetry guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-026` | Thinking with the execution tool | **low** | **PREVENTED** | `none` | Separate thinking, executing, and reviewing so expensive execution context is not spent deciding; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-027` | Response without a mode | **low** | **PREVENTED** | `none` | Route work by phase - think, execute, review - so the agent knows its mode; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-028` | Forgettable manual monitoring | **low** | **PREVENTED** | `none` | Make thresholds visible and automatable so the user does not manually count messages; the canonical measurement-and-telemetry guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-029` | Full-state re-reading | **medium** | **REMEDIATED** | `none` | Core memory manifests must stay under fixed line budgets so context is not saturated; a static size gate fails when a manifest exceeds its budget.  | `audit_d10_tokenomics` |
| `TK-030` | Non-integrated external tools | **medium** | **DOC_ONLY** | `required` | Every script path cited in the authority/budget docs must exist on disk; a static reference check fails on dangling citations (spectral scripts).  | `audit_d10_tokenomics` |
| `TK-031` | Promised savings not measured | **low** | **PREVENTED** | `none` | Measure token usage before and after so a reduction is not merely declared; the canonical measurement-and-telemetry guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-032` | Invisible quotas | **low** | **PREVENTED** | `none` | Plan for limits, backoff, and degradation so the session is not cut off by unbudgeted quotas; the canonical measurement-and-telemetry guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-033` | Entropy without pruning — input governance without output governance | **low** | **PREVENTED** | `none` | Govern output as strictly as input by hunting orphans and dead artifacts as a gate, not only blocking junk on the way in; the canonical guidance must stay published and linked from the index, which a CI link-check verifies.  | `scripts/validate_golden_standard_catalogs.py` |
| `TK-034` | Accumulated tokenomics debt (Cost Compounding) | **medium** | **PREVENTED** | `none` | Per-session token accumulation must be bounded; when output exceeds the efficiency budget, execution is blocked and compaction forced.  | `_check_and_flag_compact` |

## Principles

These entries are preserved as project-agnostic doctrine and now consumed as first-class principles by GS users and downstream tools.

| ID | Principle |
|---|---|
| `PR-001` | Unassumed incompetence |
| `PR-002` | Blind trust |
| `PR-003` | Demo as quality |
| `PR-004` | Aesthetics as integrity |
| `PR-005` | Non-human audit of the core |
| `PR-006` | Operational optimism |
| `PR-007` | Contaminated self-audit |
| `PR-008` | Failure not turned into doctrine |
| `PR-009` | Fake human test |
| `PR-010` | "Looks good" as a metric |
| `PR-011` | Free top score |
| `PR-012` | Audit false positive |
| `PR-013` | Agent as autonomous engineer |
| `PR-014` | Blind fix |
| `PR-015` | Patched symptom |
| `PR-016` | Unreproduced bug |
| `PR-017` | Speed over precision |
| `PR-018` | Illusory productivity |
| `PR-019` | Building without validation |
| `PR-020` | Vague specification |
| `PR-021` | Excessive assumptions |
| `PR-022` | Sidequest |
| `PR-023` | Closure pressure |
| `PR-024` | Decisions without a why |
| `PR-025` | Lost clarifications |
| `PR-026` | Premature victory |
| `PR-027` | Unaudited maintainability |
| `PR-028` | Operational drift |
| `PR-029` | Correction loops |
| `PR-030` | Patches over patches |
| `PR-031` | Production without a technical owner |
| `PR-032` | Skipped pre-deprecation rescue |
| `PR-033` | Non-binding state |
| `PR-034` | Mixed audiences |
| `PR-035` | Undirected update |
| `PR-036` | Contextual saturation |
| `PR-037` | Context rot |
| `PR-038` | No prior checkpoint |
| `PR-039` | Decentralized state |
| `PR-040` | Concurrency without quarantine |
| `PR-041` | Opaque routing |
| `PR-042` | Textual memory merge |
| `PR-043` | Architectural black box |
| `PR-044` | Implicit policies |
| `PR-045` | Normative conflicts |
| `PR-046` | Module without biocontainment |
| `PR-047` | Blind chunking |
| `PR-048` | Critical code sliced up |
| `PR-049` | Unverified integrations |
| `PR-050` | Documentation hijack |
| `PR-051` | Ignored regressive compatibility |
| `PR-052` | Ornamental observability |
| `PR-053` | Evasive wrapper |
| `PR-054` | Error tolerated by policy |
| `PR-055` | Skipped reconnaissance |
| `PR-056` | Optimistic security |
| `PR-057` | Mixed security |
| `PR-058` | Late tests |
| `PR-059` | Happy path only |
| `PR-060` | No chaos |
| `PR-061` | Non-functional ignored |
| `PR-062` | Poor debug |
| `PR-063` | UI without real use |
| `PR-064` | Security boundary by convention |
| `PR-065` | Lock Panic and Fast Syntactic Patching (Lock Panic Shortcut) |
| `PR-066` | Reasoning Lock-In & AI Runaway loops (Chain-Pattern Interrupts) |
| `PR-067` | Reprocessing stable context |
| `PR-068` | Primitive context pruning |
| `PR-069` | Excessive verbal output |
| `PR-070` | Semantic pruning |
| `PR-071` | Contextual retrieval |
| `PR-072` | Structured delimiters |
| `PR-073` | Full read by default |
| `PR-074` | Whole file for a specific question |
| `PR-075` | Narrated permissions |
| `PR-076` | Hierarchical Dependency Skeleton |
| `PR-077` | Batch processing |
| `PR-078` | Capability cascade |
| `PR-079` | Deptry – reconciliation of imports against declared dependencies to detect missing, unused, transitive, misplaced dev, and stdlib declared as dependencies. |
| `PR-080` | Diagnostic assertions – when a test fails, the message must explain the discrepancy with actionable clarity. Real verified tools: pytest native assertion rewriting, pytest-clarity / pytest-icdiff for readable diffs, flake8-assertive for correct assertion methods. (Corrects a prior reference to a nonexistent package — see VC-061 hallucinated dependency.) |
| `PR-081` | Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call. |
| `PR-082` | Trivy – multi-surface scanning (images, filesystem, git, VMs, Kubernetes) for CVEs, secrets, misconfigurations, SBOM, and licenses. |
| `PR-083` | Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing. |
| `PR-084` | Governance gate between intent and execution that enforces context discipline, observability, redaction, and state control. |
| `PR-085` | Output governance – a system can have INPUT governance (quality gates) but lack OUTPUT governance (orphan pruning), accumulating refactor residue: backups, dead code, stale plan docs, spectral scripts, divergent learning logs, stale base-sets, and IDs declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk. |
| `PR-086` | Batch of predictable authorizations – group permissions, clarifications, and decisions before a long run to avoid interruptions, rereads, and reactive work. |
| `PR-087` | Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked. |
| `PR-088` | Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue. |
| `PR-089` | Descriptive names and simple topology – prefer scripts and modules that explain their purpose and flatten structure when it reduces cognitive friction. |
| `PR-090` | Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress. |
| `PR-091` | Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem. |
| `PR-092` | Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools. |
| `PR-093` | Circularity ratchet – every new vice must break a real circular relationship and drain the baseline in batches; coverage that does not reduce the circle is still theater. |
| `PR-094` | DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage. |
| `PR-095` | Anti many-to-one coverage – a test that claims to cover N vices at once loses discrimination; each guard must isolate the failure it claims to protect against. |
| `PR-096` | Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge. |
| `PR-097` | Execution and tooling hygiene – prefer simple commands, declarative edits, UTF-8, auditable evidence, and elevated permissions only as an exception; temporary helpers must disappear unless they are reusable and documented. |
| `PR-098` | Confidence Tags (Graphify pattern) – every state claim in protocol documents must carry an explicit confidence level: VERIFIED (backed by terminal log or test), INFERRED (deduced from indirect evidence), ASSUMED (no evidence, reasonable supposition). Claims without a tag are treated as ASSUMED. Applies especially to protocol specs, audit logs, and architectural decision comments. Origin: safishamsi/graphify confidence tag system for knowledge graphs. |
| `PR-099` | Semantic Wiki-Lint (Karpathy LLM Wiki pattern) – protocol documents must be audited periodically to detect: contradictions between sections, references to nonexistent files, mandates mentioned in one doc but absent in another, and inconsistent version claims. The Lint is not syntactic (that is handled by a syntactic catalog linter) but semantic: do two documents claim incompatible things about the same state? Origin: Karpathy LLM Wiki gist, Lint operation of the agent-maintained wiki framework. |
| `PR-100` | Operational uncertainty list – every session or protocol document must declare which subsystems, routes, or claims were not mechanically verified in that turn. The absence of a list equals incomplete verification. Origin: operational uncertainty discipline and anti-hallucination control. |
| `PR-101` | Dual-session awareness – before touching shared sources, the agent must verify state and latest commits so as not to step on concurrent work. If there are external changes, impact is analyzed before editing. Origin: multi-agent coexistence discipline and serialized shared-source access. |
| `PR-102` | Hub-based review – nodes with the highest fan-in or impact degree must be reviewed first when a catalog or index changes. The graph is not decorative: it prioritizes risk and orders the audit. Origin: hub-first review heuristic (graph fan-in prioritization). |
| `PR-103` | Exportable retrospective – every session must close with a structured, parseable retrospective that is persisted to a durable ledger before a context reset (COMPACT/CLEAR). Chat is not reliable memory and new knowledge must survive the reset. Origin: structured-retrospective export and a durable ledger as a source of continuity. |
| `PR-104` | Exhaustive preflight and no reopening scope post-execution – before executing any change, the agent must declare scope, foreseeable impacts, out-of-scope follow-ups, and the runner/loader that would be affected if the topology changes. If a new improvement emerges after executing, it is first recorded in the backlog; it is not offered as a post-execution suggestion. Origin: execution hygiene and the formal separation of audits between knowledge and consumption. |
| `PR-105` | Serialization of Git operations – Git commands must be executed serially within automations and orchestrators to avoid index locks, state races, and inconsistent results. When coordination or concurrent tooling exists, the safe discipline is a single Git flow at a time with controlled retries, not opportunistic parallelism. Origin: global learning on race conditions and .git/index.lock locking. |
| `PR-106` | Vibe Check (PV-Bhat/vibe-check-mcp-server, verified) – metacognition MCP server that curbs agent tunnel-vision and runaway loops via Chain-Pattern Interrupts; a direct implementation of the PR-066 mitigation. |
| `PR-107` | vibecheck (yuvrajangadsingh/vibecheck, verified) – ESLint for AI slop: a local linter that detects code smells in AI-generated code (hardcoded secrets, eval, empty catch); evidence that the catalog vices are statically detectable. |
| `PR-108` | viberails (refractionPOINT/viberails, verified) – AI Firewall that intercepts risky agent operations (Claude Code, Cursor, Gemini CLI) via hooks; an enforcement layer conceptually comparable to a policy-enforcement gate (unrelated to the homonym philips-software/cerberus). |
| `PR-109` | ratelimit (tomasbasham/ratelimit, verified) – rate limiting decorator (@limits + sleep_and_retry) as a concrete control against PR-031 (quota as surprise) and the tokenomics debt (TK-034). |
| `PR-110` | context7 (upstash/context7, verified) -- delivers up-to-date code documentation to LLMs to avoid calls to obsolete or nonexistent APIs; a direct mitigation of PR-044. |
| `PR-111` | Persistent memory layer (byterover-cli / zilliztech claude-context-memsearch, verified) -- durable cross-session memory for agents; its discipline (source, date, reconciliation) mitigates PR-045. |
| `PR-112` | serena (oraios/serena, verified) -- symbol-level (semantic) retrieval and editing so that recovered context is correct; mitigates VC-069 against blind chunking. |
| `PR-113` | Auditing stochastic systems – when behavior depends on chance, sampling, retries, probabilistic routing, or non-deterministic generation, it is not evaluated with a single run nor with an exact value. The rule is to declare the target distribution, seed when applicable, sample size, acceptable thresholds, and repetition criterion; if the surface should be deterministic, the randomness is eliminated rather than disguised as controlled. Claims about stability or correctness must be reproducible across several runs, not just plausible in one. Origin: GS audit of stochastic systems; complements VT-028 on controlled randomness. |
| `PR-114` | Equivalent-effect substitution: absence of the canonical path is a constraint, not a dead end. When the standard installation path for a tool is unavailable, identify the effect required and achieve it through an available alternative. Origin: RTK hook unavailable on Windows; CC PreToolUse Bash matcher achieves identical enforcement. Session 2026-06-21. |
| `PR-115` | External Tool Attribution: every evaluated tool must be cataloged with source URL, license, and verdict in knowledge/external_tools.md before adoption or rejection. Credit to original authors is non-negotiable. Origin: Session 2026-06-23. |
| `PR-116` | Audit Result Trichotomy: every audit check must produce exactly one of three explicit outcomes: finding, clean, or could-not-verify (CNV). CNV is not clean — a check that cannot run must never silently appear as PASS. |
| `PR-117` | Deliberate Shortcut Disclosure — every intentional simplification must name its ceiling and its upgrade trigger |
| `PR-118` | Anti-Shell Mandate — use atomic file tools; never shell write commands |
| `PR-119` | Pre-Success Empirical Gate — no success declaration without evidence |
| `PR-120` | Debt Tax Ceiling — cap code output per turn; run Simplicity Pass after |
| `PR-121` | Escalation Protocol — stop and escalate when confidence falls below 70% |

## Principle Recommendations by Canonical Domain

These actions are the operational bridge between the principles and the canonical GS domains.

| Domain | Title | Principle | Project | Action |
|---|---|---|---|---|
| `CD01` | Repository Integrity & Surface Hygiene | `PR-085` | reference | Treat leftover backups, stale plan docs, spectral scripts, and orphan residue as governance debt, not harmless clutter. |
| `CD01` | Repository Integrity & Surface Hygiene | `PR-088` | reference | Keep the root workspace clean after every audit or remediation pass so historical evidence never pollutes active context. |
| `CD01` | Repository Integrity & Surface Hygiene | `PR-097` | reference | Prefer simple, auditable execution surfaces and remove temporary helpers unless they are reusable and documented. |
| `CD02` | Completeness & State Continuity | `PR-084` | reference | Store state, evidence, checkpoints, and control signals outside the chat so the operational contract stays complete. |
| `CD02` | Completeness & State Continuity | `PR-086` | reference | Batch predictable authorizations and clarifications before long runs so the control plane can execute without interruptions. |
| `CD02` | Completeness & State Continuity | `PR-104` | reference | Declare scope, foreseeable impacts, and affected runners before execution, then record new work in backlog instead of reopening scope reactively. |
| `CD03` | Legibility & Causal Explainability | `PR-080` | pytest-good-assertions | Require failure messages that explain the discrepancy with enough clarity to debug without guesswork. |
| `CD03` | Legibility & Causal Explainability | `PR-089` | reference | Prefer descriptive names and simple topology so purpose is visible at first glance. |
| `CD03` | Legibility & Causal Explainability | `PR-098` | graphify | Tag protocol claims with VERIFIED, INFERRED, or ASSUMED so readers can separate evidence from inference. |
| `CD04` | Code Vitality & Dead Surface | `PR-085` | reference | Treat spectral scripts, stale helper layers, and dead refactor residue as a governance failure, not as harmless leftovers. |
| `CD04` | Code Vitality & Dead Surface | `PR-097` | reference | Temporary helpers must disappear unless they remain reusable, documented, and visibly load-bearing. |
| `CD04` | Code Vitality & Dead Surface | `PR-107` | vibecheck | Use local static smell detection to expose low-quality or inert AI-generated code before it becomes accepted surface. |
| `CD05` | Structural Simplicity & Blast Radius | `PR-083` | litellm | Centralize routing and fallbacks so the code does not grow provider-specific branching spaghetti. |
| `CD05` | Structural Simplicity & Blast Radius | `PR-089` | reference | Flatten structure when it reduces cognitive friction and removes needless indirection. |
| `CD05` | Structural Simplicity & Blast Radius | `PR-102` | reference | Review graph hubs first when the catalog changes because high fan-in nodes carry the largest impact radius. |
| `CD06` | Failure Handling & Recovery Paths | `PR-084` | reference | Turn failure handling into a structured protocol with next steps, evidence, and a visible recovery path. |
| `CD06` | Failure Handling & Recovery Paths | `PR-087` | reference | Treat warnings and known non-blocking findings as operational errors until they are fixed or explicitly blocked. |
| `CD06` | Failure Handling & Recovery Paths | `PR-113` | reference | When behavior is stochastic, define sampling, thresholds, and repetition criteria instead of declaring correctness from one lucky run. |
| `CD07` | Boundary Hygiene & Anti-Theater | `PR-090` | reference | Allow exclusions only when they are minimal, justified, and real; false coverage is debt, not progress. |
| `CD07` | Boundary Hygiene & Anti-Theater | `PR-093` | reference | Require each new guard to break a real circularity and reduce the baseline instead of merely naming the problem. |
| `CD07` | Boundary Hygiene & Anti-Theater | `PR-095` | reference | Split broad coverage theater into discriminative checks so one guard never pretends to cover many unrelated failures. |
| `CD08` | Runtime & Data Security | `PR-082` | trivy | Scan repos, images, filesystems, and IaC for secrets, vulnerabilities, and misconfigurations before release. |
| `CD08` | Runtime & Data Security | `PR-107` | vibecheck | Use local linting that catches hardcoded secrets, eval, and empty catch blocks as early runtime-security signals. |
| `CD08` | Runtime & Data Security | `PR-108` | viberails | Intercept risky agent operations through a policy-enforcement layer instead of trusting every generated action. |
| `CD09` | Coverage Adequacy | `PR-079` | deptry | Validate dependency declarations before running coverage gates so missing imports do not fake a green test surface. |
| `CD09` | Coverage Adequacy | `PR-093` | reference | Each new guard must shrink a real uncovered circularity baseline rather than merely expand the list of names. |
| `CD09` | Coverage Adequacy | `PR-113` | reference | Audit stochastic behavior with declared sampling and thresholds instead of single-run optimism. |
| `CD10` | Test Falsifiability & Assertion Quality | `PR-080` | pytest-good-assertions | Keep assertion output precise and inspectable so a failing test explains the discrepancy instead of performing theater. |
| `CD10` | Test Falsifiability & Assertion Quality | `PR-094` | reference | Mark non-falsifiable lessons as DOC_ONLY instead of pretending automatic coverage exists. |
| `CD10` | Test Falsifiability & Assertion Quality | `PR-095` | reference | Avoid many-to-one guards that claim to protect many vices but cannot isolate the real failure. |
| `CD11` | Context Efficiency & Tokenomics | `PR-081` | tokencost | Meter tokens before and during LLM calls so spend is visible before usage grows. |
| `CD11` | Context Efficiency & Tokenomics | `PR-083` | litellm | Unify provider routing, fallback, and cost tracking so efficiency and resilience are handled once. |
| `CD11` | Context Efficiency & Tokenomics | `PR-085` | reference | Treat output trimming, context hygiene, and history externalization as first-class controls. |
| `CD11` | Context Efficiency & Tokenomics | `PR-109` | ratelimit | Use rate limiting to avoid quota surprises and reduce reactive token waste. |
| `CD11` | Context Efficiency & Tokenomics | `PR-112` | serena | Prefer symbol-level retrieval so recovered context is correct instead of bloated by blind chunking. |
| `CD12` | Dependency & Supply-Chain Posture | `PR-079` | deptry | Compare imports against declared dependencies and fail on missing, unused, transitive, or misplaced packages. |
| `CD12` | Dependency & Supply-Chain Posture | `PR-082` | trivy | Audit packages and related build surfaces against vulnerabilities, secrets, and SBOM gaps before release. |
| `CD12` | Dependency & Supply-Chain Posture | `PR-110` | context7 | Use current documentation sources to reduce reliance on obsolete or hallucinated package APIs. |
| `CD13` | Knowledge Canonicalization & Ingestion | `PR-092` | reference | Keep GS alive by absorbing lessons from the core project and satellites without contaminating doctrine with local tooling details. |
| `CD13` | Knowledge Canonicalization & Ingestion | `PR-096` | reference | Normalize, deduplicate, and record new lessons before folding them into the central knowledge base. |
| `CD13` | Knowledge Canonicalization & Ingestion | `PR-099` | karpathy-llm-wiki | Audit protocol documents semantically to detect contradictions, stale references, and incompatible claims. |
| `CD13` | Knowledge Canonicalization & Ingestion | `PR-100` | reference | Keep an explicit uncertainty list so unverified claims are visible before they become doctrine. |
| `CD14` | Federation Drift & Version Parity | `PR-101` | reference | Check shared state and recent commits before editing so concurrent sessions do not overwrite each other silently. |
| `CD14` | Federation Drift & Version Parity | `PR-103` | reference | Persist structured retrospectives before context resets so continuity survives across sessions and federated work. |
| `CD14` | Federation Drift & Version Parity | `PR-105` | reference | Execute Git operations serially in orchestrations to avoid index locks, races, and inconsistent shared state. |
| `CD15` | Observability & Evidence Telemetry | `PR-081` | tokencost | Make cost visible before execution so token telemetry exists as evidence, not as a hindsight estimate. |
| `CD15` | Observability & Evidence Telemetry | `PR-091` | reference | Observe risky signals during execution, not after the fact, so monitoring can interrupt damage early. |
| `CD15` | Observability & Evidence Telemetry | `PR-098` | graphify | Use explicit confidence tags so state claims are measurable against real evidence instead of decorative certainty. |
| `CD15` | Observability & Evidence Telemetry | `PR-103` | reference | Persist structured retrospective exports to a durable ledger before any context reset. |
| `CD16` | Discourse Rigor & Evidence Quality | `PR-098` | graphify | Tag every state claim with explicit confidence so discourse communicates evidence quality directly. |
| `CD16` | Discourse Rigor & Evidence Quality | `PR-099` | karpathy-llm-wiki | Run semantic wiki-lint so documents do not drift into incompatible or contradictory claims. |
| `CD16` | Discourse Rigor & Evidence Quality | `PR-100` | reference | Declare which claims were not mechanically verified in the current session instead of letting ambiguity pass as fact. |
| `CD16` | Discourse Rigor & Evidence Quality | `PR-104` | reference | Declare scope, impacts, and out-of-scope follow-ups before execution so handoff prose remains bounded and honest. |
| `CD17` | Agent Boundary Security | `PR-106` | vibe-check | Use metacognitive interrupts to curb tunnel vision and runaway loops before the agent crosses unsafe behavioral boundaries. |
| `CD17` | Agent Boundary Security | `PR-108` | viberails | Intercept risky agent operations through policy hooks so boundary violations are blocked before execution. |
| `CD17` | Agent Boundary Security | `PR-111` | persistent-memory | Treat durable cross-session memory as a trust-boundary surface that requires source, date, and reconciliation discipline. |
| `CD18` | Multi-Agent Project Governance | `SP-001` | canonical-structure | Collapse all agent governance into .agents/AGENTS.md; delete all other governance files. |
| `CD18` | Multi-Agent Project Governance | `SP-002` | canonical-structure | Write every material fact into project files before session ends; chat is not durable storage. |
| `CD18` | Multi-Agent Project Governance | `SP-003` | canonical-structure | Keep tasks/backlog/ live-only; completed items are deleted after their closing commit. |
| `CD18` | Multi-Agent Project Governance | `SP-004` | canonical-structure | Delete task files on completion; the git commit message is the sole durable record. |
| `CD18` | Multi-Agent Project Governance | `SP-005` | canonical-structure | Session close (HANDOFF + STATE + audit/sessions record) is a required phase, not optional. |
| `CD18` | Multi-Agent Project Governance | `SP-006` | canonical-structure | audit.py enforces the canonical tree across CC, GS, and satellites; failing audit blocks session close. |
| `CD18` | Multi-Agent Project Governance | `SP-007` | canonical-structure | tasks/README.md and audit/README.md templates are mandatory; agents must use them. |
| `CD18` | Multi-Agent Project Governance | `SP-008` | canonical-structure | Agent self-certifies done against AGENTS.md §4 DoD; review/ only for explicitly flagged tasks. |
| `CD18` | Multi-Agent Project Governance | `SP-009` | canonical-structure | Canonicalize every material decision, session finding, and new work item before session ends — same gate as GS INGESTION_PROTOCOL, applied to project knowledge. |
| `CD18` | Multi-Agent Project Governance | `SP-010` | canonical-structure | Apply root audit to any knowledge repo using GS as a template; classify all root files correctly. |
