from __future__ import annotations

import ast
import random
from datetime import datetime

from flake8_vibes.git import get_file_commit_date
from flake8_vibes.rules.base import VibError, VibRule

_MESSAGES = [
    "'{name}' is {n} lines long and it's Thursday. this could have waited.",
    "'{name}' has {n} lines of thursday ambition. friday will not fix this.",
    "thursday energy detected in '{name}' ({n} lines). you were so close to the weekend.",
    "'{name}' is {n} lines long. written on a thursday. we all felt it.",
    "'{name}' ({n} lines) — classic thursday overreach.",
    "did '{name}' really need to be {n} lines? it's thursday. go home.",
]


def _is_thursday(filename: str) -> bool:
    """Return True if the file's last commit date (or today) is a Thursday."""
    dt = get_file_commit_date(filename)
    if dt is None:
        dt = datetime.now()
    return dt.weekday() == 3  # 3 = Thursday


def _count_lines(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    return (node.end_lineno or node.lineno) - node.lineno


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
                    errors.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f"VIB001 thursday energy detected: {msg}",
                            type(self),
                        )
                    )
        return errors
