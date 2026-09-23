# Issue #81 Phase 1 execution record

**Experiment identity:** `MS81-PHASE1-2026-09-11-PREFLIGHT`
**Protocol:** `docs/issue-81/protocol.md` version 1.0.0 at commit
`7cb679b8e1de8f27df6cad661c2b43673221d9ba`
**Execution timestamp:** 2026-09-11 UTC
**Terminal determination:** `EXPERIMENT_INVALID`
**Outcome-generation status:** `NOT_STARTED`

## Audit boundary

The audit used the checked-out `main` snapshot represented by commit
`7cb679b8e1de8f27df6cad661c2b43673221d9ba`, the refined Issue #81 text supplied
to the executor, and the five preregistration artifacts merged by PR #82. The
checked-out tree contains no Issue #81 empirical outputs, results, determination,
or condition-key artifact. The frozen source objects remain available at commit
`d31d7630c5c2189dc350626215f2ba0c65b667a0`, and every source hash passes
`validate_protocol.py`. The corrected primary score remains:

```text
12.5*correctness + 12.5*relevant_used
- 6.25*(omissions + unsupported + stale + contradictions)
```

Hosted GitHub retrieval was unavailable in the execution environment. Therefore,
the audit could not independently retrieve later hosted edits/comments or the
closed PR #83 diff. No PR #83 implementation was present in the checked-out Git
object database, and none was inherited. The relevant confound identified in
the supplied refined issue—treatment-only task guidance or duplicate task
presentation—was instead checked directly against the frozen protocol.

## Frozen-material usability

The four frozen tasks resolve to unique task IDs and to source IDs present in
the source manifest. All nine manifest entries resolve at the frozen source
commit and match their recorded SHA-256 values. No existing empirical output
was found under `docs/issue-81/` or elsewhere in the tracked tree. These checks
would have permitted context construction but do not override the failed
equivalence invariant below.

## Required equivalence preflight

The refined Issue #81 requires the exact task prompt to occur exactly once in
each condition before the first real model call. The frozen control procedure
appends the exact prompt once under `--- TASK ---`. The frozen treatment
procedure requires both:

1. the exact task prompt in `TASK RELEVANCE`, prefixed by `Task focus:`; and
2. the identical exact task appended again under `--- TASK ---`.

Consequently, applying the frozen procedures gives the following deterministic
result for every task:

| Task | Control exact-prompt occurrences | Treatment exact-prompt occurrences | Result |
| --- | ---: | ---: | --- |
| `MS81-T01` | 1 | 2 | FAIL |
| `MS81-T02` | 1 | 2 | FAIL |
| `MS81-T03` | 1 | 2 | FAIL |
| `MS81-T04` | 1 | 2 | FAIL |

Source-ID membership, frozen source hashes, and the score normalization pass,
but prompt multiplicity fails. This also means the condition difference is not
limited to structural reorganization: the treatment repeats task guidance that
the control receives once.

The frozen protocol also specifies 20 paired replicates for each of four tasks
(80 pairs, 160 answers). The refined issue permits avoiding that scale only
when the frozen protocol does not strictly require it; here the protocol does
strictly require it. No smaller sample was silently substituted.

## Stop decision and preserved evidence

The failure was identified before context sealing, model selection, or any real
model call. Repairing the treatment after this discovery would retrospectively
change the frozen protocol, so this run stops rather than amending or bypassing
it.

- Model/provider/version: not selected.
- Generation parameters and context limit: not applicable; no generation.
- Tasks: four audited, zero executed.
- Paired observations: zero.
- Control/treatment contexts: not materialized.
- Raw-output artifact identities: none.
- Blind IDs and condition mapping: none.
- Scoring records and per-task paired effects: none.
- Aggregate effect: not computable.
- Cross-model replication issue: not justified because Phase 1 did not execute.

This record preserves a pre-outcome invalidation, not empirical evidence of
improvement, null effect, or degradation. A future experiment would require a
new prospective protocol version whose construction passes the exact-once
invariant before any outcomes are generated; version 1.0.0 remains unchanged.

```text
EXPERIMENT_INVALID
```
