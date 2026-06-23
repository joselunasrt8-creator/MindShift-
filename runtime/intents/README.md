# MindShift Intent Candidates

GitHub issues are observation containers. They can hold structured information
about what was observed, how it is modeled, what evidence supports it, and what
action might be proposed for later review.

Intent candidates propose actions only. They are not authorization mechanisms,
and they do not authorize execution, create proof, grant operational authority,
trigger workflows, call APIs, merge, deploy, or mutate external systems.

Maintainer approval is required before any authority object exists. Authority
must be explicit, manual, bounded, and separate from issue creation or intent
candidate creation.

## Handoff Boundary

```text
MindShift:
Observe → Model → Validate → Intent Candidate

ContinuityOS:
Authority → Execution Boundary → Proof → Learning
```

MindShift ends at Intent Candidate. ContinuityOS begins at Authority. This
boundary keeps issues and intent candidates non-operative: they can propose
bounded actions for review only, and no execution is allowed from issue creation.
