# MindShift Instrument Execution Lifecycle Contract

**Contract version:** 1.0.0 (frozen)
**Status:** Canonical contract
**Owner:** MindShift
**Upstream artifact contract:** [Observation to Research Handoff Contract](observation-to-research-handoff-contract.md), version 1.0.0 (frozen)
**Downstream consumers:** MindShift #33, MindShift #52, MindShift #53, and Continufy Reference Execution v1.0

> Instrument-version freeze does not freeze the MindShift repository reference boundary.
> Repository-level freeze remains owned by MindShift #52.

## Purpose and boundary

This contract defines the lifecycle of a versioned MindShift **instrument**: the documented procedure that consumes frozen MindShift artifacts and produces preserved instrument outputs. It makes an execution reproducible and defines how a later instrument version may be evaluated, calibrated, packaged, retired, or superseded.

It consumes the Issue #64 artifacts unchanged: Observation, Pattern, Candidate Abstraction, Candidate Cognition, optional Construction Evidence, Candidate Evaluation Request, and Research Handoff. Their definitions, ownership, states, and transitions remain exclusively governed by the upstream artifact contract. Referencing one in an execution does not reinterpret, validate, or modify it.

This contract does **not** define research methodology, evidence admissibility, structural theory, deterministic instrumentation, legitimacy, authority, execution eligibility, deployment decisions, or scientific truth. Instrument evaluation records whether this documentation contract behaved clearly and completely; it is not an evaluation of claims in input artifacts.

## Canonical lifecycle

```text
Execute → Observe → Evaluate → Calibrate → Improve → Version → Package → Supersede
   │         │          │           │          │         │         │          │
   │         │          │           │          │         │         │          └─ preserves prior bindings
   │         │          │           │          │         │         └─ readiness determination only
   │         │          │           │          │         └─ assigns a future immutable binding
   │         │          │           │          └─ append-only proposal
   │         │          │           └─ disposition of instrument-behavior evidence
   │         │          └─ assessment of the completed execution
   │         └─ records instrument-behavior observations, including negative ones
   └─ produces a frozen Execution Record from immutable inputs
```

The arrows describe record creation, not an automatic workflow, authorization, or runtime. A lifecycle record may stop at any stage. A new execution always uses an explicitly selected released instrument version; it never silently adopts a calibration or proposal.

## 1. Execution contract

### Execution identity and immutable binding

An **Execution Record** is the authoritative, append-only record of one bounded use of one instrument version. It is complete only when every required field is present or explicitly `Unknown` with an explanation.

| Required field | Requirement |
| --- | --- |
| Execution identity | MindShift-assigned stable identifier, unique within the instrument version. |
| Instrument identity and version | Exact instrument name, semantic version, and immutable document/release reference. |
| Repository revision | Exact repository commit SHA for the instrument binding and the repository URL or identity. A branch name may be context only. |
| Immutable input manifest | Identified Issue #64 artifacts, each with identity, contract version, immutable-at-use reference/version, and transfer terms where applicable. |
| Execution metadata | Custodian, started-at and ended-at timestamps, declared bounded purpose, environment/context description, and all applicable constraints. |
| Procedure binding | Exact procedure/document sections followed and declared deviations. A deviation is evidence, never an unrecorded substitution. |
| Stopping rule and disposition | Predeclared stopping rule, observed stopping condition, and `completed`, `stopped`, or `inconclusive` execution disposition. |
| Preserved outputs | Immutable references to every produced output, including an explicit `None` with reason when no output was produced. |
| Integrity statement | Statement that the record, input manifest, and output references are frozen, plus custodian and freeze timestamp. |

The immutable input manifest is the reproduction boundary. It must identify content-addressed or repository-commit references where those mechanisms exist; otherwise it records the stable source identity, version, custodian, and a reason why a stronger immutable reference is unavailable. A mutable URL, branch name, latest release label, or unversioned artifact title alone is insufficient.

To reproduce an execution, a consumer retrieves the instrument revision and every manifest input, applies the recorded procedure and constraints, and compares newly produced outputs with the preserved outputs. A reproduction may report differences; it must not overwrite the source Execution Record.

### Stopping rules and preserved outputs

Before execution begins, its record declares one or more bounded stopping rules, such as all declared inputs have been processed, a required input is unavailable, an ambiguity prevents faithful procedure application, or the declared time/input boundary is reached. Stopping rules control record closure only; they neither authorize continuation nor decide research outcomes.

Preserved outputs include resulting MindShift artifacts or references, execution notes, unresolved items, deviations, and negative observations about instrument use. Outputs retain their own owners and contracts. The Execution Record links to them and does not absorb or rewrite them.

### Execute and observe diagram

```text
frozen instrument revision + immutable input manifest + declared constraints
                                  │
                                  ▼
                         bounded execution
                          │             │
                          ▼             ▼
               preserved outputs   instrument-behavior observations
                          │             │
                          └──────┬──────┘
                                 ▼
                         frozen Execution Record
```

## 2. Evaluation contract

An **Execution Evaluation** assesses one or more frozen Execution Records for instrument behavior. It identifies evaluator/custodian, evaluation time, scope, source execution identities, and evidence links. It does not decide whether an Observation, Pattern, candidate, request, handoff, or research result is true, sufficient, admissible, or actionable.

| Required dimension | What the evaluation records |
| --- | --- |
| Completeness | Whether required record fields, declared inputs, procedure references, and outputs are present or explicitly unresolved. |
| Traceability | Whether a reader can follow inputs, procedure, deviations, outputs, and evaluation evidence without inferred links. |
| Friction | Steps unnecessarily difficult, costly, repetitive, or unclear to perform. |
| Ambiguity | Competing plausible readings of the instrument or a missing decision boundary. |
| Information loss | Meaning, uncertainty, provenance, limitation, ownership, or identity lost between input, execution record, and output. |
| Unresolved artifacts | Inputs, outputs, links, or questions unavailable, unbound, contradictory, or `Unknown`. |
| Negative observations | Failures, absences, failed attempts, or counterexamples in instrument use, including `None identified` only after inspection. |

Each dimension receives a bounded finding: `observed`, `not observed`, or `unresolved`, with links to preserved evidence and scope limits. “Not observed” means it was not found within the stated evaluation scope; it is not a universal absence claim. Evaluation findings are instrument evidence only.

## 3. Calibration contract

A **Calibration Record** considers evaluation evidence and disposes of a specific **Calibration Candidate**: a proposed change to future instrument behavior or documentation. It never edits an Execution Record, its manifest, or its outputs.

| Required field | Requirement |
| --- | --- |
| Candidate identity | Stable identifier and exact proposed change. |
| Evidence | Links to one or more preserved Execution Records and Execution Evaluations; unsupported preference is insufficient. |
| Affected contract | Exact sections, versions, and consumer-facing behavior affected. |
| Disposition | `accepted`, `rejected`, or `deferred`, with a reason and date. |
| Compatibility and migration | Compatibility statement and consumer migration required if accepted. |
| Promotion target | Proposed future version or `None`; acceptance alone does not change a released version. |

An accepted candidate has evidence that the proposed change addresses a recorded instrument-behavior finding, preserves stated boundaries, and has an explicit compatibility and migration assessment. A rejected candidate records why the evidence or proposal is inadequate. A deferred candidate records unresolved evidence, dependency, or decision boundary and a condition for reconsideration. None of these dispositions alter historical records.

## 4. Improvement contract

An **Improvement Proposal** is the append-only implementation-facing expression of an accepted Calibration Candidate. It includes: stable proposal identity and accepted Calibration Record identity; rationale traced to preserved execution evidence; exact affected contracts, examples, and document sections; proposed wording or behavior for the next version; compatibility statement (`compatible`, `conditionally compatible`, or `breaking`); migration requirements or `none required`; proposed semantic-version change; and supersession relationship to any proposal it replaces.

Proposals are never amended in place. A correction creates a successor proposal that identifies the prior proposal and the reason it is superseded, withdrawn, or narrowed. Acceptance authorizes preparation of a future candidate version only; release occurs through the versioning and packaging contracts below.

## 5. Versioning and compatibility contract

MindShift instruments use semantic versions `MAJOR.MINOR.PATCH`.

| Change | Version change | Compatibility statement |
| --- | --- | --- |
| Clarifies an existing requirement without changing required inputs, outputs, meanings, or reproduction procedure | PATCH | Compatible with executions and consumers of the prior minor version. |
| Adds an optional field, example, or procedure path while preserving all prior required behavior | MINOR | Backward compatible; new capability is optional for prior consumers. |
| Changes/removes a required field, changes an artifact interpretation, changes reproduction procedure, or changes compatibility expectations | MAJOR | Breaking; prior consumers require an explicit migration or retirement statement. |

Every released version includes a compatibility statement, immutable release reference, change summary, links to accepted Improvement Proposals, and a migration guide when conditionally compatible or breaking. Every execution records its exact version and remains governed by that version indefinitely.

**Retirement** means a version is no longer recommended for new executions; it remains retrievable with its documentation and release binding. **Supersession** means a named newer version replaces it for a stated purpose. Neither retirement nor supersession deletes, edits, or invalidates prior executions.

## 6. Packaging-readiness contract

Packaging readiness determines whether a specific instrument version is stable enough for downstream execution. It does not authorize deployment or execution.

| State | Objective determination |
| --- | --- |
| `NOT_READY` | One or more required readiness inputs are missing, mutable, inconsistent, or unresolved. |
| `READY_FOR_FREEZE` | Required documentation, contracts, examples, and readiness evidence are complete and internally consistent; immutable release binding has not yet been made. |
| `FROZEN` | An immutable instrument-version binding, compatibility statement, and preserved readiness record exist. |
| `EXECUTED` | `FROZEN` plus at least one complete frozen Execution Record for the exact version. |
| `CALIBRATED` | `EXECUTED` plus a preserved Execution Evaluation and Calibration Record, including explicit dispositions for identified candidates. |

`FROZEN` applies only to the identified instrument version and its readiness record. It does not establish the repository-level Reference Execution v1.0 boundary, which remains owned by MindShift #52.

To reach `READY_FOR_FREEZE`, the version needs: this execution lifecycle contract and the consumed Issue #64 artifact contract identified by exact version; a complete execution contract and valid execution-record example; evaluation, calibration, improvement, versioning, and supersession contracts; at least one valid and invalid example; compatibility and migration policy; and a readiness record identifying custodian, assessed document/revision set, evidence inspected, unresolved items, and resulting state.

No readiness state is a scientific finding, authority grant, execution-eligibility decision, or deployment decision. A later state records additional evidence; it does not rewrite records at an earlier state.

## 7. Supersession policy

Supersession is a forward link, never a mutation. A superseding version, Execution Record, evaluation, calibration candidate, or proposal names the superseded record, states the relationship and reason, preserves a retrievable reference to it, and states whether reproduction compatibility is preserved.

```text
Execution Record v1 ──evidence──► Evaluation v1 ──► Calibration Candidate
       │                                                      │
       │ remains immutable                                    ▼
       └────────────────────────────────────────► Improvement Proposal
                                                               │
                                       new immutable release ◄─┘
                                                               │
                                                         Execution Record v2
                                                         (new record; not v1 edited)
```

If a historical error is discovered, create a correction or withdrawal record linked to the original record. Preserve the original as created, explain the error's effect on reproduction and interpretation, and bind future execution to the corrected successor where appropriate.

## 8. Examples

### Valid: a reproducible execution

`MS-EXEC-1.0.0-001` binds instrument `MindShift Lifecycle Contract@1.0.0` to repository commit `abc123…`, declares exact Issue #64 artifact identities and immutable-at-use references, records custodian, bounded purpose, timestamps, procedure sections, and stopping rule. It stops because all manifest inputs were processed, preserves output references and an ambiguity note, and is frozen with a timestamp. A later evaluation links that record and notes a missing migration example as a `completeness: observed` finding. This is valid because its execution can be reconstructed without changing its input set.

### Valid: calibrated successor

`MS-CAL-002` links evaluations of two v1.0.0 executions showing consumers read an optional preservation field inconsistently. It accepts a proposal to add a non-normative example, classifies the change as `MINOR` and backward compatible, and creates v1.1.0 as a new immutable release. v1.0.0 executions remain bound to v1.0.0. This is valid because calibration evidence is preserved and improvement is forward-only.

### Invalid: mutable execution binding

An “execution record” says it used the `main` branch and “the latest handoff,” without a commit, artifact version, or input manifest. It is invalid because the instrument and inputs cannot be reproduced.

### Invalid: calibration rewrites history

After learning that a procedure was ambiguous, a custodian edits the completed execution's procedure section and replaces its output link. It is invalid because calibration must produce a linked evaluation and future-version proposal; the completed execution remains frozen.

### Invalid: evaluation decides research truth

An Execution Evaluation marks a Candidate Abstraction “scientifically proven” because its execution record is complete. It is invalid because completeness measures instrument behavior and does not evaluate research claims.

## Consumer obligations

MindShift #33 consumes this lifecycle contract when assembling MindShift Canon v1. MindShift #52 uses the resulting canon and readiness evidence to define the repository-level reference boundary. MindShift #53 then executes the frozen reference run. Continufy records the cross-repository coordination envelope without inheriting MindShift semantics.

Downstream consumers may rely on an exact frozen version only when its immutable binding and compatibility statement are available. They retain execution identity, input references, instrument version, revision, uncertainty, and supersession links. They may create their own records under their own ownership, but must not mutate MindShift records or treat readiness, execution, evaluation, or calibration as authority, truth, or deployment approval.

## Closure evidence

When Issue #40 closes, its closure record must bind:

```text
Terminal outcome: DOCUMENTATION_CONTRACT_COMPLETE
Pull request:
Merged commit:
Default branch containing the contract:
Canonical document path:
README discoverability path:
Immediate downstream consumer: MindShift #33
Further downstream consumers: MindShift #52; MindShift #53; Continufy Reference Execution v1.0
Known limitations:
```

Issue closure proves that this lifecycle contract is merged, canonical, discoverable, and connected downstream. It does not prove that the repository boundary is frozen, that a reference execution occurred, or that any research claim was validated.
