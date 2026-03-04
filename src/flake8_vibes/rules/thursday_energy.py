from __future__ import annotations

import ast
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
                    errors.append(
                        (
                            node.lineno,
                            node.col_offset,
                            f"VIB001 thursday energy detected: '{node.name}' is "
                            f"{line_count} lines long and it's Thursday",
                            type(self),
                        )
                    )
        return errors
