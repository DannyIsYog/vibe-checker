from __future__ import annotations

import argparse
import ast
import random
import sys
from pathlib import Path

from flake8_vibes.rules import ALL_RULES, VibError
from flake8_vibes.scorer import VibeReport

_RESET = "\033[0m"
_BOLD = "\033[1m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{_RESET}" if enabled else text


def _score_color(score: int) -> str:
    if score >= 90:
        return _GREEN
    if score >= 70:
        return _YELLOW
    return _RED


def _file_verdict(score: int) -> str:
    if score >= 90:
        return random.choice(
            ["she ate and left no crumbs", "slaying", "immaculate", "serving"]
        )
    if score >= 70:
        return random.choice(
            ["decent energy", "not bad not great", "it's giving something"]
        )
    if score >= 50:
        return random.choice(
            ["concerning", "the vibes are questionable", "we need to talk"]
        )
    if score >= 25:
        return random.choice(["chaotic", "this is a cry for help", "bestie no"])
    return random.choice(["cooked", "it's giving dumpster fire", "expired"])


def collect_python_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.rglob("*.py"))


def check_file(filepath: Path) -> list[VibError]:
    try:
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(filepath))
    except SyntaxError:
        return []
    lines = source.splitlines()
    errors: list[VibError] = []
    for rule_class in ALL_RULES:
        errors.extend(rule_class().check(tree, str(filepath), lines))
    return errors


def build_report(
    errors_by_file: dict[str, list[VibError]], total_files: int
) -> VibeReport:
    violations_by_rule: dict[str, int] = {}
    violations_by_file: dict[str, int] = {}
    for filepath, errors in errors_by_file.items():
        violations_by_file[filepath] = len(errors)
        for _row, _col, message, _type in errors:
            code = message.split()[0]
            violations_by_rule[code] = violations_by_rule.get(code, 0) + 1
    return VibeReport(
        violations_by_rule=violations_by_rule,
        violations_by_file=violations_by_file,
        total_files=total_files,
    )


def render_report(report: VibeReport, quiet: bool = False, color: bool = False) -> str:
    lines: list[str] = []
    if not quiet:
        lines.append(f"Scanned {report.total_files} file(s)")
        lines.append(f"Total violations: {report.total_violations}")
        if report.violations_by_rule:
            lines.append("")
            lines.append("Violations by rule:")
            for code, count in sorted(report.violations_by_rule.items()):
                bar = "#" * min(count, 40)
                colored_code = _color(code, _BOLD + _RED, color)
                lines.append(f"  {colored_code}  {bar} {count}")
        if report.violations_by_file:
            lines.append("")
            lines.append("Per-file breakdown:")
            for filepath, count in sorted(report.violations_by_file.items()):
                fscore = VibeReport.file_score(count)
                filled = round(fscore / 10)
                bar = "\u2588" * filled + "\u2591" * (10 - filled)
                fverdict = _file_verdict(fscore)
                sc = _score_color(fscore)
                colored_bar = _color(bar, sc, color)
                colored_score = _color(f"{fscore:>3}/100", sc, color)
                lines.append(
                    f"  {filepath:<40} {colored_bar}  {colored_score}  {fverdict}"
                )
        lines.append("")
    sc = _score_color(report.score)
    lines.append(_color(f"Vibe score: {report.score}/100", sc, color))
    lines.append(_color(f"Verdict: {report.verdict}", sc, color))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="vibe-check",
        description="Check the vibes of your Python code.",
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="File or directory to check (default: current directory)",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        metavar="N",
        help="Exit with code 1 if vibe score is below N",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Only print score and verdict",
    )
    args = parser.parse_args()

    path = Path(args.path)
    files = collect_python_files(path)
    errors_by_file: dict[str, list[VibError]] = {}
    for f in files:
        errors_by_file[str(f)] = check_file(f)

    report = build_report(errors_by_file, total_files=len(files))
    print(render_report(report, quiet=args.quiet, color=sys.stdout.isatty()))

    if report.score < args.threshold:
        sys.exit(1)
