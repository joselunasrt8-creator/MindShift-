# Observation to Research Handoff Contract

**Contract version:** 1.0.0 (frozen)
**Status:** Canonical
**Owner:** MindShift

## Purpose and boundary

This contract defines the canonical MindShift artifacts from an incoming
observation to its handoff to a separately owned research methodology. It is a
reusable documentation contract, not a schema, runtime, instrumentation
standard, research method, or decision process.

It governs candidate formation and handoff only. It does not validate a claim,
select research methodology, establish structural theory, prescribe deterministic
instrumentation, authorize execution, confer legitimacy, or decide deployment.
Research evaluation begins only after MindShift produces a Candidate Evaluation
Request.

## Canonical terminology

| Term | Meaning | Is not |
| --- | --- | --- |
| **Observation** | A bounded account of something encountered, collected, reported, generated, or illustrated before model compression. | A verified fact or conclusion. |
| **Pattern** | A proposed recurring relationship across identified observations. | A causal law or validated finding. |
| **Candidate Abstraction** | A proposed compression of patterns that preserves stated distinctions for a stated scope. | A universal theory or validated model. |
| **Candidate Cognition** | A coherent, traceable candidate understanding assembled for a bounded inquiry. | A decision, authority, or research result. |
| **Construction Evidence** | Optional record of how a candidate artifact was assembled or transformed. | Research evidence or validation. |
| **Candidate Evaluation Request** | A bounded question and proposed evaluation inputs for research. | An evaluation or instruction to reach a result. |
| **Research Handoff** | A transfer record identifying the request, recipient, terms, and preserved uncertainty. | A transfer of truth, authority, or a favorable conclusion. |

The words **candidate**, **proposed**, and **unknown** are material. Consumers
must retain them whenever omission would imply validation or certainty.

## Common artifact rules

Every artifact has a stable MindShift-assigned identity, a contract version, one
owner, a created-at time, a lifecycle state, and explicit links to its immediate
inputs. An identity is a stable reference, not a claim of global,
deterministic, or cryptographic identity. Missing required information is
`Unknown` with an explanation; it is never inferred.

A reference neither copies ownership nor establishes evidentiary support. A
successor may link to a predecessor but must not rewrite it.

## Artifact definitions and required metadata

### 1. Observation

An Observation is the smallest accountable contract input: an account of a
phenomenon before MindShift proposes a relationship or compression.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and state. |
| Content | Bounded description of what is observed, reported, generated, or illustrated. |
| Source class | `Empirical`, `Reported`, `Synthetic`, or `Illustrative`. |
| Provenance | Source/origin, context, collection or construction method, temporal scope, and observer or custodian. |
| Confidence | Calibrated qualitative judgment or reasoned range, with its basis. |
| Limitations | Known provenance gaps, selection or measurement limits, and construction assumptions. |
| Contradictory evidence | Known conflicts, or `None identified`. |

Source class describes the observation's relation to the phenomenon; it is not a
quality score. Synthetic and illustrative observations do not independently
establish real-world occurrence, and reported observations are not direct
observation. Confidence concerns the recorded account, not a later claim.

### 2. Pattern

A Pattern is a proposed recurring relationship across at least two identified
Observations. It retains links to each observation and states the comparison
boundary and why observations are treated as meaningfully distinct or dependent.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and state. |
| Observation links | Identities of all contributing observations; no unlinked evidence. |
| Relationship and recurrence | Proposed relationship, recurrence boundary, and cases/times/settings where it appears or does not appear. |
| Supporting evidence | Traceable account of which observations support the relationship and how. |
| Uncertainty | Dependence, sampling limits, confounders, alternatives, variation, and confidence with basis. |
| Limitations | Conditions under which recurrence is unknown or inapplicable. |

A one-off account, a summary without observation links, or a relationship with no
recurrence boundary is not a Pattern.

### 3. Candidate Abstraction

A Candidate Abstraction is a proposed compression of linked Patterns that may be
reasoned about beyond their originating cases. It names both preserved
distinctions and intentionally omitted detail.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and state. |
| Derivation | Source Pattern identities and a concise account of the compression. |
| Content | Candidate abstraction and preserved distinctions. |
| Assumptions | Interpretive, contextual, and omission assumptions. |
| Scope | Intended contexts, boundary conditions, and exclusions. |
| Failure conditions | Conditions, observations, or alternatives that make it inapplicable, incomplete, or misleading. |
| Uncertainty | Inherited and compression-introduced uncertainty, competing abstractions, and confidence with basis. |

Conciseness does not make an abstraction a primitive, theory, or reusable truth.
Primitive extraction and transfer remain in the separate
[canonical research sequence](research-sequence.md).

### 4. Candidate Cognition

Candidate Cognition is a bounded, traceable candidate understanding of an
inquiry. It composes one or more Observations, zero or more Patterns, and one or
more Candidate Abstractions into an account of what research may evaluate. It is
not a person, agent, runtime object, execution plan, or conclusion.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and maturity state. |
| Inquiry and content | Bounded inquiry, current candidate understanding, and unresolved questions. |
| Composition | Constituent artifact identities; an absent layer is `None` with a reason. |
| Traceability | A readable path from each substantive statement to constituent artifacts or `Unknown`. |
| Assumptions and limits | Carried-forward assumptions, scope, failure conditions, contradictions, and uncertainty. |
| Maturity rationale | Why the recorded state is appropriate. |

Its descriptive maturity states never imply validity:

```text
assembled → framed → evaluation-requested → handed-off → superseded | retired
```

- **assembled:** constituents are collected but understanding is not yet bounded.
- **framed:** inquiry, composition, assumptions, and limits are explicit.
- **evaluation-requested:** a Candidate Evaluation Request exists.
- **handed-off:** its request has a Research Handoff record.
- **superseded** or **retired:** a later cognition replaces it, or work stops;
  history remains traceable.

### 5. Optional Construction Evidence

Construction Evidence exists only when a contributor needs to show how a
candidate artifact was assembled, transformed, selected, or summarized. It may
record intermediate comparisons, source selection, or transformations. It is
optional because linked source artifacts can themselves provide sufficient
traceability.

Required metadata is: identity and MindShift ownership; concerned artifact
identities; construction activity, actor/custodian, and time; inputs and
outputs; transformation limits; and known omissions. It demonstrates construction
provenance, not correctness. It never validates a claim by itself, even if the
construction is complete, repeatable, or persuasive.

### 6. Candidate Evaluation Request

A Candidate Evaluation Request is the only MindShift artifact that can initiate
research evaluation. It translates a Candidate Cognition into a bounded request
without selecting or directing research methodology.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and state. |
| Source cognition | Exactly one Candidate Cognition in `framed` or later state. |
| Research question | One bounded, answerable question that does not presuppose its answer. |
| Candidate claims | Claims or alternatives to evaluate, each explicitly marked candidate. |
| Assumptions and uncertainty | Inherited/request-specific assumptions, limits, contradictions, and unknowns. |
| Proposed evidence | Relevant artifact links and suggested evidence gaps; never a sufficiency finding. |
| Expected outputs | Requested research deliverables, such as a disposition, reasoning, limitations, and unresolved questions. |
| Recipient constraints | Known context, timing, confidentiality, or format constraints, or `Unknown`. |

The request must not prescribe methodology, assert an evidence threshold is met,
require a validating outcome, or authorize action based on an outcome.

### 7. Research Handoff

A Research Handoff is a MindShift-owned transfer record created only after a
Candidate Evaluation Request is ready. The transferred artifact is exactly one
identified Candidate Evaluation Request plus the linked context needed to
preserve its stated meaning.

| Required metadata | Requirement |
| --- | --- |
| Identity and ownership | Stable identity, contract version, MindShift owner, and state. |
| Transferred artifact | Identity and immutable-at-transfer reference/version of one Candidate Evaluation Request. |
| Recipient | Named receiving research methodology, team, or repository; `Unknown` only for an undelivered prepared record. |
| Custody transfer | Sender, recipient, time, transfer terms, and acknowledgement status. |
| Preserved uncertainty | Request assumptions, confidence, limitations, contradictory evidence, and unknowns, without reduction. |
| Boundary notice | Transfer does not validate claims or confer authority, legitimacy, execution, or deployment rights. |

MindShift owns the handoff record and its source artifacts. On delivery, custody
of the request copy passes to the named receiving research owner; that owner
owns its methodology, evaluation work, and newly created research outputs. Thus
each artifact has one owner: MindShift owns its source and handoff records, and
the receiver owns only new artifacts it creates. Custody is not ownership of the
MindShift source record.

## Lifecycle and transition contract

```text
Observation(s)
  → Pattern(s)
  → Candidate Abstraction(s)
  → Candidate Cognition
  → Candidate Evaluation Request
  → Research Handoff
  → [separately owned research methodology]

Optional Construction Evidence ──────→ may link to any candidate artifact
```

| Transition | Required input | MindShift output | Rule |
| --- | --- | --- | --- |
| Record observation | Encountered account and available provenance | Observation | Preserve unknowns; classify source. |
| Construct pattern | Two or more linked Observations | Pattern | State relationship, recurrence, support, and uncertainty. |
| Derive abstraction | One or more linked Patterns | Candidate Abstraction | State compression, assumptions, scope, and failure conditions. |
| Compose cognition | Linked artifacts sufficient to bound an inquiry | Candidate Cognition | Preserve traceability; do not form conclusions. |
| Request evaluation | One framed Candidate Cognition | Candidate Evaluation Request | State non-presupposing question, candidates, proposed evidence, and outputs. |
| Hand off | One ready Candidate Evaluation Request | Research Handoff | Transfer identified request with all uncertainty and boundaries intact. |

Construction Evidence can be linked during construction, but neither changes an
artifact's state nor satisfies a transition by itself. Research evaluation is
outside the MindShift lifecycle and starts only after the request is produced.

## Ownership and consumer contract

MindShift owns Observation, Pattern, Candidate Abstraction, Candidate Cognition,
optional Construction Evidence, Candidate Evaluation Request, and Research
Handoff artifacts it creates. It owns their definitions, traceability, stated
limits, and handoff boundary notice.

MindShift does not own research methodology, claim validation, structural theory,
deterministic instrumentation, execution authority, legitimacy, deployment
decisions, or downstream research output. No contract artifact can imply those
excluded responsibilities: a Pattern is not a validated finding, Candidate
Cognition is not a decision, Construction Evidence is not research evidence, a
Candidate Evaluation Request is not an evaluation, and a Research Handoff is not
authorization.

A downstream consumer receives the handoff, request, and linked context allowed
by transfer terms. It consumes the contract without redefining it by retaining
identities, source classes, assumptions, limitations, confidence bases,
contradictions, and `Unknown` values. It may add methodology-specific artifacts
under its own ownership, but must not relabel candidates as validated or overwrite
MindShift source artifacts.

If a research output is later supplied to MindShift, it enters as a new
Observation (normally a Reported Observation) with its own provenance and limits;
it does not retroactively validate or mutate the handoff source.

## Examples

### Valid

Two empirical observations from different team retrospectives record action items
without named owners. A Pattern links them and says, “Unowned retrospective
actions recur in these two teams during Q1; broader recurrence is unknown.” A
Candidate Abstraction proposes that a learning ritual needs explicit closure,
lists limited scope, and retains the possible shared-facilitator confounder.
Candidate Cognition frames the inquiry. Its request asks what relationship, if
any, exists between closure mechanisms and repeated unresolved action items in
comparable settings, and requests a documented disposition and limitations.

This is valid because provenance, candidates, uncertainty, and the boundary
between request and evaluation remain explicit.

### Invalid

“A repeatable prompt produced the same abstraction three times, so the
abstraction is validated and should be deployed.”

This is invalid: repeatable construction can be Construction Evidence, but it
does not validate an abstraction, grant deployment authority, or replace a
Candidate Evaluation Request and separately owned research work.

“Send these notes to research and approve implementation if they agree.”

This is invalid: unlinked notes are not a Candidate Evaluation Request, the
research question and uncertainty are absent, and a handoff cannot grant
implementation authority.

## Freeze and compatibility

Version 1.0.0 freezes the terminology, required metadata, ownership boundaries,
and transition rules in this document. Additive examples may be introduced only
when they do not redefine a term, required field, transition, or ownership rule.
Any semantic change requires a new contract version and an explicit compatibility
statement for downstream consumers.
