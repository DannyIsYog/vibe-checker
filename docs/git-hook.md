# Git Hook: Vibe Check on Every Commit

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
