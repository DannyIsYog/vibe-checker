from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

_BUILTINS = {
    "list",
    "dict",
    "set",
    "tuple",
    "int",
    "str",
    "float",
    "bool",
    "bytes",
    "type",
    "id",
    "input",
    "len",
    "range",
    "object",
}

# ── VIB089 — lambda assigned to variable ─────────────────────────────────────

_LAMBDA_ASSIGNED_MESSAGES = [
    "lambda assigned to a variable is a function that's embarrassed to be one. use `def`.",
    "`x = lambda ...` — that lambda has a name now. it's called a function. use `def`.",
    "assigning a lambda to a variable is writing an anonymous function and then naming it anyway.",
    "a named lambda is a `def` in denial. end the charade.",
]


class LambdaAssignedRule(VibRule):
    code = "VIB089"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            value: ast.expr | None = None
            if isinstance(node, ast.Assign):
                value = node.value
            elif isinstance(node, ast.AnnAssign):
                value = node.value
            if value is not None and isinstance(value, ast.Lambda):
                msg = random.choice(_LAMBDA_ASSIGNED_MESSAGES)
                prefix = f"VIB089 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB090 — global statement ────────────────────────────────────────────────

_GLOBAL_MESSAGES = [
    "`global` — the last resort of someone who ran out of better ideas and didn't notice.",
    "a `global` statement: the flag that a function has too much reach and too little shame.",
    "a `global` statement: the codebase just became a little harder to reason about. again.",
    "found `global`. shared mutable state and a deadline — two things that end badly together.",
]


class GlobalStatementRule(VibRule):
    code = "VIB090"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Global):
                msg = random.choice(_GLOBAL_MESSAGES)
                prefix = f"VIB090 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB091 — eval() ──────────────────────────────────────────────────────────

_EVAL_MESSAGES = [
    "`eval()` — the escape hatch that opens directly onto a security incident.",
    "you reached for `eval()`. this is where the postmortem starts.",
    "`eval()` is a code injection vulnerability that hasn't happened yet.",
    "using `eval()` is trusting the input more than the codebase deserves.",
]


class EvalUsedRule(VibRule):
    code = "VIB091"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "eval"
            ):
                msg = random.choice(_EVAL_MESSAGES)
                prefix = f"VIB091 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB092 — exec() ──────────────────────────────────────────────────────────

_EXEC_MESSAGES = [
    "`exec()` — you gave the string a compiler and a press badge and wished it luck.",
    "found `exec()`. this is not a templating engine. it is a disaster waiting for input.",
    "`exec()` detected. the security review is going to be a lot of fun.",
    "using `exec()` means you ran out of ideas and decided the string was the idea.",
]


class ExecUsedRule(VibRule):
    code = "VIB092"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "exec"
            ):
                msg = random.choice(_EXEC_MESSAGES)
                prefix = f"VIB092 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB094 — file longer than 500 lines ─────────────────────────────────────

_FILE_TOO_LONG_MESSAGES = [
    "{n} lines in one file. you built a city and called it a street address.",
    "{n} lines in one file. that's not a module, that's a monolith with an extension.",
    "file at {n} lines: long enough to have districts, neighborhoods, and feuds.",
    "{n} lines detected. at some point a file becomes a problem. that point was 500 lines ago.",
]

_MAX_FILE_LINES = 500


class FileTooLongRule(VibRule):
    code = "VIB094"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        line_count = len(lines)
        if line_count > _MAX_FILE_LINES:
            msg_tpl = random.choice(_FILE_TOO_LONG_MESSAGES)
            msg = msg_tpl.format(n=line_count)
            prefix = f"VIB094 misc: {msg}"
            return [(1, 0, prefix, type(self))]
        return []


# ── VIB095 — nested comprehension 3+ levels ──────────────────────────────────

_NESTED_COMPREHENSION_MESSAGES = [
    "3 layers of comprehension nesting. you can read it once, today, while you still remember what you were thinking.",
    "comprehension at depth 3+. elegant on the outside. impenetrable from any angle.",
    "nested comprehension stacked 3+ deep. this is a puzzle, not a feature.",
    "comprehensions nested this deep are a debugging session nobody wants to schedule.",
]

_COMP_TYPES = (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)
_NESTED_COMP_MIN_DEPTH = 3


def _max_comp_depth_in(node: ast.AST) -> int:
    """Return the max comprehension depth rooted at any comprehension inside node (inclusive)."""
    if isinstance(node, _COMP_TYPES):
        return _comprehension_depth(node)
    max_depth = 0
    for child in ast.iter_child_nodes(node):
        child_depth = _max_comp_depth_in(child)
        if child_depth > max_depth:
            max_depth = child_depth
    return max_depth


def _comprehension_depth(node: ast.AST) -> int:
    """Return the nesting depth of this comprehension node (1 = no nested comps in iters)."""
    if not isinstance(node, _COMP_TYPES):
        return 0
    max_child = 0
    for generator in node.generators:
        iter_depth = _max_comp_depth_in(generator.iter)
        if iter_depth > max_child:
            max_child = iter_depth
    return 1 + max_child


class NestedComprehensionRule(VibRule):
    code = "VIB095"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, _COMP_TYPES):
                if _comprehension_depth(node) >= _NESTED_COMP_MIN_DEPTH:
                    msg = random.choice(_NESTED_COMPREHENSION_MESSAGES)
                    prefix = f"VIB095 misc: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB096 — dict() constructor ──────────────────────────────────────────────

_DICT_CONSTRUCTOR_MESSAGES = [
    "`dict(key=value)` — the constructor nobody asked for, doing the job a literal handles fine.",
    "using `dict()` with keywords instead of a literal. the braces were right there.",
    "`dict(a=1, b=2)` — a constructor doing the work of a literal and doing it worse.",
    "found `dict()` constructor with keywords. a dict literal would have been fine.",
]


class DictConstructorRule(VibRule):
    code = "VIB096"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "dict"
                and node.keywords
            ):
                msg = random.choice(_DICT_CONSTRUCTOR_MESSAGES)
                prefix = f"VIB096 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB097 — list() around list literal ──────────────────────────────────────

_LIST_AROUND_LITERAL_MESSAGES = [
    "`list([...])` — you already had a list. you made another list of the list.",
    "wrapping a list literal in `list()` is redundant and slightly insulting.",
    "`list([...])` — a list, wrapped in a list constructor, for no reward and no reason.",
    "found `list([...])`. the brackets were doing fine on their own.",
]


class ListAroundLiteralRule(VibRule):
    code = "VIB097"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "list"
                and node.args
                and isinstance(node.args[0], ast.List)
            ):
                msg = random.choice(_LIST_AROUND_LITERAL_MESSAGES)
                prefix = f"VIB097 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB098 — assert in non-test code ─────────────────────────────────────────

_ASSERT_NON_TEST_MESSAGES = [
    "`assert` in production: a boundary condition that vanishes the moment someone runs python with a flag.",
    "`assert` outside tests: a guard that can be silenced and a guarantee that can't be trusted.",
    "`assert` in production code: an invariant that only holds if nobody optimizes the interpreter.",
    "production `assert` — a condition that exists when convenient and evaporates when optimized.",
]


class AssertInNonTestRule(VibRule):
    code = "VIB098"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if "test" in filename.lower():
            return []
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assert):
                msg = random.choice(_ASSERT_NON_TEST_MESSAGES)
                prefix = f"VIB098 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB099 — sys.exit() ──────────────────────────────────────────────────────

_SYS_EXIT_MESSAGES = [
    "`sys.exit()` in library code: an overreach with a scorched-earth policy and no survivors.",
    "`sys.exit()` buried in a library. the whole process just got an opinion it didn't ask for.",
    "`sys.exit()` — a library function that decides it's done with everything. bold.",
    "calling `sys.exit()` in non-entry-point code is forcing the process to agree with you.",
]


class SysExitRule(VibRule):
    code = "VIB099"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "exit"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "sys"
            ):
                msg = random.choice(_SYS_EXIT_MESSAGES)
                prefix = f"VIB099 misc: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB093 — __all__ that includes private names ─────────────────────────────

_ALL_PRIVATE_MESSAGES = [
    "exporting `{name}` in `__all__` — names starting with `_` are private by convention. you're breaking the contract.",
    "`__all__` includes `{name}`. private names in `__all__` is mixed messaging at the API boundary.",
    "found `{name}` in `__all__`. underscores mean 'not public'. `__all__` means 'public'. pick one.",
    "`{name}` is in `__all__` but starts with `_`. that's not an export, that's a contradiction.",
]


def _private_exports_in_assign(node: ast.Assign, rule_type: type) -> list[VibError]:
    if not any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
        return []
    if not isinstance(node.value, (ast.List, ast.Tuple)):
        return []
    errors: list[VibError] = []
    for elt in node.value.elts:
        if isinstance(elt, ast.Constant) and isinstance(elt.value, str) and elt.value.startswith("_"):
            msg = random.choice(_ALL_PRIVATE_MESSAGES).format(name=elt.value)
            errors.append((elt.lineno, elt.col_offset, f"VIB093 misc: {msg}", rule_type))
    return errors


class AllExportsPrivateRule(VibRule):
    code = "VIB093"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                errors.extend(_private_exports_in_assign(node, type(self)))
        return errors


# ── VIB100 — zero-star repo energy ───────────────────────────────────────────

_ZERO_STAR_MESSAGES = [
    "this file has no functions, no classes, and is mostly print statements. that's a script, not a module.",
    "found a file that's just print() calls with no structure. local legend, not a feature.",
    "no functions. no classes. just print(). this is not software, it's a terminal session committed to git.",
    "this file consists of print() calls and ambition. the ambition is not load-bearing.",
]

_ZERO_STAR_MIN_PRINTS = 5


class ZeroStarRepoRule(VibRule):
    code = "VIB100"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        all_nodes = list(ast.walk(tree))
        has_structure = any(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) for n in all_nodes)
        if has_structure:
            return []
        print_count = sum(
            1 for n in all_nodes
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print"
        )
        if print_count >= _ZERO_STAR_MIN_PRINTS:
            return [(1, 0, f"VIB100 misc: {random.choice(_ZERO_STAR_MESSAGES)}", type(self))]
        return []
