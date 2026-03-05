from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

_MAX_ARGS = 5
_MAX_RETURNS = 3
_MAX_NESTING = 4

_NESTING_NODES = (
    ast.If,
    ast.For,
    ast.While,
    ast.With,
    ast.Try,
    ast.AsyncFor,
    ast.AsyncWith,
)

# ── VIB030 — too-many-args ──────────────────────────────────────────────────

_TOO_MANY_ARGS_MESSAGES = [
    "'{name}' takes {n} arguments. that's not a function, that's a meeting agenda.",
    "'{name}' has {n} parameters. if you need that many, you need a dataclass.",
    "'{name}' accepts {n} arguments. your call sites are suffering in silence.",
    "'{name}' wants {n} things from you. healthy relationships have limits.",
    "'{name}' with {n} parameters is a cry for help dressed as an API.",
    "a function that takes {n} arguments has forgotten what abstraction is for.",
]


def _count_args(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    args = node.args
    count = len(args.args) + len(args.kwonlyargs)
    if args.vararg:
        count += 1
    if args.kwarg:
        count += 1
    if args.args and args.args[0].arg in ("self", "cls"):
        count -= 1
    return count


class TooManyArgsRule(VibRule):
    code = "VIB030"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                arg_count = _count_args(node)
                if arg_count > _MAX_ARGS:
                    msg_tpl = random.choice(_TOO_MANY_ARGS_MESSAGES)
                    msg = msg_tpl.format(name=node.name, n=arg_count)
                    prefix = f"VIB030 structure: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB031 — deep-nesting ───────────────────────────────────────────────────

_DEEP_NESTING_MESSAGES = [
    "indentation level {depth}: you have nested your way into a corner.",
    "nesting depth {depth} detected. your future self will not forgive this.",
    "depth {depth}. you can go deeper, but you really, really shouldn't.",
    "this code is nested {depth} levels deep. extract a function. any function.",
    "{depth} levels of nesting. the pyramid of doom is not an aspiration.",
    "nesting depth {depth}: the indentation knows something you won't admit.",
]


def _find_deep_nesting(
    node: ast.AST, depth: int, threshold: int, rule_type: type
) -> list[VibError]:
    errors: list[VibError] = []
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            errors.extend(_find_deep_nesting(child, 0, threshold, rule_type))
            continue
        if not isinstance(child, _NESTING_NODES):
            errors.extend(_find_deep_nesting(child, depth, threshold, rule_type))
            continue
        child_depth = depth + 1
        if child_depth > threshold:
            msg = random.choice(_DEEP_NESTING_MESSAGES).format(depth=child_depth)
            prefix = f"VIB031 structure: {msg}"
            errors.append((child.lineno, child.col_offset, prefix, rule_type))
        else:
            errors.extend(_find_deep_nesting(child, child_depth, threshold, rule_type))
    return errors


class DeepNestingRule(VibRule):
    code = "VIB031"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        return _find_deep_nesting(tree, 0, _MAX_NESTING, type(self))


# ── VIB032 — too-many-returns ───────────────────────────────────────────────

_TOO_MANY_RETURNS_MESSAGES = [
    "'{name}' has {n} return statements. pick an exit and commit to it.",
    "'{name}' returns {n} ways. a function should have one job and one door.",
    "{n} return statements in '{name}'. this function has commitment issues.",
    "'{name}' exits {n} times. every additional return is a missed refactor.",
    "'{name}' has {n} returns. the control flow is a choose-your-own-adventure.",
    "returning from '{name}' is a {n}-way tie. there's no winner here.",
]


def _count_returns(node: ast.AST) -> int:
    count = 0
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if isinstance(child, ast.Return):
            count += 1
        count += _count_returns(child)
    return count


class TooManyReturnsRule(VibRule):
    code = "VIB032"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                return_count = _count_returns(node)
                if return_count > _MAX_RETURNS:
                    msg_tpl = random.choice(_TOO_MANY_RETURNS_MESSAGES)
                    msg = msg_tpl.format(name=node.name, n=return_count)
                    prefix = f"VIB032 structure: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB033 — bare-except ────────────────────────────────────────────────────

_BARE_EXCEPT_MESSAGES = [
    "`except:` catches everything, including bugs you haven't written yet.",
    "bare `except` is a net cast wide enough to catch your future regrets.",
    "`except:` without a type is `except: pretend nothing happened`.",
    "catching every exception is not error handling, it's error avoidance.",
    "`except:` — the `*` of exception handling, and equally inadvisable.",
    "a bare `except` catches `KeyboardInterrupt`. think about what you've done.",
]


class BareExceptRule(VibRule):
    code = "VIB033"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                msg = random.choice(_BARE_EXCEPT_MESSAGES)
                prefix = f"VIB033 structure: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB034 — empty-except ───────────────────────────────────────────────────

_EMPTY_EXCEPT_MESSAGES = [
    "catching an exception and doing nothing is not error handling.",
    "`except: pass` is `I acknowledge this failure and choose to ignore it`.",
    "an except block with only `pass` is a suppressed scream.",
    "you caught the exception. now do something about it.",
    "`except: pass` — the code equivalent of sweeping it under the rug.",
    "silencing an exception with `pass` is not the same as fixing it.",
]


class EmptyExceptRule(VibRule):
    code = "VIB034"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ExceptHandler):
                continue
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                msg = random.choice(_EMPTY_EXCEPT_MESSAGES)
                prefix = f"VIB034 structure: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
