from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

_PATTERN = re.compile(r"#\s*(TODO|FIXME)\b", re.IGNORECASE)

# ── VIB002 — todo-shame ──────────────────────────────────────────────────────

_MESSAGES: dict[str, list[str]] = {
    "TODO": [
        "unresolved TODO left to rot",
        "a TODO is just a dream with a comment attached",
        "TODO: still here. still waiting. still judging you.",
        "you wrote TODO and kept moving. bold.",
        "this TODO has seen three sprints and counting",
        "a TODO is not a plan, it's a confession",
    ],
    "FIXME": [
        "FIXME has been here longer than some teammates",
        "you knew it was broken and shipped it anyway",
        "FIXME: acknowledged, unaddressed, unforgiven",
        "a FIXME is just a bug with good self-awareness",
        "the FIXME is still here. so is the shame.",
        "you wrote FIXME like that would make it someone else's problem",
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
