from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class VibeReport:
    violations_by_rule: dict[str, int] = field(default_factory=dict)
    total_files: int = 0

    @property
    def total_violations(self) -> int:
        return sum(self.violations_by_rule.values())

    @property
    def score(self) -> int:
        return max(0, min(100, 100 - self.total_violations * 5))

    @property
    def verdict(self) -> str:
        s = self.score
        if s >= 90:
            return "immaculate"
        elif s >= 70:
            return "decent energy"
        elif s >= 50:
            return "concerning"
        elif s >= 25:
            return "chaotic"
        else:
            return "cooked"
