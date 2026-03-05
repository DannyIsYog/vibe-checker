from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

_CODE_INDICATORS = (
    "=",
    "(",
    ")",
    "self.",
    "return ",
    "def ",
    "class ",
    "import ",
    "for ",
    "if ",
    "while ",
)
_GRAVEYARD_MIN_RUN = 3

# ── VIB021 — commented-out code graveyard ───────────────────────────────────

_COMMENTED_CODE_MESSAGES = [
    "3+ lines of commented-out code found. they're not dead enough to delete and not alive enough to run. haunted.",
    "a graveyard of commented code detected. delete it or commit to it, stop hovering.",
    "this commented-out code has survived more deploys than it deserved. impressive. also: embarrassing.",
    "found a commented-out code block. git blame will find you. it always does.",
]


def _line_looks_like_code_comment(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("#"):
        return False
    content = stripped[1:].strip()
    return any(indicator in content for indicator in _CODE_INDICATORS)


def _graveyard_positions(lines: list[str]) -> list[int]:
    positions = []
    run_start, run_length = -1, 0
    for i, line in enumerate(lines):
        if _line_looks_like_code_comment(line):
            if run_length == 0:
                run_start = i
            run_length += 1
            if run_length == _GRAVEYARD_MIN_RUN:
                positions.append(run_start + 1)
        else:
            run_start, run_length = -1, 0
    return positions


class CommentedCodeGraveyardRule(VibRule):
    code = "VIB021"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        return [
            (
                pos,
                0,
                f"VIB021 comment: {random.choice(_COMMENTED_CODE_MESSAGES)}",
                type(self),
            )
            for pos in _graveyard_positions(lines)
        ]


# ── VIB022 — type: ignore without explanation ────────────────────────────────

_TYPE_IGNORE_MESSAGES = [
    "silent type-ignore with no explanation is a lie you're asking mypy to sign off on.",
    "type-ignore alone — you know something is wrong and you chose not to say what.",
    "type-ignore without a reason is an unanswered question you committed to the repo.",
    "a type-ignore with nothing after it is a sealed verdict and a destroyed evidence bag.",
]


_TYPE_IGNORE_MARKER = "# type:" + " ignore"


def _type_ignore_has_explanation(line: str) -> bool:
    after = line[line.index(_TYPE_IGNORE_MARKER) + len(_TYPE_IGNORE_MARKER) :]
    after_stripped = re.sub(r"^\[[^\]]*\]", "", after.strip()).strip()
    return after_stripped.startswith("#")


class TypeIgnoreNoExplanationRule(VibRule):
    code = "VIB022"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _TYPE_IGNORE_MARKER in line and not _type_ignore_has_explanation(line):
                msg = random.choice(_TYPE_IGNORE_MESSAGES)
                errors.append((i + 1, 0, f"VIB022 comment: {msg}", type(self)))
        return errors


# ── VIB023 — noqa without code ──────────────────────────────────────────────

_NOQA_NO_CODE_MESSAGES = [
    "bare noqa: a silencer for the entire lint rulebook. cowardly. efficient. wrong.",
    "noqa with no code is 'i know it's wrong and i refuse to say which wrong'.",
    "noqa alone is a blanket over a pile of lint that you refused to identify.",
    "a noqa with no code is the smell of someone who gave up and called it a fix.",
]


class NoqaNoCodeRule(VibRule):
    code = "VIB023"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        _noqa = "#" + " noqa"
        for i, line in enumerate(lines):
            if _noqa in line:
                after = line[line.index(_noqa) + len(_noqa) :]
                if not after.lstrip().startswith(":"):
                    msg = random.choice(_NOQA_NO_CODE_MESSAGES)
                    prefix = f"VIB023 comment: {msg}"
                    errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB024 — TODO with a name in parens ─────────────────────────────────────

_TODO_NAMED_MESSAGES = [
    "found a named TODO. {name} hasn't fixed it. the ticket hasn't fixed it. the comment remains.",
    "TODO assigned to {name}. has {name} seen this? has {name} done anything about it? no.",
    "a named TODO is passive-aggressive task assignment. {name}'s name is here. the work is not.",
    "TODO with {name}'s name in it — the person, the comment, and the unfinished work, immortalized.",
]


_TODO_NAMED_RE = re.compile(r"#\s*TODO\s*\(([^)]+)\)", re.IGNORECASE)


class TodoNamedRule(VibRule):
    code = "VIB024"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            match = _TODO_NAMED_RE.search(line)
            if match:
                name = match.group(1).strip()
                msg_tpl = random.choice(_TODO_NAMED_MESSAGES)
                msg = msg_tpl.format(name=name)
                prefix = f"VIB024 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB026 — hack/hax comment ────────────────────────────────────────────────

_HACK_MESSAGES = [
    "a hack-tagged comment is a bug with a disclaimer attached.",
    "the hack comment — you knew when you wrote it. you know now. nothing has changed.",
    "found a hack comment. the word 'hack' implies you plan to fix it. you don't.",
    "hax detected. this is not a workaround, it's a permanent temporary decision.",
]

_HACK_RE = re.compile(r"#\s*(hack|hax)\b", re.IGNORECASE)


class HackCommentRule(VibRule):
    code = "VIB026"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _HACK_RE.search(line):
                msg = random.choice(_HACK_MESSAGES)
                prefix = f"VIB026 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB027 — do not touch ────────────────────────────────────────────────────

_DO_NOT_TOUCH_MESSAGES = [
    "the 'do not touch' comment is the developer's way of saying 'i have given up understanding this'.",
    "found a do-not-touch comment. anything that cannot be touched cannot be maintained.",
    "a do-not-touch comment means code you're afraid of — code you need to delete or rewrite.",
    "a do-not-touch label is technical debt with a restraining order.",
]

_DO_NOT_TOUCH_RE = re.compile(r"#\s*do\s+not\s+touch", re.IGNORECASE)


class DoNotTouchRule(VibRule):
    code = "VIB027"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _DO_NOT_TOUCH_RE.search(line):
                msg = random.choice(_DO_NOT_TOUCH_MESSAGES)
                prefix = f"VIB027 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB028 — this is fine ────────────────────────────────────────────────────

_THIS_IS_FINE_MESSAGES = [
    "the 'this is fine' comment — the universal sign of someone watching things burn.",
    "found a this-is-fine comment. it is not fine. you know it's not fine. the comment knows.",
    "a this-is-fine comment is a cope mechanism disguised as documentation.",
    "nothing that needs a reassurance comment is fine.",
]

_THIS_IS_FINE_RE = re.compile(r"#\s*this\s+is\s+fine", re.IGNORECASE)


class ThisIsFineRule(VibRule):
    code = "VIB028"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _THIS_IS_FINE_RE.search(line):
                msg = random.choice(_THIS_IS_FINE_MESSAGES)
                prefix = f"VIB028 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB029 — lol / wtf comment ───────────────────────────────────────────────

_LOL_WTF_MESSAGES = [
    "a lol-comment in your code means even you don't take it seriously.",
    "a wtf-comment is a code smell with an emotional response attached.",
    "found laughing in the source. your future self is not laughing.",
    "the wtf-comment — you asked the right question. now write the answer in the code instead.",
]

_LOL_WTF_RE = re.compile(r"#\s*(lol|wtf)\b", re.IGNORECASE)


class LolWtfCommentRule(VibRule):
    code = "VIB029"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _LOL_WTF_RE.search(line):
                msg = random.choice(_LOL_WTF_MESSAGES)
                prefix = f"VIB029 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors


# ── VIB025 — obvious comment ─────────────────────────────────────────────────

_OBVIOUS_COMMENT_MESSAGES = [
    "the comment and the code are saying the same thing. one of them is a waste and it's not the code.",
    "restating the code in English above the code is not documentation, it's subtitles for the obvious.",
    "comment says what the code already says. this is documentation for people who don't trust themselves.",
    "a comment that mirrors the next line is a comment that adds nothing and says everything wrong.",
]

_OBVIOUS_VERBS = frozenset(
    {
        "increment",
        "decrement",
        "initialize",
        "init",
        "reset",
        "set",
        "get",
        "return",
        "add",
        "append",
        "check",
        "update",
        "clear",
        "process",
        "calculate",
        "compute",
        "fetch",
        "load",
        "save",
        "store",
        "create",
        "delete",
        "remove",
        "count",
        "sort",
        "filter",
        "convert",
        "format",
        "assign",
        "define",
        "call",
        "run",
        "execute",
        "start",
        "stop",
        "open",
        "close",
        "read",
        "write",
        "send",
        "receive",
        "log",
        "print",
        "loop",
        "iterate",
        "build",
        "parse",
        "validate",
        "handle",
        "raise",
        "yield",
        "collect",
        "merge",
        "split",
        "join",
        "insert",
        "pop",
    }
)

_WORD_RE = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]*)\b")
_COMMENT_CONTENT_RE = re.compile(r"^\s*#\s*(.*?)\s*$")
_OBVIOUS_MAX_WORDS = 5
_OBVIOUS_LOOKAHEAD = 4


def _is_obvious_comment(comment_text: str, next_code_line: str) -> bool:
    words = comment_text.strip().split()
    first_word_ok = bool(words) and words[0].lower() in _OBVIOUS_VERBS
    short_enough = len(words) <= _OBVIOUS_MAX_WORDS
    if not (first_word_ok and short_enough):
        return False
    rest = " ".join(words[1:])
    comment_idents = {word.lower() for word in _WORD_RE.findall(rest) if len(word) > 1}
    next_idents = {word.lower() for word in _WORD_RE.findall(next_code_line)}
    return bool(comment_idents) and bool(comment_idents & next_idents)


def _next_code_line(lines: list[str], after_idx: int) -> str:
    for j in range(after_idx + 1, min(after_idx + _OBVIOUS_LOOKAHEAD, len(lines))):
        stripped = lines[j].strip()
        if stripped and not stripped.startswith("#"):
            return lines[j]
    return ""


_TOOL_PREFIXES = ("type:", "noqa", "fmt:", "pylint:", "mypy:")


def _obvious_comment_positions(lines: list[str]) -> list[int]:
    positions = []
    for i, line in enumerate(lines):
        comment_match = _COMMENT_CONTENT_RE.match(line)
        if not comment_match:
            continue
        comment_text = comment_match.group(1)
        if comment_text.startswith(_TOOL_PREFIXES):
            continue
        next_code = _next_code_line(lines, i)
        if next_code and _is_obvious_comment(comment_text, next_code):
            positions.append(i + 1)
    return positions


class ObviousCommentRule(VibRule):
    code = "VIB025"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        return [
            (
                pos,
                0,
                f"VIB025 comment: {random.choice(_OBVIOUS_COMMENT_MESSAGES)}",
                type(self),
            )
            for pos in _obvious_comment_positions(lines)
        ]


# ── VIB035 — magic comment ──────────────────────────────────────  # noqa: VIB035
# (VIB030 was already assigned to TooManyArgsRule)

_MAGIC_COMMENT_MESSAGES = [
    "a magic-tagged comment is not documentation. it is a confession.",
    "magic is not a mechanism. explaining it as such is not documentation, it's an apology.",
    "found a magic comment. if it needs that label, it needs a rewrite, not a comment.",
    "magic comment in source code: something works and nobody knows why. that's called a bug.",
]

_MAGIC_COMMENT_RE = re.compile(r"#.*\bmagic\b", re.IGNORECASE)


class MagicCommentRule(VibRule):
    code = "VIB035"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        if lines is None:
            return []
        errors: list[VibError] = []
        for i, line in enumerate(lines):
            if _MAGIC_COMMENT_RE.search(line):
                msg = random.choice(_MAGIC_COMMENT_MESSAGES)
                prefix = f"VIB035 comment: {msg}"
                errors.append((i + 1, 0, prefix, type(self)))
        return errors
