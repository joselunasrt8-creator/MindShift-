# Proof Closure

Proof closure records evidence only after a separately scoped action occurred.
It is not the action itself and does not cause an action to happen.

Proof is not authority. Authority remains the prior manual record that allowed a
bounded action to proceed to boundary review.

Proof is not eligibility. Eligibility is only a boundary outcome that says a
scoped action may proceed, or returns `NULL` when it may not proceed.

Proof is not auto-created by issue creation, intent candidates, authority
approval, checklist completion, workflow execution, or learning logs. Those
records may be linked later, but they do not themselves create proof.

Proof closure records:

- what happened;
- what authority allowed it;
- what evidence exists; and
- what remains unresolved.

If no separately scoped action occurred, proof remains NULL / not created.

## Non-operative flow

```text
Authority Record
↓
Execution Boundary Checklist
↓
Separately Scoped Action
↓
Proof Closure
```

This directory provides templates only. It does not authorize, validate, execute,
merge, deploy, call APIs, create external proof, or generate proof automatically.
