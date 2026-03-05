from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.debug_artifacts import (
    _BREAKPOINT_MESSAGES,
    _CONSOLE_LOG_MESSAGES,
    _IMPORT_PDB_MESSAGES,
    _PDB_SET_TRACE_MESSAGES,
    _PRINT_MESSAGES,
    BreakpointLeftBehindRule,
    ConsoleLogInPyRule,
    ImportPdbRule,
    PdbSetTraceRule,
    PrintLeftBehindRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_print(source: str) -> list:
    return PrintLeftBehindRule().check(parse(source))


def check_breakpoint(source: str) -> list:
    return BreakpointLeftBehindRule().check(parse(source))


def check_pdb_trace(source: str) -> list:
    return PdbSetTraceRule().check(parse(source))


def check_import_pdb(source: str) -> list:
    return ImportPdbRule().check(parse(source))


# ── VIB008: print() ──────────────────────────────────────────────────────────


def test_008_flags_print():
    errors = check_print("print('hello')")
    assert len(errors) == 1
    assert "VIB008" in errors[0][2]


def test_008_no_flag_other_call():
    assert check_print("logging.info('hello')") == []


def test_008_flags_multiple_prints():
    src = "print('a')\nprint('b')"
    errors = check_print(src)
    assert len(errors) == 2


def test_008_error_tuple_format():
    row, col, msg, typ = check_print("print('x')")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_008_messages_list():
    assert len(_PRINT_MESSAGES) >= 2


def test_008_flags_inside_function():
    src = "def foo():\n    print('debug')"
    errors = check_print(src)
    assert len(errors) == 1
    assert "VIB008" in errors[0][2]


# ── VIB009: breakpoint() ─────────────────────────────────────────────────────


def test_009_flags_breakpoint():
    errors = check_breakpoint("breakpoint()")
    assert len(errors) == 1
    assert "VIB009" in errors[0][2]


def test_009_no_flag_other_call():
    assert check_breakpoint("other_func()") == []


def test_009_error_tuple_format():
    row, col, msg, typ = check_breakpoint("breakpoint()")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_009_messages_list():
    assert len(_BREAKPOINT_MESSAGES) >= 2


# ── VIB010: pdb.set_trace() ──────────────────────────────────────────────────


def test_010_flags_pdb_set_trace():
    errors = check_pdb_trace("import pdb\npdb.set_trace()")
    assert len(errors) == 1
    assert "VIB010" in errors[0][2]


def test_010_no_flag_other_attribute():
    assert check_pdb_trace("something.set_trace()") == []


def test_010_no_flag_pdb_other_method():
    assert check_pdb_trace("pdb.run('expr')") == []


def test_010_error_tuple_format():
    row, col, msg, typ = check_pdb_trace("pdb.set_trace()")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_010_messages_list():
    assert len(_PDB_SET_TRACE_MESSAGES) >= 2


# ── VIB011: import pdb ───────────────────────────────────────────────────────


def test_011_flags_import_pdb():
    errors = check_import_pdb("import pdb")
    assert len(errors) == 1
    assert "VIB011" in errors[0][2]


def test_011_flags_from_pdb_import():
    errors = check_import_pdb("from pdb import set_trace")
    assert len(errors) == 1
    assert "VIB011" in errors[0][2]


def test_011_no_flag_other_import():
    assert check_import_pdb("import os") == []


def test_011_no_flag_from_other_import():
    assert check_import_pdb("from os import path") == []


def test_011_error_tuple_format():
    row, col, msg, typ = check_import_pdb("import pdb")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_011_messages_list():
    assert len(_IMPORT_PDB_MESSAGES) >= 2


# ── VIB012: console.log in .py ───────────────────────────────────────────────


def check_console_log(source: str) -> list:
    tree = ast.parse(textwrap.dedent(source))
    lines = textwrap.dedent(source).splitlines(keepends=True)
    return ConsoleLogInPyRule().check(tree, lines=lines)


def test_012_flags_console_log():
    errors = check_console_log("console.log(x)")
    assert len(errors) == 1
    assert "VIB012" in errors[0][2]


def test_012_flags_with_space():
    errors = check_console_log("  console.log( 'hi' )")
    assert len(errors) == 1


def test_012_no_flag_print():
    assert check_console_log("print('hi')") == []


def test_012_no_flag_in_comment():
    assert check_console_log("# console.log(x)") == []


def test_012_flags_case_insensitive():
    errors = check_console_log("Console.Log(x)")
    assert len(errors) == 1


def test_012_error_tuple_format():
    row, col, msg, typ = check_console_log("console.log(x)")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_012_messages_list():
    assert len(_CONSOLE_LOG_MESSAGES) >= 2
