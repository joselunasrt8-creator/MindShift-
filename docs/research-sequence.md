# Canonical Research Sequence

MindShift studies one sequence:

```text
Observation
→ Pattern
→ Abstraction
→ Primitive
→ Transfer
```

This is a research sequence. It is not a runtime, execution loop, computational
lifecycle, agent architecture, or governance process.

## Evidence Predicates

An evidence predicate is the research judgment that must be satisfied before a
transition is treated as supported. These predicates are prompts for explicit,
falsifiable reasoning, not schemas, machine objects, scoring rules, or execution
requirements. Evidence can be qualitative or quantitative, but its source,
context, and limits must be available for examination.

### Observation → Pattern

The transition is supported when a candidate relationship recurs across
sufficiently independent observations, relevant variation has been considered,
and recurrence is more credible than a case-specific or measurement explanation.

- **Required inputs:** The observations; their sources, contexts, and collection
  conditions; the candidate recurring relationship; and a stated account of
  which observations are meaningfully independent.
- **Admissible evidence:** Repeated occurrences across cases, times, observers,
  or settings; consistent qualitative traces; quantitative associations with
  appropriate denominators; and deliberate searches for comparable cases where
  the relationship is absent.
- **Disconfirming evidence:** Non-recurrence in comparable observations;
  dependence on one source, selection rule, or measurement artifact; contradictory
  cases under the same stated conditions; or a simpler case-specific explanation.
- **Uncertainty handling:** Record sampling limits, dependence among observations,
  plausible confounders, and the observed variation. State confidence as a
  reasoned range or calibrated qualitative judgment rather than converting an
  unknown into a claim of recurrence.
- **Must remain provisional when:** Independence is unclear, relevant negative
  cases have not been sought, the recurrence boundary is unspecified, or the
  available observations cannot distinguish the candidate relationship from a
  plausible artifact or alternative explanation.

### Pattern → Abstraction

The transition is supported when a candidate abstraction compresses the pattern
without discarding distinctions needed to explain it and yields expectations that
can be examined beyond the cases used to form it.

- **Required inputs:** The supported or provisional pattern; the observations
  from which it was inferred; a candidate abstraction; its intended scope and
  boundary conditions; and at least one competing compression or explanation.
- **Admissible evidence:** The abstraction accounts for both recurring and
  divergent cases with fewer case-specific assumptions; preserves causally or
  descriptively relevant distinctions; produces testable expectations; and
  remains useful on held-out observations or reasoned counterexamples.
- **Disconfirming evidence:** The abstraction merely renames the pattern, depends
  on details it claims to omit, loses exceptions that determine outcomes, makes
  no discriminating expectations, or is outperformed by a simpler competing
  account.
- **Uncertainty handling:** Separate uncertainty inherited from the pattern from
  uncertainty introduced by the compression. Document unresolved alternatives,
  scope sensitivity, and which omitted details might change the abstraction's
  conclusions.
- **Must remain provisional when:** No competing account or counterexample has
  been considered, boundary conditions are unknown, the abstraction has only
  been assessed on its source cases, or its useful compression depends on an
  unresolved interpretation of the pattern.

### Abstraction → Primitive

The transition is supported when a minimal distinction or mechanism can be
isolated from the abstraction, retains the abstraction's relevant explanatory
work, and can be stated independently of the originating case without claiming
unbounded universality.

- **Required inputs:** The candidate abstraction; its scope, boundary conditions,
  and explanatory commitments; the proposed primitive; examples and
  counterexamples; and plausible decompositions or simpler alternatives.
- **Admissible evidence:** Removing or altering the proposed primitive predictably
  weakens the abstraction; the same distinction or mechanism can be recognized
  in materially different representations or contexts; it preserves relevant
  contrasts; and further reduction would lose explanatory or modeling value.
- **Disconfirming evidence:** The proposed primitive bundles separable ideas,
  cannot be identified without source-case vocabulary, adds no value beyond the
  full abstraction, changes meaning across examples, or can be reduced further
  without loss.
- **Uncertainty handling:** State which aspects appear necessary, sufficient,
  neither, or still unknown. Track dependence on representation, granularity,
  and context, and retain rival candidate primitives when the evidence does not
  discriminate among them.
- **Must remain provisional when:** Minimality has not been challenged, necessity
  or explanatory contribution is unresolved, recognition outside the source
  representation is untested, or the primitive's boundary conditions remain
  unspecified.

### Primitive → Transfer

The transition is supported when use of the primitive in a meaningfully different
target context improves future modeling against a stated comparison and the
improvement survives examination for leakage, hindsight, and context-specific
advantages.

- **Required inputs:** The primitive and its claimed boundaries; a target context
  not used to derive it; the modeling task; a pre-stated expectation of what
  improvement would look like; a comparison or baseline; and observed outcomes.
- **Admissible evidence:** Prospective or held-out application improves prediction,
  explanation, decision framing, error detection, or learning efficiency relative
  to the comparison; the path from primitive to improvement is traceable; and
  replications span contexts that differ on features the primitive claims to
  ignore.
- **Disconfirming evidence:** No improvement or degradation against the baseline;
  benefit only after outcome-aware reinterpretation; failure in contexts within
  the claimed scope; reliance on source-case information unavailable in the
  target context; or equal benefit from a simpler, context-specific heuristic.
- **Uncertainty handling:** Report variation across targets, comparison quality,
  outcome-measure limits, negative results, and possible leakage. Narrow the
  transfer claim to the contexts supported rather than treating mixed evidence as
  universal success or failure.
- **Must remain provisional when:** Evaluation is retrospective only, target and
  source contexts are not meaningfully distinct, no credible comparison exists,
  improvement criteria were chosen after outcomes were known, replication is
  absent, or plausible leakage and alternative explanations remain unresolved.

## Observation

An observation names what is seen in reality before it is compressed into a
model. Useful observations attend to anomalies, friction, recurrence, and context.

### Observation methodology

Classify each observation before using it as evidence. The class describes how
the observation relates to the phenomenon; it does not rank the observation or
remove the need to examine its provenance.

- **Empirical:** Directly collected from an event, behavior, measurement, or
  artifact in the world through a stated observation or measurement process.
- **Reported:** Received through another person's account, testimony, summary,
  or documentation rather than observed directly by the researcher.
- **Synthetic:** Produced by a model, simulation, generated dataset, or other
  constructed process. Its evidentiary value depends on the assumptions and
  inputs of that process, not on independent contact with the world.
- **Illustrative:** Invented or simplified to explain, explore, or challenge an
  idea. It can clarify reasoning but is not evidence that the depicted event or
  relationship occurs in reality.

Every observation must carry a minimum accompanying record:

- **Source class:** Empirical, reported, synthetic, or illustrative.
- **Observation context:** The setting, population, system, or circumstances in
  which the observation arose.
- **Collection method:** How the observation was obtained, selected, measured,
  reported, generated, or constructed.
- **Temporal scope:** When it was collected or generated and the period it
  describes.
- **Observer or custodian:** The person or organization that observed, generated,
  reported, or currently maintains the source record.
- **Known limitations:** Provenance gaps, selection effects, measurement limits,
  construction assumptions, or other constraints on interpretation.
- **Contradictory evidence:** Known observations or accounts that conflict with
  the observation, or an explicit statement that none has yet been identified.
- **Confidence:** A calibrated qualitative judgment or reasoned range, with the
  basis for that judgment.

Missing information must be marked as unknown rather than inferred. Classification
does not convert synthetic or illustrative material into empirical evidence, and
reported observations should not be presented as direct observations.

## Pattern

A pattern is a recurring relationship across observations. A pattern matters when
it appears beyond a single case and suggests a structure that can be studied.

## Abstraction

An abstraction compresses a pattern into a form that can be reasoned about beyond
the original observation.

## Primitive

A primitive is an abstraction reduced to a reusable distinction or mechanism. In
Phase 1, MindShift does not elevate primitives into machine objects, schemas, or
runtime artifacts.

## Transfer

Transfer is the test. An abstraction or primitive is useful when it improves
future modeling outside the case that produced it.
