# Project Mycelium — Docs Validator
# Copyright (c) 2026 Zorvia Community (https://github.com/Zorvia)
#
# Licensed under the Zorvia Public License v2.0 (ZPL v2.0)
# See LICENSE.md for full text.
#
# THIS SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.
# See LICENSE.md for details and disclaimers.

"""Validate that all required documentation files exist and contain TL;DR sections."""

import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_DOCS = [
    "README.md",
    "LICENSE.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "PERFORMANCE.md",
    "DEPLOYMENT.md",
    "PRESENTER.md",
    "FAQ.md",
    "CODE_OF_CONDUCT.md",
    "NOTICE.md",
    "docs/ARCHITECTURE.md",
    "docs/DESIGN.md",
]

DOCS_NEEDING_TLDR = [
    "README.md",
    "PERFORMANCE.md",
    "DEPLOYMENT.md",
    "FAQ.md",
    "docs/ARCHITECTURE.md",
    "docs/DESIGN.md",
]


def validate_docs() -> bool:
    """Check all required docs exist and contain TL;DR where expected."""
    success = True

    print("=" * 60)
    print("  Project Mycelium — Documentation Validator")
    print("=" * 60)
    print()

    # Check existence
    for doc in REQUIRED_DOCS:
        path = os.path.join(ROOT_DIR, doc)
        if os.path.isfile(path):
            print(f"  [PASS] {doc} exists")
        else:
            print(f"  [FAIL] {doc} MISSING")
            success = False

    print()

    # Check TL;DR presence
    for doc in DOCS_NEEDING_TLDR:
        path = os.path.join(ROOT_DIR, doc)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            if "TL;DR" in content or "tl;dr" in content.lower():
                print(f"  [PASS] {doc} contains TL;DR")
            else:
                print(f"  [FAIL] {doc} missing TL;DR section")
                success = False
        else:
            print(f"  [SKIP] {doc} not found")

    print()
    if success:
        print("  All documentation checks passed!")
    else:
        print("  Some documentation checks failed.")
    print()

    return success


if __name__ == "__main__":
    ok = validate_docs()
    sys.exit(0 if ok else 1)
