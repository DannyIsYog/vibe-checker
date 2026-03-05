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
    "`global` is a way of saying 'i couldn't figure out how to pass this as an argument'.",
    "a `global` statement: the flag that a function has too much reach and too little shame.",
    "`global` used. functions should take arguments and return values. that's the deal.",
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
    "`eval()` executes arbitrary code. if you know what you're doing, you don't need it.",
    "found `eval()`. whatever you're parsing, there is a safer way. find it.",
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
    "`exec()` runs strings as code. strings are not code. or they are, and that's the problem.",
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
    "this file is {n} lines long. a file is not a novel. split it.",
    "{n} lines in one file. that's not a module, that's a monolith with an extension.",
    "file has {n} lines. files above 500 lines have given up on cohesion.",
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
    "comprehension nested 3+ levels deep. you've made something unreadable and called it clever.",
    "3+ levels of comprehension nesting: you can write it. nobody else can read it. that's the problem.",
    "nested comprehension hell detected. extract a variable. write a loop. be kind.",
    "comprehensions nested this deep are a debugging session nobody wants to schedule.",
]

_COMP_TYPES = (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)


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
                if _comprehension_depth(node) >= 3:
                    msg = random.choice(_NESTED_COMPREHENSION_MESSAGES)
                    prefix = f"VIB095 misc: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB096 — dict() constructor ──────────────────────────────────────────────

_DICT_CONSTRUCTOR_MESSAGES = [
    "`dict(key=value)` — `{'key': value}` is shorter, faster, and obvious.",
    "using `dict()` with keywords instead of a literal. the braces were right there.",
    "`dict(a=1, b=2)` is `{'a': 1, 'b': 2}` with more typing and worse performance.",
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
    "`list([1, 2, 3])` is `[1, 2, 3]` with extra steps and no benefits.",
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
    "`assert` in production code is removed by `-O`. your invariant just stopped existing.",
    "found `assert` outside tests. assertions are not validation. use an `if` and raise.",
    "`assert` in non-test code can be silenced with `python -O`. that is not a feature.",
    "production `assert` — removed by the optimizer, violated by the user. use a real check.",
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
    "`sys.exit()` in library code exits the entire process. that's the caller's call to make.",
    "found `sys.exit()`. raise an exception. let the top-level decide how to die.",
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
