# CR-IS-CAT-03A: Information System Service Catalogue Foundation

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-03A |
| **Title** | Information System Service catalogue foundation (methodology-first bring-up) |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-020` (metamodel, ISS entity introduction, D-3 disposition) |
| **Repository** | `technehub-labs/dea-catalog-information-system-services` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-10-20 |

## 1. Executive summary

This CR establishes the Information System Service catalogue as a **method**, not as content. It lands the pointer, the schema projection, the classification axes, the admission criteria, the cross-catalogue reference policy, and five CI gates. It admits **no records**.

This is the first of the five-change-request ISS programme. It follows the methodology-first rule established for the business-capability catalogue: the first increment of a catalogue establishes admission criteria, the evidence process, and the framework-overlay rules. Records come later, gated on the taxonomy CR.

## 2. Scope

### In scope

1. `metamodel-pointer.yaml` pinned to OpenDEAM v0.7.0.
2. `schemas/information-system-service.schema.json`, a projection of the metamodel entity schema with the catalogue-instance layer added.
3. `docs/FOUNDATIONS.md`: cardinal scope, exclusions, four classification axes, six admission criteria, the cross-catalogue reference policy, the repository reality reconciliation, and a nine-entry decision-points register.
4. `README.md`: catalogue boundary table, entity definition, five key tenets, relationship inventory, cross-catalogue reference table, change-control matrix.
5. Five CI gates (`scripts/check_*.py`) wired into `.github/workflows/validate-catalogue.yml`.
6. `.gitignore`, landed before any Python exists in the repository.

### Out of scope

1. **Any ISS record.** Population is `CR-IS-CAT-03D`.
2. **The classification vocabularies.** Declared as direction in FOUNDATIONS section 3, ratified in `CR-IS-CAT-03B`.
3. **The per-record documentation template.** That is `CR-IS-CAT-03C`.
4. **The `entities/` and `relationships/` directories.** Declared in the README structure block, marked as not built, arriving with their CRs.
5. **Resolution of the ISC forward reference.** `isc-rel-006` targets `dea:information-system-service-api-gateway-service` under this CR. The reference remains correctly forward-declared until the population CR admits the record.
6. **Any change to `dea:entity-platform-service` or Core `dea:Service`.**
7. **Governance portfolio registration.** That is `CR-013 (dea-governance)`.

## 3. Audit findings

The repository was created 2026-10-19 and is genuinely empty: no default branch, no commits, no files. Bring-up therefore started from nothing rather than from a scaffold whose README had drifted from its pointer.

Three findings from the audit shaped this CR.

### 3.1 The metamodel carries an internal contradiction on ISS catalog ownership

`dea-metamodel/metamodel/dea-metamodel.yaml` entity `dea:InformationSystemService` declares:

```yaml
catalog_repo: dea-catalog-platform-services
```

while the `definition` field of the same entity states:

> Catalog ownership: the dea-catalog-information-system-services repository (new repository per CR-IS-CAT-03).

The same contradiction appears in `metamodel/registry/entities.yaml`. Two authoritative fields of the same record disagree about which repository owns ISS.

**Disposition in this CR: the pointer records `dea-catalog-information-system-services`.**

The reasoning: `dea-metamodel` CR-020 section 2.2 explicitly defers the new repository to `CR-IS-CAT-03`, and section 2.2 item 7 assigns migration of `dea-catalog-platform-services` records to `CR-IS-CAT-03` and the catalog-ownership register in `CR-013`. The definition text is the later and more specific statement of intent, and it names this repository and this CR. The `catalog_repo: dea-catalog-platform-services` field predates that decision in the same record.

**This is recorded, not silently resolved.** Correcting `dea-metamodel` is a metamodel-side change outside this CR's authority. It is registered as an outstanding item in section 6 and must be raised as a metamodel CR. Until it is, a consumer reading `catalog_repo` rather than `definition` will look for ISS records in `dea-catalog-platform-services` and find none.

### 3.2 Three of the four IS-family repositories do not carry their allocated name

The OpenDEAM root model (`dea-architecture-framework/model/opendeam-model.yaml`, v0.7.0) allocates:

| Alias | Allocated repository | Actual repository |
|---|---|---|
| ISF | `dea-catalog-information-system-functions` | `dea-catalog-system-functions` |
| ISC | `dea-catalog-information-system-components` | `dea-catalog-application-components` |
| **ISS** | `dea-catalog-information-system-services` | `dea-catalog-information-system-services` (matches) |
| IF | `dea-catalog-information-system-integration-interfaces` | `dea-catalog-integration-interfaces` |

Verified against the GitHub API: three of the four allocated repository names return 404; the ISS name resolves to the empty repository.

**Disposition in this CR: ISS is the clean case.** This repository already carries its allocated name, so `metamodel-pointer.yaml` records `rename.status: not-required` and introduces no rename debt. The other three are mid-rename and are recorded in `docs/FOUNDATIONS.md` section 5 as a reconciliation table so that a reader does not have to rediscover the gap.

A consequence stated plainly in FOUNDATIONS: **reference resolution is by identifier, not by repository name**, so the rename debt does not block any cross-catalogue reference. It does mean any document naming a repository by its allocated name must be read alongside that table.

### 3.3 The ISS schema is unusually thin

The metamodel schema for `dea:InformationSystemService` carries nine properties, of which only four are required (`id`, `name`, `type`, `version`). It has no field expressing what a service actually offers, to whom, or under what terms. That is correct for a metamodel, which defines entity identity rather than catalogue content.

**Disposition in this CR:** the projection adds a `service_contract` layer (`offering`, `consumers`, `contract_status`), a `provided_by` cross-catalogue reference, an `exposed_via` reference to the II catalogue, a `specializes` field for the D-3 conditional, and a `governance` block. All normative fields are mirrored unchanged. The schema header states the rule explicitly: never widen a normative enum here to accept a value the metamodel does not define; fix the record instead.

## 4. The method this CR establishes

### 4.1 Cardinal scope: the substitutability test

> Can the same contract be fulfilled by two materially different implementations?
>
> **Yes** -> this is a service. Record it here.
> **No** -> this is a component. Record it in ISC.

This single test resolves the boundary disputes that a taxonomy table cannot. An authentication service offered to ten application components is a service; the token issuer that implements it is a component. Both statements are true; only one is a service record.

### 4.2 Four classification axes

| Axis | Vocabulary |
|---|---|
| Service kind | authentication, data-access, transaction, notification, analytics, integration, platform-runtime, other |
| Consumer class | internal-application, internal-analyst, internal-machine, external-partner, external-customer, mixed |
| Interaction pattern | request-response, event-push, event-subscribe, streaming, batch, mixed |
| Contract maturity | draft, published, deprecated, retired |

A record occupies exactly one cell per axis. Two records sharing a four-tuple are either duplicates or evidence that the axes are insufficient; the second case is a finding against the taxonomy, not against the records.

### 4.3 Six admission criteria

Substitutability passes; consumers named and non-empty; provider identified or explicitly unallocated; evidence citable; identifier canonical; lifecycle state declared. Stated in full in `docs/FOUNDATIONS.md` section 4.

### 4.4 Cross-catalogue reference policy

Every reference resolves against a pinned snapshot. A reference to a target that does not yet exist is permitted only when both the target catalogue and the owning CR are named. An unclassified reference is a hard CI failure. Forward declarations are re-verified against the live target repository at slice time.

That last rule has a precedent: `CR-IS-CAT-02F` found that two target repositories had gained records while their snapshots still claimed emptiness. A snapshot that asserts a target catalogue is empty, when it is not, misleads indefinitely.

## 5. Decision-points register

Nine decisions are recorded in `docs/FOUNDATIONS.md` section 7 as D1 through D9. Later CRs cite them by number rather than re-deriving them. D1 (substitutability boundary), D2 (consumers mandatory), D3 (interface ownership), D4 (snapshot resolution), D5 (named forward references), D6 (platform-service conditional), D7 (no rename for ISS), D8 (registry not inline), D9 (service-of-services).

## 6. Outstanding items this CR does not resolve

| Item | Owner | Severity |
|---|---|---|
| `dea-metamodel` `dea:InformationSystemService.catalog_repo` contradicts its own `definition` on catalogue ownership | metamodel CR | medium |
| ISF, ISC and IF repositories remain mid-rename against their allocation | org admin transfer | medium |
| `isc-rel-006` forward reference awaits the ISS population | `CR-IS-CAT-03D` | low, correctly gated |
| II catalogue rename debt, recorded in FOUNDATIONS section 5 | org admin transfer | low |

The first item is a real defect in an authoritative source. It is recorded here rather than fixed here because a catalogue-side CR cannot correct a metamodel-side field, and doing so here would create a second source of truth for allocation.

## 7. Gates landed

| Gate | Script | Catches |
|---|---|---|
| Parse | `scripts/check_parse.py` | Malformed YAML or JSON anywhere in the tree, not only under `entities/` |
| Pointer | `scripts/check_pointer.py` | Pointer missing required fields, or drifted from its allocation |
| Schema projection | `scripts/check_schema_projection.py` | Normative field dropped, `type` const changed, lifecycle enum drifted from the metamodel vocabulary |
| Writing rules | `scripts/check_writing_rules.py` | D-004 forbidden glyphs and D-005 triple semicolon |
| Record posture | `scripts/check_record_posture.py` | Records appearing without the population gates, or a scaffold catalogue that claims to be populated |

`CR-IS-CAT-03D` replaces the record-posture gate with a real record validator and adds taxonomy, evidence and reference-integrity gates.

### 7.1 A gate caught a defect in its own input

The parse gate failed on the first run. `metamodel-pointer.yaml` had a block sequence followed immediately by a mapping key at the same level, which is not valid YAML:

```yaml
relationships:
  - dea:specializes
  note: >-
```

A list item and a mapping key cannot share an indentation level. The structure was corrected to nest the sequence under `relationships.vocabulary`. This is recorded because it is the argument for landing the gates in the foundation CR rather than in the population CR: the gate existed only long enough to catch a defect introduced in the same PR that landed it, which is exactly the class of defect that would otherwise reach `main` unnoticed.

## 8. Verification

| Check | Result |
|---|---|
| Gate 1 parse | 0 failures across the tree |
| Gate 2 pointer | 0 findings |
| Gate 3 schema projection | 0 findings |
| Gate 4 writing rules | 0 findings |
| Gate 5 record posture | 0 findings, catalogue correctly marked scaffold |
| `metamodel-pointer.yaml` against OpenDEAM v0.7.0 | class alias `ISS`, entity id, layer L5, building block L5-integration, repository all verified |
| Schema against metamodel | 9 normative fields mirrored, lifecycle enum matches the metamodel vocabulary |
| D-004 / D-005 | clean |
| Records admitted | 0, as intended |

## 9. What this CR deliberately does not do

1. Admit a record.
2. Ratify the classification vocabularies (`CR-IS-CAT-03B`).
3. Define the per-record documentation template (`CR-IS-CAT-03C`).
4. Resolve `isc-rel-006`.
5. Correct the metamodel's catalog-ownership contradiction.
6. Create the `entities/` or `relationships/` directories.
7. Migrate any `dea-catalog-platform-services` record.

## 10. References

- `dea-metamodel` `schemas/entities/information-system-service.json`: normative entity schema
- `dea-metamodel` `change-requests/CR-020-information-system-service.md`: entity introduction, D-3 disposition
- `dea-metamodel` `change-requests/CR-017-information-systems-domain-semantic-integration.md`: parent programme
- `dea-metamodel` `change-requests/CR-021-integration-interface.md`: the interface that operationalises the service contract
- `dea-architecture-framework` `model/opendeam-model.yaml`: allocation of ISS to this repository
- `dea-architecture-framework` `docs/is-semantic-architecture/opendeam-identifier-map.yaml`: identifier mapping
- `dea-catalog-application-components` CR-IS-CAT-02F: forward-reference verification, the policy this CR adopts
- `dea-catalog-system-functions`: sibling catalogue, 50 records, the ISS analogue