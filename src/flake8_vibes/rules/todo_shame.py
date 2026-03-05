from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

_PATTERN = re.compile(r"#\s*(TODO|FIXME)\b", re.IGNORECASE)

# ── VIB002 — todo-shame ──────────────────────────────────────────────────────

_MESSAGES: dict[str, list[str]] = {
    "TODO": [
        "unresolved TODO left to age like milk, not wine",
        "a TODO is a dream with a comment attached and no follow-through",
        "TODO: still here. still waiting. still judging every commit you've made since.",
        "you wrote TODO and kept moving. bold. irresponsible. classic.",
        "this TODO has survived more sprints than some of your teammates",
        "a TODO is not a plan. it's a confession that you knew and did nothing.",
    ],
    "FIXME": [
        "FIXME has been here longer than some teammates and has more institutional knowledge",
        "you knew it was broken. you wrote FIXME. you shipped it. incredible.",
        "FIXME: acknowledged, unaddressed, unforgiven, and now publicly humiliated",
        "a FIXME is just a bug that developed self-awareness and still didn't get fixed",
        "the FIXME is still here. so is the shame. they have moved in together.",
        "you wrote FIXME like that was going to make it someone else's problem. it did not.",
    ],
}


def _pick_message(tag: str) -> str:
    return random.choice(_MESSAGES[tag])


class TodoShameRule(VibRule):
    code = "VIB002"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for lineno, line in enumerate(lines, start=1):
            match = _PATTERN.search(line)
            if match:
                tag = match.group(1).upper()
                col = match.start()
                msg = _pick_message(tag)
                prefix = f"VIB002 todo shame: {msg}"
                errors.append((lineno, col, prefix, type(self)))
        return errors
