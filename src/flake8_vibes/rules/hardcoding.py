from __future__ import annotations

import ast
import random
import re

from flake8_vibes.rules.base import VibError, VibRule

# ── VIB041 — magic number ──────────────────────────────────────  # noqa: VIB035

_MAGIC_NUMBER_MESSAGES = [
    "the number {n} appears in logic with no name, no context, and maximum future confusion.",
    "magic number {n}: a constant that knows its value but not its purpose.",
    "{n} in a comparison with no context. the next person who reads this inherits the mystery.",
    "{n}: a number with no label, no purpose in writing, and a promising future as a haunting.",
]

_MAGIC_NUMBER_ALLOWED = {-1, 0, 1, 2}
_MIN_MAGIC_BINOP = 3

_COMPARISON_OPS = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE)


def _is_magic_int(node: ast.AST) -> int | None:
    """Return the int value if node is a magic number constant, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        if node.value not in _MAGIC_NUMBER_ALLOWED:
            return node.value
    return


def _magic_compare_errors(node: ast.Compare, rule_type: type) -> list[VibError]:
    errors: list[VibError] = []
    for comparator in node.comparators:
        val = _is_magic_int(comparator)
        if val is not None:
            msg = random.choice(_MAGIC_NUMBER_MESSAGES).format(n=val)
            errors.append((comparator.lineno, comparator.col_offset, f"VIB041 hardcoding: {msg}", rule_type))
    return errors


def _magic_binop_errors(node: ast.BinOp, rule_type: type) -> list[VibError]:
    errors: list[VibError] = []
    for operand in (node.left, node.right):
        val = _is_magic_int(operand)
        if val is not None and abs(val) >= _MIN_MAGIC_BINOP:
            msg = random.choice(_MAGIC_NUMBER_MESSAGES).format(n=val)
            errors.append((operand.lineno, operand.col_offset, f"VIB041 hardcoding: {msg}", rule_type))
    return errors


class MagicNumberRule(VibRule):
    code = "VIB041"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                errors.extend(_magic_compare_errors(node, type(self)))
            elif isinstance(node, ast.BinOp) and not isinstance(node.op, (ast.Mod,)):
                errors.extend(_magic_binop_errors(node, type(self)))
        return errors


# ── VIB042 — hardcoded URL ────────────────────────────────────────────────────

_HARDCODED_URL_MESSAGES = [
    "a URL in source code is infrastructure pretending to be a constant.",
    "hardcoded URL detected. when it changes — and it will — you'll find every copy the hard way.",
    "a hardcoded URL is a commitment to an address that has no idea you're depending on it.",
    "URL baked into source: somewhere, an ops engineer is already tired just thinking about it.",
]

_URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)


class HardcodedUrlRule(VibRule):
    code = "VIB042"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and _URL_RE.search(node.value)
            ):
                msg = random.choice(_HARDCODED_URL_MESSAGES)
                prefix = f"VIB042 hardcoding: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB043 — hardcoded port number ───────────────────────────────────────────

_HARDCODED_PORT_MESSAGES = [
    "port {n} is hardcoded. configs are for configs. source is for logic.",
    "hardcoded port {n}: works on your machine, disaster everywhere else.",
    "{n} buried in source is a port number that will change and take you by surprise.",
    "port {n} in source: a deployment detail wearing a code costume.",
]

_WELL_KNOWN_PORTS = {
    80, 443, 3000, 5000, 5432, 8000, 8080, 8888,  # noqa: VIB043
    3306, 6379, 27017, 9200, 9092, 5672, 1433, 1521, 11211, 9000,  # noqa: VIB043
}


class HardcodedPortRule(VibRule):
    code = "VIB043"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, int)
                and not isinstance(node.value, bool)
                and node.value in _WELL_KNOWN_PORTS
            ):
                msg = random.choice(_HARDCODED_PORT_MESSAGES).format(n=node.value)
                prefix = f"VIB043 hardcoding: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB044 — hardcoded path ───────────────────────────────────────────────────

_HARDCODED_PATH_MESSAGES = [
    "hardcoded path detected. that directory exists on one machine. probably yours.",
    "a path in source is a path to someone's specific setup. config files exist.",
    "found a hardcoded filesystem path. it will break on every machine that isn't yours.",
    "a hardcoded path: an assumption about the filesystem that everyone else will inherit and resent.",
]

_PATH_PREFIXES = ("/home/", "/Users/", "C:\\", "C:/", "/var/lib/", "/var/www/")  # noqa: VIB044


class HardcodedPathRule(VibRule):
    code = "VIB044"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and any(node.value.startswith(p) for p in _PATH_PREFIXES)
            ):
                msg = random.choice(_HARDCODED_PATH_MESSAGES)
                prefix = f"VIB044 hardcoding: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB045 — hardcoded timeout ────────────────────────────────────────────────

_HARDCODED_TIMEOUT_MESSAGES = [
    "`time.sleep({n})` — a raw number where a named constant refused to show up.",
    "sleeping for {n} seconds hardcoded in source. the day you need to change it, you'll find every copy.",
    "hardcoded `time.sleep({n})`: a guess dressed as precision.",
    "{n} seconds, hardcoded, with no name to explain why it's {n} and not something else.",
]

_TIMEOUT_KW_MESSAGES = [
    "literal timeout value in a call: a number with no name and a future full of 'where did this come from'.",
    "timeout={n} hardcoded. this is a config value wearing a code costume.",
    "timeout literal buried in a function call. the value is present, the reasoning is not.",
    "hardcoded timeout: the right number until the requirements change, which is always.",
]


def _is_numeric_literal(node: ast.AST) -> float | int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    return


class HardcodedTimeoutRule(VibRule):
    code = "VIB045"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            # time.sleep(X)
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr == "sleep"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "time"
                and node.args
            ):
                val = _is_numeric_literal(node.args[0])
                if val is not None and val > 0:
                    msg = random.choice(_HARDCODED_TIMEOUT_MESSAGES).format(n=val)
                    prefix = f"VIB045 hardcoding: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
            # timeout=X keyword argument
            for kw in node.keywords:
                if kw.arg == "timeout":
                    val = _is_numeric_literal(kw.value)
                    if val is not None:
                        msg = random.choice(_TIMEOUT_KW_MESSAGES).format(n=val)
                        prefix = f"VIB045 hardcoding: {msg}"
                        errors.append((kw.value.lineno, kw.value.col_offset, prefix, type(self)))
        return errors


# ── VIB046 — hardcoded credentials shape ─────────────────────────────────────

_HARDCODED_CREDS_MESSAGES = [
    "assigning a string literal to `{name}` — if that's a real credential, it now lives in the repo.",
    "`{name}` is set to a string literal. if that string is real, congratulations on the breach.",
    "`{name} = '...'` — a credential in source code is a credential in the git log is a credential that leaked.",
    "string assigned to `{name}`. credentials in source are credentials that have already leaked.",
]

_CRED_NAMES = frozenset({
    "password", "passwd", "secret", "api_key", "apikey", "access_key",
    "secret_key", "auth_token", "token", "private_key", "credentials",
    "passphrase", "client_secret", "app_secret", "db_password",
})


class HardcodedCredentialsRule(VibRule):
    code = "VIB046"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                name = target.id.lower()
                if name not in _CRED_NAMES:
                    continue
                if (
                    isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                    and node.value.value.strip()
                ):
                    msg = random.choice(_HARDCODED_CREDS_MESSAGES).format(name=target.id)
                    prefix = f"VIB046 hardcoding: {msg}"
                    errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors


# ── VIB047 — hardcoded localhost ─────────────────────────────────────────────

_HARDCODED_LOCALHOST_MESSAGES = [
    "hardcoded `localhost` — it works on your machine. the sentence writes itself.",  # noqa: VIB047
    "found `localhost` in a string literal. that's a valid host for exactly one environment.",  # noqa: VIB047
    "`localhost` in a string: an assumption baked in that will confuse the next environment immediately.",  # noqa: VIB047
    "a `localhost` reference in source. the cloud called. it is not your localhost.",  # noqa: VIB047
]


class HardcodedLocalhostRule(VibRule):
    code = "VIB047"

    def check(
        self,
        tree: ast.AST,
        filename: str = "<unknown>",
        lines: list[str] | None = None,
    ) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and ("localhost" in node.value or "127.0.0.1" in node.value)  # noqa: VIB047
            ):
                msg = random.choice(_HARDCODED_LOCALHOST_MESSAGES)
                prefix = f"VIB047 hardcoding: {msg}"
                errors.append((node.lineno, node.col_offset, prefix, type(self)))
        return errors
