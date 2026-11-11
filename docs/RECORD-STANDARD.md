# ISS Record Standard

Established by `CR-IS-CAT-03C`. This document defines what a populated record must contain, field by field, and the evidence it must cite. The gates at `scripts/check_record_evidence.py` and `scripts/check_reference_integrity.py` enforce exactly what this document says.

## 1. Field requirements

| Field | Requirement |
|---|---|
| `id` | Canonical `dea:information-system-service-<slug>`; never an external identifier, never a legacy id (E004) |
| `type` | Constant `InformationSystemService` |
| `name` | Vendor-neutral capability name, 1 to 200 characters |
| `description` | Vendor-neutral prose, at least 40 characters, at most 2000; states the contract, the substitutability test result and the provider in words |
| `version` | Semver string |
| `lifecycle_status` | One of the metamodel lifecycle vocabulary: proposed, planned, active, deprecated, retired |
| `service_kind` | One cell of the service-kind axis (TAXONOMY 2.1) |
| `consumer_class` | One cell of the consumer-class axis (TAXONOMY 2.2) |
| `interaction_pattern` | One cell of the interaction-pattern axis (TAXONOMY 2.3) |
| `external_references` | At least 3 entries from 3 distinct vendor systems; evidence only, never canonical (G-12) |
| `tags` | Axis mirrors plus `system-class:` and `sector:`, each exactly once (TAXONOMY 4) |
| `service_contract.offering` | Non-empty; the capability, functionality or data made available, in contract terms |
| `service_contract.consumers` | At least one; a service with no consumer is a capability nobody asked for (tenet 2) |
| `service_contract.contract_status` | One cell of the contract-maturity axis (TAXONOMY 2.4) |
| `provided_by` | At least one canonical component or service id resolving against the vendored ISC snapshot (criterion 3) |
| `exposed_via` | Integration interface ids, forward-declared to the IF catalogue when the target has not landed |
| `specializes` | Present only for platform-runtime records, value `dea:entity-platform-service` (D-6) |
| `governance.source_and_evidence` | Must contain a `Metamodel clause:` citation and an `Admitting CR:` citation (criterion 4) |
| `metadata.cr`, `metadata.created_by`, `metadata.created_date` | Provenance, always present |

## 2. Evidence

A record is admitted on citable evidence, never on assertion. The evidence structure is uniform:

1. **Metamodel clause.** The metamodel entity schema the record is filed under, named with the literal phrase `Metamodel clause:`.
2. **Admitting CR.** The change request that admitted the record, named with the literal phrase `Admitting CR:`.
3. **Vendor corroboration.** At least 3 distinct vendor systems in `external_references`. Vendor systems corroborate that the contract is real industry practice; they never name the canonical record and never appear in `id`, `name`, `description`, tags or the contract. A record with fewer than 3 distinct vendor systems is a candidate, not an admission.

## 3. The substitutability test

Before a record is filed, it must pass the test of FOUNDATIONS 4.1: could two materially different vendor implementations satisfy this contract? If no, the record describes an implementation and belongs in ISC, not here. The description states that the test passes.

## 4. Cross-catalogue references

References out of the record resolve under the policy of FOUNDATIONS section 4.4:

- `provided_by` targets resolve against the vendored snapshot at `docs/is-semantic-architecture/target-id-snapshots.yaml`, pinned to a commit of `dea-catalog-application-components`.
- `exposed_via` targets are declared in `docs/is-semantic-architecture/forward-declarations.yaml` with the target repository and the owning change request named, until the IF catalogue population lands and they resolve.
- The registry at `relationships/v1-alpha/relationships.yaml` carries the typed edges (`dea:provides`, `dea:exposes`); record fields are pointers, the registry is the connection assertion (D8).

## 5. Provenance

Records generated deterministically cite the generator and the deriving population in `metadata.notes`. Hand-authored records cite the sources relied upon. Authorship fields carry `Emmanuel A. Otchere` or `TechNeHub Labs` only.
