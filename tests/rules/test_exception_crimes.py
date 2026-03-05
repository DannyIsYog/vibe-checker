from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.exception_crimes import (
    _EXCEPT_EXCEPTION_MESSAGES,
    _RAISE_EXCEPTION_MESSAGES,
    ExceptExceptionRule,
    RaiseExceptionRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_except(source: str) -> list:
    return ExceptExceptionRule().check(parse(source))


def check_raise(source: str) -> list:
    return RaiseExceptionRule().check(parse(source))


# ── VIB003: except Exception ─────────────────────────────────────────────────


def test_003_flags_except_exception():
    src = "try:\n    pass\nexcept Exception:\n    pass"
    errors = check_except(src)
    assert len(errors) == 1
    assert "VIB003" in errors[0][2]


def test_003_no_flag_specific_exception():
    src = "try:\n    pass\nexcept ValueError:\n    pass"
    assert check_except(src) == []


def test_003_no_flag_bare_except():
    src = "try:\n    pass\nexcept:\n    pass"
    assert check_except(src) == []


def test_003_no_flag_tuple_exception():
    src = "try:\n    pass\nexcept (ValueError, TypeError):\n    pass"
    assert check_except(src) == []


def test_003_flags_multiple():
    src = (
        "try:\n    pass\nexcept Exception:\n    pass\n"
        "try:\n    pass\nexcept Exception:\n    pass"
    )
    errors = check_except(src)
    assert len(errors) == 2


def test_003_error_tuple_format():
    src = "try:\n    pass\nexcept Exception:\n    pass"
    row, col, msg, typ = check_except(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_003_messages_list():
    assert len(_EXCEPT_EXCEPTION_MESSAGES) >= 2


# ── VIB006: generic raise ────────────────────────────────────────────────────


def test_006_flags_raise_exception():
    src = "raise Exception('something went wrong')"
    errors = check_raise(src)
    assert len(errors) == 1
    assert "VIB006" in errors[0][2]


def test_006_no_flag_specific_exception():
    src = "raise ValueError('bad value')"
    assert check_raise(src) == []


def test_006_no_flag_bare_raise():
    src = "try:\n    pass\nexcept:\n    raise"
    assert check_raise(src) == []


def test_006_no_flag_reraise():
    src = "raise ValueError"
    assert check_raise(src) == []


def test_006_flags_multiple():
    src = "raise Exception('a')\nraise Exception('b')"
    errors = check_raise(src)
    assert len(errors) == 2


def test_006_error_tuple_format():
    src = "raise Exception('oops')"
    row, col, msg, typ = check_raise(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_006_messages_list():
    assert len(_RAISE_EXCEPTION_MESSAGES) >= 2
