# flake8-vibes

[![PyPI version](https://img.shields.io/pypi/v/flake8-vibes.svg)](https://pypi.org/project/flake8-vibes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Vibe Check: Passing](https://img.shields.io/badge/vibe%20check-passing-brightgreen)](https://github.com/your-org/flake8-vibes)

> A Flake8 plugin for the emotional and spiritual correctness of your Python code.

---

## Overview

`flake8-vibes` is a Flake8 plugin that performs vibe analysis on your codebase. Unlike traditional linters that concern themselves with correctness, style, or performance, `flake8-vibes` focuses on what really matters: whether your code is okay.

This plugin does not replace your existing linting setup. It extends it. Your code can be PEP 8 compliant, fully typed, and 100% test-covered while still being, energetically speaking, a disaster. This plugin surfaces those issues.

---

## Installation

```bash
pip install flake8-vibes
```

Once installed, Flake8 will pick it up automatically via entry points. No additional configuration required.

---

## Usage

```bash
flake8 --select=VIB your_file.py
```

Or add to your `setup.cfg` / `pyproject.toml` to always include vibe checks:

```ini
[flake8]
extend-select = VIB
```

---

## CLI: `vibe-check`

The plugin also ships a standalone CLI for a full codebase reading:

```bash
vibe-check ./src
```

### Output

```
Vibe Check Report
-----------------------------------------

  VIB001 thursday-energy     0 issues
  ...

-----------------------------------------
  Vibe Score: 87 / 100

  Verdict: decent energy
-----------------------------------------
```

### Scoring

| Score    | Verdict         |
|----------|-----------------|
| 90-100   | immaculate      |
| 70-89    | decent energy   |
| 50-69    | concerning      |
| 25-49    | chaotic         |
| 0-24     | cooked          |

---

## Rules

### `VIB001` — thursday-energy

**Severity:** warning

#### Rationale

Thursdays occupy a liminal position in the work week - close enough to Friday to generate excitement, far enough from Monday to have accumulated significant technical debt in the developer's psyche. Functions written on Thursdays tend toward overengineering, premature abstraction, and a particular kind of ambition that the coming weekend will not resolve. This rule flags functions exceeding 20 lines authored on a Thursday, as identified by `git blame` or, when unavailable, the system clock at lint time.

#### Example

```python
# Bad - authored on a Thursday, 27 lines long
def parse_user_preferences(input_data):
    # ... 27 lines of ambition
    pass

# Good - same function, written on a Wednesday
def parse_user_preferences(input_data):
    # ... 27 lines, but Wednesday energy is stable
    pass
```

#### Message

```
VIB001 thursday energy detected: function 'parse_user_preferences' is 27 lines long and it's Thursday
```

---

## Git Hook: Vibe Check on Every Commit

You can have `vibe-check` append a score to every commit message automatically using a `prepare-commit-msg` hook.

Create `.git/hooks/prepare-commit-msg` in your project:

```bash
#!/usr/bin/env bash
COMMIT_MSG_FILE="$1"
COMMIT_SOURCE="$2"

if [ "$COMMIT_SOURCE" = "merge" ] || [ "$COMMIT_SOURCE" = "squash" ]; then
  exit 0
fi

if ! command -v vibe-check &>/dev/null; then
  exit 0
fi

REPORT=$(vibe-check . --quiet 2>/dev/null)  # replace . with your source directory if needed
if [ -z "$REPORT" ]; then
  exit 0
fi

# Insert before any trailers (Co-Authored-By, etc.) so Git and GitHub parse them correctly
VIBE_REPORT="$REPORT" VIBE_MSG_FILE="$COMMIT_MSG_FILE" python3 << 'PYEOF'
import os, re

msg_file = os.environ["VIBE_MSG_FILE"]
report = os.environ["VIBE_REPORT"]

with open(msg_file) as f:
    msg = f.read()

vibe_block = f"\n\n# Vibe Check\n{report}"

m = re.search(r'\n(\n(?:[A-Za-z-]+: .+\n)+)$', msg)
if m:
    msg = msg[:m.start()] + vibe_block + msg[m.start():]
else:
    msg = msg + vibe_block + "\n"

with open(msg_file, "w") as f:
    f.write(msg)
PYEOF
```

Then make it executable:

```bash
chmod +x .git/hooks/prepare-commit-msg
```

Every commit will now include a vibe score in its message. The hook silently skips if `vibe-check` isn't installed, so it's safe to share setup instructions without making it a hard dependency.

---

## VS Code

Install the [Flake8 extension](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) (`ms-python.flake8`), then add this to your workspace `.vscode/settings.json`:

```json
{
  "flake8.interpreter": ["/path/to/your/python"],
  "flake8.args": ["--select=E,F,W,VIB"]
}
```

Replace `/path/to/your/python` with the interpreter where `flake8-vibes` is installed (`which python3`). Violations will appear as squiggles inline in the editor.

---

## Contributing

New rule proposals should include:

1. A `VIBxxx` code and a name (compound noun or adjective-noun pair describing a psychological or social dynamic)
2. A Rationale section written in the voice of someone who has read too much pop psychology and works in tech
3. At least one code example
4. A suggested default severity of `warning`

---

## License

MIT

---

*flake8-vibes does not make claims about your mental health, work-life balance, or professional conduct. It makes claims about your code. These are different things, mostly.*
