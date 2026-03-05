from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.return_crimes import (
    _ASSIGN_RETURN_MESSAGES,
    _EXPLICIT_RETURN_NONE_MESSAGES,
    _MUTABLE_DEFAULT_MESSAGES,
    _SHADOW_BUILTIN_MESSAGES,
    AssignThenReturnRule,
    ExplicitReturnNoneRule,
    MutableDefaultArgRule,
    ShadowBuiltinRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_return_none(source: str) -> list:
    return ExplicitReturnNoneRule().check(parse(source))


def check_assign_return(source: str) -> list:
    return AssignThenReturnRule().check(parse(source))


def check_mutable_default(source: str) -> list:
    return MutableDefaultArgRule().check(parse(source))


def check_shadow(source: str) -> list:
    return ShadowBuiltinRule().check(parse(source))


# ── VIB053: explicit return None ─────────────────────────────────────────────


def test_053_flags_explicit_return_none():
    src = "def foo():\n    return None"
    errors = check_return_none(src)
    assert len(errors) == 1
    assert "VIB053" in errors[0][2]


def test_053_no_flag_bare_return():
    src = "def foo():\n    return"
    assert check_return_none(src) == []


def test_053_no_flag_return_value():
    src = "def foo():\n    return 42"
    assert check_return_none(src) == []


def test_053_no_flag_return_none_variable():
    src = "x = None\ndef foo():\n    return x"
    assert check_return_none(src) == []


def test_053_error_tuple_format():
    src = "def foo():\n    return None"
    row, col, msg, typ = check_return_none(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_053_messages_list():
    assert len(_EXPLICIT_RETURN_NONE_MESSAGES) >= 2


# ── VIB054: assign then return ───────────────────────────────────────────────


def test_054_flags_assign_then_return():
    src = "def foo():\n    result = compute()\n    return result"
    errors = check_assign_return(src)
    assert len(errors) == 1
    assert "VIB054" in errors[0][2]


def test_054_no_flag_different_name_returned():
    src = "def foo():\n    result = compute()\n    return other"
    assert check_assign_return(src) == []


def test_054_no_flag_not_consecutive():
    src = "def foo():\n    result = compute()\n    do_something()\n    return result"
    assert check_assign_return(src) == []


def test_054_no_flag_tuple_assignment():
    src = "def foo():\n    a, b = compute()\n    return a"
    assert check_assign_return(src) == []


def test_054_error_tuple_format():
    src = "def foo():\n    x = compute()\n    return x"
    row, col, msg, typ = check_assign_return(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_054_messages_list():
    assert len(_ASSIGN_RETURN_MESSAGES) >= 2


def test_054_flags_async_function():
    src = "async def foo():\n    result = await compute()\n    return result"
    errors = check_assign_return(src)
    assert len(errors) == 1


# ── VIB055: mutable default argument ─────────────────────────────────────────


def test_055_flags_list_default():
    src = "def foo(x=[]):\n    pass"
    errors = check_mutable_default(src)
    assert len(errors) == 1
    assert "VIB055" in errors[0][2]


def test_055_flags_dict_default():
    src = "def foo(x={}):\n    pass"
    errors = check_mutable_default(src)
    assert len(errors) == 1


def test_055_flags_set_default():
    src = "def foo(x=set()):\n    pass"
    # set() is a Call, not a Set literal
    assert check_mutable_default(src) == []


def test_055_flags_set_literal():
    src = "def foo(x={1, 2}):\n    pass"
    errors = check_mutable_default(src)
    assert len(errors) == 1


def test_055_no_flag_none_default():
    src = "def foo(x=None):\n    pass"
    assert check_mutable_default(src) == []


def test_055_no_flag_string_default():
    src = "def foo(x='hello'):\n    pass"
    assert check_mutable_default(src) == []


def test_055_no_flag_int_default():
    src = "def foo(x=42):\n    pass"
    assert check_mutable_default(src) == []


def test_055_error_tuple_format():
    src = "def foo(x=[]):\n    pass"
    row, col, msg, typ = check_mutable_default(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_055_messages_list():
    assert len(_MUTABLE_DEFAULT_MESSAGES) >= 2


def test_055_kwonly_with_no_default_does_not_crash():
    # kw_defaults can contain None for args with no default
    src = "def foo(*, a, b=[]):\n    pass"
    errors = check_mutable_default(src)
    assert len(errors) == 1


# ── VIB056: shadow builtin ───────────────────────────────────────────────────


def test_056_flags_list_shadow():
    errors = check_shadow("list = [1, 2, 3]")
    assert len(errors) == 1
    assert "VIB056" in errors[0][2]


def test_056_flags_dict_shadow():
    errors = check_shadow("dict = {}")
    assert len(errors) == 1


def test_056_flags_str_shadow():
    errors = check_shadow("str = 'hello'")
    assert len(errors) == 1


def test_056_flags_len_shadow():
    errors = check_shadow("len = 5")
    assert len(errors) == 1


def test_056_no_flag_non_builtin():
    assert check_shadow("my_list = [1, 2, 3]") == []


def test_056_no_flag_user_var():
    assert check_shadow("data = 'hello'") == []


def test_056_name_in_message():
    errors = check_shadow("list = []")
    assert "list" in errors[0][2]


def test_056_error_tuple_format():
    row, col, msg, typ = check_shadow("list = []")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_056_messages_list():
    assert len(_SHADOW_BUILTIN_MESSAGES) >= 2
