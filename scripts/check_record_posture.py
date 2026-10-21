#!/usr/bin/env python3
"""Gate 5: records-directory posture.

The catalogue is at scaffold stage. This gate asserts that the repository says
what it means: if no records exist, the catalogue must be marked scaffold, and
if records appear before the population CR, the schema, taxonomy and reference
gates must be present.

It does not validate records. CR-IS-CAT-03D replaces this gate with a real
record validator.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path
import re

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/service.yaml"

REQUIRED_POPULATION_GATES = (
    "scripts/check_schema_projection.py",
    "scripts/check_record_taxonomy.py",
    "scripts/check_record_evidence.py",
    "scripts/check_reference_integrity.py",
)


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")

    if not records:
        pointer = REPO / "metamodel-pointer.yaml"
        doc = yaml.safe_load(pointer.read_text(encoding="utf-8")) or {}
        catalog_status = ((doc.get("catalog") or {}).get("status") or "").strip()
        print(f"Pointer catalog status: {catalog_status!r}")
        if catalog_status != "scaffold":
            print("  - FAIL: no records present but pointer catalog.status is not 'scaffold'")
            print("Findings: 1")
            return 1
        print("  OK: no records admitted; catalogue correctly marked scaffold")
        print("Findings: 0")
        return 0

    missing = [g for g in REQUIRED_POPULATION_GATES if not (REPO / g).exists()]
    if missing:
        print("Records are present but the population gates are incomplete:")
        for g in missing:
            print(f"  - FAIL: {g} is missing")
        print(f"Findings: {len(missing)}")
        return 1

    bad_ids = []
    for f in records:
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        rid = doc.get("id") or ""
        if not re.fullmatch(r"dea:information-system-service-[a-z0-9-]+", rid):
            bad_ids.append(f"{Path(f).relative_to(REPO)}: id {rid!r} is not a canonical ISS id")

    if bad_ids:
        print("Identifier findings:")
        for b in bad_ids:
            print(f"  - FAIL: {b}")
        print(f"Findings: {len(bad_ids)}")
        return 1

    print(f"  OK: {len(records)} record(s) carry canonical identifiers")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())