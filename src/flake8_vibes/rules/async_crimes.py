from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB074 — async function that never awaits ────────────────────────────────

_ASYNC_NO_AWAIT_MESSAGES = [
    "async function with no `await` — this is a synchronous function wearing a costume.",
    "`async def` without `await` is a promise that keeps none of its promises.",
    "found an `async` function that never awaits anything. it's async in name only.",
    "this function is `async` but does nothing async. the `async` keyword is lying.",
]


def _has_await(node: ast.AST) -> bool:
    """Walk node looking for Await, but skip nested function definitions."""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if isinstance(child, ast.Await):
            return True
        if _has_await(child):
            return True
    return False


class AsyncNoAwaitRule(VibRule):
    code = "VIB074"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef):
                if not _has_await(node):
                    msg = random.choice(_ASYNC_NO_AWAIT_MESSAGES)
                    prefix = f"VIB074 async: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB076 — asyncio.sleep(0) ────────────────────────────────────────────────

_ASYNCIO_SLEEP_0_MESSAGES = [
    "`asyncio.sleep(0)` is a yield to the event loop disguised as a nap.",
    "`asyncio.sleep(0)` — a zero-duration nap with a lot of unstated intent.",
    "`asyncio.sleep(0)`: the number zero, doing the work of an entire explanation.",
    "`asyncio.sleep(0)` is a handshake with the event loop that nobody documented.",
]


def _is_asyncio_sleep_zero(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "sleep"
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "asyncio"
        and bool(node.args)
        and isinstance(node.args[0], ast.Constant)
        and node.args[0].value == 0
    )


class AsyncioSleep0Rule(VibRule):
    code = "VIB076"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if _is_asyncio_sleep_zero(node):
                msg = random.choice(_ASYNCIO_SLEEP_0_MESSAGES)
                prefix = f"VIB076 async: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
