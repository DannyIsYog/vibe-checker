# Usage

## Installation

```bash
pip install flake8-vibes
```

Once installed, Flake8 picks it up automatically via entry points. No configuration required. It just starts having opinions.

---

## Flake8 integration

```bash
flake8 --select=VIB your_file.py
```

Or add to your `setup.cfg` / `pyproject.toml` to make the vibes a permanent fixture:

```ini
[flake8]
extend-select = VIB
```

---

## CLI: `vibe-check`

The plugin ships a standalone CLI for a full codebase reading:

```bash
vibe-check ./src
```

### Output

```
Scanned 12 file(s)
Total violations: 3

src/main.py  —  2 violations
     4:0   VIB002  todo-shame: this TODO has survived more sprints than some of your teammates
         x = compute()  # TODO: handle edge case
    17:4   VIB015  naming crime: `temp` was supposed to be temporary. it has now outlived the sprint it was born in.
         temp = process(data)

src/utils.py  —  1 violation
     9:0   VIB015  naming crime: calling it `tmp_result` is a promise you made to yourself that your git history will never let you forget.
         tmp_result = calculate()

Per-file breakdown:
  src/main.py                              ████████░░   80/100  decent energy
  src/utils.py                             ██████████  100/100  immaculate

Vibe score: 80/100
Verdict: decent energy
```

### Scoring

Each tier picks a verdict at random. The range of what you might get:

| Score  | Possible verdicts                                          |
|--------|------------------------------------------------------------|
| 90–100 | immaculate, slaying, serving, she ate and left no crumbs  |
| 70–89  | decent energy, not bad not great, it's giving something   |
| 50–69  | concerning, the vibes are questionable, we need to talk   |
| 25–49  | chaotic, this is a cry for help, bestie no                |
| 0–24   | cooked, it's giving dumpster fire, expired                |

### Options

| Flag            | Description                                                  |
|-----------------|--------------------------------------------------------------|
| `--threshold N` | Exit with code 1 if the score is below N. Good for CI gates.|
| `--quiet`       | Print only the score and verdict. No breakdown.              |
| `--json`        | Output violations as a JSON array. Pipe-friendly.            |

**`--quiet` output:**

```
Vibe score: 80/100
Verdict: decent energy
```

**`--json` output:**

```json
[
  {
    "file": "src/main.py",
    "line": 4,
    "col": 0,
    "code": "VIB002",
    "message": "todo-shame: this TODO has survived more sprints than some of your teammates"
  }
]
```

---

## Suppressing violations

To suppress a specific rule on a line:

```python
response_data = fetch()  # noqa: VIB013
```

The `# noqa:` comment must include the rule code. Bare `# noqa` without a code is flagged by VIB023.
