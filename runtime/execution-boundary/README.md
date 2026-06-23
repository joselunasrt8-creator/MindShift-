# Execution Boundary Checklist

The execution boundary checklist verifies eligibility only. It is a review
boundary, not an execution surface.

Authority does not equal execution. An authority record only makes a bounded
action reviewable for eligibility; it does not perform, trigger, schedule,
merge, deploy, call APIs, mutate external systems, or create proof.

Eligibility is not proof. Eligibility only means a bounded action passed the
review boundary or remains `NULL` when the boundary is incomplete.

The checklist verifies that:

- authority exists;
- the approved action is bounded;
- scope is defined;
- constraints are defined; and
- proof expectations are known before any separately scoped action can occur.

Missing authority, scope, constraints, or proof expectation keeps the action
`NULL` / not eligible.

The checklist does not execute actions. It does not create authority, create
proof, call APIs, merge, deploy, or mutate future eligibility.

## Flow

```text
Authority Record
↓
Execution Boundary Checklist
↓
Eligible / NULL
```
