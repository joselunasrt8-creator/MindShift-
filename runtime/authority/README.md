# Authority Records

Authority is explicit maintainer approval for a bounded action. It is a manual
record, not an execution mechanism.

Issues cannot authorize execution. Intent candidates are not authority. Authority
records must be manually created after maintainer approval and must remain
separate from observation, issue creation, and intent candidate creation.

Every authority record must define:

- approved action;
- scope;
- constraints;
- expiry; and
- expected proof.

Authority does not execute actions. It does not trigger workflows, call APIs,
merge, deploy, create proof, or mutate execution eligibility. It only documents
that a bounded action may proceed to execution-boundary review.

If approval is missing, ambiguous, expired, or unbounded, authority remains
`NULL` and the action cannot become eligible.
