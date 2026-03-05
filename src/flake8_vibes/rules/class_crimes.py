from __future__ import annotations

import ast
import random

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB063 — multiple inheritance from 3+ classes ────────────────────────────

_MULTIPLE_INHERITANCE_MESSAGES = [
    "inheriting from {n} classes: you've built a diamond of regret and called it polymorphism.",
    "`class {name}({bases})` — {n} base classes. the MRO is already filing a complaint.",
    "{n} parent classes. your class has more parents than a medieval royal and the drama to match.",
    "inheriting {n} classes means {n} sets of assumptions you now have to honor. good luck.",
]


class MultipleInheritanceRule(VibRule):
    code = "VIB063"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and len(node.bases) >= 3:
                base_count = len(node.bases)
                bases = ", ".join(
                    (b.id if isinstance(b, ast.Name) else "...") for b in node.bases
                )
                msg_tpl = random.choice(_MULTIPLE_INHERITANCE_MESSAGES)
                msg = msg_tpl.format(n=base_count, name=node.name, bases=bases)
                prefix = f"VIB063 class: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
