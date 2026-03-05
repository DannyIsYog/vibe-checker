from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB008 — print() left behind ────────────────────────────────────────────

_PRINT_MESSAGES = [
    "`print()` in production code is a confession you didn't write tests.",
    "found a `print()`. its parents are a logging module and a deadline you ignored.",
    "`print()` left behind — the printf debugging of someone who forgot to clean up.",
    "a `print()` call is a sticky note on production that says 'i was panicking'.",
]


class PrintLeftBehindRule(VibRule):
    code = "VIB008"

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
                and isinstance(node.func, ast.Name)
                and node.func.id == "print"
            ):
                msg = random.choice(_PRINT_MESSAGES)
                prefix = f"VIB008 debug: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB009 — breakpoint() in code ───────────────────────────────────────────

_BREAKPOINT_MESSAGES = [
    "`breakpoint()` committed to the codebase. you had one job.",
    "there is a `breakpoint()` here. this is a debugging session that escaped into the wild.",
    "`breakpoint()` in version control. brave. chaotic. absolutely incorrect.",
    "a stray `breakpoint()` — the cockroach of debugging artifacts.",
]


class BreakpointLeftBehindRule(VibRule):
    code = "VIB009"

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
                and isinstance(node.func, ast.Name)
                and node.func.id == "breakpoint"
            ):
                msg = random.choice(_BREAKPOINT_MESSAGES)
                prefix = f"VIB009 debug: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB010 — pdb.set_trace() ────────────────────────────────────────────────

_PDB_SET_TRACE_MESSAGES = [
    "`pdb.set_trace()` committed. the 90s called and they want their debugger back.",
    "`pdb.set_trace()` in your code is a time bomb with interactive mode.",
    "found `pdb.set_trace()`. this is not a feature, it is a scene of the crime.",
    "`pdb.set_trace()` — classic. also: not appropriate for version control.",
]


class PdbSetTraceRule(VibRule):
    code = "VIB010"

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
                and node.func.attr == "set_trace"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "pdb"
            ):
                msg = random.choice(_PDB_SET_TRACE_MESSAGES)
                prefix = f"VIB010 debug: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB011 — import pdb ──────────────────────────────────────────────────────

_IMPORT_PDB_MESSAGES = [
    "`import pdb` in committed code means the debugging session made it to production.",
    "you imported `pdb`. you forgot to remove it. these two facts are related.",
    "`import pdb` committed — the mark of someone who debugged live and never cleaned up.",
    "found `import pdb`. what were you doing, and did it work?",
]


def _node_imports_pdb(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(alias.name == "pdb" for alias in node.names)
    if isinstance(node, ast.ImportFrom):
        return node.module == "pdb"
    return False


class ImportPdbRule(VibRule):
    code = "VIB011"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if _node_imports_pdb(node):
                msg = random.choice(_IMPORT_PDB_MESSAGES)
                prefix = f"VIB011 debug: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB012 — console.log in .py file ─────────────────────────────────────────

_CONSOLE_LOG_MESSAGES = [
    "`console.log` is JavaScript's cry for help. this is Python. we have `print()`.",
    "found `console.log` in a `.py` file. the wrong language called, you answered.",
    "`console.log` in Python: someone switched languages and forgot to switch files.",
    "this is Python. `console.log` does not exist here. it never did. it never will.",
]

_CONSOLE_LOG_RE = re.compile(r"console\.log\s*\(", re.IGNORECASE)


class ConsoleLogInPyRule(VibRule):
    code = "VIB012"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            match = _CONSOLE_LOG_RE.search(line)
            if not match:
                continue
            before = line[: match.start()]
            if "#" in before or line.lstrip().startswith("#"):
                continue
            msg = random.choice(_CONSOLE_LOG_MESSAGES)
            errors.append((i + 1, 0, f"VIB012 debug: {msg}", type(self)))
        return errors
