from __future__ import annotations

import ast

import pytest

from flake8_vibes.rules.calendar_crimes import (
    DecemberCodeRule,
    FridayDeployRule,
    MondayMotivationRule,
    ThursdayEnergyRule,
    _DECEMBER_MESSAGES,
    _FRIDAY_MESSAGES,
    _MONDAY_MESSAGES,
)


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
        "flake8_vibes.rules.calendar_crimes._is_thursday", lambda _: True
    )


@pytest.fixture
def wednesday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.calendar_crimes._is_thursday", lambda _: False
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


# ── VIB064: monday motivation ─────────────────────────────────────────────────


@pytest.fixture
def monday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_monday", lambda _: True)


@pytest.fixture
def not_monday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_monday", lambda _: False)


def test_064_flags_tiny_function_on_monday(monday):
    src = "def foo():\n    pass\n"
    errors = MondayMotivationRule().check(parse(src), "test.py")
    assert len(errors) == 1
    assert "VIB064" in errors[0][2]


def test_064_no_flag_not_monday(not_monday):
    src = "def foo():\n    pass\n"
    assert MondayMotivationRule().check(parse(src), "test.py") == []


def test_064_no_flag_longer_function(monday):
    src = make_function("foo", 5)
    assert MondayMotivationRule().check(parse(src), "test.py") == []


def test_064_messages_list():
    assert len(_MONDAY_MESSAGES) >= 2


# ── VIB065: friday deploy ─────────────────────────────────────────────────────


@pytest.fixture
def friday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_friday", lambda _: True)


@pytest.fixture
def not_friday(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_friday", lambda _: False)


def test_065_flags_on_friday(friday):
    errors = FridayDeployRule().check(parse("x = 1"), "test.py")
    assert len(errors) == 1
    assert "VIB065" in errors[0][2]


def test_065_no_flag_not_friday(not_friday):
    assert FridayDeployRule().check(parse("x = 1"), "test.py") == []


def test_065_error_at_line_1(friday):
    errors = FridayDeployRule().check(parse("x = 1"), "test.py")
    assert errors[0][0] == 1


def test_065_messages_list():
    assert len(_FRIDAY_MESSAGES) >= 2


# ── VIB067: december code ─────────────────────────────────────────────────────


@pytest.fixture
def december(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_december", lambda _: True)


@pytest.fixture
def not_december(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr("flake8_vibes.rules.calendar_crimes._is_december", lambda _: False)


def test_067_flags_in_december(december):
    errors = DecemberCodeRule().check(parse("x = 1"), "test.py")
    assert len(errors) == 1
    assert "VIB067" in errors[0][2]


def test_067_no_flag_not_december(not_december):
    assert DecemberCodeRule().check(parse("x = 1"), "test.py") == []


def test_067_error_at_line_1(december):
    errors = DecemberCodeRule().check(parse("x = 1"), "test.py")
    assert errors[0][0] == 1


def test_067_messages_list():
    assert len(_DECEMBER_MESSAGES) >= 2
