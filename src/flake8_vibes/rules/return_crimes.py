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
    "`return None` is redundant. the function already returns `None` by doing nothing.",
    "explicit `return None` — you took the time to say nothing explicitly. python doesn't need this.",
    "`return None` is the statement of a function that doesn't know how to end gracefully.",
    "bare `return` was right there. `return None` is just more letters for the same silence.",
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
    "assign then immediately return — just return the expression. the variable adds nothing.",
    "you assigned a variable to return it one line later. that variable had a zero-line lifespan.",
    "intermediate variable assigned and immediately returned. cut the middleman.",
    "assign then return: two lines to do what one line could. bold choice. wrong choice.",
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


def _check_assign_return(
    body: list[ast.stmt], rule_type: type
) -> list[VibError]:
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
    "mutable default argument — this list is shared across every call. that is never what you wanted.",
    "a mutable default is a bug that hasn't introduced itself yet. it will.",
    "default mutable argument: the same object, every call, forever. use `None` and check.",
    "found a mutable default argument. it persists between calls. you will be confused later.",
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
                    errors.append(
                        (node.lineno, node.col_offset, prefix, type(self))
                    )
        return errors
