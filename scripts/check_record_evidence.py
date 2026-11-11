#!/usr/bin/env python3
"""Gate 7 (CR-IS-CAT-03C/03D): record evidence conformance.

Every admitted record must carry the evidence a service record owes its
reader: the metamodel clause it is filed under, the admitting change request,
vendor corroboration of at least 3 distinct vendor systems (evidence only,
never canonical, per G-12), a description a reader can act on, and a service
contract that names an offering and at least one consumer (tenet 2).
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/service.yaml"

MIN_DESCRIPTION = 40
MIN_DISTINCT_VENDOR_SYSTEMS = 3


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")
    findings: list[str] = []

    for f in records:
        rel = Path(f).relative_to(REPO)
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        rid = doc.get("id") or str(rel)

        evidence = ((doc.get("governance") or {}).get("source_and_evidence")) or ""
        if "Metamodel clause:" not in evidence:
            findings.append(f"{rel}: governance.source_and_evidence must cite the metamodel clause")
        if "Admitting CR:" not in evidence:
            findings.append(f"{rel}: governance.source_and_evidence must name the admitting CR")

        refs = doc.get("external_references") or []
        distinct = {r.get("system") for r in refs if r.get("system")}
        if len(distinct) < MIN_DISTINCT_VENDOR_SYSTEMS:
            findings.append(
                f"{rel}: {len(distinct)} distinct vendor system(s) cited; "
                f"admission requires at least {MIN_DISTINCT_VENDOR_SYSTEMS}")

        description = doc.get("description") or ""
        if len(description) < MIN_DESCRIPTION:
            findings.append(f"{rel}: description is shorter than {MIN_DESCRIPTION} characters")

        contract = doc.get("service_contract") or {}
        offering = (contract.get("offering") or "").strip()
        consumers = contract.get("consumers") or []
        if not offering:
            findings.append(f"{rel}: service_contract.offering is empty")
        if len(consumers) < 1:
            findings.append(f"{rel}: service_contract.consumers must name at least one consumer")

    if findings:
        for x in findings[:80]:
            print(f"  - FAIL: {x}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
        print(f"Findings: {len(findings)}")
        return 1
    print(f"  OK: {len(records)} records carry metamodel clause, admitting CR, "
          f"at least {MIN_DISTINCT_VENDOR_SYSTEMS} distinct vendor systems, "
          f"substantive descriptions and named consumers")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
