# flake8-vibes

[![PyPI version](https://img.shields.io/pypi/v/flake8-vibes.svg)](https://pypi.org/project/flake8-vibes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vibe Check: Passing](https://img.shields.io/badge/vibe%20check-passing-brightgreen)](https://github.com/DannyIsYog/vibe-checker)

> A Flake8 plugin for the emotional and spiritual correctness of your Python code.

![vibe-check demo](demo/demo.gif)

![VS Code extension demo](demo/vscode.gif)

## Overview

`flake8-vibes` is a Flake8 plugin that performs vibe analysis on your codebase. Unlike traditional linters that concern themselves with correctness, style, or performance, `flake8-vibes` focuses on what really matters: whether your code is okay (emotionally).

Your code can be PEP 8 compliant, fully typed, and 100% test-covered while still being, energetically speaking, a disaster. This plugin surfaces those issues.

It integrates via Flake8's standard entry point system, ships a `vibe-check` CLI for full codebase readings, and produces violation messages that are specific, accurate, and not particularly gentle.

## Key Features

| Feature | Vibe |
|---|---|
| **87 rules, 17 categories** | naming crimes, boolean chaos, exception dishonesty, complexity, hardcoding, docstring energy, temporal risk, and more |
| **Git-aware** | `git blame` tells VIB001 exactly who wrote that function on a Thursday |
| **`vibe-check` CLI** | per-file scores, verdicts, and a final reckoning |
| **Standard Flake8** | `flake8 --select=VIB` — works with your existing config and CI |
| **Randomised messages** | every rule picks from 2+ options, so the shame stays fresh |
| **VS Code extension** | squiggles and inline judgment without leaving the editor |
| **Pre-commit hook** | the vibe score lives in your git history, forever |

## Rules

A highlight reel. → [Full rules reference](docs/rules.md)

---

**`VIB001` thursday-energy** — flags functions over 20 lines authored on a Thursday, as identified by `git blame`. Thursdays are a liminal space: too close to Friday to think clearly, too far from Monday to care.

```
'process_invoice_batch' is 34 lines of pure thursday hubris. we felt it. the diff felt it.
```

---

**`VIB002` todo-shame** — a `TODO` is a dream with a comment attached. A `FIXME` is a bug with good self-awareness. Acknowledging a problem and solving it are not the same thing.

```
this TODO has survived more sprints than some of your teammates
FIXME: acknowledged, unaddressed, unforgiven, and now publicly humiliated
```

---

**`VIB013` naming-crime** — `data`, `result`, `info`, `stuff`, `obj`. A variable named `data` is a box labelled "box."

```
`data` holds everything and describes absolutely nothing. a true void.
```

---

**`VIB018` final-hubris** — nothing named `final_` is final. It will be changed twice before lunch.

```
`final_result` — the hubris of `final` in a variable name that will be changed twice before lunch.
```

---

**`VIB041` magic-number** — a bare integer in a comparison tells you the value, not the meaning. `>= 5` means nothing. `>= MAX_RETRIES` means everything.

```
magic number 5: a constant that knows its value but not its purpose.
```

---

**`VIB081` boolean-chaos** — `== True` when you already have a boolean. What more do you need.

```
None is a singleton. you don't compare singletons with `==`. this is non-negotiable.
```

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

## In the Wild

We ran `vibe-check` across 12 of the most beloved Python repos. No one was ready.

| Repo | Files | Violations | Score | Verdict |
|------|------:|-----------:|------:|---------|
| [django](https://github.com/django/django) | 902 | 8,801 | 51/100 | concerning |
| [flask](https://github.com/pallets/flask) | 24 | 608 | 0/100 | cooked |
| [fastapi](https://github.com/tiangolo/fastapi) | 48 | 1,066 | 0/100 | cooked |
| [pandas](https://github.com/pandas-dev/pandas) | 1,414 | 56,653 | 0/100 | expired |
| [scikit-learn](https://github.com/scikit-learn/scikit-learn) | 631 | 26,277 | 0/100 | cooked |
| [transformers](https://github.com/huggingface/transformers) | 2,476 | 54,012 | 0/100 | cooked |
| [pip](https://github.com/pypa/pip) | 401 | 5,907 | 26/100 | this is a cry for help |
| [ruff](https://github.com/astral-sh/ruff) | 14 | 136 | 51/100 | the vibes are questionable |
| [pytest](https://github.com/pytest-dev/pytest) | 73 | 1,734 | 0/100 | it's giving dumpster fire |
| [bottle](https://github.com/bottlepy/bottle) | 30 | 1,561 | 0/100 | cooked |
| [requests](https://github.com/psf/requests) | 18 | 413 | 0/100 | it's giving dumpster fire |
| [rich](https://github.com/Textualize/rich) | 100 | 1,552 | 22/100 | cooked |

Django is the only one that cleared 50. Ruff lints everything except, apparently, itself. Pandas has 56,653 violations, which tracks.

→ [Full report](reports/report.md)

## Installation

```bash
pip install flake8-vibes
```

Once installed, Flake8 picks it up automatically via entry points. No configuration required to get started.

## Usage

**Via Flake8:**

```bash
flake8 --select=VIB your_file.py
```

**Enable project-wide in `setup.cfg` or `pyproject.toml`:**

```ini
[flake8]
extend-select = VIB
```

**Full codebase reading via the CLI:**

```bash
vibe-check ./src
```

**Suppress a specific rule inline:**

```python
response_data = fetch()  # noqa: VIB013
```

## Contributing

You want all-green CI and the satisfaction of telling people you contribute to a linter. Valid. Here's the fastest way in.

The lowest-lift contribution is adding messages to an existing rule. Every rule picks from a list at random — more messages means more variety, less déjà vu, and more ways to make someone stare at their screen and reconsider their variable names.

Find the rule file in `src/flake8_vibes/rules/`, locate the `_MESSAGES` list, drop in a string, open a PR. The message needs to be lowercase, specific to the violation, and have actual opinions. "this could be improved" is not a message. It's a LinkedIn comment. Rewrite it.

```python
# src/flake8_vibes/rules/boolean_chaos.py
_EQUALS_TRUE_MESSAGES = [
    "comparing to `True` explicitly is a trust issue with your own type system and honestly? it shows.",
    "`== True` — you already have a boolean. what are you waiting for. use it.",
    # yours goes here. make it count.
]
```

No new files. No registration. No tests to write. Just a string with a spine.

Want to go deeper — new rules, fixes, changes to how the plugin works? That's in [CONTRIBUTING.md](CONTRIBUTING.md). It has opinions too.

## Documentation

- [Usage & installation](docs/usage.md)
- [Full rules reference](docs/rules.md)
- [Git hook setup](docs/git-hook.md)
- [VS Code extension](docs/vscode.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

---

*`flake8-vibes` does not make claims about your mental health, work-life balance, or professional conduct. It makes claims about your code. These are different things, mostly.*

*This project was inspired by [scx_horoscope](https://github.com/zampierilucas/scx_horoscope) and built using [Claude](https://claude.ai).*
