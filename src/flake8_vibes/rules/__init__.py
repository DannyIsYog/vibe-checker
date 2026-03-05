from __future__ import annotations

from flake8_vibes.rules.async_crimes import AsyncioSleep0Rule, AsyncNoAwaitRule
from flake8_vibes.rules.base import VibError, VibRule
from flake8_vibes.rules.boolean_chaos import (
    EqualsFalseRule,
    EqualsNoneRule,
    EqualsTrueRule,
    NotEqualsRule,
)
from flake8_vibes.rules.class_crimes import MultipleInheritanceRule
from flake8_vibes.rules.comment_sins import (
    CommentedCodeGraveyardRule,
    DoNotTouchRule,
    HackCommentRule,
    LolWtfCommentRule,
    NoqaNoCodeRule,
    ThisIsFineRule,
    TodoNamedRule,
    TypeIgnoreNoExplanationRule,
)
from flake8_vibes.rules.debug_artifacts import (
    BreakpointLeftBehindRule,
    ImportPdbRule,
    PdbSetTraceRule,
    PrintLeftBehindRule,
)
from flake8_vibes.rules.exception_crimes import ExceptExceptionRule, RaiseExceptionRule
from flake8_vibes.rules.import_drama import ImportInFunctionRule, StarImportRule
from flake8_vibes.rules.misc_chaos import (
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
from flake8_vibes.rules.naming_crimes import (
    CopySuffixRule,
    FinalVariableRule,
    FlagVariableRule,
    GodVariableRule,
    NewPrefixRule,
    SingleLetterRule,
    TempVariableRule,
    VagueClassRule,
)
from flake8_vibes.rules.return_crimes import (
    AssignThenReturnRule,
    ExplicitReturnNoneRule,
    MutableDefaultArgRule,
    ShadowBuiltinRule,
)
from flake8_vibes.rules.string_crimes import (
    FormatPositionalRule,
    PercentFormatRule,
    StringConcatInLoopRule,
)
from flake8_vibes.rules.structure_complexity import (
    BareExceptRule,
    DeepNestingRule,
    EmptyExceptRule,
    TooManyArgsRule,
    TooManyReturnsRule,
)
from flake8_vibes.rules.test_vibes import (
    AssertTrueRule,
    TestNamedTestItRule,
    TestNoAssertionRule,
    TimeSleepInTestRule,
)
from flake8_vibes.rules.thursday_energy import ThursdayEnergyRule
from flake8_vibes.rules.todo_shame import TodoShameRule

ALL_RULES: list[type[VibRule]] = [
    ThursdayEnergyRule,
    TodoShameRule,
    # exception crimes
    ExceptExceptionRule,
    RaiseExceptionRule,
    # debug artifacts
    PrintLeftBehindRule,
    BreakpointLeftBehindRule,
    PdbSetTraceRule,
    ImportPdbRule,
    # comment sins
    CommentedCodeGraveyardRule,
    TypeIgnoreNoExplanationRule,
    NoqaNoCodeRule,
    TodoNamedRule,
    HackCommentRule,
    DoNotTouchRule,
    ThisIsFineRule,
    LolWtfCommentRule,
    # structure complexity
    TooManyArgsRule,
    DeepNestingRule,
    TooManyReturnsRule,
    BareExceptRule,
    EmptyExceptRule,
    # class crimes
    MultipleInheritanceRule,
    # test vibes
    TestNoAssertionRule,
    TestNamedTestItRule,
    AssertTrueRule,
    TimeSleepInTestRule,
    # import drama
    StarImportRule,
    ImportInFunctionRule,
    # return crimes
    ExplicitReturnNoneRule,
    AssignThenReturnRule,
    MutableDefaultArgRule,
    ShadowBuiltinRule,
    # async crimes
    AsyncNoAwaitRule,
    AsyncioSleep0Rule,
    # string crimes
    StringConcatInLoopRule,
    PercentFormatRule,
    FormatPositionalRule,
    # misc chaos
    LambdaAssignedRule,
    GlobalStatementRule,
    EvalUsedRule,
    ExecUsedRule,
    FileTooLongRule,
    NestedComprehensionRule,
    DictConstructorRule,
    ListAroundLiteralRule,
    AssertInNonTestRule,
    SysExitRule,
    # boolean chaos
    EqualsTrueRule,
    EqualsFalseRule,
    EqualsNoneRule,
    NotEqualsRule,
    # naming crimes
    GodVariableRule,
    SingleLetterRule,
    TempVariableRule,
    NewPrefixRule,
    CopySuffixRule,
    FinalVariableRule,
    FlagVariableRule,
    VagueClassRule,
]

_codes = [r.code for r in ALL_RULES]
_dupes = {c for c in _codes if _codes.count(c) > 1}
if _dupes:
    raise RuntimeError(f"duplicate rule codes: {_dupes}")

__all__ = ["ALL_RULES", "VibError", "VibRule"]
