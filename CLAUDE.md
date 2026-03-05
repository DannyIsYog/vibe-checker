# Commit messages must match the vibes

All commit messages must feel like they were written by someone who takes code quality seriously but not literally. The tone is sassy, direct, and a little judgmental — like a senior dev who has seen things and is done being polite about it.

Good examples:
- `feat(VIB002): call out your TODOs before they call you out`
- `chore: teach your editor to feel something`
- `fix: the vibes were off, now they aren't`
- `feat(VIB033): bare except has been getting away with it for too long`

Bad examples:
- `add todo shame rule`
- `fix bug`
- `update files`

# Rules must have randomized messages

Every rule must define at least 2 messages and pick between them using `random.choice(messages)`.

Messages must have bite. They should be:
- Specific to what went wrong, not generic
- Sassy, a little judgmental, but never mean-spirited
- Written in lowercase (sentence case is fine, all-caps is not)
- Short enough to scan, sharp enough to sting

Soft, sanitised messages like "this could be improved" are not acceptable. If the message could appear in a corporate style guide, rewrite it.

# Every new rule needs tests and docs

When adding a new rule:
1. Add a test file at `tests/rules/test_<rule_name>.py` covering both triggering and non-triggering cases, and edge cases.
2. Add the rule to `docs/rules.md` with its code, name, what it catches, and an example violation.

The docs should match the tone of the messages — direct, a little sassy, no corporate softening.

# VS Code extension development

The extension lives in `vscode-extension/`. It is symlinked into `~/.vscode/extensions/vibe-checker` for local development — no repackaging or reinstalling needed.

After changing `vscode-extension/src/extension.ts`:
1. `cd vscode-extension && npm run compile`
2. Reload VS Code (`Cmd+Shift+P` → "Developer: Reload Window")

Use `npm run watch` to auto-recompile on save.

# The code must vibe-check itself

After every code change, run `vibe-check src/` and confirm the score is 100/100. If it isn't, fix the violations before considering the task done. The source code is not allowed to fail its own linter.

Never suppress violations with `# noqa` in source files under `src/`. Fix the code. If a rule fires on its own constants or helpers, restructure — extract a named constant, shorten the function, rename the variable. The linter doesn't get a pass just because it's the one doing the linting.
