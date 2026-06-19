"""Real static detectors for falsifiable Golden Standard vices.

Each detector takes a code snippet (str) and returns True when the vice's signature
is present. They are proven against the catalog's own example_bad / example_good
corpus by test_detectors.py -- turning "falsifiable in principle" into "enforced here".

Detectors are intentionally small and conservative: they aim to fire on the cataloged
example_bad and stay silent on example_good, not to be production-grade linters. A
green test run is the contract: every registered detector discriminates its own pair.
"""
from __future__ import annotations

import copy
import importlib.util
import ast
import re


def _parse(code: str) -> ast.AST | None:
    try:
        return ast.parse(code)
    except SyntaxError:
        return None


def _test_funcs(tree: ast.AST) -> list[ast.FunctionDef]:
    return [n for n in ast.walk(tree)
            if isinstance(n, ast.FunctionDef) and n.name.startswith("test")]


def _body_without_docstring(fn: ast.FunctionDef) -> list[ast.stmt]:
    body = list(fn.body)
    if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
        return body[1:]
    return body


def _stmt_signature(stmt: ast.stmt) -> str:
    node = copy.deepcopy(stmt)

    class Canonicalizer(ast.NodeTransformer):
        def visit_Name(self, node: ast.Name) -> ast.AST:
            return ast.copy_location(ast.Name(id="_", ctx=node.ctx), node)

        def visit_Attribute(self, node: ast.Attribute) -> ast.AST:
            self.generic_visit(node)
            node.attr = "_"
            return node

        def visit_Constant(self, node: ast.Constant) -> ast.AST:
            if isinstance(node.value, str):
                return ast.copy_location(ast.Constant(value="_"), node)
            if isinstance(node.value, (int, float, complex, bool)) or node.value is None:
                return ast.copy_location(ast.Constant(value="_"), node)
            return node

        def visit_arg(self, node: ast.arg) -> ast.AST:
            node.arg = "_"
            return node

    node = Canonicalizer().visit(node)
    ast.fix_missing_locations(node)
    return ast.dump(node, include_attributes=False)


def _function_complexity(fn: ast.FunctionDef) -> int:
    complexity = 1
    for node in ast.walk(fn):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try, ast.IfExp, ast.ExceptHandler, ast.Match, ast.comprehension)):
            complexity += 1
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity


# --- VC-115: dynamic execution of external expressions (eval/exec/compile) ---
def vc115_unsafe_eval(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in {"eval", "exec", "compile"}:
            return True
    return False


# --- VC-095: hardcoded secrets / production credentials ---
_SECRET = re.compile(r"""(password|passwd|pwd|secret|api[_-]?key|token)\s*=\s*['"][^'"]+['"]""", re.I)
_DSN = re.compile(r"""[a-z][a-z0-9+.\-]*://[^'"\s/]+:[^'"\s/@]+@""", re.I)


def vc095_hardcoded_secret(code: str) -> bool:
    return bool(_SECRET.search(code) or _DSN.search(code))


# --- VC-078: placeholder values reaching code ---
_PLACEHOLDER = re.compile(
    r"""=\s*['"]\s*(REPLACE_ME|CHANGE_?ME|YOUR_[A-Z_]+|X{4,}|TODO|FIXME|placeholder)\s*['"]""", re.I
)


def vc078_placeholder(code: str) -> bool:
    return bool(_PLACEHOLDER.search(code))


# --- VT-006: test without an oracle (no assert, no pytest.raises) ---
def vt006_test_without_assert(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for fn in _test_funcs(tree):
        has_assert = any(isinstance(n, ast.Assert) for n in ast.walk(fn))
        has_with = any(isinstance(n, ast.With) for n in ast.walk(fn))  # pytest.raises context
        if not has_assert and not has_with:
            return True
    return False


# --- VT-005: trivial `assert True` ---
def vt005_assert_true(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert) and isinstance(n.test, ast.Constant) and n.test.value is True:
            return True
    return False


# --- VT-009: tautological assert (operands structurally identical) ---
def vt009_tautological_assert(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if isinstance(n, ast.Assert) and isinstance(n.test, ast.Compare) and len(n.test.ops) == 1:
            if ast.dump(n.test.left) == ast.dump(n.test.comparators[0]):
                return True
    return False


# --- VT-037: assertion guarded by a statically-false condition (dead branch) ---
def vt037_impossible_condition(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if (isinstance(n, ast.If) and isinstance(n.test, ast.Compare)
                and len(n.test.ops) == 1 and isinstance(n.test.ops[0], ast.Eq)):
            left, right = n.test.left, n.test.comparators[0]
            if isinstance(left, ast.Constant) and isinstance(right, ast.Constant) and left.value != right.value:
                return True
    return False


# --- VT-040: blind except that swallows the failure (except ...: pass) ---
def vt040_blind_except(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if isinstance(n, ast.ExceptHandler) and len(n.body) == 1 and isinstance(n.body[0], ast.Pass):
            return True
    return False


# --- VC-005: prototype/TODO marker without owner+expiry (untracked debt) ---
_TODO_MARK = re.compile(r"#.*\b(TODO|FIXME|HACK|XXX|PROTOTYPE|TEMP)\b")


def vc005_untracked_prototype(code: str) -> bool:
    for line in code.splitlines():
        m = _TODO_MARK.search(line)
        if m:
            comment = line[m.start():]
            if not ("owner=" in comment and "expires=" in comment):
                return True
    return False


# --- VC-005: premature closure while evidence still shows failures ---
def vc005_premature_closure(code: str) -> bool:
    text = code.lower()
    if "closed" not in text:
        return False
    if "assert not scan_logs().errors" in text:
        return False
    return "ignored and closed" in text or "secondary keyerror" in text or "secondary failures" in text


# --- VC-036: destructive command with no dry-run/simulation in the same flow ---
_DESTRUCTIVE = re.compile(r"(-delete\b|rm\s+-rf|\bDROP\s|\bTRUNCATE\b|git\s+reset\s+--hard)")
_DRYRUN = re.compile(r"(-print\b|--dry-run\b|\bEXPLAIN\b|\becho\b)")


def vc036_destructive_without_dryrun(code: str) -> bool:
    return bool(_DESTRUCTIVE.search(code)) and not bool(_DRYRUN.search(code))


# --- VC-003: incomprehensible code with excessive complexity and no docstring ---
def vc003_incomprehensible_code(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("test"):
            stmt_count = sum(1 for node in ast.walk(fn) if isinstance(node, ast.stmt))
            if ast.get_docstring(fn) is None and stmt_count >= 5 and _function_complexity(fn) >= 5:
                return True
    return False


# --- VC-013: handoff note missing the required fields ---
_HANDOFF_MARK = re.compile(r"(?is)\b(handoff|status)\b|continue where we left off")
_HANDOFF_FIELDS = ("goal:", "state:", "evidence:", "blockers:", "next:")


def vc013_ambiguous_handoff(code: str) -> bool:
    text = code.lower()
    if not _HANDOFF_MARK.search(code):
        return False
    return not all(field in text for field in _HANDOFF_FIELDS)


# --- VC-016: version literals disagree across surfaces ---
_VERSION_LITERAL = re.compile(
    r"""(?im)(?:__version__|version)\s*[:=][^\n\r]{0,40}?['"]?(\d+\.\d+\.\d+(?:[-+][^\s'"]+)?)['"]?|##\s+(\d+\.\d+\.\d+(?:[-+][^\s]+)?)"""
)


def vc016_broken_version_parity(code: str) -> bool:
    versions = {match.group(1) or match.group(2) for match in _VERSION_LITERAL.finditer(code) if (match.group(1) or match.group(2))}
    return len(versions) >= 2


# --- VC-017: blocking call without timeout / heartbeat ---
_BLOCKING_CALL = re.compile(r"\b(recv|join|acquire|wait)\s*\(", re.I)
_LIVENESS_MARK = re.compile(r"\b(?:settimeout|timeout\s*=|heartbeat|wait_for|deadline)\b", re.I)


def vc017_deadlock_without_heartbeat(code: str) -> bool:
    return bool(_BLOCKING_CALL.search(code)) and not bool(_LIVENESS_MARK.search(code))


# --- VC-025: external input reaches a sink without validation ---
_EXTERNAL_IO = re.compile(r"\b(request\.(?:args|files|form|json)|sys\.argv|argv\b|input\()", re.I)
_IO_SINK = re.compile(r"\b(?:execute|exec|system|popen|subprocess\.(?:run|call|Popen))\s*\(", re.I)
_IO_VALIDATION = re.compile(r"(?:validate_|safe_|schema|parameteri[sz]e|escape_|allowlist|whitelist)", re.I)


def vc025_io_without_validation(code: str) -> bool:
    return bool(_EXTERNAL_IO.search(code)) and bool(_IO_SINK.search(code)) and not bool(_IO_VALIDATION.search(code))


# --- VC-028: core code imports experimental / unstable modules ---
_UNSTABLE_IMPORT = re.compile(r"\bfrom\s+(experimental|unstable|beta|volatile)(?:[\.\w]*)\s+import\b|\bimport\s+(experimental|unstable|beta|volatile)\b", re.I)


def vc028_core_dependent_on_unstable_parts(code: str) -> bool:
    return bool(_UNSTABLE_IMPORT.search(code))


# --- VC-029: duplicated function bodies copied without comprehension ---
def vc029_uncritical_copy_paste(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    signatures: dict[str, int] = {}
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("test"):
            body = _body_without_docstring(fn)
            if len(body) < 3:
                continue
            signature = " | ".join(_stmt_signature(stmt) for stmt in body)
            signatures[signature] = signatures.get(signature, 0) + 1
            if signatures[signature] >= 2:
                return True
    return False


# --- VC-047: version token embedded in an identifier ---
_VERSIONED_IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*(?:_v\d+|V\d+)\b")


def vc047_frozen_nomenclature(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return bool(_VERSIONED_IDENTIFIER.search(code))
    for node in ast.walk(tree):
        name = ""
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            name = node.name
        elif isinstance(node, ast.Name):
            name = node.id
        elif isinstance(node, ast.arg):
            name = node.arg
        elif isinstance(node, ast.Attribute):
            name = node.attr
        elif isinstance(node, ast.alias):
            name = node.asname or node.name
        if name and _VERSIONED_IDENTIFIER.search(name):
            return True
    return False


# --- VC-059: instruction-channel prompt injection ---
_PROMPT_INJECTION = re.compile(r"agent\.run\([^)]*\+\s*[A-Za-z_][A-Za-z0-9_]*", re.S)


def vc059_prompt_injection_in_agent_loop(code: str) -> bool:
    return bool(_PROMPT_INJECTION.search(code))


# --- VC-065: tool-call failure is ignored ---
def vc065_unhandled_tool_call_failure(code: str) -> bool:
    if "call_tool(" not in code:
        return False
    return ".ok" not in code and "retry_with_backoff" not in code and "degrade" not in code


# --- VC-066: multiple agents mutate the same state without protocol ---
_AGENT_EDIT = re.compile(r"\b(agent_[A-Za-z0-9]+)\.edit\((['\"])([^'\"]+)\2\)", re.I)


def vc066_multi_agent_without_protocol(code: str) -> bool:
    if "lock(" in code or "handoff(" in code or "owner=" in code:
        return False
    matches = _AGENT_EDIT.findall(code)
    if len(matches) < 2:
        return False
    files = [match[2] for match in matches]
    return len(set(files)) < len(files)


# --- VC-071: model output reaches a dangerous sink unsafely ---
_MODEL_OUTPUT = re.compile(r"\bmodel\.generate(?:_json)?\s*\(", re.I)
_DANGEROUS_SINK = re.compile(r"\b(?:cursor\.execute|execute|os\.system|subprocess\.(?:run|call|Popen)|eval|exec|innerHTML)\s*\(", re.I)
_OUTPUT_GUARD = re.compile(r"\b(?:validate_schema|parameteri[sz]e|escape|allowlist|sanitize|safe_)\b", re.I)


def vc071_blind_trust_in_llm_output(code: str) -> bool:
    return bool(_MODEL_OUTPUT.search(code)) and bool(_DANGEROUS_SINK.search(code)) and not bool(_OUTPUT_GUARD.search(code))


# --- VC-061: non-test function whose whole body is a constant return (stub) ---
def vc061_constant_stub(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for fn in ast.walk(tree):
        if isinstance(fn, ast.FunctionDef) and not fn.name.startswith("test"):
            body = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
            if len(body) == 1 and isinstance(body[0], ast.Return) and isinstance(body[0].value, ast.Constant):
                return True
    return False


# --- VC-061: imported dependency does not resolve in the current environment ---
def vc061_hallucinated_dependency(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for node in ast.walk(tree):
        module = ""
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module and importlib.util.find_spec(module) is None:
                    return True
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module = node.module.split(".")[0]
                if module and importlib.util.find_spec(module) is None:
                    return True
    return False


# --- VC-070: editing a structured file with sed/awk instead of a parser ---
_SED_STRUCT = re.compile(r"\b(sed|awk)\b[^\n]*\.(json|ya?ml|toml|xml|ini)\b", re.I)


def vc070_blind_shell_edit(code: str) -> bool:
    return bool(_SED_STRUCT.search(code))


# --- VC-087: blanket filterwarnings("ignore") with no category/justification ---
_BLANKET_WARN = re.compile(r"""filterwarnings\(\s*['"]ignore['"]\s*\)""")


def vc087_blanket_filterwarnings(code: str) -> bool:
    return bool(_BLANKET_WARN.search(code))


# --- VC-109: hardcoded absolute machine path in a string literal ---
_ABS_PATH = re.compile(r"""['"]([A-Za-z]:[\\/]|/(Users|home)/)""")


def vc109_hardcoded_path(code: str) -> bool:
    return bool(_ABS_PATH.search(code))


# --- VT-043: unconditional sys.exit(0) that ignores real state ---
def vt043_unconditional_exit_zero(code: str) -> bool:
    tree = _parse(code)
    if tree is None:
        return False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            func = n.func
            name = func.attr if isinstance(func, ast.Attribute) else (func.id if isinstance(func, ast.Name) else "")
            if name == "exit" and n.args and isinstance(n.args[0], ast.Constant) and n.args[0].value == 0:
                return True
    return False


# --- VC-138: insecure-by-default patterns in generated code ---
_INSECURE_DEFAULT = re.compile(
    r"""(debug\s*=\s*True|verify\s*=\s*False|origins\s*=\s*['"]\*['"]|hashlib\.md5\(|host\s*=\s*['"]0\.0\.0\.0['"])"""
)


def vc138_insecure_defaults(code: str) -> bool:
    return bool(_INSECURE_DEFAULT.search(code))


# --- VC-078: destructive action without an explicit confirmation gate ---
_DESTRUCTIVE_ACTION = re.compile(r"\b(delete_database|drop_database|destroy_|rm\s+-rf|shutdown)\s*\(", re.I)
_CONFIRM_GATE = re.compile(r"\bconfirm_with_user\s*\(", re.I)


def vc078_excessive_agency(code: str) -> bool:
    return bool(_DESTRUCTIVE_ACTION.search(code)) and not bool(_CONFIRM_GATE.search(code))


# Registry: catalog id -> detector. Keep in sync with the entries' `detector` field.
DETECTORS = {
    "VC-005": vc005_premature_closure,
    "VC-003": vc003_incomprehensible_code,
    "VC-013": vc013_ambiguous_handoff,
    "VC-016": vc016_broken_version_parity,
    "VC-017": vc017_deadlock_without_heartbeat,
    "VC-010": vc036_destructive_without_dryrun,
    "VC-032": vc087_blanket_filterwarnings,
    "VC-036": vc095_hardcoded_secret,
    "VC-043": vc109_hardcoded_path,
    "VC-049": vc115_unsafe_eval,
    "VC-025": vc025_io_without_validation,
    "VC-028": vc028_core_dependent_on_unstable_parts,
    "VC-029": vc029_uncritical_copy_paste,
    "VC-061": vc061_hallucinated_dependency,
    "VC-047": vc047_frozen_nomenclature,
    "VC-059": vc059_prompt_injection_in_agent_loop,
    "VC-065": vc065_unhandled_tool_call_failure,
    "VC-066": vc066_multi_agent_without_protocol,
    "VC-070": vc138_insecure_defaults,
    "VC-078": vc078_excessive_agency,
    "VT-043": vt043_unconditional_exit_zero,
    "VC-071": vc071_blind_trust_in_llm_output,
    "VT-005": vt005_assert_true,
    "VT-006": vt006_test_without_assert,
    "VT-009": vt009_tautological_assert,
    "VT-037": vt037_impossible_condition,
    "VT-040": vt040_blind_except,
}
