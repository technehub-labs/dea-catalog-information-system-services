#!/usr/bin/env python3
"""Gate 3: the catalogue schema is a faithful projection of the metamodel schema.

The schema at schemas/information-system-service.schema.json is a projection of
dea-metamodel/schemas/entities/information-system-service.json with the
catalogue-instance layer added. This gate asserts the projection has not drifted
from the metamodel on the normative fields.

The rule this gate exists to enforce: never widen a normative enum here to
accept a value the metamodel does not define. If a record fails because it
carries a value the metamodel does not have, the record is wrong, not the
schema. A catalogue that diverges from the metamodel is a second source of truth.

The population CR (CR-IS-CAT-03D) extends this gate to validate actual records
against the schema. Until records exist, this gate validates the schema itself.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "information-system-service.schema.json"

# Normative values mirrored from dea-metamodel/schemas/entities/information-system-service.json
# (lifecycle vocabulary per metamodel/vocabularies/lifecycle.yaml).
EXPECTED_TYPE_CONST = "InformationSystemService"
EXPECTED_LIFECYCLE_ENUM = ["proposed", "planned", "active", "deprecated", "retired"]
EXPECTED_REQUIRED = ["id", "type", "name", "version", "lifecycle_status"]

# Fields that must exist on a metamodel record. If the metamodel adds one, add it here.
NORMATIVE_FIELDS = [
    "id",
    "type",
    "name",
    "description",
    "version",
    "lifecycle_status",
    "external_references",
    "tags",
    "metadata",
]

# Fields this catalogue adds on top of the metamodel. Catalogue-instance layer.
CATALOGUE_INSTANCE_FIELDS = [
    "service_contract",
    "provided_by",
    "exposed_via",
    "specializes",
    "governance",
]


def main() -> int:
    if not SCHEMA_PATH.exists():
        print("FAIL: schemas/information-system-service.schema.json is missing")
        return 1

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"FAIL: schema does not parse: {exc}")
        return 1

    findings: list[str] = []
    props = schema.get("properties") or {}
    required = schema.get("required") or []

    if schema.get("type") != "object":
        findings.append(f"schema root type is {schema.get('type')!r}, expected 'object'")

    for field in EXPECTED_REQUIRED:
        if field not in required:
            findings.append(f"schema does not require {field}")
        if field not in props:
            findings.append(f"schema is missing property {field}")

    for field in NORMATIVE_FIELDS:
        if field not in props:
            findings.append(f"normative metamodel field {field} is absent from the projection")

    for field in CATALOGUE_INSTANCE_FIELDS:
        if field not in props:
            findings.append(f"catalogue-instance field {field} is absent from the projection")

    type_const = (props.get("type") or {}).get("const")
    if type_const != EXPECTED_TYPE_CONST:
        findings.append(f"props.type.const is {type_const!r}, expected {EXPECTED_TYPE_CONST!r}")

    lifecycle_enum = (props.get("lifecycle_status") or {}).get("enum")
    if lifecycle_enum != EXPECTED_LIFECYCLE_ENUM:
        findings.append(
            f"props.lifecycle_status.enum is {lifecycle_enum!r}; it has drifted from the "
            f"metamodel vocabulary {EXPECTED_LIFECYCLE_ENUM!r}"
        )

    id_pattern = (props.get("id") or {}).get("pattern")
    if not id_pattern:
        findings.append("props.id has no pattern; a catalogue id form must be pinned")

    print()
    if findings:
        print("Schema projection findings:")
        for f in findings:
            print(f"  - {f}")
    print(f"Schema projection checked. Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())