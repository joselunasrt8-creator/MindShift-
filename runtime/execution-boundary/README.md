# Execution Boundary Checklist

The execution boundary is the point where a proposed action is checked before it can become eligible for execution. It is a review boundary, not an execution surface.

Authority does not equal execution. An `APPROVED` authority record only makes an action reviewable for eligibility; it does not perform, trigger, schedule, merge, deploy, call APIs, mutate external systems, or create proof.

The execution-boundary checklist verifies that:

- authority exists;
- the approved action is bounded;
- scope is defined;
- constraints are defined; and
- proof expectations are known before any separately scoped execution can occur.

This checklist does not execute anything. Eligibility is not proof, and proof is only created after separately scoped execution has occurred.

If any required condition is missing, the action remains `NULL` / not eligible.

## Flow

```text
Intent Candidate
↓
Authority Record
↓
Execution Boundary Checklist
↓
Eligible / NULL
```
