# MindShift Runtime

The MindShift runtime is a non-operative documentation model for preserving
bounded intent, manual authority, boundary review, proof closure, and learning
records without creating an execution platform.

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

## Boundary Invariants

- Intent candidates are not authority.
- Authority is not execution.
- Eligibility is not proof.
- Proof is not authority.
- Learning does not mutate authority.
- Learning does not mutate execution eligibility.
- No automatic external execution.

## Runtime Artifacts

- `runtime/intents/README.md` defines issue-backed observation and intent candidate boundaries.
- `runtime/authority/README.md` defines manual maintainer authority records.
- `runtime/execution-boundary/README.md` defines eligibility review boundaries.
- `runtime/proof/README.md` defines evidence-only proof closure.
- `runtime/learning/README.md` defines learning logs that create new observations only.

The runtime records topology and evidence only. It does not authorize, validate,
execute, merge, deploy, call APIs, create proof automatically, or mutate future
execution eligibility.
