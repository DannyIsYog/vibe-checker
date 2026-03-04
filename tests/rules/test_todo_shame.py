from __future__ import annotations

import ast

from flake8_vibes.rules.todo_shame import TodoShameRule, _MESSAGES


def check(source: str) -> list:
    tree = ast.parse(source)
    lines = source.splitlines()
    return TodoShameRule().check(tree, "test.py", lines)


def test_flags_todo():
    errors = check("x = 1  # TODO: fix this\n")
    assert len(errors) == 1
    assert "VIB002" in errors[0][2]


def test_flags_fixme():
    errors = check("x = 1  # FIXME: broken\n")
    assert len(errors) == 1
    assert "VIB002" in errors[0][2]


def test_all_todo_messages_covered():
    assert len(_MESSAGES["TODO"]) >= 2
    assert len(_MESSAGES["FIXME"]) >= 2


def test_case_insensitive():
    errors = check("# todo: something\n")
    assert len(errors) == 1


def test_clean_code():
    errors = check("x = 1\ndef foo(): pass\n")
    assert errors == []


def test_multiple_todos():
    source = "# TODO: one\nx = 1\n# FIXME: two\n"
    errors = check(source)
    assert len(errors) == 2
    assert errors[0][0] == 1
    assert errors[1][0] == 3


def test_correct_line_number():
    source = "x = 1\ny = 2\n# TODO: here\n"
    errors = check(source)
    assert errors[0][0] == 3


def test_returns_empty_when_no_lines():
    tree = ast.parse("x = 1")
    errors = TodoShameRule().check(tree, "test.py", lines=None)
    assert errors == []


def test_error_tuple_format():
    errors = check("# TODO: fix\n")
    row, col, msg, typ = errors[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)
