# CR-IS-CAT-03D: ISS Catalogue Population

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-03D |
| **Title** | Admit the first service records: 623 vendor-neutral service contracts |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-IS-CAT-03B` (taxonomy), `CR-IS-CAT-03C` (record standard) |
| **Repository** | `technehub-labs/dea-catalog-information-system-services` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR populates the catalogue with 623 records: 622 vendor-neutral service contracts derived deterministically from the corroborated function population of the ISF programme, plus one special admission that resolves the outstanding ISC forward reference `isc-rel-006`. The catalogue moves from `scaffold` to `populated` in the pointer. Every record passes the six gates the foundation and governance CRs established, at population scale.

## 2. Scope

### In scope

1. 623 records under `entities/v1-alpha/services/<system-class>/<id>/service.yaml`, one per canonical id `dea:information-system-service-<slug>`, plus a per-system `index.yaml` per system class.
2. The special admission `dea:information-system-service-api-gateway-service`, resolving ISC registry `isc-rel-006` (declared by `CR-IS-CAT-02D` in `dea-catalog-application-components`).
3. `scripts/build_target_snapshots.py` and the vendored snapshot `docs/is-semantic-architecture/target-id-snapshots.yaml` (276 component ids at pinned commit `1530a667a9eace490fa3344d9afa32fabfb93e64`).
4. Extension of Gate 3 (`scripts/check_schema_projection.py`) to validate every record against the schema, per the note its own docstring carried since the foundation CR.
5. `metamodel-pointer.yaml`: `catalog.status` moves from `scaffold` to `populated`.

### Out of scope

1. **The relationship registry and forward declarations.** They land in `CR-IS-CAT-03E`.
2. **Integration interface records.** Owned by the IF catalogue (`CR-IS-CAT-04A/04B`); exposures are forward-declared.
3. **Any vendor record.** Vendor systems corroborate; they never name a canonical record (G-12).

## 3. How the population was derived

Deterministic per G-10, from the corroborated function population (594 functions across 34 generic system classes and 63 sub-systems):

1. Each sub-system's corroborated functions cluster into service contracts through a curated service vocabulary: contract names are authored vendor-neutral, and each function is assigned to exactly one service of its own sub-system by keyword match. All 594 functions are assigned; none is duplicated across services.
2. Each service contract inherits the sub-system's provider: the F1 component id in the ISC catalogue, resolved against the vendored snapshot.
3. Each service carries the vendor corroboration of its deriving functions: at least 3 distinct vendor systems in `external_references`, evidence only.
4. Each service occupies exactly one cell per classification axis (CR-IS-CAT-03B), one `system-class` tag and one `sector` tag.

The one special admission is authored rather than derived: the API gateway service the ISC registry already forward-references. Its evidence structure is identical to the derived records.

## 4. Population shape

| Measure | Count |
|---|---|
| Records | 623 |
| System classes | 34 |
| Distinct providers (F1 component ids, resolved) | 64 |
| Service-kind cells populated | 8 of 8 |
| Forward-declared exposures (one per record) | 623 |
| Records with fewer than 3 distinct vendor systems | 0 |

## 5. Gates landed or extended

| Gate | Script | Change |
|---|---|---|
| Records directory posture | `scripts/check_record_posture.py` | Unchanged; its population-gate checklist is now satisfied |
| Schema projection | `scripts/check_schema_projection.py` | Extended: validates every record against the schema (draft-07 subset validator, no third-party dependency) |
| Taxonomy | `scripts/check_record_taxonomy.py` | Landed by CR-IS-CAT-03B; enforces axis placement at population scale |
| Evidence | `scripts/check_record_evidence.py` | Landed by CR-IS-CAT-03C; enforces the evidence bar at population scale |

## 6. Verification

1. All six gates pass against the populated tree (the reference-integrity gate lands with `CR-IS-CAT-03E` in the same PR; the PR head is not green until it does).
2. ISC registry `isc-rel-006` target `dea:information-system-service-api-gateway-service` now exists; the forward reference is resolved.
3. `dea:information-system-service-identity-service`, the target of an ISF registry relationship, exists and is provided by `dea:information-system-component-identity-broker`.

## 7. What this CR deliberately does not do

1. It does not resolve the exposed-via pointers to live IF records: the IF catalogue is verified empty at slice time; the exposures are declared forward under `CR-IS-CAT-03E` with the owning CR named.
2. It does not retire the ISC forward declaration `isc-rel-006`: that reclassification happens ISC-side.
3. It does not alter the metamodel pointer's metamodel block; only `catalog.status` changes.

## 8. References

- `docs/RECORD-STANDARD.md`, `docs/TAXONOMY.md`.
- ISC registry `isc-rel-006` (`CR-IS-CAT-02D`), resolved by the special admission.
- `CR-IS-CAT-03E` for the registry, forward declarations and reference integrity gate landing in this PR.
