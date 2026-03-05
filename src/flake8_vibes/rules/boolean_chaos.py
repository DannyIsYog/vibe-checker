from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule


def _is_const(node: ast.expr, value: object) -> bool:
    return isinstance(node, ast.Constant) and node.value is value


def _check_compare_against(
    tree: ast.AST,
    value: object,
    messages: list[str],
    code: str,
    rule_type: type,
) -> list[VibError]:
    errors: list[VibError] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        sides = [node.left, *node.comparators]
        for op, left, right in zip(node.ops, sides, sides[1:]):
            if not isinstance(op, ast.Eq):
                continue
            if _is_const(left, value) or _is_const(right, value):
                msg = random.choice(messages)
                prefix = f"{code} boolean chaos: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, rule_type))
    return errors


# ── VIB081 — equals-true ─────────────────────────────────────────────────────

_EQUALS_TRUE_MESSAGES = [
    "comparing to `True` explicitly is a trust issue with your own type system and honestly? it shows.",
    "`== True` — you already have a boolean. what are you waiting for. use it.",
    "if it's True it's True. asking Python to confirm doesn't make it more True.",
    "`== True` is a tautology wearing a trench coat. no one is fooled.",
    "your type system knows it's True. the question is why YOU don't.",
    "`== True`. the boolean was right there. you walked past it. why.",
]


class EqualsTrueRule(VibRule):
    code = "VIB081"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(
            tree, True, _EQUALS_TRUE_MESSAGES, self.code, type(self)
        )


# ── VIB082 — equals-false ────────────────────────────────────────────────────

_EQUALS_FALSE_MESSAGES = [
    "`if not x` was RIGHT THERE and you looked it dead in the face and typed `== False` anyway.",
    "`== False` is just `not` with extra steps, less confidence, and worse vibes.",
    "Python has a `not` keyword. it's been here since 1991. i'm begging you to use it.",
    "`== False` — asking Python to confirm what it already knows. exhausting for everyone.",
    "`if not x` exists. it has always existed. it will outlive us all.",
    "this is literally just `not x` in a trench coat and the coat isn't even good.",
]


class EqualsFalseRule(VibRule):
    code = "VIB082"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(
            tree, False, _EQUALS_FALSE_MESSAGES, self.code, type(self)
        )


# ── VIB083 — equals-none ─────────────────────────────────────────────────────

_EQUALS_NONE_MESSAGES = [
    "`is None` exists specifically for you and you chose `== None` anyway. rude.",
    "`== None` works until a `__eq__` override makes it your problem. and it will.",
    "None is a singleton. you identity-check singletons. this is not a debate.",
    "`== None` is technically allowed and spiritually a cry for help.",
    "`is None` has been here the whole time. waiting. patient. judging.",
    "PEP 8 asked nicely. flake8 asked sternly. we are not asking.",
]


class EqualsNoneRule(VibRule):
    code = "VIB083"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(
            tree, None, _EQUALS_NONE_MESSAGES, self.code, type(self)
        )


# ── VIB084 — not-equals ──────────────────────────────────────────────────────

_NOT_EQUALS_MESSAGES = [
    "`not x == y` is `x != y` with passive-aggressive energy and worse readability.",
    "you negated the entire comparison instead of just flipping the operator. bold choice. wrong choice.",
    "`!=` is one character. it is on your keyboard right now. i have seen it there.",
    "`not x == y` — the scenic route to a conclusion everyone else reached immediately.",
    "this is literally just `!=` in a disguise and the disguise is not working.",
    "operator precedence anxiety expressed as a crime against clarity.",
]


class NotEqualsRule(VibRule):
    code = "VIB084"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.UnaryOp):
                continue
            if not isinstance(node.op, ast.Not):
                continue
            if not isinstance(node.operand, ast.Compare):
                continue
            if any(isinstance(op, ast.Eq) for op in node.operand.ops):
                msg = random.choice(_NOT_EQUALS_MESSAGES)
                prefix = f"VIB084 boolean chaos: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
