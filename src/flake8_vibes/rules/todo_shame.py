from __future__ import annotations

import ast
import re

from flake8_vibes.rules.base import VibError, VibRule

_PATTERN = re.compile(r"#\s*(TODO|FIXME)\b", re.IGNORECASE)


class TodoShameRule(VibRule):
    code = "VIB002"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for lineno, line in enumerate(lines, start=1):
            match = _PATTERN.search(line)
            if match:
                tag = match.group(1).upper()
                col = match.start()
                errors.append(
                    (
                        lineno,
                        col,
                        f"VIB002 todo shame: unresolved {tag} left to rot",
                        type(self),
                    )
                )
        return errors
