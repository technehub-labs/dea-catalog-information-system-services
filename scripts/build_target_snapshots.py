#!/usr/bin/env python3
"""Deterministic regenerator for the vendored ISC target-id snapshot.

Run locally before opening a PR that touches cross-catalogue references.
Re-commits docs/is-semantic-architecture/target-id-snapshots.yaml with the
harvested ids of the dea-catalog-application-components working copy.

Usage: python3 scripts/build_target_snapshots.py [--isc-path PATH] [--pin SHA]
  --isc-path PATH   path to a local checkout of dea-catalog-application-components
                    (default: ../dea-catalog-application-components relative to
                    this repository, then /home/hermes/dea-work/...)
  --pin SHA         the commit the working copy represents; if omitted, the
                    script tries git rev-parse and falls back to 'unknown'.

This script is the single source of truth for the vendored snapshot. The CI
gate (scripts/check_reference_integrity.py) reads the snapshot YAML and NEVER
re-fetches at run time, so CI is deterministic and offline-safe.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

WORKDIR = Path(__file__).resolve().parent.parent
SNAPSHOT_PATH = WORKDIR / "docs" / "is-semantic-architecture" / "target-id-snapshots.yaml"
DEFAULT_PATHS = [
    WORKDIR.parent / "dea-catalog-application-components",
    Path("/home/hermes/dea-work/dea-catalog-application-components"),
]


def harvest(repo_path: Path) -> dict:
    snap = {}
    for f in sorted((repo_path / "entities").rglob("component.yaml")):
        try:
            doc = yaml.safe_load(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(doc, dict) or not doc.get("id"):
            continue
        snap[doc["id"]] = {
            "name": doc.get("name"),
            "source_file": str(f.relative_to(repo_path)),
        }
    return snap


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--isc-path", default=None)
    ap.add_argument("--pin", default=None)
    args = ap.parse_args()

    candidates = ([Path(args.isc_path)] if args.isc_path else []) + DEFAULT_PATHS
    repo = next((c for c in candidates if c.exists()), None)
    if repo is None:
        print("FAIL: no local dea-catalog-application-components checkout found")
        return 1

    pin = args.pin
    if pin is None:
        try:
            pin = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=str(repo)).decode().strip()
        except Exception:
            pin = "unknown"

    snap = harvest(repo)
    doc = {
        "schema": "dea.iss.target-id-snapshots.v1",
        "generated_for": "CR-IS-CAT-03E reference integrity resolution",
        "pinned_commits": {"dea-catalog-application-components": pin},
        "snapshots": {"dea-catalog-application-components": snap},
        "counts": {"dea-catalog-application-components": len(snap)},
    }
    SNAPSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_PATH.write_text(yaml.safe_dump(doc, sort_keys=True, allow_unicode=True), encoding="utf-8")
    print(f"Snapshot written: {len(snap)} ids from {repo} pinned at {pin}")
    print(f"Path: {SNAPSHOT_PATH.relative_to(WORKDIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
