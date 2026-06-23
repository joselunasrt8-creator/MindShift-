# Runtime Lifecycle

The runtime lifecycle maps MindShift observations into bounded documentation
artifacts without creating an execution platform.

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

Each stage preserves a separate responsibility. No stage inherits authority from
a later stage, and no stage automatically performs external execution.

## Manual runbook

Use the [manual runtime lifecycle runbook](manual-runbook.md) as the
contributor-facing guide for using the lifecycle without creating authority,
execution, eligibility, or proof automatically.

## Closure rule

Learning closes the loop only by producing a new observation. Any future action
must begin again with an issue or intent candidate and pass through manual
approval, authority, boundary review, eligibility, separately scoped action,
proof closure, and learning.
