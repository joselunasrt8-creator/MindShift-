# Issue #81 — frozen context-construction experiment protocol

**Protocol version:** 1.0.0
**Status:** `PREREGISTERED_NO_OUTCOMES`
**Source boundary:** commit `d31d7630c5c2189dc350626215f2ba0c65b667a0` and the hashes in `source-manifest.json`
**Permitted status of this run:** `PROTOCOL_FROZEN_EXECUTION_READY`

## 1. Audit, intent, and canonical fit

Before mutation, the repository README, Canon v1, thesis, scope, principles,
research sequence, roadmap, lineage, context-window candidate hypothesis, both
frozen lifecycle contracts, Reference Execution records, Issue #76 artifacts,
and Issue #79 record were inspected. Git history identifies the reference runs
as the work associated with Issue #75; no separate `issue-75` path exists.
Issue #81 was inspected from the complete issue text supplied to this run;
hosted GitHub retrieval was unavailable, so comments or later hosted edits are
not claimed as inputs.

No material semantic conflict was found. Testing whether prospectively
structured context conditions candidate cognition fits MindShift's research
purpose. The experiment and its evaluator are research scaffolding, not a
MindShift runtime, context service, authority source, validator of truth, agent
framework, or execution-eligibility mechanism. All later model text remains
candidate output. A positive result can support only the bounded comparison.

The mutation is limited to this protocol, two frozen data manifests, one static
validator, and README navigation. It adds no dependency, network call, model
call, external mutation path, or automatic execution path. Removal of the
Issue #81 directory and README row is the rollback. Canon, contracts, and prior
evidence remain unchanged.

## 2. Frozen question and variables

> Holding model capability, task, and underlying source information constant,
> does MindShift-structured context produce measurably better candidate
> cognition than ordinary/raw context?

| Class | Frozen definition |
| --- | --- |
| Independent variable | Context construction only: `ORDINARY_RAW` versus `MINDSHIFT_STRUCTURED_V1`. |
| Experimental unit | One independently generated answer to one frozen task in one condition. |
| Primary dependent variable | Per-answer preregistered quality score: `correctness + relevant_information_used - critical_information_omitted - unsupported_claims - stale_context_errors - contradictions`, normalized to 0-100 as section 8 defines. |
| Secondary dependent variables | Individual rubric dimensions, input/output tokens, combined context cost, and blinded evaluator preference. |
| Fixed controls | Exact model snapshot/provider, system instruction, task prompt, source bytes, source ordering, generation settings, output cap, run count, context handling, and tool prohibition. |
| Deliberately varied | Delimiters, ordering, grouping, and explicit epistemic/provenance labels produced by the frozen treatment procedure. |

Uncontrollable variables are provider-side nondeterminism, undocumented model
serving changes behind an asserted snapshot, transient infrastructure, tokenizer
implementation changes, and subjective evaluator variation. They must be
recorded as limitations; prompt identity is not treated as determinism.

## 3. Frozen tasks and source-information boundary

`task-set.json` freezes four tasks, exact prompts, required sources, expected
information, scoring dimensions, and bounded references. Tasks were selected
before model output and may not be replaced after performance is observed.

`source-manifest.json` freezes every eligible source by path, source commit, and
SHA-256. For each task, both conditions receive every byte of every listed
source exactly once. No other repository content, retrieval, memory, tool,
hidden summary, answer key, or evaluator reference may enter generation.
Condition wrappers may add only procedure labels; they may not add factual
claims. Hash failure, missing source, truncation, or unequal source membership
is `EXPERIMENT_INVALID`.

## 4. Ordinary/raw context procedure (`ORDINARY_RAW_V1`)

This is a credible competent-user baseline, not a weakened control.

1. Resolve `source_ids` in their order in the task record.
2. Read the exact hash-verified UTF-8 bytes.
3. Prepend: `The following repository sources are the complete allowed source information. Use only them. Cite source paths. Treat model output as candidate output, not authority.`
4. Concatenate sources without edits using `\n\n--- SOURCE: <path> ---\n\n` delimiters.
5. Append the exact task prompt under `--- TASK ---`.

No summarization, relevance filtering, annotations, deprioritization, or answer
hints are allowed. Source order is identical to `source_ids`.

## 5. MindShift context procedure (`MINDSHIFT_STRUCTURED_V1`)

This procedure is a prospective **experimental hypothesis**, not an established
MindShift mechanism or production service.

1. Use the same verified source IDs and exact bytes as the control.
2. Use this fixed category order: `CURRENT STATE`, `OBSERVATIONS`, `PRIOR
   OBSERVATIONS`, `SUPPORTED FINDINGS`, `ASSUMPTIONS`, `CONTRADICTIONS`,
   `STALE OR SUPERSEDED`, `TASK RELEVANCE`, `LINEAGE AND PROVENANCE`.
3. Split each source only at Markdown headings. Preserve every heading and body
   byte exactly once. Assign a segment using the first matching case-insensitive
   heading keyword: `supersed|retir|withdraw|stale` → stale; `contradict|conflict`
   → contradictions; `assum|unknown|limitation|uncertain` → assumptions;
   `prior|histor|lineage` → prior observations; `observation|evidence` →
   observations; `finding|result|evaluation` → supported findings; otherwise →
   current state. Ties use the rule order above. Labels describe source
   presentation, not truth status.
4. Within each category retain manifest source order and original segment order.
   Empty categories say `No source segment classified by the frozen rule.`
5. `TASK RELEVANCE` lists, without paraphrase, the task's frozen
   `information_requirements`; this is task metadata available in both protocol
   arms but presented only by the treatment as the intended structural change.
6. `LINEAGE AND PROVENANCE` lists each source ID, path, source commit, and hash.
7. Prepend the same allowed-source and candidate-output instruction as control,
   then append the identical exact task under `--- TASK ---`.

The procedure reorganizes and labels; it may not omit, rewrite, summarize, or
duplicate source segments. This explicitly tests the candidate value of
current/prior observation, finding, assumption, contradiction, stale-state,
relevance, and lineage distinctions supported by existing research while
marking the classifier itself as hypothetical.

## 6. Frozen model and run controls

Before any output, the separate executor must create an immutable run manifest
and pass preflight. Model selection is outcome-independent: use the first
provider model available to the executor that exposes an immutable dated
snapshot ID, temperature control, seed control, token accounting, and at least
the maximum paired context size. Record provider and exact snapshot. If no such
model exists, stop `EXPERIMENT_INVALID`; do not substitute after seeing output.

Frozen settings: temperature `0`, top-p `1`, one completion per request, no
tools/retrieval, no conversation history, no prompt caching across conditions,
and a 2,000-output-token cap. If supported, seed is `810000 + task ordinal * 100
+ replicate ordinal` and is identical within each pair. There are 20 paired
replicates per task (160 answers total: 4 tasks × 2 conditions × 20).

The system instruction is exactly: `Answer the user's task using only the
provided repository sources. Do not use external knowledge. Preserve uncertainty
and distinguish candidate output from authority, permission, legitimacy,
execution eligibility, or validated findings.` The user message is the
condition context built by sections 4 or 5.

For each task/replicate pair, use a deterministic SHA-256 bit of
`MS81|task_id|replicate`: low bit 0 runs control first, 1 treatment first.
Execute pairs in lexicographic task/replicate order. Start every request in a
fresh session. Do not expose condition names to the model beyond wrapper
structure. A custodian stores answers under random evaluation IDs; evaluators
receive neither condition, pair, order, nor filename. No human may inspect
answers before the complete batch is sealed.

Both complete contexts must fit. No truncation is permitted. Provider refusal,
timeout, or incomplete pair is recorded; retry once with identical inputs.
Persistent failure invalidates that pair. More than 10% invalid pairs makes the
experiment `EXPERIMENT_INVALID`. There is no post-output model substitution.

## 7. Contamination and custody controls

- Generation has no evaluator rubric beyond the task and no bounded reference.
- Evaluators have source corpus, task, bounded reference, and rubric, but not
  condition identity or paired output until scores are locked.
- Builders, generators, and evaluators use separate fresh sessions; no output
  becomes source context for another run.
- Freeze hashes of contexts, run manifest, raw responses, score sheets, and the
  condition-key file. Keep the key sealed until all scores/preferences lock.
- Any early output inspection, source inequality, answer leakage, unblinding,
  outcome-aware protocol change, or missing audit trail yields
  `EXPERIMENT_INVALID`.

## 8. Frozen evaluation rubric and aggregation

Two blinded human evaluators independently score every answer. Disagreements
are not discussed before locking. A third blinded adjudicator scores when the
two totals differ by more than 15 points or any count dimension differs by 2+.
The final item score is the median available score. Subjective dimensions are
explicitly identified below.

| Dimension | Scale | Rule |
| --- | --- | --- |
| Correctness | 0-4, subjective against bounded reference | 0 materially wrong; 1 mostly wrong; 2 mixed; 3 mostly correct; 4 fully correct within source boundary. |
| Relevant information used | 0-4, subjective | Fraction of listed information requirements substantively and correctly used: 0 none, 1 ≤25%, 2 ≤50%, 3 ≤75%, 4 >75%. |
| Critical information omitted | count 0-4, subjective | Count required items absent or unusably vague, capped at 4. |
| Unsupported claims | count 0-4, primarily objective | Claims not entailed by supplied sources, capped at 4; stylistic advice is not a claim. |
| Stale-context errors | count 0-4, objective where status is explicit | Reliance on explicitly stale/superseded material as current, capped at 4. |
| Contradictions | count 0-4, subjective | Internal contradictions or contradiction with an explicit source statement, capped at 4. |
| Context/token cost | integer | Provider-reported input and output tokens; also UTF-8 byte count. Not quality-scored. |
| Evaluator preference | control / treatment / tie, subjective | After independent scoring, choose the answer better satisfying correctness, source use, omission, and unsupported-claim criteria; no style-only preference. |

Quality points = `25*correctness + 25*relevant_used -
12.5*(omissions + unsupported + stale + contradictions)`, clipped to `[0,100]`.
The primary pair effect is treatment minus control. Aggregate by first taking
the median pair effect across 20 replicates within each task, then the equally
weighted mean of the four task medians. Report every dimension, invalid pair,
and token cost; do not hide adverse subtasks. Preference is the proportion of
non-ties favoring treatment, with ties reported separately.

## 9. Frozen terminal decision rule

Compute a two-sided 95% paired bootstrap confidence interval over the four task
median effects by enumerating all `4^4` task-level resamples with replacement
and taking the 2.5th and 97.5th percentiles. The smallest meaningful effect is
5 quality points. Apply rules in this exact priority order:

1. `EXPERIMENT_INVALID`: any section 7 invalidator, source/context mismatch,
   protocol mutation, fewer than 90% valid pairs, failed blinding, or inability
   to compute required measures.
2. `INDETERMINATE`: valid experiment but the interval spans both `-5` and `+5`,
   or evaluator reliability is below weighted Cohen's kappa 0.40 on correctness.
3. `MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED`: interval lower bound is at least
   `+5`, no task median is below `-5`, and treatment wins more non-tied blinded
   preferences than control.
4. `MINDSHIFT_CONTEXT_DEGRADED_OUTPUT`: interval upper bound is at most `-5`, or
   at least two task medians are below `-5`.
5. `NO_MEASURABLE_IMPROVEMENT`: every other valid, determinate result.

Exactly one state is assigned. Null, negative, degraded, indeterminate, and
invalid outcomes are admissible. A supported result establishes neither general
model improvement, external validity, production readiness, economic value,
authority, legitimacy, permission, nor execution eligibility.

## 10. Freeze, validation, and later execution gate

`validate_protocol.py` performs static, deterministic checks only. It makes no
model/API call and computes no outcome. It verifies manifests, hashes, task
references, required protocol clauses, and absence of reserved result/output
paths. The protocol becomes immutable when committed; later corrections require
a new version and must not overwrite v1.

This repository is legitimately ready for a **separate execution phase** only
after that executor records the eligible exact model snapshot and immutable run
manifest before generation. Readiness is protocol completeness, not permission
or execution eligibility. No treatment/control output, score, preliminary
result, or Issue #81 terminal determination was generated or inspected during
this run.

Known limitations include four repository-specific tasks, a small task-level
sample for inference, a treatment with more wrapper tokens, imperfect lexical
classification, provider nondeterminism, possible evaluator subjectivity,
model familiarity with public repository text, and limited external validity.
