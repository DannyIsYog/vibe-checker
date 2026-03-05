from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.structure_complexity import (
    _BARE_EXCEPT_MESSAGES,
    _DEEP_NESTING_MESSAGES,
    _EMPTY_EXCEPT_MESSAGES,
    _TOO_MANY_ARGS_MESSAGES,
    _TOO_MANY_RETURNS_MESSAGES,
    _count_args,
    _count_returns,
    _find_deep_nesting,
    BareExceptRule,
    DeepNestingRule,
    EmptyExceptRule,
    TooManyArgsRule,
    TooManyReturnsRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_args(source: str) -> list:
    return TooManyArgsRule().check(parse(source))


def check_nesting(source: str) -> list:
    return DeepNestingRule().check(parse(source))


def check_returns(source: str) -> list:
    return TooManyReturnsRule().check(parse(source))


def check_bare(source: str) -> list:
    return BareExceptRule().check(parse(source))


def check_empty(source: str) -> list:
    return EmptyExceptRule().check(parse(source))


def _nest(depth: int, inner: str = "pass") -> str:
    code = inner
    for _ in range(depth):
        code = "if True:\n" + textwrap.indent(code, "    ")
    return code


# ── VIB030: too-many-args ───────────────────────────────────────────────────


def test_030_flags_six_args():
    errors = check_args("def foo(a, b, c, d, e, f): pass")
    assert len(errors) == 1
    assert "VIB030" in errors[0][2]


def test_030_no_flag_five_args():
    assert check_args("def foo(a, b, c, d, e): pass") == []


def test_030_no_flag_four_args():
    assert check_args("def foo(a, b, c, d): pass") == []


def test_030_self_excluded():
    src = "class X:\n    def foo(self, a, b, c, d, e): pass"
    assert check_args(src) == []


def test_030_self_excluded_still_flags():
    src = "class X:\n    def foo(self, a, b, c, d, e, f): pass"
    errors = check_args(src)
    assert len(errors) == 1
    assert "VIB030" in errors[0][2]


def test_030_cls_excluded():
    src = "class X:\n    @classmethod\n    def foo(cls, a, b, c, d, e): pass"
    assert check_args(src) == []


def test_030_vararg_counts():
    errors = check_args("def foo(a, b, c, d, e, *args): pass")
    assert len(errors) == 1


def test_030_kwarg_counts():
    errors = check_args("def foo(a, b, c, d, e, **kwargs): pass")
    assert len(errors) == 1


def test_030_kwonly_counts():
    errors = check_args("def foo(a, b, c, d, *, e, f): pass")
    assert len(errors) == 1


def test_030_async_function():
    errors = check_args("async def foo(a, b, c, d, e, f): pass")
    assert len(errors) == 1
    assert "VIB030" in errors[0][2]


def test_030_error_tuple_format():
    row, col, msg, typ = check_args("def foo(a, b, c, d, e, f): pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_030_messages_list():
    assert len(_TOO_MANY_ARGS_MESSAGES) >= 2


def test_030_count_args_helper():
    node = ast.parse("def foo(a, b, c): pass").body[0]
    assert isinstance(node, ast.FunctionDef)
    assert _count_args(node) == 3


def test_030_count_args_with_self():
    node = ast.parse("def foo(self, a, b): pass").body[0]
    assert isinstance(node, ast.FunctionDef)
    assert _count_args(node) == 2


# ── VIB031: deep-nesting ────────────────────────────────────────────────────


def test_031_flags_five_levels():
    src = _nest(5)
    errors = check_nesting(src)
    assert len(errors) >= 1
    assert "VIB031" in errors[0][2]


def test_031_no_flag_four_levels():
    src = _nest(4)
    assert check_nesting(src) == []


def test_031_no_flag_three_levels():
    src = _nest(3)
    assert check_nesting(src) == []


def test_031_flags_inside_function():
    src = "def foo():\n" + textwrap.indent(_nest(5), "    ")
    errors = check_nesting(src)
    assert len(errors) >= 1
    assert "VIB031" in errors[0][2]


def test_031_function_resets_nesting():
    # 3 levels around a function definition, then 3 inside = fine
    src = _nest(3, inner="def inner():\n" + textwrap.indent(_nest(3), "    "))
    assert check_nesting(src) == []


def test_031_error_tuple_format():
    src = _nest(5)
    row, col, msg, typ = check_nesting(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_031_messages_list():
    assert len(_DEEP_NESTING_MESSAGES) >= 2


def test_031_find_deep_nesting_helper():
    tree = ast.parse(_nest(5))
    errors = _find_deep_nesting(tree, 0, 4, DeepNestingRule)
    assert len(errors) >= 1


def test_031_for_loop_counts():
    src = "def foo():\n    for a in b:\n        for c in d:\n            for e in f:\n                for g in h:\n                    for i in j:\n                        pass"
    errors = check_nesting(src)
    assert len(errors) >= 1
    assert "VIB031" in errors[0][2]


# ── VIB032: too-many-returns ────────────────────────────────────────────────


def test_032_flags_four_returns():
    src = "def foo(x):\n    if x == 1: return 1\n    if x == 2: return 2\n    if x == 3: return 3\n    return 4"
    errors = check_returns(src)
    assert len(errors) == 1
    assert "VIB032" in errors[0][2]


def test_032_no_flag_three_returns():
    src = "def foo(x):\n    if x == 1: return 1\n    if x == 2: return 2\n    return 3"
    assert check_returns(src) == []


def test_032_no_flag_two_returns():
    src = "def foo(x):\n    if x: return 1\n    return 0"
    assert check_returns(src) == []


def test_032_nested_function_not_counted():
    src = (
        "def outer():\n"
        "    def inner():\n"
        "        return 1\n"
        "        return 2\n"
        "        return 3\n"
        "        return 4\n"
        "    return 0\n"
    )
    # outer has 1 return, inner has 4 returns
    errors = check_returns(src)
    # outer should not be flagged, inner should
    assert len(errors) == 1
    assert "VIB032" in errors[0][2]


def test_032_async_function():
    src = "async def foo(x):\n    if x == 1: return 1\n    if x == 2: return 2\n    if x == 3: return 3\n    return 4"
    errors = check_returns(src)
    assert len(errors) == 1
    assert "VIB032" in errors[0][2]


def test_032_error_tuple_format():
    src = "def foo(x):\n    if x == 1: return 1\n    if x == 2: return 2\n    if x == 3: return 3\n    return 4"
    row, col, msg, typ = check_returns(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_032_messages_list():
    assert len(_TOO_MANY_RETURNS_MESSAGES) >= 2


def test_032_count_returns_helper():
    node = ast.parse("def foo(x):\n    if x: return 1\n    return 0").body[0]
    assert isinstance(node, ast.FunctionDef)
    assert _count_returns(node) == 2


def test_032_count_returns_skips_nested():
    src = "def outer():\n    def inner():\n        return 99\n    return 0"
    node = ast.parse(src).body[0]
    assert isinstance(node, ast.FunctionDef)
    assert _count_returns(node) == 1


# ── VIB033: bare-except ─────────────────────────────────────────────────────


def test_033_flags_bare_except():
    src = "try:\n    pass\nexcept:\n    pass"
    errors = check_bare(src)
    assert len(errors) == 1
    assert "VIB033" in errors[0][2]


def test_033_no_flag_typed_except():
    src = "try:\n    pass\nexcept Exception:\n    pass"
    assert check_bare(src) == []


def test_033_no_flag_specific_exception():
    src = "try:\n    pass\nexcept ValueError:\n    pass"
    assert check_bare(src) == []


def test_033_no_flag_tuple_of_exceptions():
    src = "try:\n    pass\nexcept (TypeError, ValueError):\n    pass"
    assert check_bare(src) == []


def test_033_flags_multiple_bare_excepts():
    src = (
        "try:\n    pass\nexcept:\n    pass\n"
        "try:\n    pass\nexcept:\n    pass"
    )
    errors = check_bare(src)
    assert len(errors) == 2


def test_033_error_tuple_format():
    src = "try:\n    pass\nexcept:\n    pass"
    row, col, msg, typ = check_bare(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_033_messages_list():
    assert len(_BARE_EXCEPT_MESSAGES) >= 2


# ── VIB034: empty-except ────────────────────────────────────────────────────


def test_034_flags_except_pass():
    src = "try:\n    pass\nexcept Exception:\n    pass"
    errors = check_empty(src)
    assert len(errors) == 1
    assert "VIB034" in errors[0][2]


def test_034_flags_bare_except_pass():
    src = "try:\n    pass\nexcept:\n    pass"
    errors = check_empty(src)
    assert len(errors) == 1
    assert "VIB034" in errors[0][2]


def test_034_no_flag_except_with_action():
    src = "try:\n    pass\nexcept Exception as e:\n    print(e)"
    assert check_empty(src) == []


def test_034_no_flag_except_with_raise():
    src = "try:\n    pass\nexcept Exception:\n    raise"
    assert check_empty(src) == []


def test_034_no_flag_except_with_log_and_pass():
    src = "try:\n    pass\nexcept Exception:\n    print('error')\n    pass"
    assert check_empty(src) == []


def test_034_flags_multiple_empty_excepts():
    src = (
        "try:\n    pass\nexcept TypeError:\n    pass\n"
        "try:\n    pass\nexcept ValueError:\n    pass"
    )
    errors = check_empty(src)
    assert len(errors) == 2


def test_034_error_tuple_format():
    src = "try:\n    pass\nexcept Exception:\n    pass"
    row, col, msg, typ = check_empty(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_034_messages_list():
    assert len(_EMPTY_EXCEPT_MESSAGES) >= 2
