from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB003 — except Exception cowardice ────────────────────────────────────

_EXCEPT_EXCEPTION_MESSAGES = [
    "`except Exception` is `except` for people who want credit for typing a word.",
    "catching `Exception` is a coward's `except:` wearing a tie.",
    "`except Exception` — you named it, but you still don't know what it is.",
    "catching `Exception` means you're handling every error the same. that is not handling errors.",
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
    "raised `Exception` with a message. a specific exception type was right there and you walked past it.",
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
