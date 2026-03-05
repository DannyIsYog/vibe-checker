from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.comment_sins import (
    _COMMENTED_CODE_MESSAGES,
    _DO_NOT_TOUCH_MESSAGES,
    _HACK_MESSAGES,
    _LOL_WTF_MESSAGES,
    _NOQA_NO_CODE_MESSAGES,
    _THIS_IS_FINE_MESSAGES,
    _TODO_NAMED_MESSAGES,
    _TYPE_IGNORE_MESSAGES,
    CommentedCodeGraveyardRule,
    DoNotTouchRule,
    HackCommentRule,
    LolWtfCommentRule,
    NoqaNoCodeRule,
    ThisIsFineRule,
    TodoNamedRule,
    TypeIgnoreNoExplanationRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check_with_lines(rule_cls: type, source: str) -> list:
    lines = source.splitlines(keepends=True)
    return rule_cls().check(parse(source), lines=lines)


def check_no_lines(rule_cls: type, source: str) -> list:
    return rule_cls().check(parse(source))


# ── VIB021: commented-out code ────────────────────────────────────────────────


def test_021_flags_three_consecutive_code_comments():
    src = "# x = 1\n# y = 2\n# z = 3\n"
    errors = check_with_lines(CommentedCodeGraveyardRule, src)
    assert len(errors) == 1
    assert "VIB021" in errors[0][2]


def test_021_no_flag_two_consecutive():
    src = "# x = 1\n# y = 2\n"
    assert check_with_lines(CommentedCodeGraveyardRule, src) == []


def test_021_no_flag_plain_comments():
    src = "# this is a note\n# another note\n# third note\n"
    assert check_with_lines(CommentedCodeGraveyardRule, src) == []


def test_021_returns_empty_if_no_lines():
    assert check_no_lines(CommentedCodeGraveyardRule, "# x = 1\n# y = 2\n# z = 3\n") == []


def test_021_flags_at_first_line():
    src = "x = 1\n# a = 1\n# b = (2)\n# c = 3\n"
    errors = check_with_lines(CommentedCodeGraveyardRule, src)
    assert len(errors) == 1
    assert errors[0][0] == 2  # second line


def test_021_messages_list():
    assert len(_COMMENTED_CODE_MESSAGES) >= 2


def test_021_flags_self_dot_pattern():
    src = "# self.x = 1\n# self.y = 2\n# self.z = 3\n"
    errors = check_with_lines(CommentedCodeGraveyardRule, src)
    assert len(errors) == 1


# ── VIB022: type: ignore without explanation ──────────────────────────────────


def test_022_flags_bare_type_ignore():
    src = "x = foo()  # type: ignore\n"
    errors = check_with_lines(TypeIgnoreNoExplanationRule, src)
    assert len(errors) == 1
    assert "VIB022" in errors[0][2]


def test_022_no_flag_with_explanation():
    src = "x = foo()  # type: ignore  # foo returns Any\n"
    assert check_with_lines(TypeIgnoreNoExplanationRule, src) == []


def test_022_no_flag_with_code_and_explanation():
    src = "x = foo()  # type: ignore[assignment]  # intentional\n"
    assert check_with_lines(TypeIgnoreNoExplanationRule, src) == []


def test_022_returns_empty_if_no_lines():
    assert check_no_lines(TypeIgnoreNoExplanationRule, "x = 1  # type: ignore\n") == []


def test_022_messages_list():
    assert len(_TYPE_IGNORE_MESSAGES) >= 2


def test_022_flags_with_code_but_no_explanation():
    src = "x = foo()  # type: ignore[assignment]\n"
    errors = check_with_lines(TypeIgnoreNoExplanationRule, src)
    assert len(errors) == 1


# ── VIB023: noqa without code ────────────────────────────────────────────────


def test_023_flags_bare_noqa():
    src = "x = very_long_thing  # noqa\n"
    errors = check_with_lines(NoqaNoCodeRule, src)
    assert len(errors) == 1
    assert "VIB023" in errors[0][2]


def test_023_no_flag_noqa_with_code():
    src = "x = very_long_thing  # noqa: E501\n"
    assert check_with_lines(NoqaNoCodeRule, src) == []


def test_023_returns_empty_if_no_lines():
    assert check_no_lines(NoqaNoCodeRule, "x = 1  # noqa\n") == []


def test_023_messages_list():
    assert len(_NOQA_NO_CODE_MESSAGES) >= 2


# ── VIB024: TODO with name in parens ─────────────────────────────────────────


def test_024_flags_named_todo():
    src = "# TODO(alice): fix this\n"
    errors = check_with_lines(TodoNamedRule, src)
    assert len(errors) == 1
    assert "VIB024" in errors[0][2]


def test_024_no_flag_plain_todo():
    src = "# TODO: fix this\n"
    assert check_with_lines(TodoNamedRule, src) == []


def test_024_returns_empty_if_no_lines():
    assert check_no_lines(TodoNamedRule, "# TODO(alice): fix\n") == []


def test_024_messages_list():
    assert len(_TODO_NAMED_MESSAGES) >= 2


def test_024_name_in_message():
    src = "# TODO(bob): refactor\n"
    errors = check_with_lines(TodoNamedRule, src)
    assert "bob" in errors[0][2]


# ── VIB026: hack/hax comment ─────────────────────────────────────────────────


def test_026_flags_hack():
    src = "# hack: this is terrible\n"
    errors = check_with_lines(HackCommentRule, src)
    assert len(errors) == 1
    assert "VIB026" in errors[0][2]


def test_026_flags_hax():
    src = "# hax: shhhh\n"
    errors = check_with_lines(HackCommentRule, src)
    assert len(errors) == 1


def test_026_case_insensitive():
    src = "# HACK: big hack\n"
    errors = check_with_lines(HackCommentRule, src)
    assert len(errors) == 1


def test_026_no_flag_other_comment():
    src = "# this is a regular comment\n"
    assert check_with_lines(HackCommentRule, src) == []


def test_026_returns_empty_if_no_lines():
    assert check_no_lines(HackCommentRule, "# hack\n") == []


def test_026_messages_list():
    assert len(_HACK_MESSAGES) >= 2


# ── VIB027: do not touch ─────────────────────────────────────────────────────


def test_027_flags_do_not_touch():
    src = "# do not touch\n"
    errors = check_with_lines(DoNotTouchRule, src)
    assert len(errors) == 1
    assert "VIB027" in errors[0][2]


def test_027_case_insensitive():
    src = "# DO NOT TOUCH\n"
    errors = check_with_lines(DoNotTouchRule, src)
    assert len(errors) == 1


def test_027_no_flag_other_comment():
    src = "# touch this carefully\n"
    assert check_with_lines(DoNotTouchRule, src) == []


def test_027_returns_empty_if_no_lines():
    assert check_no_lines(DoNotTouchRule, "# do not touch\n") == []


def test_027_messages_list():
    assert len(_DO_NOT_TOUCH_MESSAGES) >= 2


# ── VIB028: this is fine ─────────────────────────────────────────────────────


def test_028_flags_this_is_fine():
    src = "# this is fine\n"
    errors = check_with_lines(ThisIsFineRule, src)
    assert len(errors) == 1
    assert "VIB028" in errors[0][2]


def test_028_case_insensitive():
    src = "# This Is Fine\n"
    errors = check_with_lines(ThisIsFineRule, src)
    assert len(errors) == 1


def test_028_no_flag_other_comment():
    src = "# everything is totally on fire but we're handling it\n"
    assert check_with_lines(ThisIsFineRule, src) == []


def test_028_returns_empty_if_no_lines():
    assert check_no_lines(ThisIsFineRule, "# this is fine\n") == []


def test_028_messages_list():
    assert len(_THIS_IS_FINE_MESSAGES) >= 2


# ── VIB029: lol/wtf comment ──────────────────────────────────────────────────


def test_029_flags_lol():
    src = "# lol\n"
    errors = check_with_lines(LolWtfCommentRule, src)
    assert len(errors) == 1
    assert "VIB029" in errors[0][2]


def test_029_flags_wtf():
    src = "# wtf\n"
    errors = check_with_lines(LolWtfCommentRule, src)
    assert len(errors) == 1


def test_029_case_insensitive():
    src = "# LOL this broke everything\n"
    errors = check_with_lines(LolWtfCommentRule, src)
    assert len(errors) == 1


def test_029_no_flag_other_comment():
    src = "# everything is fine\n"
    assert check_with_lines(LolWtfCommentRule, src) == []


def test_029_returns_empty_if_no_lines():
    assert check_no_lines(LolWtfCommentRule, "# lol\n") == []


def test_029_messages_list():
    assert len(_LOL_WTF_MESSAGES) >= 2
