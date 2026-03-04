from __future__ import annotations

from flake8_vibes.rules.base import VibError, VibRule
from flake8_vibes.rules.thursday_energy import ThursdayEnergyRule
from flake8_vibes.rules.todo_shame import TodoShameRule

ALL_RULES: list[type[VibRule]] = [
    ThursdayEnergyRule,
    TodoShameRule,
]

__all__ = ["ALL_RULES", "VibError", "VibRule"]
