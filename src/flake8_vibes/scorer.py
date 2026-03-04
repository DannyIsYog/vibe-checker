from __future__ import annotations

import random
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
            return random.choice(["she ate and left no crumbs", "slaying", "immaculate", "serving"])
        elif s >= 70:
            return random.choice(["decent energy", "not bad not great", "it's giving something"])
        elif s >= 50:
            return random.choice(["concerning", "the vibes are questionable", "we need to talk"])
        elif s >= 25:
            return random.choice(["chaotic", "this is a cry for help", "bestie no"])
        else:
            return random.choice(["cooked", "it's giving dumpster fire", "expired"])
