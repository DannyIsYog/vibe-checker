from __future__ import annotations

import ast

import pytest

from flake8_vibes.rules.thursday_energy import ThursdayEnergyRule


def make_function(name: str, num_lines: int, async_: bool = False) -> str:
    """Generate a function with a given number of lines."""
    keyword = "async def" if async_ else "def"
    body = "\n".join(f"    x_{i} = {i}" for i in range(num_lines))
    return f"{keyword} {name}():\n{body}\n"


def parse(source: str) -> ast.AST:
    return ast.parse(source)


@pytest.fixture
def thursday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: True
    )


@pytest.fixture
def wednesday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: False
    )


def test_flags_long_function_on_thursday(thursday):
    source = make_function("big_fn", 25)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert len(errors) == 1
    row, col, msg, typ = errors[0]
    assert row == 1
    assert col == 0
    assert "VIB001" in msg
    assert "big_fn" in msg
    assert "Thursday" in msg


def test_clean_short_function_on_thursday(thursday):
    source = make_function("small_fn", 5)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert errors == []


def test_clean_long_function_on_wednesday(wednesday):
    source = make_function("big_fn", 25)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert errors == []


def test_flags_async_function_on_thursday(thursday):
    source = make_function("async_fn", 25, async_=True)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert len(errors) == 1
    assert "async_fn" in errors[0][2]


def test_multiple_functions_only_flags_long_ones(thursday):
    source = make_function("short_fn", 5) + "\n" + make_function("long_fn", 25)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert len(errors) == 1
    assert "long_fn" in errors[0][2]


def test_exactly_at_limit_not_flagged(thursday):
    # 20 lines exactly: not flagged (must be > 20)
    source = make_function("border_fn", 20)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert errors == []


def test_one_over_limit_flagged(thursday):
    # 21 lines: should be flagged
    source = make_function("over_fn", 21)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert len(errors) == 1


def test_error_tuple_format(thursday):
    source = make_function("fn", 25)
    tree = parse(source)
    errors = ThursdayEnergyRule().check(tree, "test.py")
    assert len(errors) == 1
    row, col, msg, typ = errors[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)
