from __future__ import annotations

import random
from dataclasses import dataclass, field

_SCORE_MAX = 100
_SCORE_PENALTY = 5

_SCORE_VERDICTS: list[tuple[int, list[str]]] = [
    (90, ["she ate and left no crumbs", "slaying", "immaculate", "serving"]),
    (70, ["decent energy", "not bad not great", "it's giving something"]),
    (50, ["concerning", "the vibes are questionable", "we need to talk"]),
    (25, ["chaotic", "this is a cry for help", "bestie no"]),
    (0, ["cooked", "it's giving dumpster fire", "expired"]),
]


def score_to_verdict(score: int) -> str:
    options = next(opts for threshold, opts in _SCORE_VERDICTS if score >= threshold)
    return random.choice(options)


@dataclass
class VibeReport:
    violations_by_rule: dict[str, int] = field(default_factory=dict)
    violations_by_file: dict[str, int] = field(default_factory=dict)
    total_files: int = 0

    @property
    def total_violations(self) -> int:
        return sum(self.violations_by_rule.values())

    @property
    def score(self) -> int:
        if self.total_files == 0:
            return _SCORE_MAX
        density = self.total_violations / self.total_files
        return max(0, min(_SCORE_MAX, round(_SCORE_MAX - density * _SCORE_PENALTY)))

    @staticmethod
    def file_score(count: int) -> int:
        return max(0, min(_SCORE_MAX, _SCORE_MAX - count * _SCORE_PENALTY))

    @property
    def verdict(self) -> str:
        return score_to_verdict(self.score)
