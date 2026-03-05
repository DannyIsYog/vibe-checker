from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.test_vibes import (
    _ASSERT_TRUE_MESSAGES,
    _COPY_PASTED_TEST_MESSAGES,
    _NO_ASSERTION_MESSAGES,
    _TEST_IT_MESSAGES,
    _TIME_SLEEP_MESSAGES,
    AssertTrueRule,
    CopyPastedTestRule,
    TestNamedTestItRule,
    TestNoAssertionRule,
    TimeSleepInTestRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_no_assertion(source: str, filename: str = "test_foo.py") -> list:
    return TestNoAssertionRule().check(parse(source), filename=filename)


def check_test_it(source: str) -> list:
    return TestNamedTestItRule().check(parse(source))


def check_assert_true(source: str) -> list:
    return AssertTrueRule().check(parse(source))


def check_time_sleep(source: str, filename: str = "test_foo.py") -> list:
    return TimeSleepInTestRule().check(parse(source), filename=filename)


# ── VIB069: test with no assertions ──────────────────────────────────────────


def test_069_flags_test_no_assert():
    src = "def test_foo():\n    x = 1\n"
    errors = check_no_assertion(src)
    assert len(errors) == 1
    assert "VIB069" in errors[0][2]


def test_069_no_flag_test_with_assert():
    src = "def test_foo():\n    assert True\n"
    assert check_no_assertion(src) == []


def test_069_no_flag_non_test_file():
    src = "def test_foo():\n    x = 1\n"
    assert check_no_assertion(src, filename="module.py") == []


def test_069_no_flag_non_test_function():
    src = "def helper():\n    x = 1\n"
    assert check_no_assertion(src) == []


def test_069_name_in_message():
    src = "def test_bar():\n    pass\n"
    errors = check_no_assertion(src)
    assert "test_bar" in errors[0][2]


def test_069_messages_list():
    assert len(_NO_ASSERTION_MESSAGES) >= 2


def test_069_assert_in_if_block():
    src = "def test_baz():\n    if True:\n        assert 1 == 1\n"
    assert check_no_assertion(src) == []


def test_069_nested_def_skipped_still_flags_outer():
    src = (
        "def test_outer():\n" "    def inner():\n" "        assert True\n" "    pass\n"
    )
    # outer has no assert (inner's assert doesn't count)
    errors = check_no_assertion(src)
    assert len(errors) == 1
    assert "VIB069" in errors[0][2]


def test_069_nested_def_with_assert_nested_in_if():
    src = (
        "def test_outer():\n"
        "    if condition:\n"
        "        def inner():\n"
        "            assert True\n"
        "    pass\n"
    )
    # outer has no assert (inner is a nested def)
    errors = check_no_assertion(src)
    assert len(errors) == 1


# ── VIB070: test named test_it ────────────────────────────────────────────────


def test_070_flags_test_it():
    errors = check_test_it("def test_it():\n    assert True")
    assert len(errors) == 1
    assert "VIB070" in errors[0][2]


def test_070_no_flag_other_name():
    assert check_test_it("def test_something():\n    assert True") == []


def test_070_no_flag_test_it_prefix():
    assert check_test_it("def test_it_works():\n    assert True") == []


def test_070_messages_list():
    assert len(_TEST_IT_MESSAGES) >= 2


def test_070_flags_regardless_of_file():
    errors = TestNamedTestItRule().check(
        parse("def test_it():\n    assert True"), filename="module.py"
    )
    assert len(errors) == 1


# ── VIB071: assert True ──────────────────────────────────────────────────────


def test_071_flags_assert_true():
    errors = check_assert_true("assert True")
    assert len(errors) == 1
    assert "VIB071" in errors[0][2]


def test_071_no_flag_assert_false():
    assert check_assert_true("assert False") == []


def test_071_no_flag_assert_expression():
    assert check_assert_true("assert x == 1") == []


def test_071_no_flag_assert_variable():
    assert check_assert_true("assert is_valid") == []


def test_071_messages_list():
    assert len(_ASSERT_TRUE_MESSAGES) >= 2


# ── VIB072: time.sleep in test ────────────────────────────────────────────────


def test_072_flags_time_sleep_in_test():
    src = "import time\ntime.sleep(1)"
    errors = check_time_sleep(src)
    assert len(errors) == 1
    assert "VIB072" in errors[0][2]


def test_072_no_flag_in_non_test_file():
    src = "import time\ntime.sleep(1)"
    assert check_time_sleep(src, filename="module.py") == []


def test_072_no_flag_asyncio_sleep():
    src = "import asyncio\nasyncio.sleep(0)"
    assert check_time_sleep(src) == []


def test_072_messages_list():
    assert len(_TIME_SLEEP_MESSAGES) >= 2


# ── VIB073: copy-pasted test body ────────────────────────────────────────────


def check_copy_paste(source: str) -> list:
    tree = ast.parse(textwrap.dedent(source))
    return CopyPastedTestRule().check(tree, filename="test_stuff.py")


def test_073_flags_identical_tests():
    src = textwrap.dedent("""\
        def test_one():
            assert 1 == 1

        def test_two():
            assert 1 == 1
    """)
    errors = check_copy_paste(src)
    assert len(errors) == 1
    assert "VIB073" in errors[0][2]


def test_073_no_flag_different_bodies():
    src = textwrap.dedent("""\
        def test_one():
            assert 1 == 1

        def test_two():
            assert 2 == 2
    """)
    assert check_copy_paste(src) == []


def test_073_no_flag_single_test():
    src = "def test_one():\n    assert 1 == 1\n"
    assert check_copy_paste(src) == []


def test_073_no_flag_non_test_file():
    src = textwrap.dedent("""\
        def test_one():
            assert 1 == 1

        def test_two():
            assert 1 == 1
    """)
    tree = ast.parse(src)
    assert CopyPastedTestRule().check(tree, filename="helpers.py") == []


def test_073_messages_list():
    assert len(_COPY_PASTED_TEST_MESSAGES) >= 2
