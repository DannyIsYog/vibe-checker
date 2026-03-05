from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.import_drama import (
    _DEAD_FUTURE_MESSAGES,
    _IMPORT_IN_FUNCTION_MESSAGES,
    _OS_PATH_MESSAGES,
    _STAR_IMPORT_MESSAGES,
    _UNUSED_IMPORT_MESSAGES,
    FutureImportDeadRule,
    ImportInFunctionRule,
    OsPathImportRule,
    StarImportRule,
    UnusedImportRule,
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


# ── VIB049: unused import ─────────────────────────────────────────────────────


def check_unused(source: str) -> list:
    tree = ast.parse(textwrap.dedent(source))
    return UnusedImportRule().check(tree)


def test_049_flags_unused_module_import():
    errors = check_unused("import os")
    assert len(errors) == 1
    assert "VIB049" in errors[0][2]


def test_049_no_flag_used_import():
    src = "import os\nos.getcwd()"
    assert check_unused(src) == []


def test_049_flags_unused_from_import():
    errors = check_unused("from os import path")
    assert len(errors) == 1
    assert "VIB049" in errors[0][2]


def test_049_no_flag_used_from_import():
    src = "from os import path\npath.join('a', 'b')"
    assert check_unused(src) == []


def test_049_no_flag_future_import():
    src = "from __future__ import annotations"
    assert check_unused(src) == []


def test_049_no_flag_in_all():
    src = "from mymod import MyClass\n__all__ = ['MyClass']"
    assert check_unused(src) == []


def test_049_messages_list():
    assert len(_UNUSED_IMPORT_MESSAGES) >= 2


# ── VIB050: dead __future__ import ───────────────────────────────────────────


def check_future(source: str) -> list:
    return FutureImportDeadRule().check(ast.parse(textwrap.dedent(source)))


def test_050_flags_print_function():
    errors = check_future("from __future__ import print_function")
    assert len(errors) == 1
    assert "VIB050" in errors[0][2]


def test_050_flags_unicode_literals():
    errors = check_future("from __future__ import unicode_literals")
    assert len(errors) == 1


def test_050_flags_division():
    errors = check_future("from __future__ import division")
    assert len(errors) == 1


def test_050_no_flag_annotations():
    assert check_future("from __future__ import annotations") == []


def test_050_messages_list():
    assert len(_DEAD_FUTURE_MESSAGES) >= 2


# ── VIB052: import os for os.path ─────────────────────────────────────────────


def check_os_path(source: str) -> list:
    return OsPathImportRule().check(ast.parse(textwrap.dedent(source)))


def test_052_flags_os_only_for_path():
    src = "import os\nx = os.path.join('a', 'b')"
    errors = check_os_path(src)
    assert len(errors) == 1
    assert "VIB052" in errors[0][2]


def test_052_no_flag_os_used_for_more():
    src = "import os\nos.getcwd()\nos.path.join('a', 'b')"
    assert check_os_path(src) == []


def test_052_no_flag_no_os_import():
    src = "import sys\nsys.exit(0)"
    assert check_os_path(src) == []


def test_052_no_flag_no_os_usage():
    # os is imported but not used at all — VIB049 handles that
    assert check_os_path("import os") == []


def test_052_messages_list():
    assert len(_OS_PATH_MESSAGES) >= 2
