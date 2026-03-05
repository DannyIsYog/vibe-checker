from __future__ import annotations

import argparse
import ast
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from flake8_vibes.rules import ALL_RULES, VibError
from flake8_vibes.scorer import VibeReport, score_to_verdict

_SCORE_HIGH = 90
_SCORE_MED = 70
_BAR_WIDTH = 10

_RESET = "\033[0m"
_BOLD = "\033[1m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_RED = "\033[31m"


def _color(text: str, code: str, enabled: bool) -> str:
    return f"{code}{text}{_RESET}" if enabled else text


def _score_color(score: int) -> str:
    if score >= _SCORE_HIGH:
        return _GREEN
    if score >= _SCORE_MED:
        return _YELLOW
    return _RED


def _file_verdict(score: int) -> str:
    return score_to_verdict(score)


def collect_python_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(path.rglob("*.py"))


def _is_noqa_suppressed(error: VibError, lines: list[str]) -> bool:
    lineno, _, message, _ = error
    if lineno < 1 or lineno > len(lines):
        return False
    line = lines[lineno - 1]
    code = message.split()[0]
    idx = line.find("# noqa:")
    if idx == -1:
        return False
    after = line[idx + len("# noqa:"):].strip()
    return code in {c.strip() for c in after.split(",")}


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
    return [e for e in errors if not _is_noqa_suppressed(e, lines)]


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


def _render_rules_section(report: VibeReport, color: bool) -> list[str]:
    if not report.violations_by_rule:
        return []
    lines = ["", "Violations by rule:"]
    for code, count in sorted(report.violations_by_rule.items()):
        bar = "#" * min(count, 40)
        colored_code = _color(code, _BOLD + _RED, color)
        lines.append(f"  {colored_code}  {bar} {count}")
    return lines


def _render_files_section(report: VibeReport, color: bool) -> list[str]:
    if not report.violations_by_file:
        return []
    lines = ["", "Per-file breakdown:"]
    for filepath, count in sorted(report.violations_by_file.items()):
        fscore = VibeReport.file_score(count)
        filled = round(fscore / _BAR_WIDTH)
        bar = "\u2588" * filled + "\u2591" * (_BAR_WIDTH - filled)
        fverdict = _file_verdict(fscore)
        sc = _score_color(fscore)
        colored_bar = _color(bar, sc, color)
        colored_score = _color(f"{fscore:>3}/100", sc, color)
        lines.append(f"  {filepath:<40} {colored_bar}  {colored_score}  {fverdict}")
    return lines


def render_report(report: VibeReport, quiet: bool = False, color: bool = False) -> str:
    lines: list[str] = []
    if not quiet:
        lines.append(f"Scanned {report.total_files} file(s)")
        lines.append(f"Total violations: {report.total_violations}")
        lines.extend(_render_rules_section(report, color))
        lines.extend(_render_files_section(report, color))
        lines.append("")
    sc = _score_color(report.score)
    lines.append(_color(f"Vibe score: {report.score}/100", sc, color))
    lines.append(_color(f"Verdict: {report.verdict}", sc, color))
    return "\n".join(lines)


def _format_json(errors_by_file: dict[str, list[VibError]]) -> str:
    violations = []
    for filepath, errors in errors_by_file.items():
        for row, col, message, _ in errors:
            code, _, rest = message.partition(" ")
            violations.append(
                {
                    "file": filepath,
                    "line": row,
                    "col": col,
                    "code": code,
                    "message": rest,
                }
            )
    return json.dumps(violations)


def _add_optional_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--threshold",
        type=int,
        default=0,
        metavar="N",
        help="Exit with code 1 if vibe score is below N",
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Only print score and verdict"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output violations as a JSON array"
    )


def _build_arg_parser() -> argparse.ArgumentParser:
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
    _add_optional_args(parser)
    return parser


def main() -> None:
    args = _build_arg_parser().parse_args()
    files = collect_python_files(Path(args.path))
    workers = min(os.cpu_count() or 1, len(files)) if len(files) > 1 else 1
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(check_file, files))
    errors_by_file: dict[str, list[VibError]] = {str(f): r for f, r in zip(files, results)}
    if args.json:
        sys.stdout.write(_format_json(errors_by_file) + "\n")
        return
    report = build_report(errors_by_file, total_files=len(files))
    sys.stdout.write(render_report(report, quiet=args.quiet, color=sys.stdout.isatty()) + "\n")
    if report.score < args.threshold:
        raise SystemExit(1)
