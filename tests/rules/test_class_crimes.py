from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.class_crimes import (
    _MULTIPLE_INHERITANCE_MESSAGES,
    MultipleInheritanceRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_multi_inherit(source: str) -> list:
    return MultipleInheritanceRule().check(parse(source))


# ── VIB063: multiple inheritance ─────────────────────────────────────────────


def test_063_flags_three_bases():
    src = "class Foo(A, B, C):\n    pass"
    errors = check_multi_inherit(src)
    assert len(errors) == 1
    assert "VIB063" in errors[0][2]


def test_063_flags_four_bases():
    src = "class Foo(A, B, C, D):\n    pass"
    errors = check_multi_inherit(src)
    assert len(errors) == 1


def test_063_no_flag_two_bases():
    assert check_multi_inherit("class Foo(A, B):\n    pass") == []


def test_063_no_flag_one_base():
    assert check_multi_inherit("class Foo(A):\n    pass") == []


def test_063_no_flag_no_bases():
    assert check_multi_inherit("class Foo:\n    pass") == []


def test_063_error_tuple_format():
    src = "class Foo(A, B, C):\n    pass"
    row, col, msg, typ = check_multi_inherit(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_063_messages_list():
    assert len(_MULTIPLE_INHERITANCE_MESSAGES) >= 2


def test_063_name_in_message():
    src = "class MyThing(A, B, C):\n    pass"
    errors = check_multi_inherit(src)
    # n should appear in message
    assert "3" in errors[0][2]
