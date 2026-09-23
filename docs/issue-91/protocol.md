# Issue #91 — prospective work-continuation preparation

## Boundary and status

This directory freezes materials for a later, separately invoked blinded
assessment. It does not contain an assessment. MindShift produces candidate
recommendations only:

```text
Proposal != Authority
Cognition != Legitimacy
Validation != Execution
AI output is never executable
```

Every future assessment must set `authority` to `null` and
`execution_eligible` to `false`. Validation establishes structural and protocol
admissibility, never substantive correctness, permission, or eligibility.

## Prospective scope

The cohort includes every locally reconstructable historical MindShift work
proposal found during the Issue #91 audit that had (a) a committed prospective
artifact, (b) a reliable Git cutoff, (c) exact source bytes at that cutoff, and
(d) a later committed record. Selection did not depend on whether a future
recommendation would appear successful. Issue #79 was excluded because its
only local artifact already contains its terminal result. Issue #76 was
excluded because no later independently completed disposition is present.

For each included item, descriptive fields are a conservative transcription of
the cited cutoff source. No later record was used to create target uncertainty,
expected evidence, alternatives, blockers, assessment criteria, or
recommendation rules. If a cost was not explicit at cutoff it is `null`.

## Temporal and blinding rules

An admissible evidence object must resolve from its recorded Git commit and
path, match its SHA-256, have a commit timestamp no later than the item's
`cutoff_timestamp`, and be listed in both `evidence_refs` and
`evidence_hashes`. The primary source commit equals the cutoff commit. Evidence
after the cutoff is inadmissible even when it is historically accurate.

`assessment-input/` contains only reconstructed cutoff material. `outcomes/`
is a sibling tree and is not accepted by the reconstruction command. The
reconstructor copies an allowlisted, regular-file bundle to a new empty
directory, rejects links and unlisted paths, and verifies that neither outcome
paths nor outcome hashes occur in an assessor-readable file. A future assessor
receives only that reconstructed directory.

## Assessor configuration

The intended later run is one fresh, stateless assessor per item, with tools,
retrieval, repository access, conversation history, and shared prompt cache
disabled. Temperature is zero, one completion is requested, and only the
reconstructed assessment bundle plus the assessment schema may be supplied.
No model/provider is selected by this preparation.

## Immutable terminal rules

Preparation is `FROZEN_FOR_BLINDED_ASSESSMENT` only when all committed inputs,
schemas, validator, rubric, sources, and manifest bindings validate; two clean
reconstructions are byte-identical; outcome material is unreachable; no
assessment artifact exists; and model calls remain zero. It is
`BLOCKED_WITH_PRESERVED_EVIDENCE` when a legitimate cohort or prerequisite
cannot be established. It is `PREPARATION_INVALID` on leakage, unverifiable
identity, mutable criteria, or another protocol defect. No favorable state may
be forced, and beginning assessment requires a separate deliberate invocation.
