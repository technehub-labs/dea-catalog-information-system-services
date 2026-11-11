# Changelog

All notable changes to the Information System Service catalogue are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Allocation is recorded in the OpenDEAM root model; see `metamodel-pointer.yaml`.

## [Unreleased]

## [0.2.0] - 2026-11-11

### Added

- `CR-IS-CAT-03B`: taxonomy ratified. `docs/TAXONOMY.md` is the normative statement of the four classification axes; `service_kind`, `consumer_class` and `interaction_pattern` promoted from tags to first-class schema fields with closed enums, tags retained as mirrors; Gate 6 (`scripts/check_record_taxonomy.py`) enforces one-cell-per-axis placement, tag/field agreement, four-tuple uniqueness per system class and the D-6 platform gate.
- `CR-IS-CAT-03C`: record standard established. `docs/RECORD-STANDARD.md` defines the field-by-field requirements and the evidence bar; Gate 7 (`scripts/check_record_evidence.py`) enforces metamodel clause, admitting CR, at least 3 distinct vendor systems, substantive descriptions and named consumers.
- `CR-IS-CAT-03D`: population. 623 records admitted under `entities/v1-alpha/services/`, derived deterministically from the corroborated ISF function population, plus the special admission `dea:information-system-service-api-gateway-service` resolving ISC `isc-rel-006`. Per-system `index.yaml` files. `scripts/build_target_snapshots.py` and the vendored ISC snapshot (276 ids at pinned commit `1530a667a9eace490fa3344d9afa32fabfb93e64`). Gate 3 extended to validate every record against the schema. Pointer `catalog.status` moves to `populated`.
- `CR-IS-CAT-03E`: cross-catalogue integration. Relationship registry with 1247 typed edges (624 `dea:provides`, 623 `dea:exposes`); `docs/is-semantic-architecture/forward-declarations.yaml` declaring every exposure to the IF catalogue under `CR-IS-CAT-04B`; Gate 8 (`scripts/check_reference_integrity.py`) asserting snapshot-resolved providers, declared exposures and the two anchor records sibling catalogues depend on; CI extended to eight steps.

### Changed

- README status table: scaffold to populated, with population method and counts.

### Known issues

- The 623 `exposed_via` targets are forward-declared: the IF catalogue (`dea-catalog-integration-interfaces`) was verified empty at slice time; its population lands under `CR-IS-CAT-04A/04B`.
- `dea-metamodel` entity `dea:InformationSystemService` still carries the `catalog_repo` contradiction recorded in 0.1.0; a metamodel-side correction remains outstanding.
- ISF, ISC and IF repositories remain mid-rename against their OpenDEAM allocation. Reference resolution is by identifier, so the renames do not block resolution.

## [0.1.0] - 2026-10-20

### Added

- `CR-IS-CAT-03A`: catalogue foundation. Metamodel pointer pinned to OpenDEAM v0.7.0.
- Schema projection of the metamodel ISS entity schema with the catalogue-instance layer.
- `docs/FOUNDATIONS.md`: cardinal scope, four classification axes, six admission criteria, cross-catalogue reference policy, repository reality reconciliation, nine-decision register.
- Five CI gates: parse, pointer, schema projection, writing rules, record posture.

### Known issues

- `dea-metamodel` entity `dea:InformationSystemService` declares `catalog_repo: dea-catalog-platform-services` in one field and `dea-catalog-information-system-services` in another. This catalogue follows the definition field and the CR-020 section 2.2 deferral. A metamodel-side correction is outstanding.
- ISF, ISC and IF repositories remain mid-rename against their OpenDEAM allocation. Recorded in `docs/FOUNDATIONS.md` section 5. Reference resolution is by identifier, so the rename does not block resolution.

### Not in this release

- No records admitted. Population is `CR-IS-CAT-03D`.
- ISC forward reference `isc-rel-006` remains correctly declared.
