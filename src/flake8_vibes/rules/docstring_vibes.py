from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB085 — docstring that just repeats the function name ───────────────────

_DOC_REPEATS_NAME_MESSAGES = [
    "`{name}` has a docstring that just says `{name}` with different grammar. it adds nothing.",
    "the docstring for `{name}` restates what the name already says. congratulations, it's documented twice.",
    "`def {name}:` followed by a docstring that restates the name — that's not documentation.",
    "docstring for `{name}` could have been inferred by anyone who read the function name.",
]

_WORD_RE = re.compile(r"\b([a-z][a-z0-9]*)\b")
_DOC_REPEATS_MAX_SUMMARY_WORDS = 8
_DOC_REPEATS_MIN_NAME_WORDS = 2


def _name_words(name: str) -> set[str]:
    return {w for w in name.lower().split("_") if w}


def _doc_words(docstring: str) -> set[str]:
    return set(_WORD_RE.findall(docstring.lower()))


def _docstring_repeats_name(func_name: str, docstring: str) -> bool:
    fn_words = _name_words(func_name)
    if not fn_words or len(fn_words) < _DOC_REPEATS_MIN_NAME_WORDS:
        return False
    summary = docstring.strip().split("\n")[0].strip()
    if len(summary.split()) > _DOC_REPEATS_MAX_SUMMARY_WORDS:
        return False
    doc_words = _doc_words(summary)
    # Allow for trailing 's' / 'es' (pluralization / verb conjugation)
    matched = sum(
        1
        for w in fn_words
        if w in doc_words or w + "s" in doc_words or w + "es" in doc_words
    )
    return matched >= len(fn_words)


def _get_docstring(func: ast.FunctionDef | ast.AsyncFunctionDef) -> str | None:
    if (
        func.body
        and isinstance(func.body[0], ast.Expr)
        and isinstance(func.body[0].value, ast.Constant)
        and isinstance(func.body[0].value.value, str)
    ):
        return func.body[0].value.value
    return


class DocstringRepeatsNameRule(VibRule):
    code = "VIB085"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            doc = _get_docstring(node)
            if doc is None:
                continue
            if _docstring_repeats_name(node.name, doc):
                msg = random.choice(_DOC_REPEATS_NAME_MESSAGES).format(name=node.name)
                prefix = f"VIB085 docstring: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB086 — docstring with no period at the end ─────────────────────────────

_DOC_NO_PERIOD_MESSAGES = [
    "the summary line for `{name}` drifts off at the end without a period. it's a sentence that gave up.",
    "the docstring for `{name}` has no period at the end. it trails off like an unfinished",
    "a docstring without a period is a sentence that didn't commit to being one.",
    "no period on the summary line. the sentence is technically open. the meaning is technically incomplete.",
]


class DocstringNoPeriodRule(VibRule):
    code = "VIB086"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                doc = _get_docstring(node)
            else:
                doc = _get_class_docstring(node)
            if doc is None:
                continue
            summary = doc.strip().split("\n")[0].rstrip()
            if summary and not summary.endswith("."):
                name = getattr(node, "name", "<unknown>")
                msg = random.choice(_DOC_NO_PERIOD_MESSAGES).format(name=name)
                prefix = f"VIB086 docstring: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


def _get_class_docstring(node: ast.ClassDef) -> str | None:
    if (
        node.body
        and isinstance(node.body[0], ast.Expr)
        and isinstance(node.body[0].value, ast.Constant)
        and isinstance(node.body[0].value.value, str)
    ):
        return node.body[0].value.value
    return


# ── VIB087 — Args section that doesn't match actual parameters ───────────────

_DOC_ARGS_MISMATCH_MESSAGES = [
    "the Args section in `{name}`'s docstring lists `{extra}` which isn't a real parameter.",
    "docstring for `{name}` documents `{extra}` but that parameter doesn't exist.",
    "`{name}` has an Args section with `{extra}` — a parameter that was renamed, removed, or imagined.",
    "the docstring for `{name}` mentions `{extra}` which the signature has never heard of.",
]

_ARGS_SECTION_RE = re.compile(r"^\s*Args?\s*:\s*$", re.MULTILINE)
_ARG_LINE_RE = re.compile(r"^\s{4,}(\w+)\s*:")


def _parse_docstring_args(docstring: str) -> set[str]:
    """Extract parameter names from a Google-style Args: section."""
    lines = docstring.split("\n")
    args: set[str] = set()
    in_args = False
    base_indent: int | None = None
    for line in lines:
        stripped = line.strip()
        if re.match(r"^Args?\s*:$", stripped):
            in_args = True
            base_indent = None
            continue
        if in_args:
            if not line.strip():
                continue
            # Detect end of Args section (new section header at low indent)
            if re.match(r"^\w.*:$", stripped) and not re.match(r"^\s{4}", line):
                break
            arg_match = _ARG_LINE_RE.match(line)
            if arg_match:
                indent = len(line) - len(line.lstrip())
                if base_indent is None:
                    base_indent = indent
                if indent == base_indent:
                    args.add(arg_match.group(1))
    return args


def _get_param_names(func: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    args = func.args
    names: set[str] = set()
    for arg in args.args + args.posonlyargs + args.kwonlyargs:
        if arg.arg != "self" and arg.arg != "cls":
            names.add(arg.arg)
    if args.vararg:
        names.add(args.vararg.arg)
    if args.kwarg:
        names.add(args.kwarg.arg)
    return names


class DocstringArgsMismatchRule(VibRule):
    code = "VIB087"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            doc = _get_docstring(node)
            if doc is None or "Args" not in doc:
                continue
            doc_args = _parse_docstring_args(doc)
            if not doc_args:
                continue
            real_params = _get_param_names(node)
            extra = doc_args - real_params
            for arg_name in sorted(extra):
                msg = random.choice(_DOC_ARGS_MISMATCH_MESSAGES).format(
                    name=node.name, extra=arg_name
                )
                prefix = f"VIB087 docstring: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB088 — docstring longer than the function ───────────────────────────────

_DOC_LONGER_THAN_FUNC_MESSAGES = [
    "the docstring for `{name}` is longer than the function body. if explaining it takes more lines than doing it, reconsider doing it.",
    "`{name}` has a {doc_lines}-line docstring and a {body_lines}-line body. the documentation outran the code.",
    "docstring is {doc_lines} lines, function body is {body_lines} lines. something is backwards.",
    "`{name}`: more lines explaining it than doing it. that's either over-documented or under-coded.",
]


def _count_docstring_lines(doc: str) -> int:
    return doc.count("\n") + 1


class DocstringLongerThanFunctionRule(VibRule):
    code = "VIB088"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            doc = _get_docstring(node)
            if doc is None:
                continue
            doc_lines = _count_docstring_lines(doc)
            # total_lines = end - start = lines after the def line
            total_lines = (node.end_lineno or node.lineno) - node.lineno
            body_lines = total_lines - doc_lines
            if body_lines < 1:
                continue
            if doc_lines > body_lines:
                msg = random.choice(_DOC_LONGER_THAN_FUNC_MESSAGES).format(
                    name=node.name, doc_lines=doc_lines, body_lines=body_lines
                )
                prefix = f"VIB088 docstring: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
