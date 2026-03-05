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

Violations by rule:
  VIB002  ## 2
  VIB015  # 1

Per-file breakdown:
  src/main.py                              ████████░░   80/100  decent energy

Vibe score: 80/100
Verdict: decent energy
```

### Scoring

| Score  | Verdict       |
|--------|---------------|
| 90–100 | immaculate    |
| 70–89  | decent energy |
| 50–69  | concerning    |
| 25–49  | chaotic       |
| 0–24   | cooked        |

### Options

| Flag          | Description                                        |
|---------------|----------------------------------------------------|
| `--threshold N` | Exit with code 1 if the score is below N. Good for CI gates. |
| `--quiet`     | Print only the score and verdict. No breakdown.   |
| `--json`      | Output violations as a JSON array. Pipe-friendly. |
