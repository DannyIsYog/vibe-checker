from __future__ import annotations

import ast
import random
from collections import deque
from collections.abc import Generator

from flake8_vibes.rules.base import VibError, VibRule

# helpers shared by VIB049


def _get_all_exports(tree: ast.AST) -> set[str]:
    """Names listed in module-level __all__."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets
        ):
            if isinstance(node.value, (ast.List, ast.Tuple)):
                return {
                    elt.value
                    for elt in node.value.elts
                    if isinstance(elt, ast.Constant) and isinstance(elt.value, str)
                }
    return set()


def _get_non_import_names(tree: ast.AST) -> set[str]:
    """All Name.id values that appear in non-import AST nodes."""
    used: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            used.add(node.id)
    return used


# ── VIB048 — import * ───────────────────────────────────────────────────────

_STAR_IMPORT_MESSAGES = [
    "`import *` — somewhere in this module is everything from that module, and you've made that everyone's problem.",
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
    "import inside a function: hiding a dependency where nobody would think to look.",
    "an import inside a function is a dependency that's embarrassed of itself.",
    "function-level imports are top-level imports that couldn't commit.",
    "an import buried in a function is either a hack or a secret. neither is good news.",
]


def _walk_no_nested_funcs(node: ast.AST) -> Generator[ast.AST, None, None]:
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


# ── VIB049 — unused import ───────────────────────────────────────────────────

_UNUSED_IMPORT_MESSAGES = [
    "you imported `{name}` and never used it. it stood in the corner all night.",
    "`{name}` was imported but never called upon. the meeting invite was sent. nobody came.",
    "found unused import `{name}`. it's taking up space and contributing nothing. like a bad variable.",
    "`{name}` was imported for a role that never materialized. the audition ended. the import remained.",
]


def _from_import_errors(
    node: ast.ImportFrom, used: set[str], rule_type: type
) -> list[VibError]:
    errors: list[VibError] = []
    for alias in node.names:
        if alias.name == "*":
            continue
        name = alias.asname if alias.asname else alias.name
        if name not in used:
            msg = random.choice(_UNUSED_IMPORT_MESSAGES).format(name=name)
            errors.append(
                (node.lineno, node.col_offset, f"VIB049 import: {msg}", rule_type)
            )
    return errors


def _plain_import_errors(
    node: ast.Import, used: set[str], rule_type: type
) -> list[VibError]:
    errors: list[VibError] = []
    for alias in node.names:
        name = alias.asname if alias.asname else alias.name.split(".")[0]
        if name not in used:
            msg = random.choice(_UNUSED_IMPORT_MESSAGES).format(name=name)
            errors.append(
                (node.lineno, node.col_offset, f"VIB049 import: {msg}", rule_type)
            )
    return errors


class UnusedImportRule(VibRule):
    code = "VIB049"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        used = _get_non_import_names(tree) | _get_all_exports(tree)
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module != "__future__":
                errors.extend(_from_import_errors(node, used, type(self)))
            elif isinstance(node, ast.Import):
                errors.extend(_plain_import_errors(node, used, type(self)))
        return errors


# ── VIB050 — __future__ import that does nothing in Python 3 ─────────────────

_DEAD_FUTURE_MESSAGES = [
    "`from __future__ import {name}` — the migration is over. this import never got the memo.",
    "`from __future__ import {name}`: a relic. an artifact. a commitment to the past nobody asked for.",
    "`from __future__ import {name}` is cargo-culted from a codebase that no longer exists.",
    "`{name}` from `__future__` — python 2 is gone. this import should be too.",
]

_DEAD_FUTURE_IMPORTS = frozenset(
    {
        "print_function",
        "unicode_literals",
        "division",
        "absolute_import",
        "with_statement",
        "generators",
        "nested_scopes",
        "generator_stop",
    }
)


class FutureImportDeadRule(VibRule):
    code = "VIB050"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ImportFrom):
                continue
            if node.module != "__future__":
                continue
            for alias in node.names:
                if alias.name in _DEAD_FUTURE_IMPORTS:
                    msg = random.choice(_DEAD_FUTURE_MESSAGES).format(name=alias.name)
                    prefix = f"VIB050 import: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB052 — importing os just to use os.path ────────────────────────────────

_OS_PATH_MESSAGES = [
    "`import os` for the sole purpose of `os.path` — that's a tribute to 2003 energy and nothing else.",
    "the entire `os` module, imported to use one thing: `os.path`. expensive taste, narrow purpose.",
    "`import os` and only using `os.path`. that's a big coat for very small shoulders.",
    "you imported all of `os` and left with only `os.path`. this is an inefficient heist.",
]


def _get_os_attr_names(tree: ast.AST) -> set[str]:
    """Return set of direct os.X attribute names used in the tree."""
    attrs: set[str] = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.value, ast.Name)
            and node.value.id == "os"
        ):
            attrs.add(node.attr)
    return attrs


def _find_os_imports(tree: ast.AST) -> list[ast.Import]:
    os_imports: list[ast.Import] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(alias.name == "os" and alias.asname is None for alias in node.names):
                os_imports.append(node)
    return os_imports


class OsPathImportRule(VibRule):
    code = "VIB052"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        os_imports = _find_os_imports(tree)
        if not os_imports:
            return []
        os_attrs = _get_os_attr_names(tree)
        if not (os_attrs and all(attr == "path" for attr in os_attrs)):
            return []
        errors: list[VibError] = []
        for node in os_imports:
            msg = random.choice(_OS_PATH_MESSAGES)
            prefix = f"VIB052 import: {msg}"
            errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
