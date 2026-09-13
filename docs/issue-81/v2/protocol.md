# MindShift Issue #81 v2 matched context-effect protocol

**Protocol version:** `2.0.0`

**Prospective status:** `FROZEN_BEFORE_OUTCOMES`

**Historical boundary:** `docs/issue-81/` remains the unchanged v1
`EXPERIMENT_INVALID` record. Nothing in this directory amends or reinterprets
v1.

## Research question

Holding the model, task, source information, system instruction, inference
settings, and evaluation procedure constant, does the context organization
defined by `MINDSHIFT_STRUCTURED_V2` improve model output relative to the
competent `ORDINARY_RAW_V2` control?

The independent variable is context organization only.

## Frozen cohort and sample size

The cohort is the four tasks in `task-set.json`. Each task receives three paired
replicates, producing 12 pairs and 24 generation outputs. This small Phase 1
sample is intended to detect a directional, practically material effect across
the frozen tasks. It is not powered for a universal claim and may validly end
`INDETERMINATE`.

The sample size may not change after the first outcome request.

## Frozen sources

`source-manifest.json` binds nine repository artifacts at commit
`d31d7630c5c2189dc350626215f2ba0c65b667a0` by path and SHA-256. For each task,
both conditions receive the exact same listed sources, in the same manifest
order, with every source byte present exactly once. No retrieval, conversation
history, hidden summary, or other repository content is allowed.

## Shared instructions and metadata

The system instruction is byte-identical in both conditions:

```text
Answer the user's task using only the provided repository sources. Do not use external knowledge. Cite source paths for material claims. Preserve uncertainty and distinguish candidate output from authority, permission, legitimacy, execution eligibility, or validated findings.
```

Both user contexts begin with the same allowed-source instruction and the same
provenance block containing source ID, path, source commit, and SHA-256. The
exact task prompt is appended once, and only once, under `--- TASK ---`.

## Control constructor: `ORDINARY_RAW_V2`

After the shared instruction and provenance block, concatenate each complete
source in manifest order with this delimiter:

```text
--- SOURCE: <source-id> | <path> ---
```

No summarization, filtering, annotation, classification, reordering, or task
guidance is permitted.

## Treatment constructor: `MINDSHIFT_STRUCTURED_V2`

After the shared instruction and provenance block:

1. Split each source at Markdown ATX headings while preserving every byte.
2. Classify each segment from its heading only, using the first matching rule:
   - `supersed|retir|withdraw|stale` -> `STALE OR SUPERSEDED`
   - `contradict|conflict` -> `CONTRADICTIONS`
   - `assum|unknown|limitation|uncertain` -> `ASSUMPTIONS`
   - `prior|histor|lineage` -> `PRIOR OBSERVATIONS`
   - `observation|evidence` -> `OBSERVATIONS`
   - `finding|result|evaluation` -> `SUPPORTED FINDINGS`
   - otherwise -> `CURRENT STATE`
3. Emit categories in this exact order:
   `CURRENT STATE`, `OBSERVATIONS`, `PRIOR OBSERVATIONS`,
   `SUPPORTED FINDINGS`, `ASSUMPTIONS`, `CONTRADICTIONS`,
   `STALE OR SUPERSEDED`.
4. Within a category, preserve manifest source order and original segment order.
5. Emit only the fixed category and segment delimiters implemented in
   `experiment.py`; do not add summaries, relevance statements, truth claims,
   answer hints, or empty-category prose.

Category labels are prospective structural syntax. They are not validated truth
labels. The treatment contains no `TASK RELEVANCE` section and never repeats or
paraphrases the task.

## Deterministic preflight

Before the first outcome request, `experiment.py preflight` must prove for every
task:

- repository and source commit identity;
- source ID, path, order, hash, and byte equivalence;
- every source byte occurs exactly once in each condition's source trace;
- no source omission or duplicated segment;
- treatment-only material is limited to the frozen structural syntax;
- byte-identical system instruction;
- byte-identical task prompt occurring exactly once in each condition;
- evaluator-only `information_requirements`, `bounded_reference`, rubric text,
  and terminal rules are absent from generation contexts;
- model and settings are frozen;
- every v2 protocol artifact is tracked and byte-identical to the recorded Git
  commit (an uncommitted package cannot pass);
- the five v1 historical artifacts match `historical-v1-manifest.json`;
- protocol, task, source, model, rubric, terminal-rule, and constructor hashes
  are recorded;
- no v2 raw output, score, effect, determination, or sealed condition-key
  artifact already exists.

Any failed invariant ends the attempted v2 run as `EXPERIMENT_INVALID`. It may
not be repaired after an outcome has been observed.

## Frozen generation model and settings

`model-settings.json` selects `gpt-4.1-mini-2025-04-14` through the OpenAI Chat
Completions API. The dated snapshot is fixed. Temperature is `0`, top-p is `1`,
the maximum output is 1,800 tokens, tools and retrieval are absent, and each
request starts without conversation history. Within a pair the same
prospectively derived seed is used; the seed schedule is recorded in the run
manifest. Provider usage, returned model identity, system fingerprint when
available, HTTP timing, and raw response bytes are preserved.

Provider access is a separate execution gate. A missing credential, unavailable
snapshot, or response that cannot verify the selected model stops before
experimental outcomes are accepted.

## Randomization and custody

Pairs execute in task/replicate order. Condition order within a pair is set by
the low bit of SHA-256 over `MS81-V2|task-id|replicate`. Anonymous evaluation IDs
are generated before scoring. The evaluator receives task, frozen sources,
bounded reference, rubric, and one anonymous output, but no condition, pair,
execution-order, context, or filename information. Pairwise preference receives
two anonymous answers labeled X and Y in lexicographic anonymous-ID order. The condition key
is not used by evaluation requests and is opened only after all scores and
preferences are sealed.

## Frozen rubric

Two blinded model-evaluator passes score every answer independently using the
same dated model snapshot and evaluator settings. A third pass adjudicates when
the first two quality totals differ by more than 15 points or any count
dimension differs by at least 2. This model-as-judge design is a limitation; it
is symmetric across conditions and preserved explicitly rather than treated as
human validation.

| Dimension | Scale | Frozen interpretation |
| --- | --- | --- |
| Factual/task correctness | 0-4 | Wrong to fully correct within supplied sources. |
| Relevant information used | 0-4 | None to more than 75% of frozen requirements used correctly. |
| Critical omissions | 0-4 count | Missing required items, capped at 4. |
| Unsupported claims | 0-4 count | Material claims not entailed by sources, capped at 4. |
| Stale-context errors | 0-4 count | Explicitly stale/superseded material treated as current. |
| Contradictions | 0-4 count | Internal or explicit source contradictions, capped at 4. |
| Uncertainty calibration | 0-4 | Overclaiming to appropriately bounded uncertainty. |
| Decision usefulness | 0-4 | Unusable to directly useful for the frozen task. |

Quality score:

```text
6.25 * (correctness + relevant_used + uncertainty_calibration + decision_usefulness
        - critical_omissions - unsupported_claims - stale_context_errors - contradictions)
```

The score is clipped to `[0, 100]`. The final item score is the median of the
two passes, or of all three when adjudication is triggered. Context UTF-8 bytes,
provider input/output tokens, and latency are reported separately and never
folded into quality.

## Frozen aggregation and terminal mapping

The pair effect is treatment quality minus control quality. Compute each task's
median pair effect and their equally weighted mean. Compute a deterministic
10,000-resample task-stratified paired bootstrap interval using seed `810081`.
Linear-weighted Cohen's kappa on the two initial correctness ratings is the
reliability measure.

Apply these rules in order:

1. `EXPERIMENT_INVALID` if any preflight invariant fails, blinding or custody
   fails, fewer than 11 of 12 complete pairs remain, a required measure is
   missing, or the frozen protocol changes after outcomes begin.
2. `INDETERMINATE` if correctness kappa is below `0.40`, or the 95% interval
   spans both `-5` and `+5`.
3. `MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED` if the interval lower bound is at
   least `+5`, no task median is below `-5`, treatment wins more non-tied blinded
   pair preferences, and treatment does not increase aggregate unsupported plus
   stale errors.
4. `MINDSHIFT_CONTEXT_DEGRADED_OUTPUT` if the interval upper bound is at most
   `-5`, or at least two task medians are below `-5`.
5. `NO_MEASURABLE_IMPROVEMENT` for every other valid, determinate result.

Exactly one terminal determination is allowed. Negative, tied, degraded, null,
indeterminate, and invalid results are valid evidence.

## Stopping rules

Stop immediately before further calls on any preflight failure, credential or
model-identity failure, source/context mismatch, evaluator leakage, outcome-aware
mutation, or evidence overwrite attempt. Retry a transient API failure twice
with identical request bytes. More than one incomplete pair invalidates the
experiment. Do not expand tasks, replicates, models, rubric, or thresholds after
observing any outcome.

## Claim boundary

A supported result applies only to this frozen repository commit, task/source
cohort, context constructors, model snapshot, settings, and scoring procedure.
It does not establish general model improvement, cross-model transfer,
production readiness, economic value, authority, permission, legitimacy, or
execution eligibility.
