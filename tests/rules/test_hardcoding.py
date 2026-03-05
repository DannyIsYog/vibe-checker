from __future__ import annotations

import ast
import textwrap

from flake8_vibes.rules.hardcoding import (
    _HARDCODED_CREDS_MESSAGES,
    _HARDCODED_LOCALHOST_MESSAGES,
    _HARDCODED_PATH_MESSAGES,
    _HARDCODED_PORT_MESSAGES,
    _HARDCODED_TIMEOUT_MESSAGES,
    _HARDCODED_URL_MESSAGES,
    _MAGIC_NUMBER_MESSAGES,
    HardcodedCredentialsRule,
    HardcodedLocalhostRule,
    HardcodedPathRule,
    HardcodedPortRule,
    HardcodedTimeoutRule,
    HardcodedUrlRule,
    MagicNumberRule,
)


def parse(source: str) -> ast.AST:
    return ast.parse(textwrap.dedent(source))


def check(rule_cls: type, source: str) -> list:
    return rule_cls().check(parse(source))


# ── VIB041: magic number ──────────────────────────────────────────────────────


def test_041_flags_magic_in_comparison():
    src = "if x > 42:\n    pass"
    errors = check(MagicNumberRule, src)
    assert len(errors) == 1
    assert "VIB041" in errors[0][2]


def test_041_no_flag_zero():
    assert check(MagicNumberRule, "if x > 0:\n    pass") == []


def test_041_no_flag_one():
    assert check(MagicNumberRule, "if x >= 1:\n    pass") == []


def test_041_no_flag_minus_one():
    assert check(MagicNumberRule, "if x == -1:\n    pass") == []


def test_041_flags_in_bin_op():
    src = "x = a + 99"
    errors = check(MagicNumberRule, src)
    assert len(errors) == 1


def test_041_error_tuple_format():
    row, col, msg, typ = check(MagicNumberRule, "if x > 42:\n    pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_041_messages_list():
    assert len(_MAGIC_NUMBER_MESSAGES) >= 2


# ── VIB042: hardcoded URL ─────────────────────────────────────────────────────


def test_042_flags_http_url():
    errors = check(HardcodedUrlRule, 'x = "http://example.com"')
    assert len(errors) == 1
    assert "VIB042" in errors[0][2]


def test_042_flags_https_url():
    errors = check(HardcodedUrlRule, 'x = "https://api.example.com/v1"')
    assert len(errors) == 1


def test_042_no_flag_plain_string():
    assert check(HardcodedUrlRule, 'x = "example.com"') == []


def test_042_messages_list():
    assert len(_HARDCODED_URL_MESSAGES) >= 2


# ── VIB043: hardcoded port ────────────────────────────────────────────────────


def test_043_flags_8080():
    errors = check(HardcodedPortRule, "port = 8080")
    assert len(errors) == 1
    assert "VIB043" in errors[0][2]


def test_043_flags_5432():
    errors = check(HardcodedPortRule, "port = 5432")
    assert len(errors) == 1


def test_043_no_flag_random_number():
    assert check(HardcodedPortRule, "x = 42") == []


def test_043_messages_list():
    assert len(_HARDCODED_PORT_MESSAGES) >= 2


# ── VIB044: hardcoded path ────────────────────────────────────────────────────


def test_044_flags_home_path():
    errors = check(HardcodedPathRule, 'x = "/home/alice/projects/foo"')
    assert len(errors) == 1
    assert "VIB044" in errors[0][2]


def test_044_flags_users_path():
    errors = check(HardcodedPathRule, 'x = "/Users/alice/Documents"')
    assert len(errors) == 1


def test_044_flags_windows_path():
    errors = check(HardcodedPathRule, 'x = "C:\\\\Users\\\\alice"')
    assert len(errors) == 1


def test_044_no_flag_relative_path():
    assert check(HardcodedPathRule, 'x = "config/settings.yaml"') == []


def test_044_messages_list():
    assert len(_HARDCODED_PATH_MESSAGES) >= 2


# ── VIB045: hardcoded timeout ─────────────────────────────────────────────────


def test_045_flags_time_sleep():
    src = "import time\ntime.sleep(5)"
    errors = check(HardcodedTimeoutRule, src)
    assert len(errors) == 1
    assert "VIB045" in errors[0][2]


def test_045_flags_timeout_kwarg():
    src = "requests.get(url, timeout=30)"
    errors = check(HardcodedTimeoutRule, src)
    assert len(errors) == 1


def test_045_no_flag_sleep_zero():
    src = "import time\ntime.sleep(0)"
    assert check(HardcodedTimeoutRule, src) == []


def test_045_messages_list():
    assert len(_HARDCODED_TIMEOUT_MESSAGES) >= 2


# ── VIB046: hardcoded credentials ─────────────────────────────────────────────


def test_046_flags_password_assignment():
    errors = check(HardcodedCredentialsRule, 'password = "s3cr3t"')
    assert len(errors) == 1
    assert "VIB046" in errors[0][2]


def test_046_flags_api_key():
    errors = check(HardcodedCredentialsRule, 'api_key = "abc123def456"')
    assert len(errors) == 1


def test_046_no_flag_non_cred_name():
    assert check(HardcodedCredentialsRule, 'username = "alice"') == []


def test_046_no_flag_empty_string():
    assert check(HardcodedCredentialsRule, 'password = ""') == []


def test_046_messages_list():
    assert len(_HARDCODED_CREDS_MESSAGES) >= 2


# ── VIB047: hardcoded localhost ───────────────────────────────────────────────


def test_047_flags_localhost():
    errors = check(HardcodedLocalhostRule, 'url = "http://localhost:8080"')
    assert len(errors) == 1
    assert "VIB047" in errors[0][2]


def test_047_flags_loopback_ip():
    errors = check(HardcodedLocalhostRule, 'host = "127.0.0.1"')
    assert len(errors) == 1


def test_047_no_flag_remote_host():
    assert check(HardcodedLocalhostRule, 'host = "example.com"') == []


def test_047_messages_list():
    assert len(_HARDCODED_LOCALHOST_MESSAGES) >= 2
