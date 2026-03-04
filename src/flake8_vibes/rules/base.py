from __future__ import annotations

import ast

VibError = tuple[int, int, str, type]


class VibRule:
    code: str

    def check(self, tree: ast.AST, filename: str = "<unknown>") -> list[VibError]:
        raise NotImplementedError
