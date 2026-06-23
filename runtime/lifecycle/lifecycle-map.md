# Lifecycle Map

| Stage | Artifact | Output | Boundary |
| --- | --- | --- | --- |
| Issue | GitHub issue or observation record | Observed problem or opportunity | Creates no authority |
| Intent Candidate | Intent candidate issue template | Proposed action for review | Creates no authority or proof |
| Manual Approval | Maintainer approval reference | Permission to create authority record | Does not execute |
| Authority Record | `runtime/authority/` record | Bounded approval | Authority is not execution |
| Execution Boundary Checklist | `runtime/execution-boundary/` checklist | Eligible / NULL | Eligibility is not proof |
| Separately Scoped Action | External bounded action | Action result | Outside this documentation model |
| Proof Closure | `runtime/proof/` closure | Evidence record | Proof is not authority |
| Learning Log | `runtime/learning/` log | Interpreted lesson | Learning does not mutate authority or eligibility |
| New Observation | Future issue or observation | Next loop input | No automatic external execution |

## Canonical loop

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
