from __future__ import annotations

import pytest

from flake8_vibes.scorer import VibeReport

TIER_90 = {"she ate and left no crumbs", "slaying", "immaculate", "serving"}
TIER_70 = {"decent energy", "not bad not great", "it's giving something"}
TIER_50 = {"concerning", "the vibes are questionable", "we need to talk"}
TIER_25 = {"chaotic", "this is a cry for help", "bestie no"}
TIER_0 = {"cooked", "it's giving dumpster fire", "expired"}


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
    ("violations", "expected_tier"),
    [
        (0, TIER_90),
        (2, TIER_90),  # score=90
        (3, TIER_70),  # score=85
        (6, TIER_70),  # score=70
        (7, TIER_50),  # score=65
        (10, TIER_50),  # score=50
        (11, TIER_25),  # score=45
        (15, TIER_25),  # score=25
        (16, TIER_0),  # score=20
        (100, TIER_0),  # score=0
    ],
)
def test_verdict_thresholds(violations: int, expected_tier: set[str]):
    report = VibeReport(
        violations_by_rule={"VIB001": violations} if violations else {},
        total_files=1,
    )
    assert report.verdict in expected_tier
