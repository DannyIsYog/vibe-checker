from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

_EQUALS_TRUE_MESSAGES = [
    "comparing to `True` explicitly is a trust issue with your own type system. use `if x:` instead — booleans are already truthy.",
    "`== True` — you already have a boolean, what more do you need. just write `if x:` and let it be.",
    "if it's True it's True. you don't have to check twice. `if x:` does everything `== True` does, with less insecurity.",
    "`== True` is a tautology wrapped in anxiety. the fix is `if x:` — Python evaluates booleans natively.",
    "your type system knows it's True. why don't you? drop the `== True` and just write `if x:`.",
    "comparing to `True` like you need a second opinion. you don't. `if x:` is all you need.",
]

_EQUALS_FALSE_MESSAGES = [
    "`if not x` was right there and you walked right past it. replace `== False` with `if not x:`.",
    "`== False` is just `not` with extra steps and less confidence. write `if not x:` instead.",
    "you compared to `False` like Python doesn't have a `not` keyword. it does. use `if not x:`.",
    "`== False` — you're asking Python to confirm what it already knows. `if not x:` is cleaner and idiomatic.",
    "`if not x` exists. it's been here the whole time. use it.",
    "this is `not x` in a trench coat. take the coat off. write `if not x:`.",
]

_EQUALS_NONE_MESSAGES = [
    "`is None` exists for a reason and that reason is you. None is a singleton — identity check with `is None`, not equality.",
    "`== None` works until it doesn't. `is None` always does. PEP 8 E711: use `if x is None:`.",
    "None is a singleton. you don't compare singletons with `==`. use `is None` — it checks identity, not equality.",
    "`== None` is technically fine and spiritually wrong. `is None` is the idiomatic Python way, and mypy will thank you.",
    "`is None` was right there. it's always been right there. swap `== None` for `is None` and sleep better.",
    "PEP 8 asked nicely. we're asking less nicely. use `is None` — `==` can be overridden by `__eq__`, `is` cannot.",
]

_NOT_EQUALS_MESSAGES = [
    "`not x == y` is `x != y` with passive-aggressive energy. just write `x != y`.",
    "you negated the whole comparison instead of flipping the operator. `x != y` is cleaner and means the same thing.",
    "`!=` exists. it's one character. it's right there on your keyboard. use `x != y` instead of `not x == y`.",
    "`not x == y` — the long way around to say something simple. the short way is `x != y`.",
    "this is `!=` in disguise and the disguise is bad. write `x != y` — it's explicit, readable, and correct.",
    "operator precedence anxiety expressed as code. `not x == y` works but `x != y` says what you mean directly.",
]


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
                errors.append((node.lineno, node.col_offset, f"{code} boolean chaos: {msg}", rule_type))
    return errors


class EqualsTrueRule(VibRule):
    code = "VIB081"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(tree, True, _EQUALS_TRUE_MESSAGES, self.code, type(self))


class EqualsFalseRule(VibRule):
    code = "VIB082"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(tree, False, _EQUALS_FALSE_MESSAGES, self.code, type(self))


class EqualsNoneRule(VibRule):
    code = "VIB083"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _check_compare_against(tree, None, _EQUALS_NONE_MESSAGES, self.code, type(self))


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
                errors.append((node.lineno, node.col_offset, f"VIB084 boolean chaos: {msg}", type(self)))
        return errors
