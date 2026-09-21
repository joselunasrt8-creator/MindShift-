# Issue #81 v2 execution record

**Experiment identity:** `MS81-V2-2026-09-21-MINIMAL-MATCHED`
**Frozen protocol commit:** `91cb3907c3ac2f219e9885c8277db94f63db16e9`
**Execution environment:** Codex Cloud, Linux workspace, UTC
**Preflight:** `PASS`
**Generation status:** `NOT_STARTED`
**Paired observations:** `0 of 4`
**Run status:** `PROVIDER_IDENTITY_BLOCKED`
**Empirical terminal determination:** `NOT_ASSIGNED`

## Audit and lineage

The checked-out history was audited before mutation. Commit `7cb679b` added the
five v1 preregistration artifacts associated locally with PR #82. Commit
`53224ac` added the v1 pre-outcome invalid record after detecting that the
treatment presented the task twice. The v1 record also says closed PR #83 was
not present in its Git object database. No local Git object, ref, remote, or
artifact identifies the contents of PRs #84 or #85. The checkout has no remote,
GitHub CLI is unauthenticated, and hosted GitHub/API access returned an
environmental authorization/network failure, so hosted issue comments and PR
diffs could not be independently recovered. This is an audit limitation, not a
claim that those hosted objects do not exist.

The complete current Issue #81 requirements supplied to this execution were
treated as the governing issue text. Repository-wide path and content searches
found the v1 protocol, task/source manifests, validator, and invalid execution
record, but no empirical Issue #81 model response, score, blind key, or result.
The v1 artifacts remain byte-identical to the pre-v2 Git blobs and are neither
repaired nor used as effectiveness evidence.

V2 has separate identity, versioned paths, and lineage. An initial hosted freeze
was reviewed before any model generation. PR review found three prospective
specification defects: one task did not follow frozen manifest source order,
the request-order hash bit lacked an explicit arm mapping, and evaluator
preference aggregation/tie handling was underspecified. Because zero model
calls and zero outcome inspections had occurred, those defects were corrected
prospectively rather than treated as outcome-aware mutation.

The corrected protocol, task set, source manifest, and constructor are frozen at
commit `91cb3907c3ac2f219e9885c8277db94f63db16e9`. The evidence validator binds
their exact Git blob identities at that commit and rejects any later mutation.
The deterministic preflight was regenerated only after this corrected freeze
and made zero model calls.

## Deterministic equivalence preflight

`preflight.json` was regenerated after the corrected freeze by the frozen constructor. All
four pairs pass. For every task it records identical source IDs, source
identities, hashes, and bytes; exact reconstruction with no omission or
duplication; byte-identical task and fixed controls; exactly one task occurrence
per arm; and no constructor access to evaluator-only metadata. It also seals
each prospective context hash and byte cost. The system instruction hash is
`ca1c2c29f0c5602ddc4e46420e28184826460d95a533e5cd6ef9c9f8b097d6fe`.
The only intentional context difference is source organization and its frozen
generic structure/provenance labels.

The preflight made zero model calls. No v2 output existed before the freeze or
was generated while checking equivalence.

## Provider/model verification and stop boundary

The host execution surface is identified as Codex Cloud, and this interactive
assistant identifies itself as an OpenAI GPT-5.6 Sol model. That interaction is
not an eligible experiment mechanism: the environment exposes no exact serving
snapshot/version, request API, authenticated provider credential, controllable
fresh-session batch interface, token-accounting response, or way to attest that
the frozen temperature, top-p, output cap, cache, and seed settings govern eight
independent calls. `OPENAI_BASE_URL` exists, but no `OPENAI_API_KEY`, Anthropic
key, or Google key is present; no `codex`/`openai` executable or corresponding
Python provider package is installed. A configuration/environment name was not
treated as provider proof.

Consequently, the actual model/provider identity required by the frozen
protocol cannot be established for experimental generation in this environment.
No substitute model was selected, no request was sent, no raw response was
created, and no output was inspected. The run stops at:

```text
PROVIDER_IDENTITY_BLOCKED
```

This is not one of the five empirical terminal determinations and must not be
reported as one. In particular, it is not `EXPERIMENT_INVALID`: the frozen v2
design passed preflight, but the external execution prerequisite is absent.
Issue #81 is therefore not closed by this change.

## Remaining requirement

Resume this exact frozen v2—without changing its files—only in an environment
that can record and use one actual provider/model identity for all eight calls,
enforce or accurately report every frozen setting, preserve response metadata
and raw bytes, and provide two independent blinded human evaluators. Execution
must then preserve four complete pairs, output provenance, blind identities,
locked scores, per-task effects, and exactly one frozen terminal determination.

## Limitations and non-claims

- The original Codex execution could not retrieve hosted Issue #81/PR state. Later hosted review recovered that state and identified prospective protocol defects; they were corrected and re-frozen before any model output.
- No claim is made about immutable snapshot availability outside this workspace.
- Zero empirical observations means no effect, null effect, degradation, or
  indeterminacy is inferred.
- Even a later positive v2 result would apply only to its frozen configuration;
  it would not establish universal improvement, capability gain, production or
  economic value, authority, legitimacy, permission, or execution eligibility.
