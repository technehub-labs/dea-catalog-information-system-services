# CR-IS-CAT-03E: ISS Cross-Catalogue Integration

| Field | Value |
|---|---|
| **CR** | CR-IS-CAT-03E |
| **Title** | Relationship registry, forward declarations and reference integrity gate |
| **Status** | Implemented in this PR |
| **Layer** | Catalogue (Digital Profile) |
| **Programme** | Information Systems Semantic Architecture |
| **Parent CR** | `CR-IS-CAT-03D` (population) |
| **Repository** | `technehub-labs/dea-catalog-information-system-services` |
| **Author** | Emmanuel A. Otchere |
| **Date** | 2026-11-11 |

## 1. Executive summary

This CR hardens the populated catalogue's cross-catalogue posture: it lands the relationship registry carrying the typed `dea:provides` and `dea:exposes` edges for every admitted record, the forward-declaration register for exposures whose targets live in the not-yet-populated IF catalogue, and the reference-integrity gate that fails the build on any reference that neither resolves nor is declared.

## 2. Scope

### In scope

1. `relationships/v1-alpha/relationships.yaml`: 1247 typed edges. 624 `dea:provides` edges (component to service; one service names two providers) and 623 `dea:exposes` edges (service to interface, forward).
2. `docs/is-semantic-architecture/forward-declarations.yaml`: one declaration per exposure, naming the target repository (`dea-catalog-integration-interfaces`) and the owning change request (`CR-IS-CAT-04B`), per FOUNDATIONS 4.4.
3. `scripts/check_reference_integrity.py` (Gate 8): every `provided_by` target resolves against the vendored ISC snapshot; every `exposed_via` target is declared forward with both the target repository and the owning CR named; the two anchor records the sibling catalogues depend on exist; anything else fails.
4. The anchor-record assertions: `dea:information-system-service-identity-service` (ISF registry dependency) and `dea:information-system-service-api-gateway-service` (ISC registry `isc-rel-006`).
5. `.github/workflows/validate-catalogue.yml`: steps 6, 7 and 8 wire the taxonomy, evidence and reference-integrity gates into CI.

### Out of scope

1. **Re-verification of forward declarations against a populated IF catalogue.** The IF repository was verified empty at slice time (2026-11-11); its population lands under `CR-IS-CAT-04A/04B` in the same programme wave. When it lands, the exposures resolve and the declarations retire.
2. **The ISC-side reclassification of `isc-rel-006` from forward to resolved.** That is an ISC change request.
3. **Snapshot pin advancement.** The snapshot stays pinned at the ISC commit the population resolved against; advancing it is a deliberate later change with its own evidence.

## 3. Registry design

| Property | Decision | Rationale |
|---|---|---|
| Location | `relationships/v1-alpha/relationships.yaml` | Connection assertions live in the registry, not as inline state on records (metamodel CR-3, FOUNDATIONS D8). Record fields are pointers; the registry carries the typed edges. |
| Edge ids | `rel:iss-NNNN-provides`, `rel:iss-NNNN-exposes` | Stable, sequentially numbered, deterministic per G-10. |
| Forward edges | `validity_status: planned`, evidence cites the declaration | A forward edge is not an assertion that the target exists; it is an assertion that the target is owned and pending. |
| Provenance | Every edge cites the CR and the pinned snapshot | The registry is auditable without a live fetch. |

## 4. Gates landed

| Gate | Script | Asserts |
|---|---|---|
| Reference integrity | `scripts/check_reference_integrity.py` | Snapshot-resolved providers, declared exposures, anchor records present, zero unresolved |

## 5. Verification

1. Gate 8 passes with 624 resolved provider references and 623 forward-declared exposures, zero findings.
2. The registry edge count matches the record-derived edge count exactly.
3. CI runs eight steps; the PR is green only when all eight pass.

## 6. References

- `docs/FOUNDATIONS.md` section 4.4 (cross-catalogue reference policy: resolution, forward declaration, rebase, verification).
- `CR-IS-CAT-04A/04B` (IF catalogue foundation and population, owning the declared targets).
- `scripts/build_target_snapshots.py` (landed by `CR-IS-CAT-03D`), the source of the vendored snapshot this gate reads.
