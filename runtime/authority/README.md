# Authority Records

Authority records are explicit, bounded documentation artifacts created only
after manual approval of an intent candidate.

Authority records do not execute actions, create proof, change eligibility,
merge changes, deploy systems, call APIs, or mutate external state. They only
record what was approved, by whom, under what scope, and under which constraints.

## Position in the lifecycle

```text
Intent Candidate
↓
Manual Approval
↓
Authority Record
↓
Execution Boundary Checklist
```

An authority record makes a scoped proposal available for execution-boundary
review. It does not make the action eligible by itself.

## Required authority fields

- linked issue or intent candidate;
- manual approval reference;
- approved scope;
- explicit constraints;
- prohibited actions or exclusions;
- expected proof artifacts; and
- unresolved risks or NULL conditions.

If manual approval is absent, authority remains NULL / not created.
