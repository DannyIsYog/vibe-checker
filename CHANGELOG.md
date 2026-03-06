# Changelog

## 0.1.2 — 2026-03-06

- Fixed VIB053 compatibility with mypy strict mode
- Extracted rule helpers to prevent the linter from flagging its own source
- Enforced `noqa` ban in `src/` — the linter does not get a pass

## 0.1.1 — 2026-03-05

- CI: dropped Python 3.9 from format-check (3.13 already handles it)
- Commit format check tightened across all rule files

## 0.1.0 — initial release

33 rules across 8 categories:

- **VIB001** thursday-energy — functions written on Thursdays, flagged on sight
- **VIB002** todo-shame — TODOs and FIXMEs that survived too many sprints
- **VIB013–VIB020** naming crimes — variables that describe shape instead of purpose
- **VIB031–VIB032** complexity — nesting depth and return statement proliferation
- **VIB033–VIB036** hardcoding — magic numbers, ports, paths, and localhost strings
- **VIB041–VIB043** exception handling — bare excepts, silent passes, caught-everything
- **VIB051–VIB054** docstring energy — docstrings that restate the function name and call it a day
- **VIB081–VIB084** boolean chaos — `== True`, `== False`, `== None`, and `not x == y`

Ships with `vibe-check` CLI, randomised violation messages, `# noqa: VIBXXX` suppression, git pre-commit hook, and a VS Code extension.
