from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.exception_crimes import (
    _EXCEPT_EXCEPTION_MESSAGES,
    _RAISE_EXCEPTION_MESSAGES,
    _RERAISE_NO_LOG_MESSAGES,
    ExceptExceptionRule,
    RaiseExceptionRule,
    ReraiseNoLogRule,
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


# ── VIB007: re-raise without logging ─────────────────────────────────────────

def parse7(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_reraise(source: str) -> list:
    tree = parse7(source)
    lines = textwrap.dedent(source).splitlines(keepends=True)
    return ReraiseNoLogRule().check(tree, lines=lines)


def test_007_flags_bare_reraise():
    src = """
        try:
            pass
        except ValueError:
            raise
    """
    errors = check_reraise(src)
    assert len(errors) == 1
    assert "VIB007" in errors[0][2]


def test_007_no_flag_with_logging():
    src = """
        try:
            pass
        except ValueError:
            logger.error("oops")
            raise
    """
    assert check_reraise(src) == []


def test_007_no_flag_reraise_with_exc():
    src = """
        try:
            pass
        except ValueError:
            raise RuntimeError("wrapped")
    """
    assert check_reraise(src) == []


def test_007_no_flag_no_reraise():
    src = """
        try:
            pass
        except ValueError:
            pass
    """
    assert check_reraise(src) == []


def test_007_no_flag_with_warning_log():
    src = """
        try:
            pass
        except ValueError:
            log.warning("bad")
            raise
    """
    assert check_reraise(src) == []


def test_007_error_tuple_format():
    src = "try:\n    pass\nexcept ValueError:\n    raise"
    errors = check_reraise(src)
    row, col, msg, typ = errors[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_007_messages_list():
    assert len(_RERAISE_NO_LOG_MESSAGES) >= 2
