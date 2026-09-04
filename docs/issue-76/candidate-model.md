# Candidate Model for Repository Agent Legibility

**Artifact identity:** `MS-76-CANDIDATE-001`
**Artifact role:** Issue-specific Candidate Abstraction and Candidate Cognition
**Owner:** MindShift
**Package status:** `candidate-ready-for-empirical-handoff` (not a frozen-contract lifecycle state)
**Source observations:** [`MS-76-OBSERVATIONS-001`](source-observations.md)
**Repository binding:** `joselunasrt8-creator/MindShift-` at starting commit
`b48ea9933547217357b6e22cac7d33fbc1d63711` and tree
`87f0ab5de3c613a02d9da78144873fa62155341b`

## 1. Exact candidate abstraction

> A repository may be more agent-legible when a small, revision-bound context
> record makes its purpose, admissible transformations, evidence obligations,
> failure behavior, and authority boundary explicit. The record is navigation
> context only: it proposes how to interpret and route work, while the consumer
> independently checks current repository evidence and retains every decision.

This is the smallest coherent abstraction because it describes the context an
agent would need to avoid category and boundary errors without implementing a
router, tool, permission system, or execution surface. “Skill” below names the
hypothesized context representation; it does not mean capability, authority, or
a validated contract.

## 2. Candidate representation

### Minimum viable fields

| Field | Semantics | Why minimum |
| --- | --- | --- |
| `representation_identity` | Stable identifier for this candidate record. | Enables lineage and explicit replacement. |
| `repository_identity` | Unambiguous repository owner/name or equivalent immutable identity. | Prevents applying context to an unintended repository. |
| `repository_revision` | Exact commit and, when available, tree/content digest inspected to form the record. | Makes freshness and contradiction checks possible; a branch or `latest` is insufficient. |
| `purpose_and_scope` | Bounded repository purpose, included concerns, and exclusions. | Establishes what the record may describe. |
| `inputs_transformations_outputs` | Accepted input object types, candidate transformations, and produced object types, including explicit unsupported cases. | Supplies the smallest useful navigation map without granting execution. |
| `invariants_and_prohibitions` | Distinctions that must survive and actions the representation cannot recommend or perform. | Makes boundary violations falsifiable. |
| `context_and_evidence` | Required source paths/contracts, provenance standard, assumptions, uncertainties, and contradiction links. | Distinguishes documented claims from verified current behavior. |
| `failure_completion_semantics` | Named success/candidate states plus `NULL`, `BLOCKED`, ambiguity, and escalation behavior. | Prevents forced answers and false completion. |
| `authority_boundary` | Explicit statement of who retains permission, acceptance, eligibility, and mutation decisions. | Prevents navigation context from becoming authority. |

The fields may be grouped differently in a tested presentation, but none of
these semantics may disappear from the minimum candidate. In particular,
repository identity without revision binding is not a valid minimum.

### Optional fields

| Field | Include when | Reason optional |
| --- | --- | --- |
| `owned_object_types` | Ownership is evidenced and materially disambiguates routing. | Often derivable from scope and I/O; external ownership may be unresolved. |
| `upstream_relationships` / `downstream_relationships` | Exact, current relationships are evidenced. | Topology can overlap and change; omission is safer than invented routing. |
| `handoff_preconditions` | The repository produces handoff candidates. | Not every repository participates in a staged handoff. |
| `compatibility_window` | Maintainers have defined compatible revisions/contracts. | A window cannot be inferred from semantic version labels alone. |
| `examples` / `reference_executions` | Experiments test their incremental effect and cargo-cult risk. | Examples can bias agents and are not proof of a general contract. |
| `human_contact_or_escalation_target` | A maintained target exists. | `Unknown` plus fail-closed behavior is valid when none exists. |
| `supersedes` / `revoked_by` | A successor or revocation record exists. | These are lifecycle links, not baseline content. |

### Unresolved representation alternatives

1. One Markdown context record per repository.
2. Ordinary canonical docs plus a short index, with no “skill” artifact.
3. A shared ontology with only identity, revision, and local deltas per
   repository.
4. One Continufy-level context record with repository-specific sections.
5. Capability- or object-type specialization rather than repository
   specialization.

No machine-readable schema is added. MindShift's native candidate and handoff
artifacts are Markdown, and deterministic schema validation would establish
only syntactic conformance while prematurely fixing unresolved field grouping.

### Smallest candidate instance: MindShift

This instance demonstrates that the minimum fields can represent one repository
without becoming an installed skill. It is the candidate test input, not a
validated account of all behavior at later revisions.

| Minimum field | Candidate value at the bound revision |
| --- | --- |
| `representation_identity` | `MS-76-MIN-REP-001` |
| `repository_identity` | `joselunasrt8-creator/MindShift-` |
| `repository_revision` | Commit `b48ea9933547217357b6e22cac7d33fbc1d63711`; tree `87f0ab5de3c613a02d9da78144873fa62155341b` |
| `purpose_and_scope` | Context and cognition-governance research: study observations becoming transferable abstractions that improve future modeling; excludes runtime, structural analysis, authority, legitimacy, eligibility, proof, governed mutation, replay, and repository governance. |
| `inputs_transformations_outputs` | Encountered accounts and provenance → record Observations → propose linked Patterns → derive Candidate Abstractions → compose Candidate Cognition → prepare Candidate Evaluation Requests and Research Handoffs. Outputs remain candidates. Unsupported or insufficiently evidenced transformation → `NULL` or `BLOCKED`. |
| `invariants_and_prohibitions` | Preserve artifact identity, ownership, immediate inputs, uncertainty, limitations, contradictions, and version binding. Do not infer unknowns, validate truth, authorize action, determine eligibility, mutate external systems, or silently rewrite history. |
| `context_and_evidence` | Read `README.md`, `docs/canon-v1.md`, `docs/thesis.md`, `docs/scope.md`, and the two frozen lifecycle contracts at the bound revision. Link substantive claims to immediate inputs; record absent evidence as `Unknown`. |
| `failure_completion_semantics` | Produce a traceable candidate or explicit `NULL`/`BLOCKED`/`AMBIGUOUS`. Completeness is documentary and traceability-bounded, never scientific validation or acceptance. |
| `authority_boundary` | MindShift governs only its records. The agent, producer, and representation cannot grant permission, execution eligibility, external ownership, acceptance, or deployment. A consumer evaluates every handoff independently. |

## 3. Placement distinctions

| Information class | Proper surface | Examples | Boundary |
| --- | --- | --- | --- |
| Ordinary explanation | Repository documentation | mission, architecture narrative, tutorials, maintainer guidance | May orient; does not prove implementation behavior. |
| Candidate repository context (“skill”) | Small revision-bound navigation record | purpose/scope, object flow, evidence paths, uncertainty, prohibitions, failure semantics | Proposal for empirical comparison; not installed or authoritative. |
| Implementation contract | Code/API/schema/test surface owned by the implementing repository | type definitions, accepted parameters, deterministic validation, runtime errors | Must be verified against the exact implementation; this package creates none. |
| Governance-sensitive information | Separately authorized governance mechanism | permissions, required routing, acceptance authority, execution eligibility, policy enforcement, persistent behavior-changing defaults | Must not be inferred from a skill or created by this package. |

Persistence becomes governance-sensitive when the record automatically changes
agent selection, tool access, write eligibility, approval, routing, default
behavior, or acceptance. Descriptions of owners and consumers also become
sensitive if treated as exclusive or controlling rather than evidenced
candidates.

## 4. Preserved invariants and completion semantics

```text
Skill ≠ authority
Instruction ≠ permission
Capability ≠ execution eligibility
Repository ownership ≠ cross-repository authority
Handoff proposal ≠ accepted handoff
Agent navigation ≠ autonomous execution
Documentation ≠ validated skill contract
Persistence ≠ legitimacy
Schema-valid candidate model ≠ empirically validated repository-skill architecture
AI output remains a proposal
```

Candidate navigation outcomes are:

- `CANDIDATE_OUTPUT`: a bounded, provenance-linked proposal was produced;
- `NULL`: evidence does not support the transformation or no unique result can
  be formed without invention;
- `BLOCKED`: a named prerequisite prevents evaluation;
- `AMBIGUOUS`: multiple supported interpretations or consumers remain; return
  candidates and escalate rather than choose invisibly.

“Complete” means the candidate record is traceable and its declared output or
failure state is present. It never means accepted, true, executable, deployed,
or authorized.

## 5. Candidate repository topology

The following is an evaluated hypothesis, not a canonical pipeline or ownership
assignment for external repositories.

| Repository/surface | Candidate local transformation | Evidence status and ambiguity |
| --- | --- | --- |
| MindShift | observations → patterns/models → candidate abstractions → research handoffs | Locally supported, although Issue #76's shorthand omits Pattern and Candidate Cognition stages present in canon. |
| architecturalboundary-research | research question → preregistration → execution → evidence → bounded determination | Supplied as a candidate; external authoritative contracts were not admitted. Could overlap MindShift at question framing and handoff. |
| Methodology-Engineering | candidate transformation → methodology contract → validation/promotion | Supplied as a candidate. “Validation” must not be confused with MindShift record validation; promotion ownership needs external evidence. |
| Structology / structural-analysis-foundations | structural concepts → formal structural knowledge | Naming and division are ambiguous; objects may be shared with SYNAPSE and Methodology Engineering. |
| SYNAPSE | bounded system input → deterministic structural analysis/evidence | MindShift explicitly lacks authority to specify SYNAPSE semantics. “Evidence” ownership/admissibility is unresolved. |
| ContinuityOS | intent candidate → legitimacy structure → execution eligibility or `NULL` | Candidate only. MindShift cannot create legitimacy, permission, or eligibility. |
| StateGate | repository transition proposal → `VALID | NULL | PROOF` | Candidate only. Meaning of `VALID` and `PROOF`, relationship to ContinuityOS, and authority are unresolved. |

### Overlaps, missing stages, and routing ambiguity

- Research-question framing may belong to both MindShift handoff preparation and
  ABR preregistration; custody and ownership must remain artifact-specific.
- “Candidate transformation” may be a MindShift abstraction, a methodology
  input, or both by reference. Reference does not duplicate ownership.
- Structural concepts can legitimately be observations, candidate
  abstractions, methodology subjects, and formal objects in different records.
- “Evidence” spans provenance, construction evidence, instrument evidence,
  empirical research evidence, and structural proof; the unqualified term is
  not routable.
- The proposed topology omits intake/admission, custody acknowledgement,
  rejection/return, version negotiation, correction/supersession, and
  conflicting-owner resolution.
- StateGate and ContinuityOS appear to overlap around transition validity,
  proof, legitimacy, and eligibility. No deterministic ordering is justified.
- Structology versus `structural-analysis-foundations` may be an alias,
  relationship, or separate ownership boundary; it remains `Unknown`.
- A task spanning methods, structural concepts, and execution evidence may
  legitimately have multiple consumers. Split artifacts or human coordination
  may be superior to a unique route.
- Repository boundaries are poor specialization units when a capability spans
  repositories, a monorepo has unrelated domains, or versioned contracts—not
  repositories—are the stable unit.

Accordingly, unsupported routes return `NULL`; multiple evidence-supported
consumers return `AMBIGUOUS`; missing required external specifications return
`BLOCKED`. The model never guesses a single consumer.

## 6. Cross-repository handoff candidate

```text
producer artifact
      ↓
producer checks only its own handoff preconditions
      ↓
handoff proposal (non-authorizing)
      ↓
consumer independently evaluates current evidence and compatibility
      ↓
ACCEPT | REJECT | NULL | BLOCKED
```

### Minimum handoff fields

| Field | Required meaning |
| --- | --- |
| `handoff_identity` | Stable identity and proposal state. |
| `source_repository` | Exact producer repository identity. |
| `source_revision` | Commit plus tree/digest where available. |
| `artifact_identity_type_reference` | Stable artifact ID, type, and immutable-at-proposal reference. |
| `evidence_and_provenance` | Linked sources, construction lineage, uncertainties, contradictions, and limitations. |
| `proposed_consumer` | One named candidate consumer or explicit `AMBIGUOUS` with candidates. |
| `requested_transformation` | Bounded non-presupposing request; never an instruction or result. |
| `constraints_and_non_authority` | Applicable exclusions, prohibited interpretations, custody/ownership, and authority boundary. |
| `compatibility_and_freshness` | Expected consumer contract/version if known and result of source freshness check. |
| `unresolved_limitations` | Explicit `Unknown`, missing prerequisites, alternatives, and escalation need. |

### Evaluation rules

- Invalid: missing identity/revision/artifact binding, mutable-only source,
  untraceable evidence, concealed contradiction, unsupported requested
  transformation, presumed acceptance, or producer-granted consumer authority.
- Ambiguous consumer: record candidate consumers and return `NULL` or
  `BLOCKED` under the producer vocabulary; do not broadcast or select silently.
- Unsupported route: return `NULL` with the unsupported relationship; do not
  invent an adapter or reinterpret the artifact.
- Rejection: consumer creates its own immutable `REJECT` record with rationale;
  rejection does not mutate or invalidate the producer artifact.
- Version incompatibility: consumer returns `BLOCKED` or `REJECT` with exact
  versions and required migration; producer cannot waive consumer constraints.
- Stale source: no acceptance evaluation proceeds until the consumer records a
  compatible current binding or requests a successor. A stale proposal remains
  historical evidence, not a current instruction.
- `ACCEPT`: acknowledges custody and only the specifically requested evaluation
  under consumer-owned rules. It is not support for the candidate claim.
- `NULL`: consumer cannot form the requested result without unsupported
  assumptions. `BLOCKED`: a stated prerequisite could permit later evaluation.

## 7. Staleness, contradiction, and versioning

**Candidate invariant:** A behavior-changing repository representation should
remain traceable to the repository state, contracts, and governance artifacts
it claims to represent.

The safest candidate is fail-closed:

1. Bind representation version, repository commit/tree, source artifact
   versions/digests, and inspected paths.
2. Before use, compare the current target identity and revision with that
   binding and inspect declared supersession/revocation links.
3. If equal, freshness is only `revision-matched`, not behavior validated.
4. If different, use only when an explicit compatibility record covers the
   changed revision and relevant sources; otherwise classify `STALE` and stop.
5. If current implementation, docs, contracts, or governance artifacts
   contradict the record, preserve both references, classify `CONTRADICTED`,
   and stop affected guidance even when the commit matches.
6. Correction, withdrawal, revocation, and supersession create forward records;
   history remains retrievable. Revocation prevents new use but does not erase
   prior use.

Semantic versions may name representation changes but cannot prove repository
compatibility. Compatibility windows must enumerate covered repository and
contract versions plus reviewed change classes. A repository revision change
does not automatically preserve validity. Current documentation is not, by
itself, a validated representation of current behavior. Automated drift
detection is a possible future test subject, not implemented here.

## 8. Alternatives and unresolved questions

Serious alternatives retained for comparison are:

- ordinary repository documentation is sufficient;
- one Continufy-level system context performs better;
- a shared ontology plus thin repository metadata performs better;
- maintenance and staleness cost exceeds any performance benefit;
- capability, object type, contract, or task stage is a better unit than a
  repository;
- agents route effectively without specialized context;
- specialization suppresses useful exploration;
- reference examples produce cargo-cult behavior;
- human routing remains necessary; and
- topology overlaps make deterministic routing unsound.

Unresolved questions include which field presentation is smallest in practice,
whether repository identity adds value after current docs are supplied, what
latency/maintenance budget is acceptable, who publishes compatibility records,
and whether `AMBIGUOUS` should be distinct from `NULL` in every consumer.

## 9. Negative and counterexample cases

1. A polished skill bound to `main` claims it is current: invalid mutable
   binding.
2. A correct scope summary tells an agent to merge: boundary violation;
   instruction is not permission.
3. Producer marks a handoff accepted: invalid; only the consumer can accept.
4. A schema passes while behavior has changed: syntactic success, stale model.
5. Documentation and code disagree: contradiction must be exposed, not resolved
   in favor of documentation.
6. One object is owned at different lifecycle stages by several repositories:
   unique routing is not justified; identity and custody are stage-specific.
7. No consumer supports the requested transformation: `NULL`, not best-effort
   cross-repository execution.
8. Two consumers plausibly support it: `AMBIGUOUS` and escalation, not arbitrary
   selection.
9. An example improves imitation but increases boundary violations: evidence
   against including examples, even if task completion rises.
10. A repository changes only unrelated files: compatibility might be
    supportable, but must be recorded rather than assumed.

## 10. Explicit non-promotions

This candidate does **not**:

- validate repository-specialized agent skills;
- make “repository skill” a canonical MindShift artifact;
- authorize deployment, installation, routing, tool use, or mutation anywhere;
- define canonical cross-repository architecture or repository ownership;
- accept a handoff on behalf of ABR #131 or any consumer;
- modify governance, permissions, execution eligibility, or downstream rules;
- implement a compiler, router, plugin, loader, validator, or authority engine;
- establish that examples, schemas, persistent context, or automated drift
  detection are desirable; or
- use ABR #130 or #131 conclusions as premises.

## 11. Bounded determination

The candidate is explicit, alternatives and ambiguity are preserved, handoff
and staleness semantics are testable, and no implementation or authority is
created. Its legitimate state is:

`CANDIDATE_MODEL_READY_FOR_EMPIRICAL_HANDOFF`

This state describes package readiness only. It is not empirical support,
validation, downstream acceptance, or permission to deploy.
