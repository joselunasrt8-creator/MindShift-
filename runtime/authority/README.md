# Authority Records

Authority records are explicit, bounded approvals created only after manual approval of an intent candidate.

Authority is not execution. An authority record does not perform, trigger, schedule, merge, deploy, call APIs, mutate external systems, create proof, or change future execution eligibility.

An authority record must preserve:

- linked intent candidate;
- manual approval source;
- approved bounded action;
- scope;
- constraints;
- expiry; and
- expected proof.

If any required field is missing, the proposed action cannot pass the execution-boundary checklist and remains `NULL` / not eligible.

```text
Intent Candidate
↓
Manual Approval
↓
Authority Record
↓
Execution Boundary Checklist
```
