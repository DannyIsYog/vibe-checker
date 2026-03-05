from __future__ import annotations

from flake8_vibes.rules.base import VibError, VibRule
from flake8_vibes.rules.boolean_chaos import (
    EqualsFalseRule,
    EqualsNoneRule,
    EqualsTrueRule,
    NotEqualsRule,
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
from flake8_vibes.rules.structure_complexity import (
    BareExceptRule,
    DeepNestingRule,
    EmptyExceptRule,
    TooManyArgsRule,
    TooManyReturnsRule,
)
from flake8_vibes.rules.thursday_energy import ThursdayEnergyRule
from flake8_vibes.rules.todo_shame import TodoShameRule

ALL_RULES: list[type[VibRule]] = [
    ThursdayEnergyRule,
    TodoShameRule,
    TooManyArgsRule,
    DeepNestingRule,
    TooManyReturnsRule,
    BareExceptRule,
    EmptyExceptRule,
    EqualsTrueRule,
    EqualsFalseRule,
    EqualsNoneRule,
    NotEqualsRule,
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
