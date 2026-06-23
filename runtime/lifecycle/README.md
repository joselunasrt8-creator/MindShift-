# Runtime Lifecycle

The MindShift runtime lifecycle is a non-operative topology map. It explains how
intent, authority, boundary review, proof, and learning relate without creating
an execution platform.

```text
Intent Candidate
→ Manual Maintainer Approval
→ Authority Record
→ Execution Boundary Checklist
→ Eligible / NULL
→ Separately Scoped Action
→ Proof Closure
→ Learning Log
→ New Observation
```

## Lifecycle Invariants

- Intent candidates are proposals only.
- Authority must be explicit, manual, bounded, and separate from issue creation.
- Boundary review can return eligibility or `NULL`; it does not execute actions.
- Proof closure records evidence after a separately scoped action occurred.
- Learning logs interpret proof and can only inform future intent candidates.
- Every new action starts a fresh lifecycle and requires fresh authority.

This lifecycle does not authorize, validate, execute, merge, deploy, call APIs,
create proof, or mutate future execution eligibility.
