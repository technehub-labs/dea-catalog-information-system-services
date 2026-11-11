# CR-IS-CAT-03B: ISS Record Taxonomy

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-03B |
| **Title** | Ratify the four classification axes and promote three of them to first-class fields |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-IS-CAT-03A` (foundation) |
| **Repository** | `technehub-labs/dea-catalog-information-system-services` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR ratifies the four classification axes declared in FOUNDATIONS section 3, promotes the three tag-carried axes (`service_kind`, `consumer_class`, `interaction_pattern`) to first-class schema fields with closed enums, and lands the taxonomy gate that enforces one-cell-per-record placement. It admits no records; it is the gate the population CR (`CR-IS-CAT-03D`) depends on.

## 2. Scope

### In scope

1. `docs/TAXONOMY.md`: the normative statement of the four axes, their vocabularies, placement rules, mutual exclusivity, tag mirrors and change control.
2. `schemas/information-system-service.schema.json`: three new catalogue-instance properties (`service_kind`, `consumer_class`, `interaction_pattern`), each a closed enum mirroring the ratified vocabulary. The tag mirrors remain; the gate asserts tag and field agree.
3. `scripts/check_record_taxonomy.py` (Gate 6): one-cell-per-axis, tag/field agreement, four-tuple uniqueness within a system class, and the D-6 platform gate (platform-runtime records must specialize `dea:entity-platform-service`; no other record may).

### Out of scope

1. **Any record admission.** Population is `CR-IS-CAT-03D`.
2. **Contract maturity.** Already a first-class field (`service_contract.contract_status`); its vocabulary is ratified here but its mechanics are unchanged.
3. **Renaming or removing a vocabulary cell.** No populated record exists yet, so there is nothing to migrate.

## 3. Decisions

| Decision | Rationale |
|---|---|
| Promote to first-class fields, keep tags as mirrors | FOUNDATIONS 3 promised promotion at taxonomy ratification. Fields make the axes queryable and schema-checked; tag mirrors keep tag-driven tooling working during the transition. Drift between the two is a CI failure, not a convention. |
| Closed enums in the projection | The projection rule stands: never widen a normative enum. These are catalogue-instance fields, not metamodel fields, so the enum lives in the projection and this CR owns it. |
| Four-tuple collision means duplicate only with shared provider and offering | The vocabulary admits 1152 four-tuple cells and at most 288 per system class, so distinct records in one cell are mathematically inevitable at population scale. The gate therefore fails on a true duplicate (same system class, provider set, four-tuple and offering) and treats a bare four-tuple collision as a classification fact, per FOUNDATIONS 3: when genuinely distinct records collide, the finding is against the axes and is raised here, in the taxonomy CR. |
| `mixed` is legitimate, not a default | A record whose consumers or patterns were not analysed is not understood well enough to admit; populating `mixed` by habit would hollow out the axis. |

## 4. Gates landed

| Gate | Script | Asserts |
|---|---|---|
| Taxonomy | `scripts/check_record_taxonomy.py` | One cell per axis per record; tag/field agreement; four-tuple uniqueness per system class; D-6 platform gate |

## 5. Verification

1. Every record admitted by `CR-IS-CAT-03D` passes Gate 6 with zero findings.
2. Tag mirrors and fields agree on all records.
3. No record populates `other` as its service kind without the taxonomy review that its use invites.

## 6. References

- `docs/FOUNDATIONS.md` section 3 (classification axes), section 6 (decision register D-6).
- `CR-IS-CAT-03D` (population, gated on this CR).
- `CR-IS-CAT-03C` (record standard, companion to this CR).
