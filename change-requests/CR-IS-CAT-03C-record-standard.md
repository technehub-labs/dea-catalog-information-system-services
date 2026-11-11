# CR-IS-CAT-03C: ISS Record Standard

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-03C |
| **Title** | Per-record template and evidence checklist |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-IS-CAT-03A` (foundation); `CR-IS-CAT-03B` (taxonomy) |
| **Repository** | `technehub-labs/dea-catalog-information-system-services` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR defines what a populated record must contain, field by field, and the evidence it must cite: the metamodel clause, the admitting change request, and vendor corroboration of at least 3 distinct vendor systems. It lands the evidence gate that enforces the standard. It admits no records; it is the second gate the population CR depends on.

## 2. Scope

### In scope

1. `docs/RECORD-STANDARD.md`: the field-by-field requirement table, the evidence structure (metamodel clause, admitting CR, vendor corroboration), the substitutability test, cross-catalogue reference handling and provenance.
2. `scripts/check_record_evidence.py` (Gate 7): per record, `governance.source_and_evidence` must cite a metamodel clause and an admitting CR, `external_references` must carry at least 3 distinct vendor systems, the description must be substantive, and the service contract must name an offering and at least one consumer.

### Out of scope

1. **Any record admission.** Population is `CR-IS-CAT-03D`.
2. **Reference resolution mechanics.** The forward-declaration register and the integrity gate are `CR-IS-CAT-03E`.

## 3. The evidence bar

| Requirement | Why |
|---|---|
| `Metamodel clause:` present | A record filed outside the entity's normative definition is in the wrong catalogue. |
| `Admitting CR:` present | Every record has a change-control trail; a record nobody admitted is an orphan. |
| At least 3 distinct vendor systems in `external_references` | One vendor corroborates a product, not a service class. Three distinct vendor systems corroborate that the contract is industry practice rather than one vendor's design. They are evidence only; the canonical record stays vendor-neutral (G-12). |
| Description of at least 40 characters | A one-line description cannot state a contract, its substitutability and its provider. |
| Non-empty offering, at least one named consumer | Tenet 2: a service with no consumer is a capability nobody has asked for. |

## 4. Gates landed

| Gate | Script | Asserts |
|---|---|---|
| Evidence | `scripts/check_record_evidence.py` | Metamodel clause, admitting CR, 3 distinct vendor systems, substantive description, named offering and consumers |

## 5. Verification

1. Every record admitted by `CR-IS-CAT-03D` passes Gate 7 with zero findings.
2. No admitted record carries a vendor token in `id`, `name`, description, tags or contract fields; vendor systems appear in `external_references` and in `governance.source_and_evidence` citations only.

## 6. References

- `docs/FOUNDATIONS.md` section 4 (admission criteria), G-12 (vendor neutrality).
- `docs/TAXONOMY.md` (ratified by `CR-IS-CAT-03B`).
- `CR-IS-CAT-03D` (population, gated on this CR).
