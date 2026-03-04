from __future__ import annotations

import subprocess
from unittest.mock import patch

from flake8_vibes.git import get_file_commit_date


def test_returns_none_when_git_not_found():
    with patch("subprocess.run", side_effect=FileNotFoundError):
        result = get_file_commit_date("some_file.py")
    assert result is None


def test_returns_none_on_timeout():
    exc = subprocess.TimeoutExpired(cmd="git", timeout=5)
    with patch("subprocess.run", side_effect=exc):
        result = get_file_commit_date("some_file.py")
    assert result is None


def test_returns_none_on_os_error():
    with patch("subprocess.run", side_effect=OSError("permission denied")):
        result = get_file_commit_date("some_file.py")
    assert result is None


def test_returns_none_when_no_output():
    mock_result = type("R", (), {"stdout": ""})()
    with patch("subprocess.run", return_value=mock_result):
        result = get_file_commit_date("some_file.py")
    assert result is None


def test_returns_datetime_on_valid_output():
    mock_result = type("R", (), {"stdout": "2024-01-04 15:30:00 +0000"})()
    with patch("subprocess.run", return_value=mock_result):
        result = get_file_commit_date("some_file.py")
    assert result is not None
    assert result.year == 2024
    assert result.month == 1
    assert result.day == 4
