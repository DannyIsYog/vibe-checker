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
    "comparing to `True` explicitly is a trust issue with your own type system.",
    "`== True` — you already have a boolean, what more do you need.",
    "if it's True it's True. you don't have to check twice.",
    "`== True` is a tautology wrapped in anxiety.",
    "your type system knows it's True. why don't you?",
    "comparing to `True` like you need a second opinion. you don't.",
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
    "`if not x` was right there and you walked right past it.",
    "`== False` is just `not` with extra steps and less confidence.",
    "you compared to `False` like Python doesn't have a `not` keyword. it does.",
    "`== False` — you're asking Python to confirm what it already knows.",
    "`if not x` exists. it's been here the whole time.",
    "this is `not x` in a trench coat.",
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
    "`is None` exists for a reason and that reason is you.",
    "`== None` works until it doesn't.",
    "None is a singleton. you don't compare singletons with `==`.",
    "`== None` is technically fine and spiritually wrong.",
    "`is None` was right there. it's always been right there.",
    "PEP 8 asked nicely. we're asking less nicely.",
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
    "`not x == y` is `x != y` with passive-aggressive energy.",
    "you negated the whole comparison instead of flipping the operator.",
    "`!=` exists. it's one character. it's right there on your keyboard.",
    "`not x == y` — the long way around to say something simple.",
    "this is `!=` in disguise and the disguise is bad.",
    "operator precedence anxiety expressed as code.",
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
