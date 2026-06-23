# MindShift Runtime

The MindShift runtime is a non-operative documentation model for preserving
bounded intent, explicit authority, execution-boundary review, proof closure,
and learning records without creating an execution platform.

## Canonical Lifecycle

```text
Issue
→ Intent Candidate
→ Manual Approval
→ Authority Record
→ Execution Boundary Checklist
→ Eligible / NULL
→ Separately Scoped Action
→ Proof Closure
→ Learning Log
→ New Observation
```

The lifecycle is recursive only as documentation: a new observation may become a
future issue or intent candidate, but no later stage automatically authorizes or
executes any future action.

## Boundary Invariants

Intent candidates are not authority.

Authority is not execution.

Eligibility is not proof.

Proof is not authority.

Learning does not mutate authority.

Learning does not mutate execution eligibility.

No automatic external execution.

## Artifact Responsibilities

- Issues and intent candidates preserve observations and proposed intent for
  review.
- Manual approval is required before an authority record can exist.
- Authority records document explicit, bounded approval; they do not execute.
- Execution-boundary checklists determine only whether a scoped action is
  eligible or NULL.
- Separately scoped actions occur outside this documentation model and must be
  bounded independently.
- Proof closure records evidence after a separately scoped action has occurred.
- Learning logs interpret proof closure and produce new observations without
  mutating prior authority, eligibility, or proof.

If no separately scoped action occurred, proof remains NULL / not created. If no
proof closure exists, learning remains NULL / not created.
