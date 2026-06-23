# Lifecycle Map

| Step | Artifact | Creates Authority? | Executes Action? | Output |
| --- | --- | --- | --- | --- |
| Observation | Issue or note | No | No | Intent candidate material |
| Intent Candidate | `runtime/intents/README.md` | No | No | Proposal for review |
| Manual Approval | Maintainer decision | Yes, only when explicit and bounded | No | Authority record |
| Boundary Review | `runtime/execution-boundary/README.md` | No | No | Eligible / `NULL` |
| Separately Scoped Action | External to this template | No | Only if separately authorized | Changed object |
| Proof Closure | `runtime/proof/README.md` | No | No | Evidence record |
| Learning Log | `runtime/learning/README.md` | No | No | New observation |

## Replay Rule

A lifecycle may be replayed only as a new bounded review. Prior proof or learning
cannot be reused as authority for another action.
