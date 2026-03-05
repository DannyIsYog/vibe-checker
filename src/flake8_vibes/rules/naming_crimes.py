from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

_GOD_NAMES = frozenset({"data", "result", "info", "stuff", "thing", "obj"})

_GOD_VARIABLE_MESSAGES = [
    "`{name}` holds everything and describes nothing. rename it to reflect what it actually contains.",
    "you named it `{name}`. that name fits anything. give it a name that fits only this.",
    "`{name}` is a variable that refused to be specific. what does it actually hold? name it that.",
    "every codebase has a `{name}`. yours doesn't need one. give it a name with intention.",
]

_SINGLE_LETTER_MESSAGES = [
    "`{name}` outside a loop is a variable with a secret identity. give it a name that describes what it holds.",
    "single-letter variables outside loops are readability crimes. rename `{name}` to something your future self can understand.",
    "`{name}` is one character and zero context. outside a loop or comprehension, that's not concise — it's opaque.",
    "you used `{name}` like everyone knows what it is. outside a loop, they don't. name it.",
]

_PLACEHOLDER_NAME_MESSAGES = [
    "`{name}` was supposed to be temporary. it wasn't. rename it to something that describes what it actually holds.",
    "temp variables that outlive their branch are permanent problems. rename `{name}` before someone else inherits it.",
    "`{name}` — the naming equivalent of 'I'll clean this up later'. you won't. rename it now.",
    "calling it `{name}` is a promise you made to yourself that you broke. give it a real name.",
]

_NEW_PREFIX_MESSAGES = [
    "`{name}` implies there's an `old_` version nearby. there isn't. drop the prefix and name it for what it holds.",
    "the `new_` prefix means you had an `old_` and didn't clean up. rename `{name}` to describe the value, not its origin.",
    "`{name}` — temporal naming is not naming. what does it hold? call it that.",
    "if you need `new_` to tell it apart, you have two things and one idea. refactor, then rename `{name}`.",
]

_COPY_SUFFIX_MESSAGES = [
    "`{name}` — version numbers in variable names is what git branches are for. rename it to say what makes it different.",
    "you added `_copy` or a number to `{name}` instead of thinking of a better name. it's not too late. rename it.",
    "`{name}` is a variable name that tells you its history, not its purpose. name it for what it does.",
    "suffixing numbers or `_copy` on `{name}` is a naming strategy that fails at scale. what does this one actually represent?",
]

_OVERCONFIDENT_NAME_MESSAGES = [
    "`{name}` — `final` is not a description, it's a wish. three PRs from now it'll be `final_v2`. name it for its content.",
    "nothing in code is final. `{name}` will be renamed. get ahead of it and name it what it actually is.",
    "`{name}` — the hubris of `final` in a variable name. describe the value, not your confidence in it.",
    "every `final_` variable has a sibling named `final_final_`. break the cycle. rename `{name}` to something honest.",
]

_OPAQUE_BOOL_MESSAGES = [
    "`{name}` is a boolean that refused to describe itself. use `is_`, `has_`, `should_`, or `can_` — answer a yes/no question.",
    "a variable called `{name}` tells you it's a boolean and nothing else. what does it flag? name it that.",
    "`{name}` is the least informative boolean name available. `is_valid`, `has_errors`, `should_retry` — pick one that fits.",
    "rename `{name}` to something that reads like a question with a yes/no answer. `flag` is not a question.",
]

_VAGUE_CLASS_MESSAGES = [
    "`{name}` manages something. the question is what. add a docstring, narrow its scope, or rename it to be honest.",
    "Manager classes are where responsibility goes to hide. what does `{name}` actually manage? document it.",
    "`{name}` — every codebase has one, none of them know what it does. split it into focused classes or add a docstring.",
    "a class with Manager in the name is a class with identity issues. `{name}` — what exactly is being managed here?",
]


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
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            for gen in node.generators:
                targets.append(gen.target)
        for t in targets:
            for n in ast.walk(t):
                if isinstance(n, ast.Name):
                    positions.add((n.lineno, n.col_offset))
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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB013 naming crime: {msg}", type(self))
                )
        return errors


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
                    errors.append(
                        (node.lineno, node.col_offset, f"VIB014 naming crime: {msg}", type(self))
                    )
        return errors


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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB015 naming crime: {msg}", type(self))
                )
        return errors


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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB016 naming crime: {msg}", type(self))
                )
        return errors


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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB017 naming crime: {msg}", type(self))
                )
        return errors


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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB018 naming crime: {msg}", type(self))
                )
        return errors


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
                errors.append(
                    (node.lineno, node.col_offset, f"VIB019 naming crime: {msg}", type(self))
                )
        return errors


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
                    errors.append(
                        (node.lineno, node.col_offset, f"VIB020 naming crime: {msg}", type(self))
                    )
        return errors
