# VS Code Integration

There are two ways to get vibe violations in your editor.

---

## Option A: via the MS Flake8 extension (simplest)

Install the [Flake8 extension](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8) (`ms-python.flake8`), then add this to your workspace `.vscode/settings.json`:

```json
{
  "flake8.interpreter": ["/path/to/your/python"],
  "flake8.args": ["--select=E,F,W,VIB"]
}
```

Replace `/path/to/your/python` with the interpreter where `flake8-vibes` is installed (`which python3`). Violations will appear as squiggles inline in the editor — every bad variable name, every suppressed exception, every thursday crime, right there in your face while you write it.

---

## Option B: via the bundled Vibe Checker extension (richer)

The repo ships a custom VS Code extension in `vscode-extension/` with inline ghost text, hover messages, and a "Check Workspace" command that gives you the full vibe-check breakdown without leaving the editor.

It's currently a local extension — not yet on the marketplace. To use it:

```bash
cd vscode-extension
npm install
npm run compile
```

Then symlink it into your VS Code extensions directory:

```bash
ln -s "$(pwd)" ~/.vscode/extensions/vibe-checker
```

Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window") and the extension will activate on any Python file.

Use `npm run watch` to auto-recompile on save while developing.

---

No waiting for CI to tell you the vibes are off. You'll know immediately.
