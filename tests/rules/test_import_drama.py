from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.import_drama import (
    _IMPORT_IN_FUNCTION_MESSAGES,
    _STAR_IMPORT_MESSAGES,
    ImportInFunctionRule,
    StarImportRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_star(source: str) -> list:
    return StarImportRule().check(parse(source))


def check_in_func(source: str) -> list:
    return ImportInFunctionRule().check(parse(source))


# ── VIB048: import * ─────────────────────────────────────────────────────────


def test_048_flags_star_import():
    errors = check_star("from os import *")
    assert len(errors) == 1
    assert "VIB048" in errors[0][2]


def test_048_no_flag_named_import():
    assert check_star("from os import path") == []


def test_048_no_flag_plain_import():
    assert check_star("import os") == []


def test_048_flags_multiple_star_imports():
    src = "from os import *\nfrom sys import *"
    errors = check_star(src)
    assert len(errors) == 2


def test_048_error_tuple_format():
    row, col, msg, typ = check_star("from os import *")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_048_messages_list():
    assert len(_STAR_IMPORT_MESSAGES) >= 2


# ── VIB051: import inside function ───────────────────────────────────────────


def test_051_flags_import_in_function():
    src = "def foo():\n    import os\n    return os.path"
    errors = check_in_func(src)
    assert len(errors) == 1
    assert "VIB051" in errors[0][2]


def test_051_flags_from_import_in_function():
    src = "def foo():\n    from os import path\n    return path"
    errors = check_in_func(src)
    assert len(errors) == 1
    assert "VIB051" in errors[0][2]


def test_051_no_flag_top_level_import():
    assert check_in_func("import os") == []


def test_051_flags_inside_async_function():
    src = "async def foo():\n    import os\n    return os.path"
    errors = check_in_func(src)
    assert len(errors) == 1
    assert "VIB051" in errors[0][2]


def test_051_error_tuple_format():
    src = "def foo():\n    import os"
    row, col, msg, typ = check_in_func(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_051_messages_list():
    assert len(_IMPORT_IN_FUNCTION_MESSAGES) >= 2


def test_051_no_flag_class_level():
    src = "class Foo:\n    import os"
    assert check_in_func(src) == []


def test_051_nested_function_not_double_counted():
    src = (
        "def outer():\n"
        "    def inner():\n"
        "        import os\n"
        "    pass\n"
    )
    # inner import should be flagged once (from inner fn traversal), not twice
    errors = check_in_func(src)
    assert len(errors) == 1
    assert "VIB051" in errors[0][2]
