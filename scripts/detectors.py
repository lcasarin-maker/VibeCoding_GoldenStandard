"""Real static detectors for falsifiable Golden Standard vices.

Each detector takes a code snippet (str) and returns True when the vice's signature
is present. They are proven against the catalog's own example_bad / example_good
corpus by test_detectors.py -- turning "falsifiable in principle" into "enforced here".

Detectors are intentionally small and conservative: they aim to fire on the cataloged
example_bad and stay silent on example_good, not to be production-grade linters. A
green test run is the contract: every registered detector discriminates its own pair.
"""
from __future__ import annotations

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


# --- VC-036: destructive command with no dry-run/simulation in the same flow ---
_DESTRUCTIVE = re.compile(r"(-delete\b|rm\s+-rf|\bDROP\s|\bTRUNCATE\b|git\s+reset\s+--hard)")
_DRYRUN = re.compile(r"(-print\b|--dry-run\b|\bEXPLAIN\b|\becho\b)")


def vc036_destructive_without_dryrun(code: str) -> bool:
    return bool(_DESTRUCTIVE.search(code)) and not bool(_DRYRUN.search(code))


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


# Registry: catalog id -> detector. Keep in sync with the entries' `detector` field.
DETECTORS = {
    "VC-005": vc005_untracked_prototype,
    "VC-036": vc036_destructive_without_dryrun,
    "VC-061": vc061_constant_stub,
    "VC-070": vc070_blind_shell_edit,
    "VC-087": vc087_blanket_filterwarnings,
    "VC-109": vc109_hardcoded_path,
    "VT-043": vt043_unconditional_exit_zero,
    "VC-078": vc078_placeholder,
    "VC-095": vc095_hardcoded_secret,
    "VC-115": vc115_unsafe_eval,
    "VT-005": vt005_assert_true,
    "VT-006": vt006_test_without_assert,
    "VT-009": vt009_tautological_assert,
    "VT-037": vt037_impossible_condition,
    "VT-040": vt040_blind_except,
}
