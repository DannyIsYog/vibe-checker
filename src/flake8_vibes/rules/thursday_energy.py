from __future__ import annotations

import ast
import random
from datetime import datetime

from flake8_vibes.git import get_file_commit_date
from flake8_vibes.rules.base import VibError, VibRule


def _is_thursday(filename: str) -> bool:
    """Return True if the file's last commit date (or today) is a Thursday."""
    dt = get_file_commit_date(filename)
    if dt is None:
        dt = datetime.now()
    return dt.weekday() == 3  # 3 = Thursday


def _count_lines(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    return (node.end_lineno or node.lineno) - node.lineno


# ── VIB001 — thursday-energy ─────────────────────────────────────────────────

_MESSAGES = [
    "'{name}' is {n} lines long and it's Thursday. you absolute menace.",
    "'{name}' has {n} lines of thursday ambition. friday will not save you from this.",
    "thursday energy fully detected in '{name}' ({n} lines). you were one day away. ONE day.",
    "'{name}' is {n} lines of pure thursday hubris. we felt it. the diff felt it.",
    "'{name}' ({n} lines) — a thursday crime committed in broad daylight.",
    "{n} lines. on a thursday. '{name}' didn't have to be like this and yet here we are.",
]


def _pick_message(name: str, n: int) -> str:
    return random.choice(_MESSAGES).format(name=name, n=n)


class ThursdayEnergyRule(VibRule):
    code = "VIB001"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        thursday = _is_thursday(filename)
        if not thursday:
            return errors
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                line_count = _count_lines(node)
                if line_count > 20:
                    msg = _pick_message(node.name, line_count)
                    prefix = f"VIB001 thursday energy detected: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
