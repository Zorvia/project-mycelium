#!/usr/bin/env python3
# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""
generate_license_headers.py — Verify that all source files have the Zorvia header.

Usage:
    python scripts/generate_license_headers.py [--fix]

Without --fix, only reports files missing the header.
With --fix, prepends the header to files that lack it.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

HEADER_PY = """\
# Project Mycelium — Nurturing Knowledge Without the Cloud
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.
"""

HEADER_TS = """\
/*
  Project Mycelium — Nurturing Knowledge Without the Cloud
  Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)

  Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
  See LICENSE.md for full text.

  THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
  See LICENSE.md for details and disclaimers.
*/
"""

PATTERNS = {
    "**/*.py": ("Zorvia Public License", HEADER_PY),
    "**/*.ts": ("Zorvia Public License", HEADER_TS),
    "**/*.tsx": ("Zorvia Public License", HEADER_TS),
}

EXCLUDE = {"node_modules", ".git", "__pycache__", "dist", "demo", ".venv", "venv"}


def should_skip(path: Path) -> bool:
    parts = path.relative_to(ROOT).parts
    return any(p in EXCLUDE for p in parts)


def check_header(path: Path, needle: str) -> bool:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return needle in text[:500]
    except Exception:
        return True  # skip unreadable


def main() -> None:
    fix_mode = "--fix" in sys.argv
    missing: list[Path] = []

    for glob, (needle, header) in PATTERNS.items():
        for path in ROOT.rglob(glob):
            if should_skip(path):
                continue
            if not check_header(path, needle):
                missing.append(path)
                if fix_mode:
                    original = path.read_text(encoding="utf-8")
                    path.write_text(header + "\n" + original, encoding="utf-8")
                    print(f"  ✓ Fixed: {path.relative_to(ROOT)}")

    if missing and not fix_mode:
        print(f"⚠  {len(missing)} file(s) missing the Zorvia license header:")
        for p in missing:
            print(f"  - {p.relative_to(ROOT)}")
        print("\nRun with --fix to add headers automatically.")
        sys.exit(1)
    elif fix_mode and missing:
        print(f"\n✓ Fixed {len(missing)} file(s).")
    else:
        print("✓ All source files have the Zorvia license header.")


if __name__ == "__main__":
    main()
