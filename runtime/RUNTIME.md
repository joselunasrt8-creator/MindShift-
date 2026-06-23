# MindShift Runtime

The MindShift runtime keeps proposed action review separate from execution. Runtime records describe progression, readiness, closure, and learning; they do not perform external actions, auto-create authority, auto-create proof, or mutate external systems.

## Runtime Progression

```text
Observe
→ Intent Candidate
→ Authority Record
→ Execution Boundary Checklist
→ Proof Closure
→ Learning Log
```

## Lifecycle

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

## Intent Candidates

Issue templates create structured intent candidates. An intent candidate is a proposal for review, not an authorization mechanism. Intent candidates do not authorize execution, create proof, grant operational authority, or change execution eligibility.

## Authority Records

Authority records are explicit, bounded approvals created only after manual approval. An `APPROVED` authority record does not execute an action. It only allows the proposed action to be reviewed for eligibility against bounded scope, explicit constraints, expiry, and expected proof.

## Execution Boundary Checklist

The execution boundary checklist is the first eligibility check after authority. It verifies readiness only.

The checklist does not execute actions, call external services, merge, deploy, mutate external systems, or generate proof. Eligibility is not proof; proof can only be created after a separately scoped execution has occurred.

Missing authority, missing scope, missing constraints, or missing proof expectation keeps the action `NULL` / not eligible.

## Proof Closure

Proof closure records evidence after separately scoped execution. Proof closure does not create authority, widen authority, approve future action, change eligibility, merge, deploy, call APIs, or execute anything.

## Learning Logs

Learning logs happen after proof closure. Learning is interpretive only: it records what changed, what was validated, what was falsified, and what should become the next observation. Learning does not mutate authority or execution eligibility.
