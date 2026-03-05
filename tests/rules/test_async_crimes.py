from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.async_crimes import (
    _ASYNC_NO_AWAIT_MESSAGES,
    _ASYNCIO_SLEEP_0_MESSAGES,
    AsyncioSleep0Rule,
    AsyncNoAwaitRule,
    _has_await,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_no_await(source: str) -> list:
    return AsyncNoAwaitRule().check(parse(source))


def check_sleep_0(source: str) -> list:
    return AsyncioSleep0Rule().check(parse(source))


# ── VIB074: async no await ───────────────────────────────────────────────────


def test_074_flags_async_no_await():
    src = "async def foo():\n    return 1"
    errors = check_no_await(src)
    assert len(errors) == 1
    assert "VIB074" in errors[0][2]


def test_074_no_flag_with_await():
    src = "async def foo():\n    return await bar()"
    assert check_no_await(src) == []


def test_074_no_flag_sync_function():
    src = "def foo():\n    return 1"
    assert check_no_await(src) == []


def test_074_nested_function_not_considered():
    src = "async def outer():\n" "    def inner():\n" "        pass\n" "    return 1\n"
    # outer has no await (the nested sync fn doesn't count)
    errors = check_no_await(src)
    assert len(errors) == 1
    assert "VIB074" in errors[0][2]


def test_074_await_in_nested_async_does_not_satisfy_outer():
    src = (
        "async def outer():\n"
        "    async def inner():\n"
        "        await something()\n"
        "    return 1\n"
    )
    errors = check_no_await(src)
    assert any("VIB074" in e[2] for e in errors)


def test_074_error_tuple_format():
    src = "async def foo():\n    pass"
    row, col, msg, typ = check_no_await(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_074_messages_list():
    assert len(_ASYNC_NO_AWAIT_MESSAGES) >= 2


def test_074_has_await_helper():
    tree = parse("async def foo():\n    await bar()")
    func = tree.body[0]  # type: ignore[attr-defined]
    assert _has_await(func)


def test_074_has_await_helper_false():
    tree = parse("async def foo():\n    return 1")
    func = tree.body[0]  # type: ignore[attr-defined]
    assert not _has_await(func)


# ── VIB076: asyncio.sleep(0) ─────────────────────────────────────────────────


def test_076_flags_asyncio_sleep_0():
    src = "import asyncio\nawait asyncio.sleep(0)"
    errors = check_sleep_0(src)
    assert len(errors) == 1
    assert "VIB076" in errors[0][2]


def test_076_no_flag_asyncio_sleep_nonzero():
    src = "await asyncio.sleep(1)"
    assert check_sleep_0(src) == []


def test_076_no_flag_other_sleep():
    src = "await time.sleep(0)"
    assert check_sleep_0(src) == []


def test_076_no_flag_asyncio_other_method():
    src = "asyncio.run(main())"
    assert check_sleep_0(src) == []


def test_076_error_tuple_format():
    src = "asyncio.sleep(0)"
    row, col, msg, typ = check_sleep_0(src)[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_076_messages_list():
    assert len(_ASYNCIO_SLEEP_0_MESSAGES) >= 2
