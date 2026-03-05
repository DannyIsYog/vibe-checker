from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB003 — except Exception cowardice ────────────────────────────────────

_EXCEPT_EXCEPTION_MESSAGES = [
    "`except Exception` is `except` for people who want credit for typing a word.",
    "catching `Exception` is a coward's `except:` wearing a tie.",
    "`except Exception` — you named it, but you still don't know what it is.",
    "catching `Exception` is the software equivalent of a shrug emoji and a 200 response.",
]


class ExceptExceptionRule(VibRule):
    code = "VIB003"

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
            if (
                node.type is not None
                and isinstance(node.type, ast.Name)
                and node.type.id == "Exception"
            ):
                msg = random.choice(_EXCEPT_EXCEPTION_MESSAGES)
                prefix = f"VIB003 exception: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB006 — generic raise ──────────────────────────────────────────────────

_RAISE_EXCEPTION_MESSAGES = [
    "`raise Exception(...)` is the error message equivalent of naming a file `file.txt`.",
    "`raise Exception(...)` — you described the crime in prose. the type system wanted a charge.",
    "`raise Exception(...)` — so you know something went wrong but not what. bold.",
    "generic `Exception` raise is a distress flare with no location data.",
]


class RaiseExceptionRule(VibRule):
    code = "VIB006"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Raise):
                continue
            if (
                node.exc is not None
                and isinstance(node.exc, ast.Call)
                and isinstance(node.exc.func, ast.Name)
                and node.exc.func.id == "Exception"
            ):
                msg = random.choice(_RAISE_EXCEPTION_MESSAGES)
                prefix = f"VIB006 exception: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB007 — re-raise without logging ────────────────────────────────────────

_RERAISE_NO_LOG_MESSAGES = [
    "the exception came, it was witnessed, it left. no record. no trace. no shame.",
    "you caught it, said nothing, and threw it back. the stack trace thanks you for nothing.",
    "caught and re-raised without a word. the perfect way to make debugging everyone else's problem.",
    "catching to re-raise with no evidence is how you guarantee the bug dies a mysterious death in production.",
]

_LOG_METHOD_NAMES = {"error", "warning", "warn", "info", "debug", "exception", "critical", "log"}


def _handler_has_logging(handler: ast.ExceptHandler) -> bool:
    for node in ast.walk(handler):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in _LOG_METHOD_NAMES:
                return True
    return False


class ReraiseNoLogRule(VibRule):
    code = "VIB007"

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
            reraises = [n for n in ast.walk(node) if isinstance(n, ast.Raise) and n.exc is None]
            if reraises and not _handler_has_logging(node):
                for reraise in reraises:
                    msg = random.choice(_RERAISE_NO_LOG_MESSAGES)
                    errors.append((reraise.lineno, reraise.col_offset, f"VIB007 exception: {msg}", type(self)))
        return errors
