from __future__ import annotations

import pytest

from flake8_vibes.scorer import VibeReport


def test_score_100_no_violations():
    report = VibeReport(violations_by_rule={}, total_files=5)
    assert report.score == 100
    assert report.total_violations == 0


def test_score_decreases_per_violation():
    report = VibeReport(violations_by_rule={"VIB001": 2}, total_files=1)
    assert report.total_violations == 2
    assert report.score == 90


def test_score_clamps_to_zero():
    report = VibeReport(violations_by_rule={"VIB001": 100}, total_files=1)
    assert report.score == 0


def test_score_multiple_rules():
    report = VibeReport(violations_by_rule={"VIB001": 3, "VIB002": 2}, total_files=10)
    assert report.total_violations == 5
    assert report.score == 75


@pytest.mark.parametrize(
    ("violations", "expected_verdict"),
    [
        (0, "immaculate"),
        (2, "immaculate"),  # score=90
        (3, "decent energy"),  # score=85... wait: 100-15=85 -> decent energy
        (6, "decent energy"),  # score=70
        (7, "concerning"),  # score=65
        (10, "concerning"),  # score=50
        (11, "chaotic"),  # score=45
        (15, "chaotic"),  # score=25
        (16, "cooked"),  # score=20
        (100, "cooked"),  # score=0
    ],
)
def test_verdict_thresholds(violations: int, expected_verdict: str):
    report = VibeReport(
        violations_by_rule={"VIB001": violations} if violations else {},
        total_files=1,
    )
    assert report.verdict == expected_verdict
