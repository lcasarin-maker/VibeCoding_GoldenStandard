# Falsifiability Report — Golden Standard Catalog

This report classifies all catalog entries into 5 distinct falsifiability classes based on how they can be validated and prevented.

## Distribution Summary

| Falsifiability Class | Entry Count | Percentage | Description |
| --- | --- | --- | --- |
| `static-regex` | 47 | 9.8% | Simple pattern matching of source code (e.g. banned functions, regex rules). |
| `static-ast` | 47 | 9.8% | Abstract Syntax Tree parsing (e.g. complexity, function structures). |
| `runtime-test` | 190 | 39.7% | Behavioral test runs (e.g. boundary testing, exception validation). |
| `llm-judge` | 21 | 4.4% | Semantic output validation (e.g. faithfulness, hallucinations). |
| `manual-audit` | 174 | 36.3% | Human review and peer verification (e.g. design alignment, workflow context). |

**Total evaluated entries:** 479

## Detailed Inventory

| ID | Title | Class | Verification Rationale |
| --- | --- | --- | --- |
| AV-001 | Empty collection input | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-002 | Empty and whitespace-only string | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-003 | Single-element collection | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-004 | All-equal elements | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| AV-005 | Monotonically decreasing input | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-006 | Zero-value parameter (k=0, n=0, d=0) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-007 | Integer overflow and INT32 clamping | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-008 | Self-referential or identity operation | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-009 | All-zero matrix or empty grid | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-010 | Duplicate values in input | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-011 | Negative values in numeric input | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-012 | Idempotent repeated operation | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-013 | Boundary depth parameter in tree modification (d=1) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-014 | k equals or exceeds collection size | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-015 | Ambiguous sign prefix in string parsers | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-016 | Variable shadowing in nested scopes | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-017 | All-same elements in turbulent/mountain subarray | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-018 | Graph with no edges (isolated nodes) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-019 | Cache miss before any put (LRU/cache state query before population) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-020 | String replacement with non-matching source | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-021 | Unreachable target (impossible / -1 result) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-022 | Cycle detection in tree/graph inputs | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-023 | Large input triggering O(n²) TLE | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-024 | All-negative max subarray (must return single element) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-025 | Circular array boundary wrapping | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-026 | Counting permutations with all-duplicate elements | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-027 | String prefix == full string (KMP/rolling-hash edge) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-028 | Flood / overflow with no dry day available | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-029 | Minimum/maximum with single-candidate input | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| AV-030 | Null / empty tree input | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-031 | Constant output regardless of input (mathematical fixed point) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-032 | Time window boundary (23:59 → 00:00 midnight rollover) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-033 | Source equals destination (zero-cost path) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-034 | Stack/queue exhausted before target reached (cascade collision) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-035 | Alien word order contradiction (prefix-before-shorter) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-036 | Operation before any data inserted (empty data structure query) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-037 | Carry propagation in linked list arithmetic | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-038 | No valid path / combination exists (backtracking returns empty) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-039 | Count matrix with all-negative or all-zero cells | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-040 | Subsequence with s longer than t (immediately false) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-041 | Integer conversion edge cases (0, negative, exact INT32_MAX) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-042 | Interval intersection with one empty list | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-043 | Trie / prefix search with no matching prefix | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-044 | Course cycle detection (circular prerequisite) | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| AV-045 | Power function with exponent 0, negative, or INT32_MAX | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-046 | Remove ALL duplicates from sorted list (entire list erased) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-047 | Path sum in empty tree or single-leaf-miss (targetSum ≠ root value) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-048 | BST validation fails on subtree global constraint (not just parent) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-049 | Sliding window of size 1 (result equals input array) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-050 | Partition impossible when total not divisible by k | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-051 | Unique paths on 1xN or Nx1 grid (exactly one path) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-052 | Symmetric tree with null root or single node | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-053 | Probability converges to 1.0 for large n (threshold detection) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-054 | Pattern-triplet impossible when n<=2 (degenerate size) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-055 | Zero-element pairing — [0,0] valid pair; odd count of zeros invalid | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-056 | Calculator — bare number, chained division, nested negation | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-057 | Clock angle at 12:00 is 0.0 not 360; half-degree results for non-round minutes | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| AV-058 | Flood avoidance — dry-day as no-op when nothing rained; same lake twice without gap fails | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-059 | Accounts-merge — duplicate entries dedup; same name without shared email stays separate | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-060 | Add-row-to-tree at d=1 creates new root; old root becomes left child | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-061 | 2-keys-keyboard — n=1 costs 0; prime n costs n steps (no factor shortcut) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-062 | 24-game — all-same cards often impossible; fractional intermediates required | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-063 | Arithmetic slices — n<3 always 0; constant-difference (d=0) is valid arithmetic | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-064 | Burst-balloons — single balloon or zero-value balloon edge cases | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-065 | Calendar-booking — touching endpoints are NOT overlapping; single booking always True | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-066 | Coin-change — amount=0 yields 0 coins; impossible amounts yield -1 not infinity | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| AV-067 | Combination-sum-IV — target=0 yields 1 (empty combination); no coin reaches target yields 0 | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-068 | Complex-number multiplication — zero operand and negative imaginary string format | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-069 | Decode-ways — leading zero → 0 paths; embedded zero kills downstream paths | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-070 | Decoded-string-at-index — K always points to a character, never past end; single-char expansion | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-071 | Zigzag-array — single element costs 0; all-equal array costs 2 (must reduce one parity) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-072 | Closest-divisors — num=1 yields [1,2]; large num may have highly asymmetric factorization | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-073 | Minimum-time-difference — duplicate timestamps → 0; circular wrap across midnight | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-074 | Missing-number — [0] missing 1; [1] missing 0; complete array missing n | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-075 | N-queens — n=1 exactly one solution; n=2,3 yield empty list (no solution) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-076 | Network-delay-time — single node with no edges → 0; source cannot reach all → -1 | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| AV-077 | Move-zeroes — empty array no-op; all-zeros stays same; negative values are NOT zero | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-078 | Multiply-strings — "0"×anything="0"; leading zeros must be stripped from result | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-079 | Number-of-atoms — single atom no-count; same element repeated merges; nested multiplier | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-080 | Number-of-dice-rolls — target < d (minimum sum impossible) → 0; d=1 f=1 → exactly 1 | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-081 | Number-of-digit-one — n=0→0; n=1→1; n=20→12 (counts 1s as digits not numbers) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-082 | Number-of-longest-IS — all-equal array → n paths; strictly decreasing → n single-element paths | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-083 | Music-playlists — n=1, goal>1, k=0 yields 1 (only one song, must repeat) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-084 | Online-stock-span — single price → [1]; all-equal prices span grows; all-decreasing all 1s | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-085 | Optimal-division — single element returns itself; two elements never uses parens; n≥3 always uses one grouping | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-086 | Sub-arrays-with-odd-sum — single even element → 0; single odd element → 1; all-even array → 0 | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-087 | Monotone-increasing-digits — N=0→0; single-digit→itself; 10→9; 100→99 (drop-cascade) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-088 | Remove-invalid-parentheses — empty string → [""]; all-invalid → [""]; no-invalid → input as-is | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-089 | Reverse-bits — n=0→0; n=1→2147483648 (bit placed at position 31); output is 32-bit unsigned | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-090 | Reverse-k-group — k > list length leaves list unchanged; k=1 is identity; empty list → empty | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-091 | Remove-duplicates-sorted-array — empty array → []; all-same → [one]; negative values work | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-092 | Reconstruct-itinerary — single flight [A→B]; must use all tickets; sort by lexicographic order | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| AV-093 | String-to-integer-atoi — empty string → 0; spaces-only → 0; leading "+" valid; "+-" → 0; INT overflow clamp | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-094 | Three-sum — empty array → []; no solution → []; [0,0,0] → \[\[0,0,0\]\]; deduplicate triplets | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-095 | Trapping-rain-water — empty → 0; flat → 0; strictly decreasing → 0 (water flows off right) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-096 | Two-sum — target=0 with negatives; pair at ends; large values; duplicate values | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-097 | Unique-BSTs — n=0→1 (empty tree is valid); n=1→1; Catalan number sequence | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-098 | Word-break — empty string → True; word not in dict → False; repeated word check | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-099 | Valid-parentheses — empty string is valid; single char → False; nested mismatch "(]" → False | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-100 | AI-agent generates SQL via f-string when prompted with "skip validation" instruction | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-101 | Agent hardcodes secrets when told "we'll add proper auth later" | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| AV-102 | Agent trajectory skips required tool call under step-limit pressure | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-103 | LLM-as-judge scores paraphrase and contradiction identically without augmentation | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| AV-104 | Agent adds abstraction or wrapper when deletion solves the problem | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-001 | Unassumed incompetence | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-002 | Blind trust | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-003 | Demo as quality | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-004 | Aesthetics as integrity | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-005 | Non-human audit of the core | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-006 | Operational optimism | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-007 | Contaminated self-audit | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-008 | Failure not turned into doctrine | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-009 | Fake human test | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-010 | "Looks good" as a metric | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-011 | Free top score | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-012 | Audit false positive | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-013 | Agent as autonomous engineer | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-014 | Blind fix | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-015 | Patched symptom | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-016 | Unreproduced bug | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-017 | Speed over precision | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-018 | Illusory productivity | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-019 | Building without validation | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-020 | Vague specification | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-021 | Excessive assumptions | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-022 | Sidequest | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-023 | Closure pressure | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-024 | Decisions without a why | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-025 | Lost clarifications | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-026 | Premature victory | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-027 | Unaudited maintainability | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-028 | Operational drift | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-029 | Correction loops | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-030 | Patches over patches | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-031 | Production without a technical owner | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-032 | Skipped pre-deprecation rescue | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-033 | Non-binding state | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-034 | Mixed audiences | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-035 | Undirected update | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-036 | Contextual saturation | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-037 | Context rot | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-038 | No prior checkpoint | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-039 | Decentralized state | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-040 | Concurrency without quarantine | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-041 | Opaque routing | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-042 | Textual memory merge | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-043 | Architectural black box | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-044 | Implicit policies | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-045 | Normative conflicts | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-046 | Module without biocontainment | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-047 | Blind chunking | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-048 | Critical code sliced up | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-049 | Unverified integrations | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-050 | Documentation hijack | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-051 | Ignored regressive compatibility | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-052 | Ornamental observability | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-053 | Evasive wrapper | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-054 | Error tolerated by policy | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-055 | Skipped reconnaissance | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-056 | Optimistic security | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-057 | Mixed security | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-058 | Late tests | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-059 | Happy path only | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-060 | No chaos | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-061 | Non-functional ignored | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-062 | Poor debug | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-063 | UI without real use | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-064 | Security boundary by convention | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-065 | Lock Panic and Fast Syntactic Patching (Lock Panic Shortcut) | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-066 | Reasoning Lock-In & AI Runaway loops (Chain-Pattern Interrupts) | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-067 | Reprocessing stable context | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-068 | Primitive context pruning | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-069 | Excessive verbal output | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-070 | Semantic pruning | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-071 | Contextual retrieval | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-072 | Structured delimiters | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-073 | Full read by default | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-074 | Whole file for a specific question | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-075 | Narrated permissions | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-076 | Hierarchical Dependency Skeleton | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-077 | Batch processing | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-078 | Capability cascade | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-079 | Deptry – reconciliation of imports against declared dependencies to detect missing, unused, transitive, misplaced dev, and stdlib declared as dependencies. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-080 | Diagnostic assertions – when a test fails, the message must explain the discrepancy with actionable clarity. Real verified tools: pytest native assertion rewriting, pytest-clarity / pytest-icdiff for readable diffs, flake8-assertive for correct assertion methods. (Corrects a prior reference to a nonexistent package — see VC-061 hallucinated dependency.) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-081 | Tokencost – upfront token metering and USD conversion to make spend visible before executing an LLM call. | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-082 | Trivy – multi-surface scanning (images, filesystem, git, VMs, Kubernetes) for CVEs, secrets, misconfigurations, SBOM, and licenses. | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-083 | Litellm – provider-agnostic gateway with routing, fallback, cost tracking, guardrails, logging, and load balancing. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-084 | Governance gate between intent and execution that enforces context discipline, observability, redaction, and state control. | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| PR-085 | Output governance – a system can have INPUT governance (quality gates) but lack OUTPUT governance (orphan pruning), accumulating refactor residue: backups, dead code, stale plan docs, spectral scripts, divergent learning logs, stale base-sets, and IDs declared without content. Root cause: the gate validated letter (Path.exists) not currency (active route). Lesson: the same gate that blocks bad code blocks the leftover junk. | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-086 | Batch of predictable authorizations – group permissions, clarifications, and decisions before a long run to avoid interruptions, rereads, and reactive work. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-087 | Zero debt before advancing – every warning or non-blocking finding is treated as an operational error until fixed or explicitly blocked. | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-088 | Output hygiene and clean root – historical artifacts are reference, not source of truth; when an audit closes the root must be free of operational residue. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-089 | Descriptive names and simple topology – prefer scripts and modules that explain their purpose and flatten structure when it reduces cognitive friction. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-090 | Minimal and real exclusions – whitelists, excludes, skips, xfails, stubs, mocks, and placeholders only with verifiable cause; false coverage is debt, not progress. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-091 | Real-time vigilance – observe signals, costs, and deviations during execution, not only in the post-mortem. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-092 | Living Golden Standard – preserve pure, agnostic knowledge kept up to date with the lessons from the project and the satellites without mixing it with concrete tools. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-093 | Circularity ratchet – every new vice must break a real circular relationship and drain the baseline in batches; coverage that does not reduce the circle is still theater. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-094 | DOC_ONLY honesty – if a lesson is not falsifiable by a physical gate, it must be labeled DOC_ONLY instead of simulating automatic coverage. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-095 | Anti many-to-one coverage – a test that claims to cover N vices at once loses discrimination; each guard must isolate the failure it claims to protect against. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-096 | Canonical ingestion of lessons – normalize, deduplicate, and record new satellite lessons before incorporating them into the central knowledge. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-097 | Execution and tooling hygiene – prefer simple commands, declarative edits, UTF-8, auditable evidence, and elevated permissions only as an exception; temporary helpers must disappear unless they are reusable and documented. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-098 | Confidence Tags (Graphify pattern) – every state claim in protocol documents must carry an explicit confidence level: VERIFIED (backed by terminal log or test), INFERRED (deduced from indirect evidence), ASSUMED (no evidence, reasonable supposition). Claims without a tag are treated as ASSUMED. Applies especially to protocol specs, audit logs, and architectural decision comments. Origin: safishamsi/graphify confidence tag system for knowledge graphs. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-099 | Semantic Wiki-Lint (Karpathy LLM Wiki pattern) – protocol documents must be audited periodically to detect: contradictions between sections, references to nonexistent files, mandates mentioned in one doc but absent in another, and inconsistent version claims. The Lint is not syntactic (that is handled by a syntactic catalog linter) but semantic: do two documents claim incompatible things about the same state? Origin: Karpathy LLM Wiki gist, Lint operation of the agent-maintained wiki framework. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-100 | Operational uncertainty list – every session or protocol document must declare which subsystems, routes, or claims were not mechanically verified in that turn. The absence of a list equals incomplete verification. Origin: operational uncertainty discipline and anti-hallucination control. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-101 | Dual-session awareness – before touching shared sources, the agent must verify state and latest commits so as not to step on concurrent work. If there are external changes, impact is analyzed before editing. Origin: multi-agent coexistence discipline and serialized shared-source access. | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-102 | Hub-based review – nodes with the highest fan-in or impact degree must be reviewed first when a catalog or index changes. The graph is not decorative: it prioritizes risk and orders the audit. Origin: hub-first review heuristic (graph fan-in prioritization). | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-103 | Exportable retrospective – every session must close with a structured, parseable retrospective that is persisted to a durable ledger before a context reset (COMPACT/CLEAR). Chat is not reliable memory and new knowledge must survive the reset. Origin: structured-retrospective export and a durable ledger as a source of continuity. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-104 | Exhaustive preflight and no reopening scope post-execution – before executing any change, the agent must declare scope, foreseeable impacts, out-of-scope follow-ups, and the runner/loader that would be affected if the topology changes. If a new improvement emerges after executing, it is first recorded in the backlog; it is not offered as a post-execution suggestion. Origin: execution hygiene and the formal separation of audits between knowledge and consumption. | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-105 | Serialization of Git operations – Git commands must be executed serially within automations and orchestrators to avoid index locks, state races, and inconsistent results. When coordination or concurrent tooling exists, the safe discipline is a single Git flow at a time with controlled retries, not opportunistic parallelism. Origin: global learning on race conditions and .git/index.lock locking. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-106 | Vibe Check (PV-Bhat/vibe-check-mcp-server, verified) – metacognition MCP server that curbs agent tunnel-vision and runaway loops via Chain-Pattern Interrupts; a direct implementation of the PR-066 mitigation. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-107 | vibecheck (yuvrajangadsingh/vibecheck, verified) – ESLint for AI slop: a local linter that detects code smells in AI-generated code (hardcoded secrets, eval, empty catch); evidence that the catalog vices are statically detectable. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-108 | viberails (refractionPOINT/viberails, verified) – AI Firewall that intercepts risky agent operations (Claude Code, Cursor, Gemini CLI) via hooks; an enforcement layer conceptually comparable to a policy-enforcement gate (unrelated to the homonym philips-software/cerberus). | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-109 | ratelimit (tomasbasham/ratelimit, verified) – rate limiting decorator (@limits + sleep_and_retry) as a concrete control against PR-031 (quota as surprise) and the tokenomics debt (TK-034). | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-110 | context7 (upstash/context7, verified) -- delivers up-to-date code documentation to LLMs to avoid calls to obsolete or nonexistent APIs; a direct mitigation of PR-044. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-111 | Persistent memory layer (byterover-cli / zilliztech claude-context-memsearch, verified) -- durable cross-session memory for agents; its discipline (source, date, reconciliation) mitigates PR-045. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-112 | serena (oraios/serena, verified) -- symbol-level (semantic) retrieval and editing so that recovered context is correct; mitigates VC-069 against blind chunking. | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-113 | Auditing stochastic systems – when behavior depends on chance, sampling, retries, probabilistic routing, or non-deterministic generation, it is not evaluated with a single run nor with an exact value. The rule is to declare the target distribution, seed when applicable, sample size, acceptable thresholds, and repetition criterion; if the surface should be deterministic, the randomness is eliminated rather than disguised as controlled. Claims about stability or correctness must be reproducible across several runs, not just plausible in one. Origin: GS audit of stochastic systems; complements VT-028 on controlled randomness. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-114 | Equivalent-effect substitution: absence of the canonical path is a constraint, not a dead end. When the standard installation path for a tool is unavailable, identify the effect required and achieve it through an available alternative. Origin: RTK hook unavailable on Windows; CC PreToolUse Bash matcher achieves identical enforcement. Session 2026-06-21. | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| PR-115 | External Tool Attribution: every evaluated tool must be cataloged with source URL, license, and verdict in knowledge/external_tools.md before adoption or rejection. Credit to original authors is non-negotiable. Origin: Session 2026-06-23. | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-116 | Audit Result Trichotomy: every audit check must produce exactly one of three explicit outcomes: finding, clean, or could-not-verify (CNV). CNV is not clean — a check that cannot run must never silently appear as PASS. | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-117 | Deliberate Shortcut Disclosure — every intentional simplification must name its ceiling and its upgrade trigger | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| PR-118 | Anti-Shell Mandate — use atomic file tools; never shell write commands | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| PR-119 | Pre-Success Empirical Gate — no success declaration without evidence | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-120 | Debt Tax Ceiling — cap code output per turn; run Simplicity Pass after | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| PR-121 | Escalation Protocol — stop and escalate when confidence falls below 70% | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| SP-001 | Single governance hub | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-002 | No material fact in chat | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| SP-003 | Live debt only in backlog | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-004 | Resolved debt goes to git log only | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-005 | Session close is mandatory | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| SP-006 | Consistent structure across federated repos | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-007 | Templates mandatory for tasks and sessions | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-008 | Agent self-certifies task completion | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| SP-009 | Project knowledge must be canonicalized before session end | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| SP-010 | Knowledge repo root discipline | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-001 | Missing checkpoint | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-002 | Chat memory as the primary source | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-003 | Project switch without closure | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-004 | Re-explained setup | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-005 | Prose-heavy handoff | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-006 | Manual history merge | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-007 | Duplicated source of truth | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-008 | Empirical memory segregation | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-009 | Exploration tax | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-010 | Bloated tool schemas | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-011 | Giant multi-objective prompt | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-012 | Backlog mixed with the objective | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-013 | Output constraint | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-014 | Prefilling | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-015 | Example optimization | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-016 | Raw logs | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| TK-017 | Summary without density | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-018 | Verbose audit output | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-019 | Noisy observability | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-020 | Lexical Compression of Diagnostics | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-021 | Stable context caching | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-022 | Context compaction | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-023 | Cache cliff | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-024 | No headroom | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-025 | Invisible rollback cost | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-026 | Thinking with the execution tool | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-027 | Response without a mode | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-028 | Forgettable manual monitoring | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-029 | Full-state re-reading | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| TK-030 | Non-integrated external tools | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| TK-031 | Promised savings not measured | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-032 | Invisible quotas | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-033 | Entropy without pruning — input governance without output governance | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| TK-034 | Accumulated tokenomics debt (Cost Compounding) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-001 | Optimism without proof | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-002 | Prototype turned into debt | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-003 | Incomprehensible code | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-004 | Stochastic Conversational Optimism without proof | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-005 | Premature closure | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-006 | Non-externalized plan | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-007 | Non-surgical scope | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VC-008 | State drift | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-009 | Full rewrite | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-010 | No dry run | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-011 | Blind regeneration | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-012 | Invisible debt | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-013 | Ambiguous handoff | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-014 | Monolithic memory | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-015 | Hallucinated integration | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-016 | Broken version parity | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-017 | Deadlock without a heartbeat | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-018 | Stub as architecture | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-019 | State Concurrency Drift (Dual-Session Drift) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-020 | Lying documentation | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-021 | Late schema | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-022 | Spatial blindness | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-023 | Unmapped dependencies | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-024 | Blind shell manipulation | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-025 | I/O without validation | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-026 | Lax typing | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-027 | Permanent placeholder | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-028 | Core dependent on unstable parts | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-029 | Uncritical copy-paste | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-030 | Dependencies without a gate | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-031 | Tolerated dead file | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-032 | Normalized warning | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-033 | Memory not loaded | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-034 | Lazy file-not-found | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-035 | Partial audit called total | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-036 | Direct production access | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-037 | Code without tests | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-038 | Optimistic config | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-039 | Ignored infrastructure | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-040 | Component omission | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-041 | Phantom setup | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-042 | Implicit permission matrix | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-043 | Environmental literal path | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-044 | Quota as surprise | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-045 | Exclusion without prior audit | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-046 | Propagation without adoption verification | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-047 | Frozen nomenclature | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-048 | Finding without a remediation plan | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-049 | Dynamic execution of external expressions | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-050 | Automatic installation of unverified dependencies | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-051 | Non-atomic destructive write of critical state | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-052 | Zombie Compatibility Theater | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-053 | Critical Redundancies and Repetitive AI-slop Patterns | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-054 | Supply-Chain Contamination via Silent Executions | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-055 | Indiscriminate Staging of Untracked Directories (Unfiltered Git Staging) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-056 | Hasty Deprecation without Analysis (Hasty Deprecation) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-057 | Non-externalized retrospective | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-058 | Post-execution suggestion that reopens scope | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-059 | Prompt injection in the agent loop (Prompt Injection) | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-060 | Context Poisoning | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VC-061 | Hallucinated dependency (slopsquatting) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-062 | Echo-Chamber Review | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-063 | Architectural drift in long sessions (Architecture Drift) | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VC-064 | Spec Ambiguity Cascade | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-065 | Unhandled tool-call failure in the agent loop | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-066 | Multi-agent coordination without a protocol | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-067 | Use of an obsolete or hallucinated API of a real library | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-068 | Poisoned or stale persistent memory (cross-session) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-069 | Retrieval (RAG) that feeds wrong context | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VC-070 | Generated code insecure by default | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-071 | Blind trust in LLM output (Insecure Output Handling) | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-072 | Continuity gap between agents (orphan handoff) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-073 | Orphan changes evaded (evasive partial commit) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VC-074 | Agent instruction hijack (Prompt Injection / P1-P2) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-075 | System prompt leakage (System Prompt Leakage / P6-P8) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-076 | Unauthorized data exfiltration (Data Exfiltration / E1-E4) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-077 | Unjustified privilege escalation (Privilege Escalation / PE1-PE3) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-078 | Excessive and uncontrolled agency (Excessive Agency / EA1-EA4) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-079 | Persistent memory poisoning (Memory Poisoning / MP1-MP3) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-080 | Insecure tool call or chaining (Tool Misuse / TM1-TM3) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-081 | Unauthorized persistent behavior (Rogue Agent / RA1-RA2) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-082 | Least-privilege violation in MCP (MCP Least Privilege / LP1-LP4) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-083 | Envenenamiento de descripciones de herramientas (MCP Tool Poisoning / TP1-TP4) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-084 | Canonical source first (no sink patching) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-085 | Doctrine before enforcement (source-first ordering) | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-086 | No backlog entry, no work | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-087 | Self-polluting tooling (scratch written into the tracked working tree) | `static-regex` | Falsifiable via static regex matching against source code patterns. |
| VC-088 | Execution before plan (planless agent) | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VC-089 | Addition when deletion suffices | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VC-090 | Premature abstraction (YAGNI interface) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-091 | Unnecessary dependency introduction | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VC-092 | Elif chain measured as deep nesting (AST-depth blind spot) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-093 | Unjustified Semgrep suppression (bare # nosemgrep) | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VC-094 | BOM in config file silently kills the first key | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-001 | Hardcoded return | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-002 | Permanent stub | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-003 | Response by exact datum | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-004 | Copying the expected value | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-005 | Trivial assert | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-006 | Test without assert | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-007 | Presence not correctness | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-008 | Message not result | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-009 | Tautology | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-010 | Implementation test | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-011 | Incorrect expected value | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-012 | Coverage without asserts | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-013 | Tests for percentage | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-014 | Circular test | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-015 | Test too broad | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-016 | Ceremonial textual assertion | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-017 | Hardcoded evidence | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-018 | Fragile string matching | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-019 | Valid error hash | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-020 | One hundred percent as the goal | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-021 | Regression without a sentinel | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-022 | Green ceremony and Tautological Assertions | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-023 | Complacent mock | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-024 | Incomplete fake | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VT-025 | Network stub | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-026 | Simplified database | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-027 | Fixed clock | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-028 | Controlled randomness | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-029 | Fake filesystem | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-030 | Friendly monkey patch | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-031 | Command stub | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-032 | Partial mock scan | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-033 | Wrapper as remediation | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-034 | Approved placeholder | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-035 | Permanent xfail | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-036 | Permanent skip | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-037 | Impossible condition | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-038 | Order dependency | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-039 | Temporal dependency | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-040 | Absorbed exception | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-041 | Ignored error output | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-042 | False success log | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-043 | Unconditional successful exit | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-044 | Ignored return | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-045 | Single happy path | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-046 | Magic datum | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-047 | Small dataset | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-048 | No empty/null/zero | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-049 | No special characters | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-050 | No boundary dates | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-051 | Informational CI | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-052 | Ignore errors | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-053 | Tests outside the active branch | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-054 | Optional tests | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-055 | Unattended notification | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-056 | Complacent post-bug test | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-057 | Skip later | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-058 | Divergent feature flag | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-059 | Variable alters validation | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-060 | Setup cleans too much | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-061 | UI by delta | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-062 | Full dead file | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-063 | False documented interface | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-064 | Invisible broken tests | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-065 | Broken global capture | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-066 | Orphan tests | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-067 | False negative from docstring | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-068 | Backups as deprecated | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-069 | Misleading name | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-070 | Missing setup validation | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-071 | Non-resumable handoff | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-072 | Documentary rollback | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-073 | Compatibility not evaluated | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-074 | Untested observability | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-075 | Incomplete Test Discovery | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-076 | System dependency | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-077 | Misleading timeout | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-078 | Single local machine | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-079 | Unpenetrated sandbox | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-080 | Physical Address Coupling | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-081 | Author tests their own implementation | `llm-judge` | Falsifiable under llm-judge: requires semantic evaluation of output alignment using an LLM evaluator. |
| VT-082 | Review without tests | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-083 | Encoded expected value | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-084 | Hardcoded approval | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-085 | Complacent golden file | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-086 | Normalized expected failure | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-087 | Tolerated warning | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-088 | Error tolerance | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-089 | Convenience wrapper | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-090 | Tested placeholder | `static-ast` | Falsifiable via AST complexity and structure parsing. |
| VT-091 | Documented domain not implemented | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-092 | Section as compliance | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-093 | Docstrings as quality | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-094 | Handling by keyword | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-095 | Tests of the protocol, not the subject | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-096 | Stale evidence | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-097 | Ceremonial chaos | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-098 | Lying passed report | `runtime-test` | Falsifiable under runtime-test: requires stress/concurrency integration testing. |
| VT-099 | Dead version constant | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-100 | Permissions not rigorous | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-101 | Unvalidated routing | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-102 | Hardcoded approved list | `runtime-test` | Falsifiable under runtime-test: requires boundary testing with empty/extreme values. |
| VT-103 | Expected hardcoded in the evaluator | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-104 | Warnings outside the score | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-105 | No hook-existence test | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-106 | Unrevalidated exclusion | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-107 | Stack incompleto silencioso | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-108 | Name disconnected from the domain | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-109 | Redundant Frameworks and Middleman Theater (Testing Bridge Theater) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-110 | Hidden-Directory Fragmentation (Dot-Directory Fragmentation) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-111 | Deferred Without Registration | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-112 | Ghost Dependency Drift | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-113 | Lack of Mutation Testing (Lack of Test Mutation Validation) | `static-regex` | Falsifiable under static-regex: requires pattern matching detector to flag prohibited occurrences. |
| VT-114 | Multi-Repository Sync Drift | `manual-audit` | Falsifiable under manual-audit: requires human code review / peer verification. |
| VT-115 | False Drift Positive from Line Endings (CRLF/LF Hash Mismatch) | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
| VT-116 | Decoy comment satisfies a text-based validator | `runtime-test` | Falsifiable under pytest suite by simulating the failure state. |
