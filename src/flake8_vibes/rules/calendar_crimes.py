from __future__ import annotations

import ast
import random

from flake8_vibes.git import get_file_commit_date
from flake8_vibes.rules.base import VibError, VibRule

_THURSDAY = 3
_FRIDAY = 4
_MONDAY = 0
_DECEMBER = 12
_THURSDAY_ENERGY_THRESHOLD = 20
_MONDAY_SMALL_THRESHOLD = 3


def _is_thursday(filename: str) -> bool:
    """Return True if the file's last commit date is a Thursday."""
    dt = get_file_commit_date(filename)
    if dt is None:
        return False  # no git history — no judgment
    return dt.weekday() == _THURSDAY


def _count_lines(node: ast.FunctionDef | ast.AsyncFunctionDef) -> int:
    return (node.end_lineno or node.lineno) - node.lineno


# ── VIB001 — thursday-energy ─────────────────────────────────────────────────

_MESSAGES = [
    "'{name}' is {n} lines long and it's Thursday. you absolute menace.",
    "'{name}' has {n} lines of thursday ambition. friday will not save you from this.",
    "thursday energy fully detected in '{name}' ({n} lines). you were one day away. ONE day.",
    "'{name}' is {n} lines of pure thursday hubris. we felt it. the diff felt it.",
    "'{name}' ({n} lines) — a thursday crime committed in broad daylight.",
    "{n} lines. on a thursday. '{name}' didn't have to be like this and yet here we are.",
]


def _pick_message(name: str, n: int) -> str:
    return random.choice(_MESSAGES).format(name=name, n=n)


class ThursdayEnergyRule(VibRule):
    code = "VIB001"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        thursday = _is_thursday(filename)
        if not thursday:
            return errors
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                line_count = _count_lines(node)
                if line_count > _THURSDAY_ENERGY_THRESHOLD:
                    msg = _pick_message(node.name, line_count)
                    prefix = f"VIB001 thursday energy detected: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB064 — monday motivation ────────────────────────────────────────────────

_MONDAY_MESSAGES = [
    "'{name}' is {n} lines on a Monday. suspicious simplicity. what does it hide.",
    "monday energy in '{name}' ({n} lines). this is either elegant or a stub. we know which.",
    "'{name}' written on a Monday: {n} lines. the ambition arrives later, uninvited.",
    "small function on a monday: '{name}' ({n} lines). the week just started and you're already cutting corners.",
]


def _is_monday(filename: str) -> bool:
    dt = get_file_commit_date(filename)
    if dt is None:
        return False
    return dt.weekday() == _MONDAY


class MondayMotivationRule(VibRule):
    code = "VIB064"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        if not _is_monday(filename):
            return errors
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                line_count = _count_lines(node)
                if line_count < _MONDAY_SMALL_THRESHOLD:
                    msg = random.choice(_MONDAY_MESSAGES).format(name=node.name, n=line_count)
                    prefix = f"VIB064 calendar: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB065 — friday deploy ────────────────────────────────────────────────────

_FRIDAY_MESSAGES = [
    "this file was last touched on a Friday. the weekend is a diff review nobody wanted.",
    "committed on a Friday. we hope the oncall is someone else.",
    "friday commit detected. whatever ships today ships without a safety net.",
    "last touched on a Friday. it works right now. check back Monday.",
]


def _is_friday(filename: str) -> bool:
    dt = get_file_commit_date(filename)
    if dt is None:
        return False
    return dt.weekday() == _FRIDAY


class FridayDeployRule(VibRule):
    code = "VIB065"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if not _is_friday(filename):
            return []
        msg = random.choice(_FRIDAY_MESSAGES)
        return [(1, 0, f"VIB065 calendar: {msg}", type(self))]


# ── VIB067 — december code ────────────────────────────────────────────────────

_DECEMBER_MESSAGES = [
    "this file was last modified in December. everyone was distracted. it shows.",
    "december commit: half the team was off, the other half was thinking about being off.",
    "written in December. the holiday deadline was real and this code paid the price.",
    "december energy detected. any reviewer was in 'ship it before the holidays' mode.",
]


def _is_december(filename: str) -> bool:
    dt = get_file_commit_date(filename)
    if dt is None:
        return False
    return dt.month == _DECEMBER


class DecemberCodeRule(VibRule):
    code = "VIB067"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if not _is_december(filename):
            return []
        msg = random.choice(_DECEMBER_MESSAGES)
        return [(1, 0, f"VIB067 calendar: {msg}", type(self))]
