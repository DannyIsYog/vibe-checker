from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path


def get_file_commit_date(filepath: str) -> datetime | None:
    """Return the last commit datetime for a file, or None if unavailable."""
    try:
        resolved = Path(filepath).resolve()
        proc = subprocess.run(
            ["git", "log", "-1", "--format=%ai", "--", str(resolved)],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=str(resolved.parent),
        )
        output = proc.stdout.strip()
        if not output:
            return None
        # git format %ai: "2024-01-04 15:30:00 +0000"
        return datetime.fromisoformat(output)
    except (subprocess.TimeoutExpired, FileNotFoundError, ValueError, OSError):
        return None
