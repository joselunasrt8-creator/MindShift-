# InstrumentRunRecord Contract

**Contract version:** 1.0.0  
**Status:** Proposed Layer 2 measurement contract  
**Owner:** MindShift

## Purpose

InstrumentRunRecord captures what was observed during one prospective instrument run. It is non-authoritative instrument-behavior evidence. It does not validate research claims, establish legitimacy, grant authority, grant permission, or determine execution eligibility.

It complements, and does not replace, the frozen [Instrument Execution Lifecycle Contract](../instrument-execution-lifecycle-contract.md). The lifecycle contract's authoritative Execution Record, Execution Evaluation, and Calibration Record retain their existing meanings and ownership.

## Record binding

Every record binds the exact instrument runner commit, repository revision where available, input manifest and item digests, environment/tool state, timestamps, observed dispositions, resource observations, and evidence artifact digests. A mutable branch name is context only; it is not an immutable identity.

Unknown values remain null where the schema permits null and must have a corresponding entry in `unknowns` with a subject path and non-empty reason. Collectors must not infer provider identity, credentials, remote refs, timing, or other unavailable facts.

## Status and disposition

`run_status` describes operational or preflight state. Its vocabulary includes blocker states such as `PROVIDER_IDENTITY_BLOCKED`, `ASSESSMENT_BLOCKED`, `EXPERIMENT_INVALID`, and `BLOCKED_BY_REPOSITORY_PERMISSIONS`, along with preflight/run terminal states.

`execution_disposition` is separate and uses only the lifecycle disposition vocabulary: `completed`, `stopped`, `inconclusive`, or null when execution did not reach a disposition.

A status token must not be translated into an execution disposition by inference.

## Expected and observed

The `expected` and `observed` objects remain separate. Observed discrepancies are recorded explicitly. Collection must not smooth, normalize, or rewrite a difference to match expectation.

## Evidence and integrity

Each evidence item references a preserved path, SHA-256 digest, and kind. A companion provenance manifest binds the record file's digest; it is not embedded into or used to mutate the record. Canonical JSON bytes are:

```python
(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
```

The companion manifest may contain the record path and SHA-256 digest. Its own digest may be calculated over the manifest object excluding its `manifest_hash` field, following the repository's established canonical-JSON pattern.

## Frozen-history boundary

This contract applies prospectively. It must not retrofit records for historical runs, modify frozen Issue #79, #81, or #91 artifacts, or change the schemas under `docs/issue-91/schemas/`.

## Interpretation boundary

A valid InstrumentRunRecord establishes only that a record conforms to this measurement contract and preserves declared observations and references. It does not establish scientific validity, reproducibility of a research claim, or instrument effectiveness. Those require separately scoped evaluation and evidence.
