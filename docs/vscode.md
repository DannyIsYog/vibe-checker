# VS Code Integration

Install the [Flake8 extension](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) (`ms-python.flake8`), then add this to your workspace `.vscode/settings.json`:

```json
{
  "flake8.interpreter": ["/path/to/your/python"],
  "flake8.args": ["--select=E,F,W,VIB"]
}
```

Replace `/path/to/your/python` with the interpreter where `flake8-vibes` is installed (`which python3`). Violations will appear as squiggles inline in the editor — every bad variable name, every suppressed exception, every thursday crime, right there in your face while you write it.

No waiting for CI to tell you the vibes are off. You'll know immediately.
