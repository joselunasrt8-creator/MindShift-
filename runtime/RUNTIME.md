# MindShift Runtime

The MindShift runtime keeps proposed action review separate from execution. Runtime records describe progression and readiness; they do not perform external actions, auto-create proof, or mutate external systems.

## Runtime Progression

```text
Issue
→ Intent Candidate
→ Manual Maintainer Approval
→ Authority Record
→ Execution Boundary Checklist
→ Proof only after scoped execution
```

## Execution Boundary Checklist

The execution boundary checklist is the first eligibility check after authority. It verifies readiness only.

An `APPROVED` authority record does not execute an action. It only allows the proposed action to be reviewed for eligibility against bounded scope, explicit constraints, expiry, and expected proof.

The checklist does not execute actions, call external services, merge, deploy, mutate external systems, or generate proof. Eligibility is not proof; proof can only be created after a separately scoped execution has occurred.

Missing authority, missing scope, missing constraints, or missing proof expectation keeps the action `NULL` / not eligible.
