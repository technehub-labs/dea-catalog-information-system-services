# Information System Service

> A service provided by an information system or a software platform to a consumer, expressed as a contract about the exchange of capability, functionality or data.

**Layer:** L5 : **Building block:** L5-integration : **Entity:** `dea:InformationSystemService` (class alias `ISS`) : **Metamodel:** [v1.0.0](https://github.com/technehub-labs/dea-metamodel)

[![View in Metamodel Explorer](https://img.shields.io/badge/Metamodel%20Explorer-View%20Entity-2C3E50?style=shield)](https://technehub-labs.github.io/metamodel/?entity=ISS)

## Status

**Scaffold.** Established by `CR-IS-CAT-03A` (ISS foundation) on 2026-10-20.

This repository currently contains the **catalogue method** and **no records**. Content population is gated on the taxonomy CR. Nothing in this repository asserts that a service exists; it establishes the criteria by which a service would be admitted, and the evidence a record must carry when it is.

| Item | State |
|---|---|
| Repository | scaffold, no records |
| Metamodel pointer | pinned to OpenDEAM v0.7.0 |
| Schema projection | landed (mirrors the metamodel entity schema) |
| Taxonomy | deferred to `CR-IS-CAT-03B` |
| Record documentation standard | deferred to `CR-IS-CAT-03C` |
| Population | deferred to `CR-IS-CAT-03D` |
| Cross-catalogue integration | deferred to `CR-IS-CAT-03E` |

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
5. **Platform service is a conditional specialisation.** Under the D-3 disposition, `dea:entity-platform-service` specialises ISS **only** when the record is genuinely a software-platform service. Non-information-system infrastructure offerings stay under Core `dea:Service`. The per-record gate is carried by the governance register.

## Relationships

| Relationship | ISS role | Notes |
|---|---|---|
| `dea:specializes` | source | Specialisation to Core `dea:Service`, or conditional to `dea:entity-platform-service` |
| `dea:provides` | source and target | A component or another service may provide it; it may provide further services |
| `dea:uses` | target | A component or process may consume it |
| `dea:exposes` | source | Presents an integration interface as the accessible surface |

Relationship connections are expressed through the relationship registry, not as inline state on the record, per metamodel CR-3.

## Cross-catalogue references

| Catalogue | Allocates | Repository | State |
|---|---|---|---|
| ISF | `dea:InformationSystemFunction` | `dea-catalog-system-functions` | populated, 50 records, 15/15 domains |
| ISC | `dea:InformationSystemComponent` | `dea-catalog-application-components` | populated, 38 records, 10/10 domains |
| ISS | `dea:InformationSystemService` | `dea-catalog-information-system-services` | **scaffold (this repository)** |
| IF | `dea:IntegrationInterface` | `dea-catalog-integration-interfaces` | scaffold |

One ISC relationship currently forward-declares an ISS target (`isc-rel-006`, `dea:information-system-service-api-gateway-service`, owning CR `CR-IS-CAT-03`). The admission population CR resolves it. See section 5 of [FOUNDATIONS.md](./docs/FOUNDATIONS.md) for the repository reality reconciliation.

## Repository structure

```
dea-catalog-information-system-services/
├── metamodel-pointer.yaml            : entity mapping (do not edit manually)
├── README.md                         : this file
├── CHANGELOG.md
├── docs/
│   └── FOUNDATIONS.md                : catalogue method + decision-points register
├── schemas/
│   └── information-system-service.schema.json   : catalogue-instance schema projection
├── entities/v1-alpha/                : records land here (deferred to CR-IS-CAT-03D)
├── relationships/v1-alpha/           : relationship registry (deferred to CR-IS-CAT-03E)
└── .github/workflows/                : CI
```

Directories for entities and relationships are **declared, not built**: they arrive with the population and integration CRs. A git clone will not show them until then.

## Change control

| Artefact | Change authority |
|---|---|
| `metamodel-pointer.yaml` | OpenDEAM root model (`dea-architecture-framework`), never hand-edited |
| `schemas/*.json` | This repository, by CR, mirroring the metamodel |
| `docs/FOUNDATIONS.md` decision register | This repository, by CR |
| Records under `entities/v1-alpha/` | This repository, by CR, gated on the taxonomy CR |
| Allocation of ISS to a catalogue | OpenDEAM root model |

## Contributing

Population requires an approved change request. See [docs/FOUNDATIONS.md](./docs/FOUNDATIONS.md) for admission criteria, evidence requirements, and the process a record must follow.