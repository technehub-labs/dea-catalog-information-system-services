# FOUNDATIONS: Information System Service catalogue

**Status:** Established by `CR-IS-CAT-03A` on 2026-10-20.
**Programme:** Information Systems Semantic Architecture (metamodel CR-017 parent programme).
**Scope of this document:** the catalogue **method**. No records are admitted here.

---

## 1. Cardinal scope

The Information System Service catalogue records **contracts offered to consumers**. A record names what a service exchanges, with whom, and under what terms. It does not record how the exchange is implemented.

The boundary test is substitutability:

> Can the same contract be fulfilled by two materially different implementations?
>
> **Yes** -> this is a service. Record it here.
> **No** -> this is a component. Record it in ISC.

This single test resolves most boundary disputes. An authentication service offered to ten application components is a service. The token issuer that implements it is a component. Both are true statements about the system; only one is a service record.

## 2. What is deliberately excluded

| Excluded | Reason |
|---|---|
| Implementation detail, deployment topology, runtime configuration | Those are component concerns (ISC) |
| Protocol specification, endpoints, message formats | Those are integration-interface concerns (II) |
| Functional behaviour the service performs internally | Those are function concerns (ISF) |
| API definitions as a distinct artefact type | A service may be exposed through APIs; the API is a contract artefact, the service is the offered capability. Tracked in the governance register, pending `CR-013` |
| Infrastructure primitives that are not software-platform services | Stay under Core `dea:Service` per the D-3 conditional disposition |

The last row is the D-3 boundary and it is the one most likely to be contested. `dea:entity-platform-service` specialises ISS **only** when the record is genuinely a software-platform service. A managed database service is a platform service. A rack of physical servers is not; it stays under Core `dea:Service`. The per-record gate is a governance-register obligation, not a schema constraint.

## 3. Classification axes

A record is classified on four axes. The axes are the admission test: a record that cannot be placed on all four is not yet understood well enough to admit.

| Axis | Question | Vocabulary |
|---|---|---|
| **Service kind** | What kind of contract is offered? | authentication, data-access, transaction, notification, analytics, integration, platform-runtime, other |
| **Consumer class** | Who consumes it? | internal-application, internal-analyst, internal-machine, external-partner, external-customer, mixed |
| **Interaction pattern** | How is the exchange shaped? | request-response, event-push, event-subscribe, streaming, batch, mixed |
| **Contract maturity** | How settled is the contract? | draft, published, deprecated, retired |

`contract_status` in the schema maps 1:1 to **contract maturity**. The other three axes are catalogue-instance classification, carried as `tags` in the initial schema and promoted to first-class fields by `CR-IS-CAT-03B` once the taxonomy is ratified.

**Mutual exclusivity.** A record occupies exactly one cell per axis. Two records that would occupy the same four-tuple are either duplicates or genuinely distinct records that the axes fail to distinguish; the second case is a finding against the axes, not against the records, and must be raised as a CR against the taxonomy.

## 4. Admission criteria

A record is admitted when all of the following hold.

1. **The substitutability test passes.** Two materially different implementations could satisfy the contract.
2. **The contract names its consumers.** `service_contract.consumers` is non-empty.
3. **The provider is identified.** `provided_by` names at least one canonical component or service id, or the record states explicitly that the provider is not yet allocated.
4. **The evidence is citable.** `governance.source_and_evidence` names the metamodel clause, the CR, and any external specification relied upon. A record whose evidence is "we know this exists" is a candidate, not an admission.
5. **The identifier is canonical.** `dea:information-system-service-<slug>`. Never an external system identifier, never a legacy id (E004).
6. **The lifecycle state is declared.** `lifecycle_status` is drawn from the metamodel lifecycle vocabulary.

## 5. Cross-catalogue reference policy

References out of this catalogue are resolved, never assumed.

| Rule | Statement |
|---|---|
| Resolution | Every cross-catalogue reference resolves against a vendored target-id snapshot pinned to a commit. |
| Forward declaration | A reference whose target does not yet exist is permitted **only** when the target catalogue and the owning change request are both named. An unclassified reference is a hard CI failure. |
| Rebase | When a target lands under a different identifier than declared, the referencing record is rebased and the rationale recorded. A forward reference is never left pointing at an identifier that will never exist. |
| Verification | A forward declaration is re-verified against the live target repository at slice time, not assumed still pending. Target catalogues that have gained content since the declaration must be recorded as such. |

The last rule exists because a snapshot claiming a target catalogue is empty, when it is not, will mislead the next reviewer indefinitely. `CR-IS-CAT-02F` found exactly this: two target catalogues had gained records while their snapshots still claimed emptiness.

### Repository reality reconciliation

The OpenDEAM root model allocates four entities to four canonical repository names. Three of those repositories do not yet carry the allocated name. This table is authoritative for this catalogue's cross-references and is re-verified at each slice.

| Alias | Entity | Allocated repository | Actual repository | State |
|---|---|---|---|---|
| ISF | `dea:InformationSystemFunction` | `dea-catalog-information-system-functions` | `dea-catalog-system-functions` | mid-rename, allocation recorded, transfer pending org admin |
| ISC | `dea:InformationSystemComponent` | `dea-catalog-information-system-components` | `dea-catalog-application-components` | mid-rename, allocation recorded, transfer pending org admin |
| **ISS** | `dea:InformationSystemService` | `dea-catalog-information-system-services` | `dea-catalog-information-system-services` | **matches allocation; no rename debt** |
| IF | `dea:IntegrationInterface` | `dea-catalog-information-system-integration-interfaces` | `dea-catalog-integration-interfaces` | mid-rename, allocation recorded, transfer pending org admin |

A consequence worth stating plainly: a cross-catalogue reference that resolves against the actual repository may not match the allocated name. Reference resolution is by **identifier**, not by repository name, so the rename debt does not block resolution. It does mean that any documentation which names a repository by its allocated name must be read together with this table.

## 6. Evidence requirements

Every admitted record carries provenance in `governance.source_and_evidence` naming:

- the metamodel clause that defines the entity,
- the change request that admitted the record,
- any external specification relied upon, cited by its own naming authority (for example an ITU-T Recommendation, an ETSI Technical Specification, an ISO/IEC standard, or a NIST publication).

Standards work cites the naming authority directly. Where a reference has no citable public specification, the record states that and names the internal source instead. An uncited assertion is a candidate.

## 7. Decision-points register

Later change requests cite these decisions by number.

| ID | Decision | Rationale |
|---|---|---|
| **D1** | The substitutability test is the cardinal scope boundary, not taxonomy placement. | A service is defined by what it offers, not by where it sits in a classification. A record that cannot be placed in a domain may still be a service. |
| **D2** | The contract names its consumers; `consumers` is required and non-empty. | A service with no consumer is a capability nobody requested. Making the consumer mandatory forces the record to answer "who is this for", which is the question that distinguishes a service from a component. |
| **D3** | The integration interface is owned by the II catalogue; ISS records reference it via `exposed_via` and never specify it. | Protocol, endpoint and interaction-pattern specification has a different owner and a different change cadence. Splitting ownership prevents the two from drifting. |
| **D4** | Cross-catalogue references resolve against pinned snapshots; unclassified references fail CI. | Prefix matching cannot distinguish a real identifier from a plausible one. The ISC and ISF catalogues both shipped synthetic references that prefix validation reported as clean. |
| **D5** | Forward references name both the target catalogue and the owning change request. | A forward reference with no owner is a permanent deferral. Naming the owner makes it a scheduled item rather than an orphan. |
| **D6** | `dea:entity-platform-service` specialises ISS only when the record is genuinely a software-platform service; other infrastructure offerings stay under Core `dea:Service`. | Carried from metamodel CR-020 disposition D-3. The gate is a governance-register obligation per record, not a schema constraint, because the distinction is semantic rather than structural. |
| **D7** | The repository carries the allocated canonical name; no rename is pending. | The allocation and the reality agree for ISS, so this catalogue introduces no rename debt. The other three IS-family catalogues are recorded in section 5. |
| **D8** | Relationship connections are expressed in the relationship registry, never as inline state on the record. | Carried from metamodel CR-3. A connection asserted in two places is a connection that will be updated in one. |
| **D9** | A service may provide a service (service-of-services). Nesting lives in the registry. | Permitted by `dea:provides` in the metamodel relationship matrix. Recording it as registry edges rather than record fields keeps nesting observable without duplicating it. |

## 8. Programme shape

The ISS catalogue follows the five-change-request programme established for the IS family.

| CR | Scope | Gates |
|---|---|---|
| **CR-IS-CAT-03A** | Foundation: method, pointer, schema projection, CI, this document. **No records.** | this slice |
| CR-IS-CAT-03B | Taxonomy: ratify the four classification axes and their vocabularies | taxonomy gate |
| CR-IS-CAT-03C | Documentation standard: per-record documentation template and evidence checklist | documentation gate |
| CR-IS-CAT-03D | Population: admit the first records, resolving the ISC forward reference | population gates |
| CR-IS-CAT-03E | Integration: cross-catalogue reference hardening, conformance reporting, governance handover | reference-integrity gate |

Each slice is independently mergeable and CI-green. A slice that cannot pass its own gates does not land.

## 9. What this document does not do

It does not admit records, does not ratify the classification vocabularies (that is `CR-IS-CAT-03B`), and does not define the per-record documentation template (that is `CR-IS-CAT-03C`). It states the method by which those later slices will be judged.

## 10. References

- `dea-metamodel` `schemas/entities/information-system-service.json`: normative entity schema
- `dea-metamodel` `change-requests/CR-020-information-system-service.md`: entity introduction, D-3 disposition
- `dea-metamodel` `change-requests/CR-017-information-systems-domain-semantic-integration.md`: parent programme
- `dea-metamodel` `change-requests/CR-021-integration-interface.md`: the integration interface that operationalises the service contract
- `dea-architecture-framework` `model/opendeam-model.yaml`: the allocation of ISS to this repository
- `dea-architecture-framework` `docs/is-semantic-architecture/opendeam-identifier-map.yaml`: identifier mapping, D-3 disposition
- `dea-catalog-system-functions` and `dea-catalog-application-components`: sibling catalogues whose forward references target this catalogue