# MindShift Runtime

The MindShift runtime is a non-operative documentation model for preserving
bounded intent, explicit authority, boundary review, proof closure, learning, and
new observations without creating an execution platform.

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

## Runtime Invariants

Intent candidates are not authority.
Authority is not execution.
Eligibility is not proof.
Proof is not authority.
Learning does not mutate authority.
Learning does not mutate execution eligibility.
No automatic external execution.

## Boundary Model

Issues may hold observations and candidate intent. Issues cannot authorize
execution. Intent candidates remain proposals until explicit manual approval is
recorded as an authority record.

Authority records bound the approved action, scope, constraints, and expiry.
Authority records do not execute actions. The execution boundary checklist can
return `Eligible` only when the bounded conditions are satisfied; otherwise it
returns `NULL`.

Eligibility is not proof. Proof closure can be recorded only after a separately
scoped action has occurred outside this documentation template. Proof closure
records evidence and unresolved gaps; it does not authorize future action.

Learning logs interpret proof closure and produce a new observation. Learning is
non-operative and does not mutate authority or execution eligibility.
