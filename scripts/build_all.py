#!/usr/bin/env python3
"""Run the full refresh and build pipeline."""

from __future__ import annotations

import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = [
    "fetch_sources.py",
    "build_index.py",
    "build_changelog.py",
    "build_patterns_index.py",
    "build_docs.py",
]


def main() -> None:
    for script in SCRIPTS:
        subprocess.run(["python3", str(REPO_ROOT / "scripts" / script)], check=True)


if __name__ == "__main__":
    main()
