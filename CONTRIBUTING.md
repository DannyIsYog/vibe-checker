# Contributing to flake8-vibes

This document defines the standards for all code in this repository. The project's premise is absurd. The engineering is not.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Tooling](#tooling)
- [Code Style](#code-style)
- [Type Annotations](#type-annotations)
- [Naming Conventions](#naming-conventions)
- [Testing](#testing)
- [Adding a New Rule](#adding-a-new-rule)
- [Documentation](#documentation)
- [Git Conventions](#git-conventions)

---

## Project Structure

```
flake8-vibes/
├── src/
│   └── flake8_vibes/
│       ├── __init__.py          # package version
│       ├── plugin.py            # Flake8 entry point
│       ├── cli.py               # vibe-check CLI
│       ├── scorer.py            # vibe score calculation
│       ├── git.py               # git blame helpers
│       └── rules/
│           ├── __init__.py      # re-exports all rules
│           ├── base.py          # VibRule base class
│           └── thursday_energy.py
├── tests/
│   ├── conftest.py              # shared fixtures
│   ├── test_plugin.py           # integration tests via Flake8 API
│   ├── test_cli.py
│   ├── test_scorer.py
│   └── rules/
│       └── test_thursday_energy.py
├── pyproject.toml
├── README.md
└── CONTRIBUTING.md
```

**Rules:**
- All source code lives under `src/` (src layout, not flat)
- One file per rule, always
- No rule logic outside `rules/`
- No shared state between rules

---

## Tooling

All tools are configured in `pyproject.toml`. No separate config files.

| Tool | Purpose |
|------|---------|
| `black` | Formatting |
| `isort` | Import sorting |
| `mypy` | Static type checking |
| `ruff` | Linting |
| `pytest` | Testing |
| `pytest-cov` | Coverage |

### Setup

```bash
pip install -e ".[dev]"
```

### Running checks

```bash
black src tests          # format
isort src tests          # sort imports
ruff check src tests     # lint
mypy src                 # type check
pytest                   # tests
```

All of the above must pass before a PR is merged. No exceptions.

### `pyproject.toml` configuration

```toml
[tool.black]
line-length = 88
target-version = ["py38"]

[tool.isort]
profile = "black"
known_first_party = ["flake8_vibes"]

[tool.mypy]
strict = true
python_version = "3.8"

[tool.ruff]
line-length = 88
select = ["E", "F", "W", "I", "N", "UP", "B", "C4", "PT"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=flake8_vibes --cov-report=term-missing --cov-fail-under=90"
```

---

## Code Style

### Formatting

- **Black** is the formatter. Do not debate Black. Do not configure Black beyond `line-length = 88`.
- **isort** with `profile = "black"` handles imports. Black and isort agree on everything when `profile = "black"` is set.

### Imports

Group in this order, separated by blank lines:

```python
# 1. stdlib
import ast
from pathlib import Path

# 2. third-party
import flake8

# 3. local
from flake8_vibes.rules.base import VibRule
```

No star imports. No `from x import *`. Ever.

### General

- Max line length: 88 (Black default)
- Prefer `pathlib.Path` over `os.path`
- Prefer f-strings over `.format()` or `%`
- No `print()` in library code - use `logging` or raise exceptions
- No mutable default arguments
- Early returns over nested conditionals

```python
# bad
def get_name(node):
    if node:
        if hasattr(node, "name"):
            return node.name
    return None

# good
def get_name(node):
    if not node:
        return None
    return getattr(node, "name", None)
```

---

## Type Annotations

All code must be fully typed. `mypy --strict` must pass with zero errors.

```python
# bad
def check(node, lines):
    ...

# good
def check(node: ast.FunctionDef, lines: list[str]) -> list[tuple[int, int, str, type]]:
    ...
```

- Use `from __future__ import annotations` in all files for forward references
- Use `X | Y` union syntax (Python 3.10+) only if `from __future__ import annotations` is present, otherwise use `Union[X, Y]` or `Optional[X]`
- Type all function signatures, including `self` return types where relevant
- Do not use `Any` unless interfacing with an untyped third-party API, and even then add a comment explaining why

---

## Naming Conventions

### Files

- Snake case: `thursday_energy.py`, not `ThursdayEnergy.py`
- One rule per file, file name matches rule name exactly

### Classes

- PascalCase: `ThursdayEnergy`, `VibRule`
- Rule classes are always named after the rule in PascalCase

### Functions and variables

- Snake case: `count_lines`, `function_node`, `is_thursday`
- Boolean variables and functions start with `is_`, `has_`, or `should_`: `is_thursday()`, `has_docstring()`, `should_skip()`
- Avoid abbreviations: `function_definition` not `func_def`, `line_count` not `lc`
- Loop variables get real names: `for line in lines` not `for l in lines`

### Constants

- Upper snake case at module level: `MAX_LINES = 20`, `VIB_CODE = "VIB001"`

### Rule error codes

- Format: `VIB` + zero-padded 3-digit number: `VIB001`, `VIB012`
- Codes are assigned sequentially and never reused, even if a rule is removed

---

## Testing

Coverage must remain at or above **90%**. The CI gate will fail below this threshold.

### Structure

Each rule gets its own test file under `tests/rules/`. Test files mirror the source structure exactly.

### What to test

Every rule test file must include:

1. **At least one violation case** - code that should trigger the rule
2. **At least one clean case** - code that should not trigger the rule
3. **Edge cases** - empty functions, decorated functions, nested functions, etc.
4. **Configuration variants** - if the rule accepts options, test each option

### How to test

Use the AST directly where possible. Do not shell out to Flake8 in unit tests.

```python
import ast
import textwrap
from flake8_vibes.rules.thursday_energy import ThursdayEnergy


def parse(source: str) -> ast.Module:
    return ast.parse(textwrap.dedent(source))


def test_flags_long_function_on_thursday(monkeypatch):
    monkeypatch.setattr("flake8_vibes.rules.thursday_energy.is_thursday", lambda: True)
    source = "def f():\n" + "    pass\n" * 25
    tree = parse(source)
    errors = ThursdayEnergy().check(tree)
    assert len(errors) == 1
    assert "VIB001" in errors[0][2]


def test_does_not_flag_short_function_on_thursday(monkeypatch):
    monkeypatch.setattr("flake8_vibes.rules.thursday_energy.is_thursday", lambda: True)
    source = "def f():\n    return 1\n"
    tree = parse(source)
    errors = ThursdayEnergy().check(tree)
    assert errors == []


def test_does_not_flag_long_function_on_wednesday(monkeypatch):
    monkeypatch.setattr("flake8_vibes.rules.thursday_energy.is_thursday", lambda: False)
    source = "def f():\n" + "    pass\n" * 25
    tree = parse(source)
    errors = ThursdayEnergy().check(tree)
    assert errors == []
```

Integration tests (via the Flake8 API) live in `tests/test_plugin.py` and test the full pipeline.

### Test naming

- `test_flags_<condition>` for tests that expect a violation
- `test_does_not_flag_<condition>` for tests that expect no violation
- `test_<thing>_with_<config_option>` for configuration variants

---

## Adding a New Rule

Follow these steps exactly, in this order.

### 1. Create the rule file

`src/flake8_vibes/rules/your_rule_name.py`

```python
from __future__ import annotations

import ast
from typing import Generator

from flake8_vibes.rules.base import VibRule, VibError

VIB_CODE = "VIBxxx"
MESSAGE = "VIBxxx your message here"
MAX_SOMETHING = 20


class YourRuleName(VibRule):
    """One-line description of what this rule checks."""

    code = VIB_CODE

    def check(self, tree: ast.AST) -> list[VibError]:
        errors: list[VibError] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if self._is_violation(node):
                    errors.append((node.lineno, node.col_offset, MESSAGE, type(self)))
        return errors

    def _is_violation(self, node: ast.FunctionDef) -> bool:
        ...
```

### 2. Register the rule

Add it to `src/flake8_vibes/rules/__init__.py`:

```python
from flake8_vibes.rules.your_rule_name import YourRuleName

__all__ = [
    ...,
    "YourRuleName",
]
```

### 3. Register in the plugin

Add to the `RULES` list in `src/flake8_vibes/plugin.py`. The plugin iterates this list and runs each rule.

### 4. Write tests

Create `tests/rules/test_your_rule_name.py`. Must cover: violation, clean case, and at least two edge cases.

### 5. Update the rules docs

Add the rule to `docs/rules.md` with its code, name, rationale, and an example. Follow the existing format.

### Rule base class contract

Every rule must:
- Inherit from `VibRule`
- Set a `code` class attribute (`VIBxxx`)
- Implement `check(self, tree: ast.AST) -> list[VibError]`
- Not import from other rules
- Not hold mutable state between `check()` calls

---

## Documentation

- All public functions and classes get a docstring
- Docstrings use the one-line summary style for simple functions, Google style for complex ones
- Internal helpers (prefixed `_`) do not require docstrings if the name is self-explanatory

```python
# fine without docstring
def _count_lines(node: ast.FunctionDef) -> int:
    return node.end_lineno - node.lineno

# needs a docstring
def check(self, tree: ast.AST) -> list[VibError]:
    """Walk the AST and return all VIB001 violations found."""
    ...
```

---

## Git Conventions

### Branches

- `main` is always releasable
- Branch names: `rule/vib001-thursday-energy`, `fix/scorer-edge-case`, `chore/update-deps`

### Commits

Follow Conventional Commits:

```
rule: add VIB001 thursday-energy
fix: handle decorated functions in VIB001
test: add edge cases for async functions in VIB001
chore: update black to 24.x
docs: add VIB001 to README
```

Types: `rule`, `fix`, `test`, `docs`, `chore`, `refactor`

### Pull requests

- One rule per PR
- All checks must pass (black, isort, ruff, mypy, pytest)
- PR description must include the rule rationale (copy from the README section)

---

*The code in this repository is held to the same standard as any production-grade static analysis tool. The rules it enforces are not.*
