#!/usr/bin/env python3
"""Gate 8 (CR-IS-CAT-03E): cross-catalogue reference integrity.

Resolution policy (FOUNDATIONS section 4): references resolve against vendored
target-id snapshots pinned to a commit, never against live fetches at run
time. A reference whose target does not yet exist is permitted only when the
target catalogue and the owning change request are both named in the
forward-declarations register; that is a declared forward reference, not an
unresolved one. Anything else is a finding.

This gate also asserts the two cross-catalogue anchor records the IS family
already depends on: dea:information-system-service-identity-service (ISF
registry) and dea:information-system-service-api-gateway-service (ISC
registry, isc-rel-006). If either disappears, a sibling catalogue's reference
goes dark; the failure belongs here, at the source.
"""

from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
RECORD_GLOB = "entities/v1-alpha/**/service.yaml"

SNAPSHOT_PATH = REPO / "docs" / "is-semantic-architecture" / "target-id-snapshots.yaml"
FORWARD_PATH = REPO / "docs" / "is-semantic-architecture" / "forward-declarations.yaml"

REQUIRED_ANCHORS = (
    "dea:information-system-service-identity-service",
    "dea:information-system-service-api-gateway-service",
)


def main() -> int:
    records = sorted(glob.glob(str(REPO / RECORD_GLOB), recursive=True))
    print(f"Record count: {len(records)}")

    if not SNAPSHOT_PATH.exists():
        print("  - FAIL: docs/is-semantic-architecture/target-id-snapshots.yaml is missing")
        print("Findings: 1")
        return 1
    if not FORWARD_PATH.exists():
        print("  - FAIL: docs/is-semantic-architecture/forward-declarations.yaml is missing")
        print("Findings: 1")
        return 1

    snap_doc = yaml.safe_load(SNAPSHOT_PATH.read_text(encoding="utf-8")) or {}
    resolved_ids = set(((snap_doc.get("snapshots") or {}).get("dea-catalog-application-components")) or {})
    pinned = (snap_doc.get("pinned_commits") or {}).get("dea-catalog-application-components")
    print(f"Snapshot ids (dea-catalog-application-components): {len(resolved_ids)}; pinned: {pinned}")

    fwd_doc = yaml.safe_load(FORWARD_PATH.read_text(encoding="utf-8")) or {}
    declared = {}
    for entry in fwd_doc.get("forward_declarations") or []:
        if isinstance(entry, dict) and entry.get("id"):
            declared[entry["id"]] = (entry.get("target_repo"), entry.get("owning_cr"))

    findings: list[str] = []
    resolved = 0
    forward = 0

    present_ids = set()
    for f in records:
        rel = Path(f).relative_to(REPO)
        doc = yaml.safe_load(open(f, encoding="utf-8")) or {}
        rid = doc.get("id") or ""
        present_ids.add(rid)

        for target in doc.get("provided_by") or []:
            if target in resolved_ids:
                resolved += 1
            else:
                findings.append(f"{rel}: provided_by target {target} does not resolve "
                                "against the vendored ISC snapshot")

        for target in doc.get("exposed_via") or []:
            if target in declared:
                repo, cr = declared[target]
                if repo != "dea-catalog-integration-interfaces":
                    findings.append(f"{rel}: exposed_via target {target} is forward-declared "
                                    f"to {repo}; the IF catalogue owns integration interfaces")
                elif not cr:
                    findings.append(f"{rel}: exposed_via target {target} is forward-declared "
                                    "without an owning CR (FOUNDATIONS 4.4 requires both named)")
                else:
                    forward += 1
            else:
                findings.append(f"{rel}: exposed_via target {target} is neither resolvable "
                                "nor declared in forward-declarations.yaml")

    for anchor in REQUIRED_ANCHORS:
        if anchor not in present_ids:
            findings.append(f"anchor record {anchor} is absent; a sibling catalogue "
                            "registry depends on it")

    print(f"References: {resolved} resolved, {forward} forward-declared, "
          f"{len(findings)} unresolved")
    if findings:
        for x in findings[:80]:
            print(f"  - FAIL: {x}")
        if len(findings) > 80:
            print(f"  ... and {len(findings) - 80} more")
    print(f"Findings: {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
