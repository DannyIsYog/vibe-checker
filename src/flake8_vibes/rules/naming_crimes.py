from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule


def _store_names(tree: ast.AST) -> list[ast.Name]:
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
    ]


def _loop_and_comp_positions(tree: ast.AST) -> set[tuple[int, int]]:
    positions: set[tuple[int, int]] = set()
    for node in ast.walk(tree):
        targets: list[ast.expr] = []
        if isinstance(node, ast.For):
            targets.append(node.target)
        elif isinstance(
            node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)
        ):
            for gen in node.generators:
                targets.append(gen.target)
        for target in targets:
            for name in ast.walk(target):
                if isinstance(name, ast.Name):
                    positions.add((name.lineno, name.col_offset))
    return positions


def _name_words(name: str) -> list[str]:
    """Split a snake_case or PascalCase name into lowercase words."""
    parts = name.split("_")
    words: list[str] = []
    for part in parts:
        # split PascalCase / camelCase into words
        subparts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]|\d+", part)
        words.extend(w.lower() for w in subparts if w)
    return words


# ── VIB013 — god-variable ────────────────────────────────────────────────────

_GOD_NAMES = frozenset({"data", "result", "info", "stuff", "thing", "obj"})

_GOD_VARIABLE_MESSAGES = [
    "`{name}` holds everything and describes absolutely nothing. a true void.",
    "you named it `{name}`. congratulations, that name fits literally anything.",
    "`{name}` is a variable that looked specificity in the eye and said no.",
    "every codebase has a `{name}`. every developer regrets it. yours is no different.",
]


class GodVariableRule(VibRule):
    code = "VIB013"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            if node.id in _GOD_NAMES:
                msg = random.choice(_GOD_VARIABLE_MESSAGES).format(name=node.id)
                prefix = f"VIB013 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB014 — single-letter ───────────────────────────────────────────────────

_SINGLE_LETTER_MESSAGES = [
    "`{name}` outside a loop has a secret identity and is refusing to share it.",
    "single-letter variables outside loops are readability crimes and you are the perpetrator.",
    "`{name}` is one character, zero context, and infinite future confusion.",
    "you used `{name}` like it's self-explanatory. outside a loop, nothing is self-explanatory.",
]


class SingleLetterRule(VibRule):
    code = "VIB014"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        excluded = _loop_and_comp_positions(tree)
        for node in _store_names(tree):
            if len(node.id) == 1 and node.id != "_":
                if (node.lineno, node.col_offset) not in excluded:
                    msg = random.choice(_SINGLE_LETTER_MESSAGES).format(name=node.id)
                    prefix = f"VIB014 naming crime: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB015 — temp-variable ───────────────────────────────────────────────────

_PLACEHOLDER_NAME_MESSAGES = [
    "`{name}` was supposed to be temporary. it has now outlived the sprint it was born in.",
    "temp variables that outlive their branch become permanent fixtures of shame.",
    "`{name}` — the naming equivalent of 'I'll refactor this later'. you won't. we both know it.",
    "calling it `{name}` is a promise you made to yourself that your git history will never let you forget.",
]


class TempVariableRule(VibRule):
    code = "VIB015"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            parts = node.id.lower().split("_")
            if any(re.fullmatch(r"temp\d*|tmp\d*", p) for p in parts):
                msg = random.choice(_PLACEHOLDER_NAME_MESSAGES).format(name=node.id)
                prefix = f"VIB015 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB016 — new-prefix ──────────────────────────────────────────────────────

_NEW_PREFIX_MESSAGES = [
    "`{name}` implies there's an `old_` version lurking nearby. there is, isn't there.",
    "`{name}` — the `new_` prefix means you kept the old one and called it a day. shameful.",
    "`{name}` — `new_` is not a name. it's a timestamp. timestamps are not names.",
    "`{name}` — if you need `new_` to tell it apart, you have two things, one idea, and a problem.",
]


class NewPrefixRule(VibRule):
    code = "VIB016"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            if node.id == "new" or node.id.startswith("new_"):
                msg = random.choice(_NEW_PREFIX_MESSAGES).format(name=node.id)
                prefix = f"VIB016 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB017 — copy-suffix ─────────────────────────────────────────────────────

_COPY_SUFFIX_MESSAGES = [
    "`{name}` — version numbers in variable names is literally what git was invented to prevent.",
    "you appended `_copy` to `{name}` instead of thinking harder. git saw. git judged.",
    "`{name}` tells you its history, not its purpose. those are not the same thing.",
    "suffixing `_copy` or a number on `{name}` is not a naming strategy. it's a surrender.",
]


class CopySuffixRule(VibRule):
    code = "VIB017"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            if re.search(r"_\d+$|_copy$", node.id):
                msg = random.choice(_COPY_SUFFIX_MESSAGES).format(name=node.id)
                prefix = f"VIB017 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB018 — final-variable ──────────────────────────────────────────────────

_OVERCONFIDENT_NAME_MESSAGES = [
    "`{name}` — `final` is not a description, it's cope. three PRs from now it'll be `final_v2_REAL`.",
    "nothing in code is final. `{name}` will be renamed and you will not be ready.",
    "`{name}` — the audacity of `final` in a variable name. the hubris. the nerve.",
    "every `final_` variable has a `final_final_` sibling and a `final_actual_` cousin. it's a family.",
]


class FinalVariableRule(VibRule):
    code = "VIB018"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            if "final" in node.id.lower().split("_"):
                msg = random.choice(_OVERCONFIDENT_NAME_MESSAGES).format(name=node.id)
                prefix = f"VIB018 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB019 — flag-variable ───────────────────────────────────────────────────

_OPAQUE_BOOL_MESSAGES = [
    "`{name}` is a boolean that looked at meaning and said 'not my department'.",
    "a variable called `{name}` tells you it's a boolean and absolutely nothing else. iconic. terrible.",
    "`{name}` is the least informative boolean name in the entire english language.",
    "`flag` is not a question, `{name}` is not an answer, and this code is not doing well.",
]


class FlagVariableRule(VibRule):
    code = "VIB019"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in _store_names(tree):
            if "flag" in node.id.lower().split("_"):
                msg = random.choice(_OPAQUE_BOOL_MESSAGES).format(name=node.id)
                prefix = f"VIB019 naming crime: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB020 — vague-class ─────────────────────────────────────────────────────

_VAGUE_CLASS_MESSAGES = [
    "`{name}` manages something. nobody knows what. not even `{name}`.",
    "Manager classes are where responsibility goes to hide and slowly die. `{name}` is no exception.",
    "`{name}` — every codebase has one. none of them can explain what it actually does. including yours.",
    "`{name}` — a class with Manager in the name is a class that has given up on identity.",
]


class VagueClassRule(VibRule):
    code = "VIB020"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if "manager" in _name_words(node.name):
                    msg = random.choice(_VAGUE_CLASS_MESSAGES).format(name=node.name)
                    prefix = f"VIB020 naming crime: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
