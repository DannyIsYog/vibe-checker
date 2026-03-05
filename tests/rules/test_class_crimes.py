from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.class_crimes import (
    _CLASS_NO_DOCSTRING_MESSAGES,
    _EMPTY_EXCEPT_DEL_MESSAGES,
    _MULTIPLE_INHERITANCE_MESSAGES,
    _NO_OP_OVERRIDE_MESSAGES,
    _STR_RETURNS_DICT_MESSAGES,
    _SUPER_INIT_MESSAGES,
    ClassNoDocstringRule,
    EmptyExceptInDelRule,
    MultipleInheritanceRule,
    NoOpOverrideRule,
    StrReturnsDictRule,
    SuperInitNotCalledRule,
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


def parse_cls(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check(rule_cls: type, source: str) -> list:
    return rule_cls().check(parse_cls(source))


# ── VIB058: __str__ returns self.__dict__ ─────────────────────────────────────


def test_058_flags_str_returns_dict():
    src = textwrap.dedent("""\
        class Foo:
            def __str__(self):
                return self.__dict__
    """)
    errors = check(StrReturnsDictRule, src)
    assert len(errors) == 1
    assert "VIB058" in errors[0][2]


def test_058_flags_str_of_dict():
    src = textwrap.dedent("""\
        class Foo:
            def __str__(self):
                return str(self.__dict__)
    """)
    errors = check(StrReturnsDictRule, src)
    assert len(errors) == 1


def test_058_no_flag_proper_str():
    src = textwrap.dedent("""\
        class Foo:
            def __str__(self):
                return f"Foo({self.x})"
    """)
    assert check(StrReturnsDictRule, src) == []


def test_058_messages_list():
    assert len(_STR_RETURNS_DICT_MESSAGES) >= 2


# ── VIB059: empty except in __del__ ──────────────────────────────────────────


def test_059_flags_empty_except_in_del():
    src = textwrap.dedent("""\
        class Foo:
            def __del__(self):
                try:
                    self.cleanup()
                except:
                    pass
    """)
    errors = check(EmptyExceptInDelRule, src)
    assert len(errors) == 1
    assert "VIB059" in errors[0][2]


def test_059_no_flag_no_try_in_del():
    src = textwrap.dedent("""\
        class Foo:
            def __del__(self):
                self.cleanup()
    """)
    assert check(EmptyExceptInDelRule, src) == []


def test_059_no_flag_except_with_body():
    src = textwrap.dedent("""\
        class Foo:
            def __del__(self):
                try:
                    self.cleanup()
                except Exception as e:
                    log.error(e)
    """)
    assert check(EmptyExceptInDelRule, src) == []


def test_059_messages_list():
    assert len(_EMPTY_EXCEPT_DEL_MESSAGES) >= 2


# ── VIB060: class no docstring 100+ lines ────────────────────────────────────


def test_060_flags_large_class_no_docstring():
    body = "\n".join(f"    x{i} = {i}" for i in range(110))
    src = f"class BigThing:\n{body}"
    errors = check(ClassNoDocstringRule, src)
    assert len(errors) == 1
    assert "VIB060" in errors[0][2]


def test_060_no_flag_small_class():
    src = "class Tiny:\n    pass"
    assert check(ClassNoDocstringRule, src) == []


def test_060_no_flag_large_class_with_docstring():
    body = "\n".join(f"    x{i} = {i}" for i in range(110))
    src = f'class BigThing:\n    """This is documented."""\n{body}'
    assert check(ClassNoDocstringRule, src) == []


def test_060_messages_list():
    assert len(_CLASS_NO_DOCSTRING_MESSAGES) >= 2


# ── VIB061: super().__init__() not called ────────────────────────────────────


def test_061_flags_missing_super_init():
    src = textwrap.dedent("""\
        class Child(Parent):
            def __init__(self):
                self.x = 1
    """)
    errors = check(SuperInitNotCalledRule, src)
    assert len(errors) == 1
    assert "VIB061" in errors[0][2]


def test_061_no_flag_with_super_call():
    src = textwrap.dedent("""\
        class Child(Parent):
            def __init__(self):
                super().__init__()
                self.x = 1
    """)
    assert check(SuperInitNotCalledRule, src) == []


def test_061_no_flag_no_bases():
    src = textwrap.dedent("""\
        class Child:
            def __init__(self):
                self.x = 1
    """)
    assert check(SuperInitNotCalledRule, src) == []


def test_061_no_flag_object_base():
    src = textwrap.dedent("""\
        class Child(object):
            def __init__(self):
                self.x = 1
    """)
    assert check(SuperInitNotCalledRule, src) == []


def test_061_messages_list():
    assert len(_SUPER_INIT_MESSAGES) >= 2


# ── VIB062: no-op override ────────────────────────────────────────────────────


def test_062_flags_passthrough_override():
    src = textwrap.dedent("""\
        class Child(Parent):
            def process(self, x):
                return super().process(x)
    """)
    errors = check(NoOpOverrideRule, src)
    assert len(errors) == 1
    assert "VIB062" in errors[0][2]


def test_062_no_flag_real_override():
    src = textwrap.dedent("""\
        class Child(Parent):
            def process(self, x):
                result = super().process(x)
                return result * 2
    """)
    assert check(NoOpOverrideRule, src) == []


def test_062_no_flag_no_bases():
    src = textwrap.dedent("""\
        class Child:
            def process(self, x):
                return super().process(x)
    """)
    assert check(NoOpOverrideRule, src) == []


def test_062_no_flag_init_override():
    src = textwrap.dedent("""\
        class Child(Parent):
            def __init__(self):
                super().__init__()
    """)
    assert check(NoOpOverrideRule, src) == []


def test_062_messages_list():
    assert len(_NO_OP_OVERRIDE_MESSAGES) >= 2
