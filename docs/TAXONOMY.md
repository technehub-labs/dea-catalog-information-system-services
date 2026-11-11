# ISS Record Taxonomy

Ratified by `CR-IS-CAT-03B`. This document is the normative statement of the four classification axes on which every Information System Service record is placed. The gate at `scripts/check_record_taxonomy.py` enforces exactly what this document says; if the two disagree, that is a finding against both.

## 1. Position

A record is classified on four axes. The axes are the admission test: a record that cannot be placed on all four is not yet understood well enough to admit (FOUNDATIONS section 3).

Three axes were carried as tags in the initial schema. This CR promotes them to first-class fields (`service_kind`, `consumer_class`, `interaction_pattern`) with closed enums in `schemas/information-system-service.schema.json`. The tags remain as mirrors so tag-driven queries keep working, and the taxonomy gate asserts tag and field agree. One axis, contract maturity, was already a first-class field (`service_contract.contract_status`).

## 2. The four axes

| Axis | Field | Question | Vocabulary |
|---|---|---|---|
| Service kind | `service_kind` | What kind of contract is offered? | authentication, data-access, transaction, notification, analytics, integration, platform-runtime, other |
| Consumer class | `consumer_class` | Who consumes it? | internal-application, internal-analyst, internal-machine, external-partner, external-customer, mixed |
| Interaction pattern | `interaction_pattern` | How is the exchange shaped? | request-response, event-push, event-subscribe, streaming, batch, mixed |
| Contract maturity | `service_contract.contract_status` | How settled is the contract? | draft, published, deprecated, retired |

### 2.1 Service kind

The kind of capability the contract offers, not the technology that implements it. Placement rules:

| Cell | The contract offers | Placed here when |
|---|---|---|
| authentication | Verification of identity and entitlement | The exchange proves or establishes who the consumer is |
| data-access | Read or write access to a governed data set | The exchange moves data in or out of a record of authority |
| transaction | A unit of work with commitment semantics | The exchange changes state and either completes or has no effect |
| notification | The emission of a signal to interested parties | The exchange pushes an occurrence to subscribers |
| analytics | Computation over data producing insight | The exchange computes over collected data and returns a result |
| integration | Movement or transformation between systems | The exchange connects heterogeneous parties |
| platform-runtime | Execution or hosting capability for workloads | The exchange provides runtime, storage or orchestration as a service |
| other | None of the above | Used sparingly; a growth in this cell is a finding against the taxonomy |

### 2.2 Consumer class

Who the contract names as its consumer. `mixed` is legitimate when the offering genuinely serves more than one class with the same terms; it is not a default for records whose consumers were not analysed.

### 2.3 Interaction pattern

How the exchange is shaped at the contract level: request-response, event-push, event-subscribe, streaming, batch, or mixed. The pattern classifies the contract, not the wire protocol; protocol belongs to the II catalogue (D3).

### 2.4 Contract maturity

How settled the contract is: draft, published, deprecated or retired. Population records enter as `published` when the contract is asserted from corroborated industry practice, or `draft` when the offering is still being characterised.

## 3. Mutual exclusivity and duplicate detection

A record occupies exactly one cell per axis. The axes classify; they do not identify. The closed vocabulary admits 8 x 6 x 6 x 4 = 1152 four-tuple cells in total and at most 288 per system class, so a population of hundreds of records necessarily places genuinely distinct records in the same cell of the same system class. A four-tuple collision is therefore a classification fact, not a finding.

Two records are duplicates when they share all of: the system class, the provider set (`provided_by`), the full four-tuple (service kind, consumer class, interaction pattern, contract maturity) and the offering text. Two records that share a four-tuple but differ in provider or offering are distinct records in one classification cell; if that cell grows large enough to blur meaning, the finding is against the axes and must be raised as a CR against this taxonomy. The gate fails the build on a true duplicate and passes records that merely share a cell.

## 4. Tag mirrors

The promoted fields carry the classification; the following tag forms mirror them, one per axis per record:

| Axis | Tag mirror |
|---|---|
| Service kind | `service-kind:<cell>` |
| Consumer class | `consumer-class:<cell>` |
| Interaction pattern | `interaction-pattern:<cell>` |

Two additional tag forms are not axes but bookkeeping and are checked by the gate for exactly-once presence: `system-class:<slug>` (the generic system class the record belongs to) and `sector:<slug>` (the industry sector). Vendor names never appear in tags; vendor systems are evidence in `external_references` only (G-12).

## 5. Change control over the vocabularies

Adding a vocabulary cell is a CR against this document plus a schema projection update plus a gate update, in one PR. Removing or renaming a cell is the same plus a record migration. A cell that grows a large population deserves subdivision; the growth signal is periodic review, not the gate.
