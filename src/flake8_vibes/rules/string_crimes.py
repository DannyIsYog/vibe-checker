from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB077 — string concat in loop ──────────────────────────────────────────

_STRING_CONCAT_LOOP_MESSAGES = [
    "string `+=` in a loop is O(n²) performance and a betrayal of `str.join`.",
    "concatenating strings in a loop. `''.join(...)` exists and it is faster and you know it.",
    "string `+=` inside a loop — every iteration copies the whole string. this is not fine.",
    "loop string concatenation detected. collect, then join. that's the contract.",
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
    "`%` string formatting hasn't been recommended since Python 2. it's 2024. let go.",
    "found `%` string formatting. f-strings exist. they're right there. use them.",
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
    "`.format()` with positional args — an f-string would have been shorter and readable.",
    "`str.format()` positional args: you made the reader count braces. use an f-string.",
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
