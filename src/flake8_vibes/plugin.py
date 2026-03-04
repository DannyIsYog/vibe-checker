from __future__ import annotations

import ast
from collections.abc import Generator

from flake8_vibes import __version__
from flake8_vibes.rules import ALL_RULES, VibError


class VibesPlugin:
    name = "flake8-vibes"
    version = __version__

    def __init__(self, tree: ast.AST, filename: str = "<unknown>") -> None:
        self._tree = tree
        self._filename = filename

    def run(self) -> Generator[VibError, None, None]:
        for rule_class in ALL_RULES:
            yield from rule_class().check(self._tree, self._filename)
