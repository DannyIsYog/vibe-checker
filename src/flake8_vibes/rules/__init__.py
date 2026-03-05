from __future__ import annotations

from flake8_vibes.rules.async_crimes import AsyncioSleep0Rule, AsyncNoAwaitRule
from flake8_vibes.rules.base import VibError, VibRule
from flake8_vibes.rules.boolean_chaos import (
    EqualsFalseRule,
    EqualsNoneRule,
    EqualsTrueRule,
    NotEqualsRule,
)
from flake8_vibes.rules.calendar_crimes import (
    DecemberCodeRule,
    FridayDeployRule,
    MondayMotivationRule,
    ThursdayEnergyRule,
)
from flake8_vibes.rules.class_crimes import (
    ClassNoDocstringRule,
    EmptyExceptInDelRule,
    MultipleInheritanceRule,
    NoOpOverrideRule,
    StrReturnsDictRule,
    SuperInitNotCalledRule,
)
from flake8_vibes.rules.comment_sins import (
    CommentedCodeGraveyardRule,
    DoNotTouchRule,
    HackCommentRule,
    LolWtfCommentRule,
    MagicCommentRule,
    NoqaNoCodeRule,
    ObviousCommentRule,
    ThisIsFineRule,
    TodoNamedRule,
    TypeIgnoreNoExplanationRule,
)
from flake8_vibes.rules.debug_artifacts import (
    BreakpointLeftBehindRule,
    ConsoleLogInPyRule,
    ImportPdbRule,
    PdbSetTraceRule,
    PrintLeftBehindRule,
)
from flake8_vibes.rules.docstring_vibes import (
    DocstringArgsMismatchRule,
    DocstringLongerThanFunctionRule,
    DocstringNoPeriodRule,
    DocstringRepeatsNameRule,
)
from flake8_vibes.rules.exception_crimes import (
    ExceptExceptionRule,
    RaiseExceptionRule,
    ReraiseNoLogRule,
)
from flake8_vibes.rules.hardcoding import (
    HardcodedCredentialsRule,
    HardcodedLocalhostRule,
    HardcodedPathRule,
    HardcodedPortRule,
    HardcodedTimeoutRule,
    HardcodedUrlRule,
    MagicNumberRule,
)
from flake8_vibes.rules.import_drama import (
    FutureImportDeadRule,
    ImportInFunctionRule,
    OsPathImportRule,
    StarImportRule,
    UnusedImportRule,
)
from flake8_vibes.rules.misc_chaos import (
    AllExportsPrivateRule,
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
    ZeroStarRepoRule,
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
    UnderscoreUsedRule,
)
from flake8_vibes.rules.string_crimes import (
    FormatPositionalRule,
    MultilineStringCommentRule,
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
    CopyPastedTestRule,
    TestNamedTestItRule,
    TestNoAssertionRule,
    TimeSleepInTestRule,
)
from flake8_vibes.rules.todo_shame import TodoShameRule

ALL_RULES: list[type[VibRule]] = [
    ThursdayEnergyRule,
    TodoShameRule,
    # exception crimes
    ExceptExceptionRule,
    RaiseExceptionRule,
    ReraiseNoLogRule,
    # debug artifacts
    PrintLeftBehindRule,
    BreakpointLeftBehindRule,
    PdbSetTraceRule,
    ImportPdbRule,
    ConsoleLogInPyRule,
    # comment sins
    CommentedCodeGraveyardRule,
    TypeIgnoreNoExplanationRule,
    NoqaNoCodeRule,
    TodoNamedRule,
    ObviousCommentRule,
    HackCommentRule,
    DoNotTouchRule,
    ThisIsFineRule,
    LolWtfCommentRule,
    MagicCommentRule,
    # structure complexity
    TooManyArgsRule,
    DeepNestingRule,
    TooManyReturnsRule,
    BareExceptRule,
    EmptyExceptRule,
    # hardcoding
    MagicNumberRule,
    HardcodedUrlRule,
    HardcodedPortRule,
    HardcodedPathRule,
    HardcodedTimeoutRule,
    HardcodedCredentialsRule,
    HardcodedLocalhostRule,
    # import drama
    StarImportRule,
    UnusedImportRule,
    FutureImportDeadRule,
    ImportInFunctionRule,
    OsPathImportRule,
    # return crimes
    ExplicitReturnNoneRule,
    AssignThenReturnRule,
    MutableDefaultArgRule,
    ShadowBuiltinRule,
    UnderscoreUsedRule,
    # class crimes
    MultipleInheritanceRule,
    StrReturnsDictRule,
    EmptyExceptInDelRule,
    ClassNoDocstringRule,
    SuperInitNotCalledRule,
    NoOpOverrideRule,
    # calendar energy
    MondayMotivationRule,
    FridayDeployRule,
    DecemberCodeRule,
    # test vibes
    TestNoAssertionRule,
    TestNamedTestItRule,
    AssertTrueRule,
    TimeSleepInTestRule,
    CopyPastedTestRule,
    # async crimes
    AsyncNoAwaitRule,
    AsyncioSleep0Rule,
    # string crimes
    StringConcatInLoopRule,
    PercentFormatRule,
    FormatPositionalRule,
    MultilineStringCommentRule,
    # docstring vibes
    DocstringRepeatsNameRule,
    DocstringNoPeriodRule,
    DocstringArgsMismatchRule,
    DocstringLongerThanFunctionRule,
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
    AllExportsPrivateRule,
    ZeroStarRepoRule,
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
