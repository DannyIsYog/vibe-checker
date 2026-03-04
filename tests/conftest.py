from __future__ import annotations

import ast

import pytest


@pytest.fixture
def parse():
    """Return a helper that parses source code into an AST."""

    def _parse(source: str) -> ast.AST:
        return ast.parse(source)

    return _parse
