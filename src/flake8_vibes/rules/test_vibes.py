from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB069 — test with no assertions ────────────────────────────────────────

_NO_ASSERTION_MESSAGES = [
    "test `{name}` has no assertions. it passes by default. that's not a test, that's a prayer.",
    "`{name}` runs to completion with nothing checked. a confidence builder with no load-bearing truth.",
    "found `{name}` with zero assertions. it's green. it means nothing.",
    "`{name}` has no assertions. whatever happened in there, you've decided to trust it. bold.",
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
    "`time.sleep()` in a test: a race condition waiting for the right CI machine to lose.",
    "`time.sleep()` in a test: you're betting the test suite on timing. timing will betray you.",
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


# ── VIB073 — copy-pasted test body ───────────────────────────────────────────

_COPY_PASTED_TEST_MESSAGES = [
    "test `{name}` has the same body as another test. that's not a second test, it's a copy.",
    "`{name}` is an exact copy of another test. two identical tests prove the same thing once.",
    "found duplicate test body in `{name}`. copy-pasting tests is one test with an identity crisis.",
    "`{name}` and another test are identical. delete one or actually test something different.",
]


def _duplicate_test_errors(
    body_dumps: dict[str, list[ast.FunctionDef]], rule_type: type
) -> list[VibError]:
    errors: list[VibError] = []
    for funcs in body_dumps.values():
        if len(funcs) >= 2:
            for func in funcs[1:]:
                msg = random.choice(_COPY_PASTED_TEST_MESSAGES).format(name=func.name)
                errors.append(
                    (func.lineno, func.col_offset, f"VIB073 test: {msg}", rule_type)
                )
    return errors


class CopyPastedTestRule(VibRule):
    code = "VIB073"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if "test" not in filename.lower():
            return []
        test_funcs = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_")
        ]
        body_dumps: dict[str, list[ast.FunctionDef]] = {}
        for func in test_funcs:
            key = ast.dump(ast.Module(body=func.body, type_ignores=[]))
            body_dumps.setdefault(key, []).append(func)
        return _duplicate_test_errors(body_dumps, type(self))
