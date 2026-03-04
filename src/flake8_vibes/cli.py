from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

from flake8_vibes.rules import ALL_RULES, VibError
from flake8_vibes.scorer import VibeReport


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
    errors: list[VibError] = []
    for rule_class in ALL_RULES:
        errors.extend(rule_class().check(tree, str(filepath)))
    return errors


def build_report(all_errors: list[VibError], total_files: int) -> VibeReport:
    violations: dict[str, int] = {}
    for _row, _col, message, _type in all_errors:
        # extract the VIBxxx code from the message
        code = message.split()[0]
        violations[code] = violations.get(code, 0) + 1
    return VibeReport(violations_by_rule=violations, total_files=total_files)


def render_report(report: VibeReport, quiet: bool = False) -> str:
    lines: list[str] = []
    if not quiet:
        lines.append(f"Scanned {report.total_files} file(s)")
        lines.append(f"Total violations: {report.total_violations}")
        if report.violations_by_rule:
            lines.append("")
            lines.append("Violations by rule:")
            for code, count in sorted(report.violations_by_rule.items()):
                bar = "#" * min(count, 40)
                lines.append(f"  {code}  {bar} {count}")
        lines.append("")
    lines.append(f"Vibe score: {report.score}/100")
    lines.append(f"Verdict: {report.verdict}")
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
    all_errors: list[VibError] = []
    for f in files:
        all_errors.extend(check_file(f))

    report = build_report(all_errors, total_files=len(files))
    print(render_report(report, quiet=args.quiet))

    if report.score < args.threshold:
        sys.exit(1)
