#!/usr/bin/env python3
"""Gate 3: the catalogue schema is a faithful projection, and records conform.

The schema at schemas/information-system-service.schema.json is a projection of
dea-metamodel/schemas/entities/information-system-service.json with the
catalogue-instance layer added. This gate first asserts the projection has not
drifted from the metamodel on the normative fields.

The rule this gate exists to enforce: never widen a normative enum here to
accept a value the metamodel does not define. If a record fails because it
carries a value the metamodel does not have, the record is wrong, not the
schema. A catalogue that diverges from the metamodel is a second source of
truth.

Since CR-IS-CAT-03D (population), this gate also validates every record under
entities/v1-alpha against the schema, using a minimal draft-07 subset validator
(type, const, enum, pattern, required, properties, additionalProperties,
items, minItems, minLength, maxLength). No third-party jsonschema dependency:
the gate stays runnable from a bare CPython with PyYAML.
"""

from __future__ import annotations

import glob
import json
import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO / "schemas" / "information-system-service.schema.json"
RECORD_GLOB = "entities/v1-alpha/**/service.yaml"

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
# The three classification axes were promoted from tags to first-class fields
# by CR-IS-CAT-03B; the tags remain as mirrors.
CATALOGUE_INSTANCE_FIELDS = [
    "service_kind",
    "consumer_class",
    "interaction_pattern",
    "service_contract",
    "provided_by",
    "exposed_via",
    "specializes",
    "governance",
]


def check_projection() -> list[str]:
    findings: list[str] = []
    if not SCHEMA_PATH.exists():
        return ["schemas/information-system-service.schema.json is missing"]

    try:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"schema does not parse: {exc}"]

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
    return findings


def _check_type(value, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    return True


def validate(value, schema: dict, where: str, findings: list[str]) -> None:
    """Minimal draft-07 subset validator. Appends findings, returns nothing."""
    if not isinstance(schema, dict):
        return

    if "type" in schema and not _check_type(value, schema["type"]):
        findings.append(f"{where}: expected {schema['type']}, found "
                        f"{type(value).__name__}")
        return

    if "const" in schema and value != schema["const"]:
        findings.append(f"{where}: {value!r} != const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        findings.append(f"{where}: {value!r} is not in enum {schema['enum']!r}")

    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            findings.append(f"{where}: {value!r} does not match pattern {pattern!r}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            findings.append(f"{where}: length {len(value)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            findings.append(f"{where}: length {len(value)} > maxLength {schema['maxLength']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            findings.append(f"{where}: {len(value)} items < minItems {schema['minItems']}")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(value):
                validate(item, item_schema, f"{where}[{i}]", findings)

    if isinstance(value, dict):
        for req in schema.get("required") or []:
            if req not in value:
                findings.append(f"{where}: required field {req} is missing")

        props = schema.get("properties") or {}
        for key, sub in props.items():
            if key in value:
                validate(value[key], sub, f"{where}.{key}" if where else key, findings)

        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in props:
                    findings.append(f"{where}: additional property {key!r} is not in the schema")


def check_records() -> tuple[list[str], int]:
    findings: list[str] = []
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    for f in records:
        rel = Path(f).relative_to(REPO)
        try:
            doc = yaml.safe_load(open(f, encoding="utf-8"))
        except Exception as exc:
            findings.append(f"{rel}: does not parse as YAML: {exc}")
            continue
        validate(doc, schema, str(rel), findings)
    return findings, len(records)


def main() -> int:
    projection = check_projection()
    record_findings, n = check_records()
    findings = projection + record_findings

    print(f"Records validated: {n}")
    print()
    if findings:
        print("Schema projection findings:")
        for f in findings[:80]:
            print(f"  - {f}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
    print(f"Schema projection checked. Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
