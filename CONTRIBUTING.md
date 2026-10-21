# Contributing to the Information System Service catalogue

## Before you propose a record

Population is gated. No record may be admitted before `CR-IS-CAT-03B` ratifies
the classification taxonomy and `CR-IS-CAT-03C` defines the documentation
standard. A pull request that adds a record before both land will fail the
record-posture gate.

Read [`docs/FOUNDATIONS.md`](./docs/FOUNDATIONS.md) first. It carries the
cardinal scope, the classification axes, the admission criteria, and the
decision register that later change requests cite by number.

## The one test

> Can the same contract be fulfilled by two materially different implementations?

If no, you are describing a component. That record belongs in
`dea-catalog-application-components`, not here.

## Change control

| Artefact | Authority |
|---|---|
| `metamodel-pointer.yaml` | OpenDEAM root model. Never hand-edited; a finding from the pointer gate means the allocation drifted |
| `schemas/*.json` | This repository, by CR, mirroring the metamodel |
| Records | This repository, by CR, gated on the taxonomy CR |

## Local validation

Run the gates before opening a pull request. They are the same scripts CI runs.

```
python3 scripts/check_parse.py
python3 scripts/check_pointer.py
python3 scripts/check_schema_projection.py
python3 scripts/check_writing_rules.py
python3 scripts/check_record_posture.py
```

## Writing rules

D-004: no en-dash, em-dash, two-em dash, or ellipsis in any artefact. D-005: no
triple semicolon in prose. Both are enforced by
`scripts/check_writing_rules.py`.

## Authorship

Commits are authored by the repository owner. See the programme cardinal rules.
