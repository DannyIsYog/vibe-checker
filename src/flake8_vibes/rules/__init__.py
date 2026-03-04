from __future__ import annotations

from flake8_vibes.rules.base import VibError, VibRule
from flake8_vibes.rules.boolean_chaos import (
    EqualsFalseRule,
    EqualsNoneRule,
    EqualsTrueRule,
    NotEqualsRule,
)
from flake8_vibes.rules.thursday_energy import ThursdayEnergyRule
from flake8_vibes.rules.todo_shame import TodoShameRule

ALL_RULES: list[type[VibRule]] = [
    ThursdayEnergyRule,
    TodoShameRule,
    EqualsTrueRule,
    EqualsFalseRule,
    EqualsNoneRule,
    NotEqualsRule,
]

__all__ = ["ALL_RULES", "VibError", "VibRule"]
