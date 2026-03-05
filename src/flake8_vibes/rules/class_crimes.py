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


_MIN_BASES_FOR_INHERITANCE_CRIME = 3


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
            if (
                isinstance(node, ast.ClassDef)
                and len(node.bases) >= _MIN_BASES_FOR_INHERITANCE_CRIME
            ):
                base_count = len(node.bases)
                bases = ", ".join(
                    (b.id if isinstance(b, ast.Name) else "...") for b in node.bases
                )
                msg_tpl = random.choice(_MULTIPLE_INHERITANCE_MESSAGES)
                msg = msg_tpl.format(n=base_count, name=node.name, bases=bases)
                prefix = f"VIB063 class: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB058 — __str__ that returns self.__dict__ ───────────────────────────────

_STR_RETURNS_DICT_MESSAGES = [
    "`__str__` that dumps `self.__dict__` is a class that overshares. write a real string.",
    "returning `self.__dict__` from `__str__` is debugging output masquerading as representation.",
    "`__str__` should be human-readable. `self.__dict__` is not readable, it's a data dump.",
    "a `__str__` that returns `self.__dict__` is not a string representation. it's a surrender.",
]


def _is_self_dict(node: ast.expr) -> bool:
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "__dict__"
        and isinstance(node.value, ast.Name)
        and node.value.id == "self"
    )


def _is_str_dict_call(val: ast.expr) -> bool:
    return (
        isinstance(val, ast.Call)
        and isinstance(val.func, ast.Name)
        and val.func.id == "str"
        and bool(val.args)
        and _is_self_dict(val.args[0])
    )


def _str_returns_dict_errors(func: ast.FunctionDef, rule_type: type) -> list[VibError]:
    errors: list[VibError] = []
    for stmt in ast.walk(func):
        if isinstance(stmt, ast.Return) and stmt.value is not None:
            if _is_self_dict(stmt.value) or _is_str_dict_call(stmt.value):
                msg = random.choice(_STR_RETURNS_DICT_MESSAGES)
                errors.append(
                    (stmt.lineno, stmt.col_offset, f"VIB058 class: {msg}", rule_type)
                )
    return errors


class StrReturnsDictRule(VibRule):
    code = "VIB058"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "__str__":
                errors.extend(_str_returns_dict_errors(node, type(self)))
        return errors


# ── VIB059 — empty except in __del__ ─────────────────────────────────────────

_EMPTY_EXCEPT_DEL_MESSAGES = [
    "`__del__` with an empty `except` is a destructor that swallows its own errors. impressive.",
    "empty `except` in `__del__`: cleanup code that hides what went wrong. doubly unhelpful.",
    "found silent failure in `__del__`. the object is dying and you don't want to know how.",
    "`__del__` with `except: pass` is the final word in exception suppression. and the worst.",
]


def _del_pass_handlers(tree: ast.AST) -> list[ast.ExceptHandler]:
    handlers = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name != "__del__":
            continue
        for stmt in ast.walk(node):
            if not isinstance(stmt, ast.Try):
                continue
            for handler in stmt.handlers:
                if all(isinstance(s, ast.Pass) for s in handler.body):
                    handlers.append(handler)
    return handlers


class EmptyExceptInDelRule(VibRule):
    code = "VIB059"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for h in _del_pass_handlers(tree):
            msg = random.choice(_EMPTY_EXCEPT_DEL_MESSAGES)
            errors.append((h.lineno, h.col_offset, f"VIB059 class: {msg}", type(self)))
        return errors


# ── VIB060 — class with no docstring and more than 100 lines ─────────────────

_CLASS_NO_DOCSTRING_MESSAGES = [
    "class `{name}` is {n} lines of mystery. it does things. it keeps them to itself.",
    "`{name}` has {n} lines and no docstring. the code is long, the communication is absent.",
    "{n}-line class `{name}` without a docstring. whatever this does, it hasn't introduced itself.",
    "`{name}`: {n} lines with no introduction, no docstring, and declining to answer questions.",
]

_CLASS_DOC_MIN_LINES = 100


def _has_docstring(node: ast.ClassDef) -> bool:
    return (
        bool(node.body)
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    )


class ClassNoDocstringRule(VibRule):
    code = "VIB060"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            line_count = (node.end_lineno or node.lineno) - node.lineno
            if line_count <= _CLASS_DOC_MIN_LINES:
                continue
            if not _has_docstring(node):
                msg = random.choice(_CLASS_NO_DOCSTRING_MESSAGES).format(
                    name=node.name, n=line_count
                )
                errors.append(
                    (node.lineno, node.col_offset, f"VIB060 class: {msg}", type(self))
                )
        return errors


# ── VIB061 — super().__init__() not called ────────────────────────────────────

_SUPER_INIT_MESSAGES = [
    "inheriting from a class and not calling `super().__init__()` is cutting in line.",
    "`__init__` in `{name}` doesn't call `super().__init__()`. the parent class has feelings too.",
    "`__init__` in `{name}` — the parent class was skipped. it will be fine. probably.",
    "`{name}` ignored the parent class in `__init__`. that relationship has consequences.",
]


def _has_super_init_call(func: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for node in ast.walk(func):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "__init__"
            and isinstance(node.func.value, ast.Call)
            and isinstance(node.func.value.func, ast.Name)
            and node.func.value.func.id == "super"
        ):
            return True
    return False


def _super_init_missing_errors(cls: ast.ClassDef, rule_type: type) -> list[VibError]:
    real_bases = [
        b for b in cls.bases if not (isinstance(b, ast.Name) and b.id == "object")
    ]
    if not real_bases:
        return []
    errors: list[VibError] = []
    for item in cls.body:
        if (
            isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
            and item.name == "__init__"
        ):
            if not _has_super_init_call(item):
                msg = random.choice(_SUPER_INIT_MESSAGES).format(name=cls.name)
                errors.append(
                    (item.lineno, item.col_offset, f"VIB061 class: {msg}", rule_type)
                )
    return errors


class SuperInitNotCalledRule(VibRule):
    code = "VIB061"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                errors.extend(_super_init_missing_errors(node, type(self)))
        return errors


# ── VIB062 — overriding a method and doing nothing different ─────────────────

_NO_OP_OVERRIDE_MESSAGES = [
    "method `{name}` overrides the parent but just calls `super().{name}(...)`. why override it.",
    "`{name}` overrides to do exactly what the parent already does. the override is decorative.",
    "overriding `{name}` to call `super().{name}(...)` with no modification is noise, not code.",
    "`{name}` is an override that changes nothing. it is a costume on a costume.",
]

_MAGIC_METHODS = frozenset(
    {
        "__init__",
        "__str__",
        "__repr__",
        "__eq__",
        "__hash__",
        "__lt__",
        "__le__",
        "__gt__",
        "__ge__",
        "__ne__",
        "__enter__",
        "__exit__",
        "__len__",
        "__iter__",
        "__next__",
        "__getitem__",
        "__setitem__",
        "__delitem__",
        "__contains__",
        "__call__",
        "__del__",
        "__new__",
    }
)


def _is_super_passthrough(func: ast.FunctionDef) -> bool:
    """True if func body is a single super().method_name(...) call or return of it."""
    body = func.body
    if len(body) != 1:
        return False
    stmt = body[0]
    call: ast.Call | None = None
    if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Call):
        call = stmt.value
    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
        call = stmt.value
    if call is None:
        return False
    return (
        isinstance(call.func, ast.Attribute)
        and call.func.attr == func.name
        and isinstance(call.func.value, ast.Call)
        and isinstance(call.func.value.func, ast.Name)
        and call.func.value.func.id == "super"
    )


def _no_op_overrides(tree: ast.AST) -> list[ast.FunctionDef]:
    overrides = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.ClassDef) or not node.bases:
            continue
        for item in node.body:
            if not isinstance(item, ast.FunctionDef):
                continue
            if item.name in _MAGIC_METHODS:
                continue
            if _is_super_passthrough(item):
                overrides.append(item)
    return overrides


class NoOpOverrideRule(VibRule):
    code = "VIB062"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for item in _no_op_overrides(tree):
            msg = random.choice(_NO_OP_OVERRIDE_MESSAGES).format(name=item.name)
            errors.append(
                (item.lineno, item.col_offset, f"VIB062 class: {msg}", type(self))
            )
        return errors
