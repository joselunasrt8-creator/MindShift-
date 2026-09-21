# Issue #81 — prospective v2 minimal matched experiment

**Protocol version:** `2.0.0`
**Status:** `PREREGISTERED_NO_OUTCOMES`
**Lineage:** new prospective successor to the unchanged v1 protocol and its
pre-outcome `EXPERIMENT_INVALID` record in `docs/issue-81/`

## 1. Question and boundary

Holding model capability, task, source information, and inference configuration
constant, does source-context organization alone improve output?

The independent variable is exactly `ORDINARY_RAW_V2` versus
`MINDSHIFT_STRUCTURED_V2`. The treatment may change source ordering, grouping,
and provenance/status labels. It may not change source bytes, task text, system
instruction, model, settings, evaluation, or available facts. This is a
repository-specific empirical comparison, not a MindShift runtime or a test of
authority, legitimacy, execution eligibility, production value, or universal
model capability.

## 2. Frozen objects

- `task-set.json` binds four tasks selected before outcomes. There is one paired
  observation per task: four pairs and eight answers total.
- `source-manifest.json` binds source identity, order, Git object bytes, and
  SHA-256 at commit `d31d7630c5c2189dc350626215f2ba0c65b667a0`.
- `construct_and_validate.py` is the executable definition of both constructors
  and the deterministic equivalence preflight.
- Every generation uses the exact system instruction and settings below.
- No empirical output may exist before this protocol is committed. After that
  commit, protocol, manifests, constructors, rubric, formula, sample size, and
  terminal rules are immutable for v2.

## 3. Matched context construction

Both conditions begin with this exact neutral wrapper:

```text
The following repository sources are the complete allowed source information. Use only them. Cite source paths. Treat model output as candidate output, not authority.
```

Both end with the task's exact `prompt`, once, under `--- TASK ---`.

`ORDINARY_RAW_V2` presents each complete source in frozen manifest order under a
`--- SOURCE: <source_id> | <path> | <commit> | <sha256> ---` delimiter.

`MINDSHIFT_STRUCTURED_V2` splits sources only before Markdown ATX headings while
preserving every source byte. It groups segments in this fixed order:

1. `STALE OR SUPERSEDED` — heading contains `supersed`, `retir`, `withdraw`, or
   `stale`;
2. `CONTRADICTIONS` — heading contains `contradict` or `conflict`;
3. `ASSUMPTIONS AND LIMITATIONS` — heading contains `assum`, `unknown`,
   `limitation`, or `uncertain`;
4. `LINEAGE AND PRIOR OBSERVATIONS` — heading contains `prior`, `histor`,
   `lineage`, `observation`, or `evidence`;
5. `SUPPORTED FINDINGS` — heading contains `finding`, `result`, or `evaluation`;
6. `CURRENT STATE` — every remaining segment.

Ties use that priority order. Within a group, manifest source order and original
segment order are retained. Every nonempty segment has a provenance delimiter
containing source ID, path, commit, hash, and byte range. Empty groups contain
only `No source segment classified by the frozen rule.` These labels are
presentation hypotheses, not assertions that their contents are true. There is
no `TASK RELEVANCE` section, task paraphrase, summary, answer hint, evaluator
metadata, or reference answer in either context.

The preflight reconstructs both conditions and must prove for every task: equal
source IDs, identities, hashes, and bytes; each required source appears once;
byte reconstruction is exact with nothing omitted or duplicated; task and
system instruction are byte-identical; the task occurs exactly once in each
complete context; evaluator-only fields do not occur in either context; and all
other frozen controls match. Any failure terminates v2 as
`EXPERIMENT_INVALID`; it must not be repaired after generation begins.

## 4. Provider and generation controls

Before generation, the executor must record from the actual execution surface:
provider, exact model identifier, any exposed model/version or immutable
snapshot, context limit, token accounting support, execution environment and
UTC timestamp. Configuration labels alone are insufficient. If the environment
cannot authenticate an actual provider/model or cannot establish a stable model
identity for all eight calls, execution stops at `PROVIDER_IDENTITY_BLOCKED`.
That is a blocker record, not an empirical terminal determination.

The same verified model serves every request with: temperature `0`, top-p `1`,
one completion, no tools or retrieval, no conversation history, no shared prompt
cache, and a maximum of 2,000 output tokens. If supported, pair seeds are
`810200 + task ordinal`; lack of seed support must be recorded but does not
permit substitution. Pair order is determined by the low bit of
`SHA-256("MS81-V2|<task_id>")`: bit `0` means control first then treatment;
bit `1` means treatment first then control. Requests use fresh sessions. A failed call may be
retried once with identical bytes. Any incomplete pair invalidates v2.

The exact system instruction is:

```text
Answer the user's task using only the provided repository sources. Do not use external knowledge. Preserve uncertainty and distinguish candidate output from authority, permission, legitimacy, execution eligibility, or validated findings.
```

Raw provider responses and provider token/response metadata must be written and
hashed before evaluation. No response may be regenerated because of its
content. No person or evaluator may inspect answers before all eight raw
responses and their hashes are sealed.

## 5. Blinding and frozen evaluation

After sealing, assign each answer an opaque random evaluation ID and place the
condition/pair mapping in a separately hashed key. Evaluators receive task,
sources, bounded reference, rubric, and randomized anonymous answers, but not
condition, pair, request order, filename, or provider response identifiers.

Two blinded human evaluators independently score each answer and lock records
before unblinding. A third blinded evaluator adjudicates when totals differ by
more than 15 points or a count differs by at least 2. Final dimension values are
the medians of available scores. If two independent blinded human evaluators
cannot be established, preserve `EVALUATION_BLOCKED`; do not manufacture scores.

| Dimension | Frozen scale |
| --- | --- |
| Correctness | integer 0–4: materially wrong, mostly wrong, mixed, mostly correct, fully correct within the source boundary |
| Relevant information used | integer 0–4: none, at most 25%, at most 50%, at most 75%, more than 75% of frozen requirements used correctly |
| Critical information omitted | count 0–4, capped |
| Unsupported claims | count 0–4, capped |
| Stale-context errors | count 0–4, capped |
| Contradictions | count 0–4, capped |
| Evaluator preference | anonymous answer A, anonymous answer B, or tie; never style-only |
| Context/token cost | exact UTF-8 context/output bytes and provider-reported input/output tokens |

Per-answer quality is
`clip(12.5*correctness + 12.5*relevant_used - 6.25*(omissions + unsupported + stale + contradictions), 0, 100)`.
Pair effect is treatment minus control. The aggregate effect is the arithmetic
mean of the four pair effects. For evaluator preference, each evaluator casts
one blinded vote per pair: treatment, control, or tie after unblinding the
sealed condition key. If a third evaluator was triggered for that pair, use the
majority of the three votes; otherwise use the two initial votes. A split
treatment/control vote, all-tie vote, or any vote set without a strict majority
is one pair-level tie. Terminal rules count pair-level treatment wins versus
pair-level control wins; tied pairs count for neither arm. Preserve all
dimensions, evaluator votes, pair-level preferences, and per-task effects.

## 6. Frozen terminal rules

Apply in this priority order and emit exactly one terminal determination only
after generation and valid evaluation:

1. `EXPERIMENT_INVALID` for any post-freeze mutation, failed invariant,
   leakage/unblinding, missing provenance or raw output, incomplete pair, or
   inability to compute required measures.
2. `MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED` when aggregate effect is at least
   `+5`, no pair effect is below `-5`, and treatment wins more non-tied blinded
   preferences than control.
3. `MINDSHIFT_CONTEXT_DEGRADED_OUTPUT` when aggregate effect is at most `-5` or
   at least two pair effects are below `-5`.
4. `NO_MEASURABLE_IMPROVEMENT` when every pair effect is strictly between `-5`
   and `+5` and preferences are tied overall.
5. `INDETERMINATE` for every other valid result.

A result supports only this frozen model/task/source/context/evaluation
configuration. Null, degradation, indeterminacy, and invalidity are evidence,
not reasons to change or rerun the experiment.
