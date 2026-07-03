---
# Cerberus Finding — Inbox Template
---

## Metadata

source: cerberus
cerberus_rule_id: CR-D16-elif-nesting
project_audited: Cerberus (CC itself, self-audit)
date_detected: 2026-07-03
origin: D:\AI\Cerberus\scripts\cerberus_mcp_server.py:165 (call_tool), flagged by
  Cerberus's own `_max_ast_nesting` in scripts/Full_dimensions_audit.py (D16 Legibility,
  "[DEUDA] ... anidamiento > 4")

## Classification

proposed_domain: VC
proposed_severity: low
tags:
  - readability
  - static-analysis
refinement_target:
evidence_for:
severity_challenge: false

---

## Finding

### Symptom
A 7-branch `if name == "check": ... elif name == "sync": ... elif ...` dispatch in
`cerberus_mcp_server.py::call_tool` was flagged by Cerberus's own nesting-depth gate
(D16 Legibility) as "anidamiento > 4" (depth 7), even though the code reads as a flat,
single-level chain of alternatives to a human — no reviewer looking at the source would
call this "deeply nested."

### Cause
Python's grammar desugars an `if/elif/elif/.../else` chain into **nested** `ast.If` nodes:
each `elif` becomes a new `If` inside the previous one's `orelse` branch. A naive AST-depth
counter (`if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try,
ast.ExceptHandler)): depth += 1`, recursing over children) therefore measures an N-branch
elif chain as N levels of nesting, conflating "many flat alternatives" with "control flow
buried inside control flow inside control flow." The metric is technically accurate about
the AST shape and misleading about the actual readability of the source text.

### Context / Example
```python
# BAD (per the AST-depth metric, though it reads flat to a human):
def call_tool(self, name, arguments):
    if name == "check":
        ...
    elif name == "sync":
        ...
    elif name == "hygiene":
        ...
    elif name == "knowledge-query":
        ...
    elif name == "adn-coverage":
        ...
    elif name == "graph-context":
        ...
    elif name == "test-impact":
        ...
    else:
        raise KeyError(...)
    # ast.If nesting depth here = 7 (one per elif), D16 gate fires at >4.

# GOOD (dispatch dict — same behavior, ast.If depth = 1):
def call_tool(self, name, arguments):
    dispatch = {"check": ..., "sync": ..., "hygiene": ..., ...}
    if name not in dispatch:
        raise KeyError(...)
    return dispatch[name]()
```

### Proposed Mitigation
- When a nesting-depth/complexity static check fires on an `if/elif` chain, prefer
  converting it to a dispatch dict (name -> callable) over silencing the check or
  manually restructuring into deeper helper functions. This is a mechanical,
  behavior-preserving refactor that both satisfies the metric and genuinely
  simplifies the code (no duplicated conditional logic, O(1) lookup).
- Static-analysis tools that count AST nesting depth for readability gates should
  special-case `elif` chains (e.g. only count the first `If` in a chain of
  `If`-in-`orelse` nodes, or cap the contribution of pure elif chains to 1) so the
  metric distinguishes "alternatives" from "genuine nesting." Filed as a follow-up
  note for Cerberus's own `_max_ast_nesting` (currently by design over-counts this
  case; the dispatch-dict fix is the correct response today, but a smarter counter
  would reduce false "DEUDA" noise going forward.)

### Evidence Artifact
evidence_artifact: D:\AI\Cerberus\scripts\cerberus_mcp_server.py (commit made
  2026-07-03, session doing CC test-suite/backlog remediation); D:\AI\Cerberus\scripts\Full_dimensions_audit.py::_max_ast_nesting
  (dimensions/_ast_rule_eval.py after CC-018's extraction) is the detector that fired.

---

## Resolution (filled by curator, do not edit)

promoted_to: VC-092
wiki_article: Wiki/Vices/VC-092.md
date_promoted: 2026-07-03
curator: Claude (Sonnet 5), GS-094 activation session
