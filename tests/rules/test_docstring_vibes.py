from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.docstring_vibes import (
    _DOC_ARGS_MISMATCH_MESSAGES,
    _DOC_LONGER_THAN_FUNC_MESSAGES,
    _DOC_NO_PERIOD_MESSAGES,
    _DOC_REPEATS_NAME_MESSAGES,
    DocstringArgsMismatchRule,
    DocstringLongerThanFunctionRule,
    DocstringNoPeriodRule,
    DocstringRepeatsNameRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check(rule_cls: type, source: str) -> list:
    return rule_cls().check(parse(source))


# ── VIB085: docstring repeats name ───────────────────────────────────────────


def test_085_flags_obvious_docstring():
    src = textwrap.dedent("""\
        def get_user():
            \"\"\"Gets the user.\"\"\"
            pass
    """)
    errors = check(DocstringRepeatsNameRule, src)
    assert len(errors) == 1
    assert "VIB085" in errors[0][2]


def test_085_flags_fetch_data():
    src = textwrap.dedent("""\
        def fetch_data():
            \"\"\"Fetches data.\"\"\"
            pass
    """)
    errors = check(DocstringRepeatsNameRule, src)
    assert len(errors) == 1


def test_085_no_flag_meaningful_docstring():
    src = textwrap.dedent("""\
        def get_user():
            \"\"\"Retrieve the currently authenticated user from the session cache.\"\"\"
            pass
    """)
    assert check(DocstringRepeatsNameRule, src) == []


def test_085_no_flag_no_docstring():
    src = "def get_user():\n    pass"
    assert check(DocstringRepeatsNameRule, src) == []


def test_085_no_flag_single_word_name():
    src = textwrap.dedent("""\
        def run():
            \"\"\"Runs something useful here.\"\"\"
            pass
    """)
    assert check(DocstringRepeatsNameRule, src) == []


def test_085_messages_list():
    assert len(_DOC_REPEATS_NAME_MESSAGES) >= 2


# ── VIB086: docstring no period ───────────────────────────────────────────────


def test_086_flags_missing_period():
    src = textwrap.dedent("""\
        def foo():
            \"\"\"Does something cool\"\"\"
            pass
    """)
    errors = check(DocstringNoPeriodRule, src)
    assert len(errors) == 1
    assert "VIB086" in errors[0][2]


def test_086_no_flag_with_period():
    src = textwrap.dedent("""\
        def foo():
            \"\"\"Does something cool.\"\"\"
            pass
    """)
    assert check(DocstringNoPeriodRule, src) == []


def test_086_no_flag_no_docstring():
    src = "def foo():\n    pass"
    assert check(DocstringNoPeriodRule, src) == []


def test_086_flags_class_docstring():
    src = textwrap.dedent("""\
        class Foo:
            \"\"\"Represents a foo\"\"\"
            pass
    """)
    errors = check(DocstringNoPeriodRule, src)
    assert len(errors) == 1


def test_086_messages_list():
    assert len(_DOC_NO_PERIOD_MESSAGES) >= 2


# ── VIB087: args mismatch ─────────────────────────────────────────────────────


def test_087_flags_extra_arg_in_docs():
    src = textwrap.dedent("""\
        def foo(x):
            \"\"\"Do foo.

            Args:
                x: the x value.
                y: the y value that does not exist.
            \"\"\"
            pass
    """)
    errors = check(DocstringArgsMismatchRule, src)
    assert len(errors) == 1
    assert "VIB087" in errors[0][2]
    assert "y" in errors[0][2]


def test_087_no_flag_matching_args():
    src = textwrap.dedent("""\
        def foo(x, y):
            \"\"\"Do foo.

            Args:
                x: the x value.
                y: the y value.
            \"\"\"
            pass
    """)
    assert check(DocstringArgsMismatchRule, src) == []


def test_087_no_flag_no_args_section():
    src = textwrap.dedent("""\
        def foo(x):
            \"\"\"Do foo with x.\"\"\"
            pass
    """)
    assert check(DocstringArgsMismatchRule, src) == []


def test_087_messages_list():
    assert len(_DOC_ARGS_MISMATCH_MESSAGES) >= 2


# ── VIB088: docstring longer than function ────────────────────────────────────


def test_088_flags_long_docstring():
    src = textwrap.dedent("""\
        def foo(x):
            \"\"\"
            This is a very detailed explanation.
            It spans multiple lines.
            It goes on and on.
            It really does.
            \"\"\"
            return x
    """)
    errors = check(DocstringLongerThanFunctionRule, src)
    assert len(errors) == 1
    assert "VIB088" in errors[0][2]


def test_088_no_flag_short_docstring():
    src = textwrap.dedent("""\
        def foo(x):
            \"\"\"Does something.\"\"\"
            a = 1
            b = 2
            c = 3
            return a + b + c + x
    """)
    assert check(DocstringLongerThanFunctionRule, src) == []


def test_088_no_flag_no_docstring():
    src = "def foo(x):\n    return x"
    assert check(DocstringLongerThanFunctionRule, src) == []


def test_088_messages_list():
    assert len(_DOC_LONGER_THAN_FUNC_MESSAGES) >= 2
