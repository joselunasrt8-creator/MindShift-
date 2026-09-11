# Issue #81 execution preparation record

**Record status:** `MODEL_REQUIREMENTS_UNSATISFIED`

**Empirical outputs generated:** none

**Recorded repository commit/tree before this implementation:**
`7cb679b8e1de8f27df6cad661c2b43673221d9ba` /
`8a445bd8b5792e705dd4bb5dd7a370a352db42cf`

This record describes infrastructure preparation only. It is not an outcome,
permission to execute, or evidence that MindShift improves candidate cognition.
The static implementation and its synthetic tests are ready, but this checkout
does not provide an independently verified eligible provider/model snapshot.
Consequently the complete empirical preflight cannot honestly emit
`EXPERIMENT_EXECUTION_READY` in this run.

## Frozen inputs verified

The authoritative inputs remain byte-for-byte unchanged from the corrected
preregistration commit:

| Artifact | SHA-256 |
| --- | --- |
| `protocol.md` | `ca183c0110c8e699271d099ab976d446927d39eeea323910d025d2eb0f64b58a` |
| `task-set.json` | `c39c99ff73c3ebde8a7ebd25d4bf475c28041536b7965164422aaec6c8d889b8` |
| `source-manifest.json` | `39b096402b2f3675cc7f2b0a86439dab96b578a4d2326d686c83ddd32c5386b4` |
| `validate_protocol.py` | `26cf50c1c3bc1d8d5eadf304daa553c0874e03ab48e79f745dfec6755b4e719a` |

The source identity is commit
`d31d7630c5c2189dc350626215f2ba0c65b667a0`; each of the nine source hashes is
read from the frozen source manifest and checked against bytes obtained with
`git show`. The task identities are `MS81-T01` through `MS81-T04`. No reserved
Issue #81 output, result, or determination path was present. Git history shows
no post-freeze mutation of the four authoritative artifacts.

## Prepared machinery

`execution.py` is an opt-in, Python-standard-library-only CLI. It provides:

- exact `ORDINARY_RAW_V1` source ordering, delimiters, unedited bytes, and task;
- deterministic `MINDSHIFT_STRUCTURED_V1` heading segmentation, frozen lexical
  classification and category ordering, authorized labels/provenance, and no
  evaluator-only metadata;
- reconstruction proof over every source byte, ordered IDs and hashes, and the
  identical task prompt;
- a write-once run manifest containing repository/frozen identities,
  constructor hash, model and generation controls, ordering, environment,
  per-context hashes, and preflight results;
- a later JSON-stdin/JSON-stdout provider-adapter harness with fresh independent
  requests, deterministic paired ordering/seeds, two explicit attempts, and
  exact provider-response bytes plus accounting-bearing provider JSON;
- randomized evaluation IDs, evaluator-visible files without condition/pair/
  order metadata, and a separately sealed read-only condition key;
- the normalized quality formula, adjudication trigger, pair/task aggregation,
  enumerated paired bootstrap interval, and frozen-priority terminal decision;
- rejection of synthetic fixtures at the empirical custody boundary.

The generation CLI is intentionally not invoked by validation or preflight.
Raw evidence paths use exclusive creation and read-only modes; an existing path
fails rather than overwriting evidence.

## Final preflight gate

An executor must supply a JSON model record with all of the following, verified
before manifest creation: `provider`, exact dated `snapshot`,
`immutable_snapshot`, `temperature_control`, `seed_control`, `token_accounting`,
`context_window_tokens`, and `tokenizer`. Boolean capability fields must be
true. The context-window check uses the complete UTF-8 byte length plus the
2,000-token output allowance as a deliberately conservative fail-closed bound.
No model may be substituted after the manifest is created.

Example (placeholder values are not eligible evidence):

```console
python3 docs/issue-81/execution.py preflight \
  --model /custodian/verified-model.json \
  --executor '<custodian/environment identity>' \
  --timestamp '<pre-generation UTC timestamp>' \
  --output /custodian/immutable-run-manifest.json
```

Only an independently verified eligible record may cause that command to emit
`EXPERIMENT_EXECUTION_READY`. Until then, the bounded state is:

`MODEL_REQUIREMENTS_UNSATISFIED`
