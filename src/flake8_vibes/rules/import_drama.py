from __future__ import annotations

import ast
import random
from collections import deque

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB048 — import * ───────────────────────────────────────────────────────

_STAR_IMPORT_MESSAGES = [
    "`import *` pollutes the namespace with everything and documents nothing.",
    "`from x import *` — you imported everything and now nothing has a known origin.",
    "a star import is `import *` of accountability. none taken.",
    "`import *` is the coding equivalent of dumping a bag onto the floor and calling it organized.",
]


class StarImportRule(VibRule):
    code = "VIB048"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == "*":
                        msg = random.choice(_STAR_IMPORT_MESSAGES)
                        prefix = f"VIB048 import: {msg}"
                        errors.append(
                            (node.lineno, node.col_offset, prefix, type(self))
                        )
        return errors


# ── VIB051 — import inside function ─────────────────────────────────────────

_IMPORT_IN_FUNCTION_MESSAGES = [
    "importing inside a function delays the problem, it doesn't solve it.",
    "an import inside a function is a dependency that's embarrassed of itself.",
    "function-level imports are top-level imports that couldn't commit.",
    "found an import inside a function. put it at the top where it belongs, like an adult.",
]


def _walk_no_nested_funcs(node: ast.AST):  # type: ignore[return]  # generator without return annotation
    """Walk AST but don't descend into nested function/async-function defs."""
    queue: deque[ast.AST] = deque(ast.iter_child_nodes(node))
    while queue:
        child = queue.popleft()
        yield child
        if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
            queue.extend(ast.iter_child_nodes(child))


class ImportInFunctionRule(VibRule):
    code = "VIB051"

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
            for child in _walk_no_nested_funcs(node):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    msg = random.choice(_IMPORT_IN_FUNCTION_MESSAGES)
                    prefix = f"VIB051 import: {msg}"
                    errors.append((child.lineno, child.col_offset, prefix, type(self)))
        return errors
