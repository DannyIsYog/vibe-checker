from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.misc_chaos import (
    _ASSERT_NON_TEST_MESSAGES,
    _DICT_CONSTRUCTOR_MESSAGES,
    _EVAL_MESSAGES,
    _EXEC_MESSAGES,
    _FILE_TOO_LONG_MESSAGES,
    _GLOBAL_MESSAGES,
    _LAMBDA_ASSIGNED_MESSAGES,
    _LIST_AROUND_LITERAL_MESSAGES,
    _NESTED_COMPREHENSION_MESSAGES,
    _SYS_EXIT_MESSAGES,
    AssertInNonTestRule,
    DictConstructorRule,
    EvalUsedRule,
    ExecUsedRule,
    FileTooLongRule,
    GlobalStatementRule,
    LambdaAssignedRule,
    ListAroundLiteralRule,
    NestedComprehensionRule,
    SysExitRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


# ── VIB089: lambda assigned ───────────────────────────────────────────────────


def test_089_flags_lambda_assigned():
    errors = LambdaAssignedRule().check(parse("f = lambda x: x + 1"))
    assert len(errors) == 1
    assert "VIB089" in errors[0][2]


def test_089_no_flag_lambda_inline():
    assert LambdaAssignedRule().check(parse("sorted(items, key=lambda x: x)")) == []


def test_089_flags_annotated_assign():
    errors = LambdaAssignedRule().check(parse("f: int = lambda x: x"))
    assert len(errors) == 1


def test_089_messages_list():
    assert len(_LAMBDA_ASSIGNED_MESSAGES) >= 2


# ── VIB090: global statement ──────────────────────────────────────────────────


def test_090_flags_global():
    src = "x = 1\ndef foo():\n    global x\n    x = 2"
    errors = GlobalStatementRule().check(parse(src))
    assert len(errors) == 1
    assert "VIB090" in errors[0][2]


def test_090_no_flag_no_global():
    assert GlobalStatementRule().check(parse("x = 1")) == []


def test_090_messages_list():
    assert len(_GLOBAL_MESSAGES) >= 2


# ── VIB091: eval() ───────────────────────────────────────────────────────────


def test_091_flags_eval():
    errors = EvalUsedRule().check(parse("eval('1 + 1')"))
    assert len(errors) == 1
    assert "VIB091" in errors[0][2]


def test_091_no_flag_other_call():
    assert EvalUsedRule().check(parse("int('42')")) == []


def test_091_messages_list():
    assert len(_EVAL_MESSAGES) >= 2


# ── VIB092: exec() ───────────────────────────────────────────────────────────


def test_092_flags_exec():
    errors = ExecUsedRule().check(parse("exec('x = 1')"))
    assert len(errors) == 1
    assert "VIB092" in errors[0][2]


def test_092_no_flag_other_call():
    assert ExecUsedRule().check(parse("compile('x', '', 'exec')")) == []


def test_092_messages_list():
    assert len(_EXEC_MESSAGES) >= 2


# ── VIB094: file too long ────────────────────────────────────────────────────


def test_094_flags_over_500_lines():
    lines = ["x = 1\n"] * 501
    rule = FileTooLongRule()
    errors = rule.check(parse("x = 1"), lines=lines)
    assert len(errors) == 1
    assert "VIB094" in errors[0][2]
    assert errors[0][0] == 1
    assert errors[0][1] == 0


def test_094_no_flag_exactly_500():
    lines = ["x = 1\n"] * 500
    assert FileTooLongRule().check(parse("x = 1"), lines=lines) == []


def test_094_no_flag_under_500():
    lines = ["x = 1\n"] * 10
    assert FileTooLongRule().check(parse("x = 1"), lines=lines) == []


def test_094_returns_empty_if_no_lines():
    assert FileTooLongRule().check(parse("x = 1")) == []


def test_094_messages_list():
    assert len(_FILE_TOO_LONG_MESSAGES) >= 2


# ── VIB095: nested comprehension ─────────────────────────────────────────────


def test_095_flags_three_levels():
    src = "[x for xs in [[y for y in [z for z in items]]] for x in xs]"
    errors = NestedComprehensionRule().check(parse(src))
    assert len(errors) >= 1
    assert "VIB095" in errors[0][2]


def test_095_no_flag_two_levels():
    src = "[x for xs in [y for y in items] for x in xs]"
    assert NestedComprehensionRule().check(parse(src)) == []


def test_095_no_flag_single_comprehension():
    src = "[x for x in items]"
    assert NestedComprehensionRule().check(parse(src)) == []


def test_095_messages_list():
    assert len(_NESTED_COMPREHENSION_MESSAGES) >= 2


def test_095_no_flag_simple_list_literal():
    src = "[1, 2, 3]"
    assert NestedComprehensionRule().check(parse(src)) == []


# ── VIB096: dict() constructor ───────────────────────────────────────────────


def test_096_flags_dict_with_keywords():
    errors = DictConstructorRule().check(parse("d = dict(a=1, b=2)"))
    assert len(errors) == 1
    assert "VIB096" in errors[0][2]


def test_096_no_flag_empty_dict_call():
    assert DictConstructorRule().check(parse("d = dict()")) == []


def test_096_no_flag_dict_literal():
    assert DictConstructorRule().check(parse("d = {'a': 1}")) == []


def test_096_messages_list():
    assert len(_DICT_CONSTRUCTOR_MESSAGES) >= 2


# ── VIB097: list() around literal ────────────────────────────────────────────


def test_097_flags_list_around_literal():
    errors = ListAroundLiteralRule().check(parse("x = list([1, 2, 3])"))
    assert len(errors) == 1
    assert "VIB097" in errors[0][2]


def test_097_no_flag_list_from_iterable():
    assert ListAroundLiteralRule().check(parse("x = list(items)")) == []


def test_097_no_flag_list_literal():
    assert ListAroundLiteralRule().check(parse("x = [1, 2, 3]")) == []


def test_097_messages_list():
    assert len(_LIST_AROUND_LITERAL_MESSAGES) >= 2


# ── VIB098: assert in non-test ────────────────────────────────────────────────


def test_098_flags_assert_in_non_test():
    errors = AssertInNonTestRule().check(
        parse("assert x > 0"), filename="my_module.py"
    )
    assert len(errors) == 1
    assert "VIB098" in errors[0][2]


def test_098_no_flag_in_test_file():
    assert (
        AssertInNonTestRule().check(
            parse("assert x > 0"), filename="test_my_module.py"
        )
        == []
    )


def test_098_no_flag_no_assert():
    assert AssertInNonTestRule().check(parse("x = 1"), filename="module.py") == []


def test_098_messages_list():
    assert len(_ASSERT_NON_TEST_MESSAGES) >= 2


# ── VIB099: sys.exit() ───────────────────────────────────────────────────────


def test_099_flags_sys_exit():
    errors = SysExitRule().check(parse("import sys\nsys.exit(1)"))
    assert len(errors) == 1
    assert "VIB099" in errors[0][2]


def test_099_no_flag_other_exit():
    assert SysExitRule().check(parse("os.exit(1)")) == []


def test_099_no_flag_sys_other_method():
    assert SysExitRule().check(parse("sys.argv")) == []


def test_099_messages_list():
    assert len(_SYS_EXIT_MESSAGES) >= 2
