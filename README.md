# flake8-vibes

[![PyPI version](https://img.shields.io/pypi/v/flake8-vibes.svg)](https://pypi.org/project/flake8-vibes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vibe Check: Passing](https://img.shields.io/badge/vibe%20check-passing-brightgreen)](https://github.com/your-org/flake8-vibes)

> A Flake8 plugin for the emotional and spiritual correctness of your Python code.

---

`flake8-vibes` is a Flake8 plugin that performs vibe analysis on your codebase. Unlike traditional linters that concern themselves with correctness, style, or performance, `flake8-vibes` focuses on what really matters: whether your code is okay.

Your code can be PEP 8 compliant, fully typed, and 100% test-covered while still being, energetically speaking, a disaster. This plugin surfaces those issues.

---

## Rules

### `VIB001` — thursday-energy

Functions written on Thursdays tend toward overengineering, premature abstraction, and a particular kind of ambition that the coming weekend will not resolve. This rule flags functions exceeding 20 lines authored on a Thursday.

```
VIB001 thursday energy detected: function 'parse_user_preferences' is 27 lines long and it's Thursday
```

### `VIB002` — todo-shame

A `TODO` is a dream with a comment attached. A `FIXME` is a bug with good self-awareness. Acknowledging a problem and solving it are not the same thing, and the diff doesn't care which one you did.

```
VIB002 todo shame: this TODO has seen three sprints and counting
VIB002 todo shame: FIXME: acknowledged, unaddressed, unforgiven
```

### `VIB013–020` — naming crimes

`data`, `result`, `temp`, `new_x`, `flag`, `Manager` — names that describe shape, not purpose. A full catalog in [docs/rules.md](docs/rules.md).

```
VIB013 naming crime: `data` holds everything and describes nothing.
VIB018 naming crime: `final_result` — the hubris of `final` in a variable name.
VIB020 naming crime: `UserManager` manages something. the question is what.
```

### `VIB081–084` — boolean chaos

`== True`, `== False`, `== None`, `not x == y` — all technically valid, all spiritually wrong.

```
VIB081 boolean chaos: `== True` — you already have a boolean, what more do you need.
VIB083 boolean chaos: None is a singleton. you don't compare singletons with `==`.
```

→ [Full rules reference](docs/rules.md)

---

## Demo

```
$ vibe-check ./src

Scanned 8 file(s)
Total violations: 7

Per-file breakdown:
  src/app.py              ████████░░  82/100  decent energy
  src/utils.py            ██████░░░░  61/100  concerning
  src/models/user.py      █████████░  91/100  slaying
  src/models/manager.py   ████░░░░░░  43/100  chaotic
  src/config.py           ██████████  100/100  immaculate
  src/auth.py             ███████░░░  74/100  decent energy
  src/tasks.py            ████████░░  80/100  decent energy
  src/helpers.py          ██████████  100/100  she ate and left no crumbs

Vibe score: 71/100
Verdict: decent energy
```

---

## Installation

```bash
pip install flake8-vibes
```

Once installed, Flake8 will pick it up automatically via entry points.

## Usage

```bash
flake8 --select=VIB your_file.py
```

Or add to your `setup.cfg` / `pyproject.toml`:

```ini
[flake8]
extend-select = VIB
```

For a full codebase reading:

```bash
vibe-check ./src
```

---

## Docs

- [Usage & installation](docs/usage.md)
- [Rules](docs/rules.md)
- [Git hook](docs/git-hook.md)
- [VS Code](docs/vscode.md)
- [Contributing](CONTRIBUTING.md)

---

*flake8-vibes does not make claims about your mental health, work-life balance, or professional conduct. It makes claims about your code. These are different things, mostly.*
