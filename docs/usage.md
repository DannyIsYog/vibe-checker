# Usage

## Installation

```bash
pip install flake8-vibes
```

Once installed, Flake8 will pick it up automatically via entry points. No additional configuration required.

---

## Flake8 integration

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

The plugin ships a standalone CLI for a full codebase reading:

```bash
vibe-check ./src
```

### Output

```
Vibe Check Report
-----------------------------------------

  VIB001 thursday-energy     0 issues
  VIB002 todo-shame          2 issues
  ...

-----------------------------------------
  Vibe Score: 87 / 100

  Verdict: decent energy
-----------------------------------------
```

### Scoring

| Score  | Verdict       |
|--------|---------------|
| 90–100 | immaculate    |
| 70–89  | decent energy |
| 50–69  | concerning    |
| 25–49  | chaotic       |
| 0–24   | cooked        |
