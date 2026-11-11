# Information System Service

> A service provided by an information system or a software platform to a consumer, expressed as a contract about the exchange of capability, functionality or data.

**Layer:** L5 : **Building block:** L5-integration : **Entity:** `dea:InformationSystemService` (class alias `ISS`) : **Metamodel:** [v1.0.0](https://github.com/technehub-labs/dea-metamodel)

[![View in Metamodel Explorer](https://img.shields.io/badge/Metamodel%20Explorer-View%20Entity-2C3E50?style=shield)](https://technehub-labs.github.io/metamodel/?entity=ISS)

## Status

**Populated.** Established by `CR-IS-CAT-03A` (ISS foundation) on 2026-10-20; populated by the `CR-IS-CAT-03B` through `CR-IS-CAT-03E` wave on 2026-11-11.

This repository contains **623 admitted records** and the eight-gate CI that holds them to the method. Nothing in a record asserts that a vendor product exists as a canonical entity; vendor systems corroborate the contract as evidence only.

| Item | State |
|---|---|
| Repository | populated, 623 records, 34 system classes |
| Metamodel pointer | pinned to OpenDEAM v0.7.0; catalog status `populated` |
| Schema projection | landed; three classification axes promoted to first-class fields (`CR-IS-CAT-03B`) |
| Taxonomy | ratified ([TAXONOMY.md](./docs/TAXONOMY.md)) |
| Record documentation standard | established ([RECORD-STANDARD.md](./docs/RECORD-STANDARD.md)) |
| Population | 623 records admitted (`CR-IS-CAT-03D`) |
| Cross-catalogue integration | registry landed; 623 exposures forward-declared to the IF catalogue (`CR-IS-CAT-03E`) |

## What this catalogue is

The catalogue of **contracts**, not of implementations. An ISS record names what a service exchanges with its consumers and under what terms. The implementation that fulfils the contract is an Information System Component, catalogued separately in `dea-catalog-application-components`.

## What this catalogue is not

| Not this | Why | Where it lives |
|---|---|---|
| A component catalogue | A component encapsulates a responsibility, structure or execution boundary; a service expresses a contract offered to consumers | `dea-catalog-application-components` (ISC) |
| A function catalogue | A function is a unit of functional behaviour performed by a system or component; a service is what is offered to a consumer | `dea-catalog-system-functions` (ISF) |
| An interface catalogue | A service names the contract; an integration interface specifies the means, protocols and interaction patterns that operationalise it | II catalogue (`dea-catalog-integration-interfaces`) |
| An API catalogue | A service may be exposed through one or more APIs; the API is the contract artefact, the service is the offered capability | Governance register, pending |

## Entity definition

| Field | Value |
|---|---|
| Entity ID | `dea:InformationSystemService` |
| OpenDEAM entity id | `dea:entity-information-system-service` |
| Class alias | `ISS` |
| Layer | L5 |
| Building block | L5-integration |
| Profile | `dea:digital` |
| Metamodel version | v1.0.0 |
| Status | planned |
| Specialises | Core `dea:Service` |
| Legacy ids | `dea:entity-information-system-service` |

## Key tenets

1. **A service is a contract, not an implementation.** If a record describes *how* something is built, it belongs in ISC, not here. The test: can the same contract be fulfilled by two different implementations? If no, the record describes an implementation.
2. **The contract names its consumers.** A service with no consumer is not a service; it is a capability nobody has asked for. `service_contract.consumers` is required and non-empty for every admitted record.
3. **The interface is owned elsewhere.** A service record names the interfaces that operationalise it via `exposed_via`, but does not specify protocol, endpoint or interaction pattern. Those belong to the II catalogue.
4. **A service may provide a service.** The service-of-services pattern is legal under `dea:provides`. Nesting is expressed in the relationship registry, not inline on the record.
5. **Platform service is a conditional specialisation.** Under the D-3 disposition, `dea:entity-platform-service` specialises ISS **only** when the record is genuinely a software-platform service. Non-information-system infrastructure offerings stay under Core `dea:Service`. The per-record gate is carried by the taxonomy gate (D-6).

## Relationships

| Relationship | ISS role | Notes |
|---|---|---|
| `dea:specializes` | source | Specialisation to Core `dea:Service`, or conditional to `dea:entity-platform-service` |
| `dea:provides` | source and target | A component or another service may provide it; it may provide further services |
| `dea:uses` | target | A component or process may consume it |
| `dea:exposes` | source | Presents an integration interface as the accessible surface |

Relationship connections are expressed through the relationship registry (`relationships/v1-alpha/relationships.yaml`), not as inline state on the record, per metamodel CR-3.

## Cross-catalogue references

| Catalogue | Allocates | Repository | State |
|---|---|---|---|
| ISF | `dea:InformationSystemFunction` | `dea-catalog-system-functions` | populated, 644 records |
| ISC | `dea:InformationSystemComponent` | `dea-catalog-application-components` | populated, 276 records |
| ISS | `dea:InformationSystemService` | `dea-catalog-information-system-services` | **populated, 623 records (this repository)** |
| IF | `dea:IntegrationInterface` | `dea-catalog-integration-interfaces` | empty, verified at slice time; population is `CR-IS-CAT-04A/04B` |

The ISC relationship `isc-rel-006` forward-declaring `dea:information-system-service-api-gateway-service` is **resolved**: the record is admitted. The ISF registry's target `dea:information-system-service-identity-service` is admitted as well. All 623 `exposed_via` targets are forward-declared to the IF catalogue under `CR-IS-CAT-04B` in `docs/is-semantic-architecture/forward-declarations.yaml`. See section 5 of [FOUNDATIONS.md](./docs/FOUNDATIONS.md) for the repository reality reconciliation.

## Population method

The 623 records were derived deterministically (G-10) from the corroborated ISF function population: 594 vendor-neutral functions across 34 generic system classes and 63 sub-systems, each corroborated by at least 3 distinct vendor systems, cluster into service contracts through a curated, vendor-neutral service vocabulary. Every record carries: one cell per classification axis, a provider resolved against the vendored ISC snapshot (pinned commit `1530a667a9eace490fa3344d9afa32fabfb93e64`), an exposure forward-declared to the IF catalogue, and at least 3 distinct vendor systems as evidence (G-12). See `CR-IS-CAT-03D` for the full derivation.

## Repository structure

```
dea-catalog-information-system-services/
├── metamodel-pointer.yaml            : entity mapping (do not edit manually)
├── README.md                         : this file
├── CHANGELOG.md
├── docs/
│   ├── FOUNDATIONS.md                : catalogue method + decision-points register
│   ├── TAXONOMY.md                   : the four classification axes (CR-IS-CAT-03B)
│   ├── RECORD-STANDARD.md            : per-record template and evidence bar (CR-IS-CAT-03C)
│   └── is-semantic-architecture/
│       ├── target-id-snapshots.yaml  : vendored ISC ids, pinned commit (D4)
│       └── forward-declarations.yaml : exposures to the IF catalogue (D5)
├── schemas/
│   └── information-system-service.schema.json   : catalogue-instance schema projection
├── entities/v1-alpha/services/       : 623 records, one service.yaml per record, per-system index.yaml
├── relationships/v1-alpha/           : relationship registry, 1247 typed edges (CR-IS-CAT-03E)
└── .github/workflows/                : CI, eight gates
```

## Change control

| Artefact | Change authority |
|---|---|
| `metamodel-pointer.yaml` | OpenDEAM root model (`dea-architecture-framework`), never hand-edited |
| `schemas/*.json` | This repository, by CR, mirroring the metamodel |
| `docs/FOUNDATIONS.md` decision register | This repository, by CR |
| `docs/TAXONOMY.md` vocabularies | This repository, by CR against the taxonomy |
| Records under `entities/v1-alpha/` | This repository, by CR, gated on the taxonomy and record standard |
| Allocation of ISS to a catalogue | OpenDEAM root model |

## Contributing

Population requires an approved change request. See [docs/FOUNDATIONS.md](./docs/FOUNDATIONS.md) for admission criteria, evidence requirements, and the process a record must follow; see [docs/RECORD-STANDARD.md](./docs/RECORD-STANDARD.md) for what a populated record must contain.
