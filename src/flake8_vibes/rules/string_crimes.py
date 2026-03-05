from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB077 — string concat in loop ──────────────────────────────────────────

_STRING_CONCAT_LOOP_MESSAGES = [
    "string concatenation inside a loop — a performance crime committed with zero ceremony.",
    "strings concatenated in a loop. somewhere a CPU fan just spun up in protest.",
    "string `+=` inside a loop — every iteration copies the whole string. this is not fine.",
    "string `+=` inside a loop: a decision with compounding consequences and no remorse.",
]


def _is_string_aug_add(child: ast.AST) -> bool:
    """Return True if child is a string AugAssign with Add op."""
    if not (isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add)):
        return False
    if isinstance(child.value, ast.JoinedStr):
        return True
    return isinstance(child.value, ast.Constant) and isinstance(child.value.value, str)


class StringConcatInLoopRule(VibRule):
    code = "VIB077"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if _is_string_aug_add(child):
                        msg = random.choice(_STRING_CONCAT_LOOP_MESSAGES)
                        prefix = f"VIB077 string: {msg}"
                        errors.append(
                            (child.lineno, child.col_offset, prefix, type(self))
                        )
        return errors


# ── VIB078 — % formatting ────────────────────────────────────────────────────

_PERCENT_FORMAT_MESSAGES = [
    "percent formatting in 2026. a choice. a baffling, deliberately backward choice.",
    "`%` formatting: the rotary phone of string interpolation. still technically works. still wrong.",
    "`'%s' % value` — the formatting of someone who learned Python in a different era.",
    "percent formatting: because you wanted your strings to feel like C. they don't need to.",
]


class PercentFormatRule(VibRule):
    code = "VIB078"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.BinOp)
                and isinstance(node.op, ast.Mod)
                and isinstance(node.left, ast.Constant)
                and isinstance(node.left.value, str)
            ):
                msg = random.choice(_PERCENT_FORMAT_MESSAGES)
                prefix = f"VIB078 string: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB079 — .format() with positional-only args ────────────────────────────

_FORMAT_POSITIONAL_MESSAGES = [
    "`.format()` with positional args: a puzzle where you count `{}` brackets to understand it.",
    "positional `.format()` args: numbered slots, no names, maximum confusion per bracket.",
    "positional `.format()` call: the f-string was invented so you wouldn't do this.",
    "`.format(a, b)` with positional args. f-strings are not a trend, they're an improvement.",
]


class FormatPositionalRule(VibRule):
    code = "VIB079"

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
                and node.func.attr == "format"
                and node.args
                and not node.keywords
            ):
                msg = random.choice(_FORMAT_POSITIONAL_MESSAGES)
                prefix = f"VIB079 string: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB080 — multiline string that's just a long comment ─────────────────────

_MULTILINE_COMMENT_MESSAGES = [
    "triple-quoted string hanging in the code, unassigned, pretending to be a comment. it isn't.",
    "this string is not a comment. it is a string expression that is doing absolutely nothing productive.",
    "a triple-quoted string with no assignment is a docstring without a home.",
    "a multiline string, unassigned, unowned, doing the dirty work of a comment with none of the honesty.",
]


def _collect_docstring_node_ids(tree: ast.AST) -> set[int]:
    """Return id()s of Expr nodes that are legitimate docstrings."""
    ids: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(
            node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)
        ):
            if (
                node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, ast.Constant)
                and isinstance(node.body[0].value.value, str)
            ):
                ids.add(id(node.body[0]))
    return ids


class MultilineStringCommentRule(VibRule):
    code = "VIB080"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        docstring_ids = _collect_docstring_node_ids(tree)
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Constant)
                and isinstance(node.value.value, str)
                and "\n" in node.value.value
                and id(node) not in docstring_ids
            ):
                msg = random.choice(_MULTILINE_COMMENT_MESSAGES)
                prefix = f"VIB080 string: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
