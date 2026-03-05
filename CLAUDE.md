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

# Every new rule needs tests and docs

When adding a new rule:
1. Add a test file at `tests/rules/test_<rule_name>.py` covering both triggering and non-triggering cases, and edge cases.
2. Add the rule to `docs/rules.md` with its code, name, what it catches, and an example violation.

# VS Code extension development

The extension lives in `vscode-extension/`. It is symlinked into `~/.vscode/extensions/vibe-checker` for local development — no repackaging or reinstalling needed.

After changing `vscode-extension/src/extension.ts`:
1. `cd vscode-extension && npm run compile`
2. Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window")

Use `npm run watch` to auto-recompile on save.

# The code must vibe-check itself

After every code change, run `vibe-check src/` and confirm the score is 100/100. If it isn't, fix the violations before considering the task done. The source code is not allowed to fail its own linter.
