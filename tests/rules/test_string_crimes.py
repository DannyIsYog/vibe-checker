from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.string_crimes import (
    _FORMAT_POSITIONAL_MESSAGES,
    _MULTILINE_COMMENT_MESSAGES,
    _PERCENT_FORMAT_MESSAGES,
    _STRING_CONCAT_LOOP_MESSAGES,
    FormatPositionalRule,
    MultilineStringCommentRule,
    PercentFormatRule,
    StringConcatInLoopRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_concat_loop(source: str) -> list:
    return StringConcatInLoopRule().check(parse(source))


def check_percent(source: str) -> list:
    return PercentFormatRule().check(parse(source))


def check_format(source: str) -> list:
    return FormatPositionalRule().check(parse(source))


# ── VIB077: string concat in loop ────────────────────────────────────────────


def test_077_flags_string_concat_in_for():
    src = "s = ''\nfor x in items:\n    s += 'hello'\n"
    errors = check_concat_loop(src)
    assert len(errors) == 1
    assert "VIB077" in errors[0][2]


def test_077_flags_string_concat_in_while():
    src = "s = ''\nwhile True:\n    s += 'x'\n    break\n"
    errors = check_concat_loop(src)
    assert len(errors) == 1
    assert "VIB077" in errors[0][2]


def test_077_no_flag_int_concat_in_loop():
    src = "n = 0\nfor x in items:\n    n += 1\n"
    assert check_concat_loop(src) == []


def test_077_no_flag_string_concat_outside_loop():
    src = "s = ''\ns += 'hello'\n"
    assert check_concat_loop(src) == []


def test_077_error_tuple_format():
    src = "s = ''\nfor x in items:\n    s += 'y'\n"
    row, col, msg, typ = check_concat_loop(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_077_messages_list():
    assert len(_STRING_CONCAT_LOOP_MESSAGES) >= 2


def test_077_flags_fstring_concat_in_loop():
    src = "s = ''\nfor x in items:\n    s += f'{x}'\n"
    errors = check_concat_loop(src)
    assert len(errors) == 1
    assert "VIB077" in errors[0][2]


# ── VIB078: % formatting ──────────────────────────────────────────────────────


def test_078_flags_percent_format():
    src = "msg = 'hello %s' % name"
    errors = check_percent(src)
    assert len(errors) == 1
    assert "VIB078" in errors[0][2]


def test_078_no_flag_modulo_int():
    assert check_percent("x = 10 % 3") == []


def test_078_no_flag_fstring():
    assert check_percent("msg = f'hello {name}'") == []


def test_078_no_flag_format_method():
    assert check_percent("msg = 'hello {}'.format(name)") == []


def test_078_error_tuple_format():
    row, col, msg, typ = check_percent("x = 'hello %s' % 'world'")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_078_messages_list():
    assert len(_PERCENT_FORMAT_MESSAGES) >= 2


# ── VIB079: .format() positional ─────────────────────────────────────────────


def test_079_flags_format_positional():
    src = "'hello {}'.format(name)"
    errors = check_format(src)
    assert len(errors) == 1
    assert "VIB079" in errors[0][2]


def test_079_no_flag_format_with_keywords():
    assert check_format("'hello {name}'.format(name=name)") == []


def test_079_no_flag_format_no_args():
    assert check_format("'hello'.format()") == []


def test_079_no_flag_other_method():
    assert check_format("x.strip()") == []


def test_079_error_tuple_format():
    row, col, msg, typ = check_format("'{}'.format(x)")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_079_messages_list():
    assert len(_FORMAT_POSITIONAL_MESSAGES) >= 2


# ── VIB080: multiline string as comment ──────────────────────────────────────

def check_multiline(source: str) -> list:
    return MultilineStringCommentRule().check(ast.parse(textwrap.dedent(source)))


def test_080_flags_standalone_multiline():
    src = textwrap.dedent("""\
        x = 1
        \"\"\"
        This is a note
        about something.
        \"\"\"
        y = 2
    """)
    errors = check_multiline(src)
    assert len(errors) == 1
    assert "VIB080" in errors[0][2]


def test_080_no_flag_function_docstring():
    src = textwrap.dedent("""\
        def foo():
            \"\"\"
            This is a docstring.
            \"\"\"
            pass
    """)
    assert check_multiline(src) == []


def test_080_no_flag_single_line_string():
    src = 'x = "not multiline"\n'
    assert check_multiline(src) == []


def test_080_no_flag_module_docstring():
    src = textwrap.dedent("""\
        \"\"\"
        Module docstring.
        \"\"\"
        x = 1
    """)
    assert check_multiline(src) == []


def test_080_messages_list():
    assert len(_MULTILINE_COMMENT_MESSAGES) >= 2
