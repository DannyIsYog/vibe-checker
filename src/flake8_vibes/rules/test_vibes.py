from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB069 — test with no assertions ────────────────────────────────────────

_NO_ASSERTION_MESSAGES = [
    "test `{name}` has no assertions. it passes by default. that's not a test, that's a prayer.",
    "`{name}` runs but never asserts anything. a test that can't fail can't prove anything.",
    "found `{name}` with zero assertions. it's green. it means nothing.",
    "`{name}` has no `assert`. it exercises code and trusts it went fine. it didn't.",
]


def _body_has_assert(body: list[ast.stmt]) -> bool:
    for stmt in body:
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if isinstance(stmt, ast.Assert):
            return True
        for child in ast.iter_child_nodes(stmt):
            if _node_has_assert(child):
                return True
    return False


def _node_has_assert(node: ast.AST) -> bool:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    if isinstance(node, ast.Assert):
        return True
    return any(_node_has_assert(c) for c in ast.iter_child_nodes(node))


class TestNoAssertionRule(VibRule):
    code = "VIB069"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if "test" not in filename.lower():
            return []
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                if not _body_has_assert(node.body):
                    msg_tpl = random.choice(_NO_ASSERTION_MESSAGES)
                    msg = msg_tpl.format(name=node.name)
                    prefix = f"VIB069 test: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB070 — test named test_it ──────────────────────────────────────────────

_TEST_IT_MESSAGES = [
    "`test_it` — it. it what? what does it do? what did you test?",
    "a test named `test_it` is a test that chose mystery over clarity.",
    "`test_it` is a test name that tests the reader's patience.",
    "found `test_it`. it tests it. thank you for the information. it means nothing.",
]


class TestNamedTestItRule(VibRule):
    code = "VIB070"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "test_it":
                msg = random.choice(_TEST_IT_MESSAGES)
                prefix = f"VIB070 test: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB071 — assert True ─────────────────────────────────────────────────────

_ASSERT_TRUE_MESSAGES = [
    "`assert True` always passes. it proves nothing. it tests nothing. why is it here.",
    "found `assert True`. congratulations, True is still True. the test suite is no smarter.",
    "`assert True` — you wrote a test that cannot fail. that is not a test.",
    "`assert True` is a test in the same way a tautology is an argument.",
]


class AssertTrueRule(VibRule):
    code = "VIB071"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Assert)
                and isinstance(node.test, ast.Constant)
                and node.test.value is True
            ):
                msg = random.choice(_ASSERT_TRUE_MESSAGES)
                prefix = f"VIB071 test: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB072 — test with time.sleep() ─────────────────────────────────────────

_TIME_SLEEP_MESSAGES = [
    "`time.sleep()` in a test is a guess wearing a timer. mock the time, not the clock.",
    "test uses `time.sleep()`. whatever you're waiting for, you should be mocking it.",
    "found `time.sleep()` in a test. flaky tests have a sleep in them. this is a flaky test.",
    "`time.sleep()` in tests is a prayer that timing will cooperate. it won't, eventually.",
]


class TimeSleepInTestRule(VibRule):
    code = "VIB072"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if "test" not in filename.lower():
            return []
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "sleep"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "time"
            ):
                msg = random.choice(_TIME_SLEEP_MESSAGES)
                prefix = f"VIB072 test: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
