# Commit messages must be on theme with the vibes

All commit messages must match the energy of this project. They should feel like they were written by someone who takes code quality seriously but not literally.

Good examples:
- `feat(VIB002): call out your TODOs before they call you out`
- `chore: teach your editor to feel something`
- `fix: the vibes were off, now they aren't`

Bad examples:
- `add todo shame rule`
- `fix bug`
- `update files`

# Rules must have randomized messages

Every rule must define at least 2 messages and pick between them using `random.choice(messages)`.

# Rule messages should be educational when possible

Messages should call out the problem *and* tell the user what to do instead. Lead with the shame, end with the fix. The tone should feel like a senior dev who's seen this before — direct, a little judgy, but ultimately trying to help.

Good examples:
- `"`== True` is a tautology wrapped in anxiety. the fix is `if x:` — Python evaluates booleans natively."`
- `"None is a singleton. you don't compare singletons with `==`. use `is None` — it checks identity, not equality."`

Bad examples:
- `"comparing to True is bad"` — no fix, no reason
- `"use is None"` — no personality, no context

# VS Code extension development

The extension lives in `vscode-extension/`. It is symlinked into `~/.vscode/extensions/vibe-checker` for local development — no repackaging or reinstalling needed.

After changing `vscode-extension/src/extension.ts`:
1. `cd vscode-extension && npm run compile`
2. Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window")

Use `npm run watch` to auto-recompile on save.

# The code must vibe-check itself

After every code change, run `vibe-check src/` and confirm the score is 100/100. If it isn't, fix the violations before considering the task done. The source code is not allowed to fail its own linter.
