# Change requests

Every change to this catalogue lands through a change request. One CR per PR, with deviations documented in the CRs themselves.

| CR | Scope | State |
|---|---|---|
| `CR-IS-CAT-03A` | Foundation: method, pointer, schema projection, CI. No records. | implemented |
| `CR-IS-CAT-03B` | Taxonomy: ratify the four classification axes; promote three to first-class fields | implemented |
| `CR-IS-CAT-03C` | Documentation standard: per-record template and evidence checklist | implemented |
| `CR-IS-CAT-03D` | Population: admit 623 records; resolve ISC forward reference `isc-rel-006` | implemented |
| `CR-IS-CAT-03E` | Integration: relationship registry, forward declarations, reference integrity gate | implemented |

The 03B through 03E wave landed as one PR (the population wave) rather than four sequential PRs. The deviation from the one-CR-per-PR convention is documented in each CR: the taxonomy, record standard and population gates only have meaning against a populated tree, and the four CRs were sliced so each one's gates fail without the next one's content. Sequencing them as four PRs would have kept main red between merges. The CRs remain individually authoritative for their scope.

## Documents

- [CR-IS-CAT-03A: Information System Service Catalogue Foundation](./CR-IS-CAT-03A-information-system-services-foundation.md)
- [CR-IS-CAT-03B: ISS Record Taxonomy](./CR-IS-CAT-03B-taxonomy.md)
- [CR-IS-CAT-03C: ISS Record Standard](./CR-IS-CAT-03C-record-standard.md)
- [CR-IS-CAT-03D: ISS Catalogue Population](./CR-IS-CAT-03D-population.md)
- [CR-IS-CAT-03E: ISS Cross-Catalogue Integration](./CR-IS-CAT-03E-cross-catalogue.md)
