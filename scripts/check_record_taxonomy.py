#!/usr/bin/env python3
"""Gate 6 (CR-IS-CAT-03B/03D): record taxonomy conformance.

Ratifies the four classification axes of CR-IS-CAT-03B against every record:
a record must occupy exactly one cell per axis; the tag mirrors of the
promoted fields must agree with the fields; duplicate detection operates on
the full identity tuple (system class, provider set, four-tuple, offering),
since the vocabulary sizes make four-tuple collisions among distinct records
mathematically inevitable at population scale (TAXONOMY 3); and the D-6
platform gate requires platform-runtime records to specialize
dea:entity-platform-service and forbids that specialization elsewhere.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/service.yaml"

SERVICE_KINDS = {"authentication", "data-access", "transaction", "notification",
                 "analytics", "integration", "platform-runtime", "other"}
CONSUMER_CLASSES = {"internal-application", "internal-analyst", "internal-machine",
                    "external-partner", "external-customer", "mixed"}
INTERACTION_PATTERNS = {"request-response", "event-push", "event-subscribe",
                        "streaming", "batch", "mixed"}
CONTRACT_MATURITIES = {"draft", "published", "deprecated", "retired"}
PLATFORM_ENTITY = "dea:entity-platform-service"

AXIS_TAGS = {
    "service_kind": "service-kind:",
    "consumer_class": "consumer-class:",
    "interaction_pattern": "interaction-pattern:",
}


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")
    findings: list[str] = []
    seen_cells: dict[tuple, str] = {}

    for f in records:
        rel = Path(f).relative_to(REPO)
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}

        tags = doc.get("tags") or []

        # Promoted first-class fields are primary; their tag mirrors must agree.
        axes = {}
        for field, prefix in AXIS_TAGS.items():
            value = doc.get(field)
            mirrors = [t.split(":", 1)[1] for t in tags if t.startswith(prefix)]
            if len(mirrors) != 1:
                findings.append(f"{rel}: tag mirror {prefix}* must appear exactly once")
            elif mirrors[0] != value:
                findings.append(f"{rel}: {field} is {value!r} but the {prefix} tag "
                                f"mirror says {mirrors[0]!r}")
            axes[field] = value

        if axes["service_kind"] not in SERVICE_KINDS:
            findings.append(f"{rel}: service_kind {axes['service_kind']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-03B")
        if axes["consumer_class"] not in CONSUMER_CLASSES:
            findings.append(f"{rel}: consumer_class {axes['consumer_class']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-03B")
        if axes["interaction_pattern"] not in INTERACTION_PATTERNS:
            findings.append(f"{rel}: interaction_pattern {axes['interaction_pattern']!r} is not a "
                            "vocabulary cell of CR-IS-CAT-03B")

        systems = [t.split(":", 1)[1] for t in tags if t.startswith("system-class:")]
        if len(systems) != 1:
            findings.append(f"{rel}: system-class tag must appear exactly once")

        contract = doc.get("service_contract") or {}
        maturity = contract.get("contract_status")
        if maturity not in CONTRACT_MATURITIES:
            findings.append(f"{rel}: contract_status must map the contract-maturity axis")

        spec = doc.get("specializes")
        if axes["service_kind"] == "platform-runtime":
            if spec != PLATFORM_ENTITY:
                findings.append(f"{rel}: platform-runtime record must specialize {PLATFORM_ENTITY} (D-6)")
        elif spec == PLATFORM_ENTITY:
            findings.append(f"{rel}: non-platform record must not specialize {PLATFORM_ENTITY} (D-6)")

        # Duplicate detection (TAXONOMY 3, as refined at population scale): the
        # four-tuple classifies, it does not identify. Two records are duplicates
        # only when they share the system class, the provider set, the full
        # four-tuple and the offering text. Records that share a four-tuple but
        # differ in offering are distinct records in one classification cell,
        # which the vocabulary sizes make mathematically inevitable.
        if systems:
            offering = (contract.get("offering") or "")
            dup_key = (systems[0], tuple(sorted(doc.get("provided_by") or [])),
                       axes["service_kind"], axes["consumer_class"],
                       axes["interaction_pattern"], maturity, offering)
            if dup_key in seen_cells:
                findings.append(
                    f"{rel}: duplicate of {seen_cells[dup_key]}; same system class, "
                    "provider set, four-tuple and offering")
            else:
                seen_cells[dup_key] = str(rel)

    if findings:
        for x in findings[:80]:
            print(f"  - FAIL: {x}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
        print(f"Findings: {len(findings)}")
        return 1
    print(f"  OK: {len(records)} records occupy exactly one cell per axis; "
          "tag mirrors agree with the promoted fields; D-6 gate satisfied")
    print("Findings: 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
