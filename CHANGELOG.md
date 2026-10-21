# Changelog

All notable changes to the Information System Service catalogue are recorded here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Allocation is recorded in the OpenDEAM root model; see `metamodel-pointer.yaml`.

## [Unreleased]

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
