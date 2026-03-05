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

# ── VIB053 — explicit return None ───────────────────────────────────────────

_EXPLICIT_RETURN_NONE_MESSAGES = [
    "`return None` — you wrote an explicit statement to achieve what silence would have accomplished.",
    "`return None` is loud about doing nothing. that's a personality flaw in a function.",
    "`return None` is the statement of a function that doesn't know how to end gracefully.",
    "`return None` — explicit, deliberate, and exactly what the implicit behavior was going to do anyway.",
]


class ExplicitReturnNoneRule(VibRule):
    code = "VIB053"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Return)
                and node.value is not None
                and isinstance(node.value, ast.Constant)
                and node.value.value is None
            ):
                msg = random.choice(_EXPLICIT_RETURN_NONE_MESSAGES)
                prefix = f"VIB053 return: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB054 — assign then immediately return ──────────────────────────────────

_ASSIGN_RETURN_MESSAGES = [
    "assigned to a variable, returned it immediately. that variable lived one line and contributed nothing.",
    "you assigned a variable to return it one line later. that variable had a zero-line lifespan.",
    "named it to immediately return it. the variable never had a chance to matter.",
    "two statements where one would have done. the extra line is doing nothing and being paid for it.",
]


def _is_assign_then_return(stmt: ast.stmt, next_stmt: ast.stmt) -> bool:
    if not (isinstance(stmt, ast.Assign) and len(stmt.targets) == 1):
        return False
    if not isinstance(stmt.targets[0], ast.Name):
        return False
    target_name = stmt.targets[0].id
    return (
        isinstance(next_stmt, ast.Return)
        and next_stmt.value is not None
        and isinstance(next_stmt.value, ast.Name)
        and next_stmt.value.id == target_name
    )


def _check_assign_return(body: list[ast.stmt], rule_type: type) -> list[VibError]:
    errors: list[VibError] = []
    for i in range(len(body) - 1):
        if _is_assign_then_return(body[i], body[i + 1]):
            msg = random.choice(_ASSIGN_RETURN_MESSAGES)
            prefix = f"VIB054 return: {msg}"
            errors.append((body[i].lineno, body[i].col_offset, prefix, rule_type))
    return errors


class AssignThenReturnRule(VibRule):
    code = "VIB054"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                errors.extend(_check_assign_return(node.body, type(self)))
        return errors


# ── VIB055 — mutable default argument ───────────────────────────────────────

_MUTABLE_DEFAULT_MESSAGES = [
    "mutable default argument: the gift that keeps giving, unsolicited, across every call forever.",
    "a mutable default is a bug that hasn't introduced itself yet. it will.",
    "a mutable default that persists between calls — a state machine you didn't know you built.",
    "a mutable default argument. it will outlive your understanding of why it's there.",
]


class MutableDefaultArgRule(VibRule):
    code = "VIB055"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for default in node.args.defaults + node.args.kw_defaults:
                if default is None:
                    continue
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    msg = random.choice(_MUTABLE_DEFAULT_MESSAGES)
                    prefix = f"VIB055 return: {msg}"
                    errors.append(
                        (default.lineno, default.col_offset, prefix, type(self))
                    )
        return errors


# ── VIB056 — shadowing a builtin ─────────────────────────────────────────────

_SHADOW_BUILTIN_MESSAGES = [
    "you named your variable `{name}`, which shadows the builtin. python is very forgiving. you should not be.",
    "`{name}` is a builtin. you just overwrote it. your future `{name}()` calls thank you for the confusion.",
    "shadowing `{name}` with an assignment. now `{name}` means something different and everyone is worse off.",
    "variable named `{name}` shadows the builtin. this is the naming equivalent of stepping on a rake.",
]


class ShadowBuiltinRule(VibRule):
    code = "VIB056"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in _BUILTINS:
                    msg_tpl = random.choice(_SHADOW_BUILTIN_MESSAGES)
                    msg = msg_tpl.format(name=target.id)
                    prefix = f"VIB056 return: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB057 — assigning to _ and then using it ────────────────────────────────

_UNDERSCORE_USED_MESSAGES = [
    "you assigned to `_` to signal you don't need it, then used it anyway. pick a side.",
    "`_ = x` followed by use of `_`: the variable you said you didn't want is being used.",
    "assigned to `_` and then loaded `_`. that's not discard, that's a variable with an identity crisis.",
    "`_` means 'i don't need this'. using it afterward means you lied. use a real name.",
]


def _has_discard_assign(tree: ast.AST) -> bool:
    return any(
        isinstance(node, ast.Assign)
        and len(node.targets) == 1
        and isinstance(node.targets[0], ast.Name)
        and node.targets[0].id == "_"
        for node in ast.walk(tree)
    )


def _call_func_ids(tree: ast.AST) -> set[int]:
    return {id(node.func) for node in ast.walk(tree) if isinstance(node, ast.Call)}


def _is_used_discard(node: ast.AST, call_funcs: set[int]) -> bool:
    return (
        isinstance(node, ast.Name)
        and node.id == "_"
        and isinstance(node.ctx, ast.Load)
        and id(node) not in call_funcs
    )


class UnderscoreUsedRule(VibRule):
    code = "VIB057"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if not _has_discard_assign(tree):
            return []
        call_funcs = _call_func_ids(tree)
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if _is_used_discard(node, call_funcs):
                msg = random.choice(_UNDERSCORE_USED_MESSAGES)
                prefix = f"VIB057 return: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
