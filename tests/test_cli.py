from __future__ import annotations

import sys
from pathlib import Path

import pytest

from flake8_vibes.cli import (
    _file_verdict,
    build_report,
    check_file,
    collect_python_files,
    main,
    render_report,
)
from flake8_vibes.scorer import VibeReport

# --- collect_python_files ---


def test_collect_single_file(tmp_path: Path):
    f = tmp_path / "foo.py"
    f.write_text("x = 1")
    result = collect_python_files(f)
    assert result == [f]


def test_collect_directory(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.py").write_text("y = 2")
    (tmp_path / "c.txt").write_text("not python")
    result = collect_python_files(tmp_path)
    names = {p.name for p in result}
    assert names == {"a.py", "b.py"}


def test_collect_empty_directory(tmp_path: Path):
    result = collect_python_files(tmp_path)
    assert result == []


# --- check_file ---


def test_check_file_valid(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: False
    )
    f = tmp_path / "clean.py"
    f.write_text("def hello(): pass\n")
    errors = check_file(f)
    assert errors == []


def test_check_file_syntax_error(tmp_path: Path):
    f = tmp_path / "bad.py"
    f.write_text("def (:\n")
    errors = check_file(f)
    assert errors == []


def test_check_file_thursday_violation(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: True
    )
    names = [
        "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
        "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
        "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
        "xray", "yankee",
    ]
    body = "\n".join(f"    {name} = {i}" for i, name in enumerate(names))
    f = tmp_path / "big.py"
    f.write_text(f"def big_fn():\n{body}\n")
    errors = check_file(f)
    vib001_errors = [e for e in errors if "VIB001" in e[2]]
    assert len(vib001_errors) == 1


# --- render_report ---


def test_render_report_default():
    report = VibeReport(violations_by_rule={"VIB001": 3}, total_files=5)
    output = render_report(report)
    assert "Scanned 5 file(s)" in output
    assert "VIB001" in output
    assert "Vibe score:" in output
    assert "Verdict:" in output


def test_render_report_quiet():
    report = VibeReport(violations_by_rule={}, total_files=2)
    output = render_report(report, quiet=True)
    assert "Scanned" not in output
    assert "Vibe score:" in output
    assert "Verdict:" in output


def test_render_report_bar_chart():
    report = VibeReport(violations_by_rule={"VIB001": 5}, total_files=1)
    output = render_report(report)
    assert "#####" in output


def test_render_report_color_enabled():
    report = VibeReport(violations_by_rule={"VIB001": 2}, total_files=1)
    output = render_report(report, color=True)
    assert "\033[" in output


def test_render_report_color_disabled():
    report = VibeReport(violations_by_rule={"VIB001": 2}, total_files=1)
    output = render_report(report, color=False)
    assert "\033[" not in output


def test_render_report_per_file_table():
    report = VibeReport(
        violations_by_rule={"VIB001": 1},
        violations_by_file={"src/main.py": 1, "src/utils.py": 0},
        total_files=2,
    )
    output = render_report(report)
    assert "src/main.py" in output
    assert "src/utils.py" in output
    assert "95/100" in output
    assert "100/100" in output


def test_render_report_per_file_zero_violations_full_bar():
    report = VibeReport(
        violations_by_rule={},
        violations_by_file={"clean.py": 0},
        total_files=1,
    )
    output = render_report(report)
    assert "100/100" in output
    assert "\u2588" * 10 in output


# --- _file_verdict ---


def test_file_verdict_all_tiers():
    verdicts_90 = ["she ate and left no crumbs", "slaying", "immaculate", "serving"]
    verdicts_70 = ["decent energy", "not bad not great", "it's giving something"]
    verdicts_50 = ["concerning", "the vibes are questionable", "we need to talk"]
    verdicts_25 = ["chaotic", "this is a cry for help", "bestie no"]
    verdicts_0 = ["cooked", "it's giving dumpster fire", "expired"]
    assert _file_verdict(100) in verdicts_90
    assert _file_verdict(75) in verdicts_70
    assert _file_verdict(55) in verdicts_50
    assert _file_verdict(30) in verdicts_25
    assert _file_verdict(0) in verdicts_0


# --- build_report ---


def test_build_report_counts_by_code():
    errors_by_file: dict[str, list] = {
        "a.py": [
            (1, 0, "VIB001 thursday energy detected: 'fn' is 25 lines long", type),
            (5, 0, "VIB001 thursday energy detected: 'fn2' is 30 lines long", type),
        ]
    }
    report = build_report(errors_by_file, total_files=3)  # type: ignore[arg-type]
    assert report.violations_by_rule == {"VIB001": 2}
    assert report.violations_by_file == {"a.py": 2}
    assert report.total_files == 3


def test_build_report_per_file_counts():
    errors_by_file: dict[str, list] = {
        "a.py": [
            (1, 0, "VIB001 thursday energy: 'fn' is huge", type),
        ],
        "b.py": [],
    }
    report = build_report(errors_by_file, total_files=2)  # type: ignore[arg-type]
    assert report.violations_by_file == {"a.py": 1, "b.py": 0}


# --- main() ---


def test_main_runs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: False
    )
    (tmp_path / "a.py").write_text("x = 1\n")
    monkeypatch.setattr(sys, "argv", ["vibe-check", str(tmp_path)])
    main()
    captured = capsys.readouterr()
    assert "Vibe score:" in captured.out


def test_main_quiet(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: False
    )
    (tmp_path / "a.py").write_text("x = 1\n")
    monkeypatch.setattr(sys, "argv", ["vibe-check", str(tmp_path), "--quiet"])
    main()
    captured = capsys.readouterr()
    assert "Scanned" not in captured.out
    assert "Vibe score:" in captured.out


def test_main_threshold_exit(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: True
    )
    body = "\n".join(f"    x_{i} = {i}" for i in range(25))
    (tmp_path / "big.py").write_text(f"def big_fn():\n{body}\n")
    monkeypatch.setattr(
        sys, "argv", ["vibe-check", str(tmp_path), "--threshold", "100"]
    )
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 1
