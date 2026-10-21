#!/usr/bin/env python3
"""Gate 4: D-004 and D-005 writing rules.

D-004: no en-dash (U+2013), em-dash (U+2014), two-em dash (U+2E3B), or
ellipsis (U+2026) anywhere in a tracked artefact.
D-005: no triple semicolon in prose. The canonical divider is a double semicolon.

Self-reference hazard: this script contains the literal escape sequences it
searches for, so it must exclude its own path and the workflow directory, or it
will always find itself. That exclusion is deliberate and documented here so a
future contributor does not "fix" it.
"""

from __future__ import annotations

import sys
from pathlib import Path
import re

REPO = Path(__file__).resolve().parent.parent
SCANNED_SUFFIXES = {".md", ".yaml", ".yml", ".json", ".py"}

FORBIDDEN_GLYPHS = {
    "\u2013": "en-dash (U+2013)",
    "\u2014": "em-dash (U+2014)",
    "\u2e3b": "two-em dash (U+2E3B)",
    "\u2026": "ellipsis (U+2026)",
}
TRIPLE_SEMICOLON = ";;;"


def iter_scannable():
    for path in sorted(REPO.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(REPO)
        parts = rel.parts
        if ".git" in parts:
            continue
        # Exclude this script and the workflow directory: both carry the
        # literal sequences they search for.
        if parts[0] == "scripts" and path.name == Path(__file__).name:
            continue
        if ".github" in parts:
            continue
        if "__pycache__" in parts:
            continue
        if path.suffix not in SCANNED_SUFFIXES:
            continue
        yield path, rel


def main() -> int:
    findings: list[str] = []

    for path, rel in iter_scannable():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        for glyph, name in FORBIDDEN_GLYPHS.items():
            for lineno, line in enumerate(text.splitlines(), 1):
                if glyph in line:
                    findings.append(f"{rel}:{lineno}: D-004 violation ({name})")

        if path.suffix == ".md":
            for lineno, line in enumerate(text.splitlines(), 1):
                if TRIPLE_SEMICOLON in line:
                    findings.append(f"{rel}:{lineno}: D-005 violation (triple semicolon)")

    scanned = sum(1 for _ in iter_scannable())
    print(f"Files scanned: {scanned}")
    if findings:
        print("Writing-rule findings:")
        for f in findings:
            print(f"  - {f}")
    print(f"Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())