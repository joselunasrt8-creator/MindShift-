# MindShift Issue #81 v2 readiness audit

**Audit date:** 2026-09-13

**Outcome generation:** none

## Historical state

- Main commit `53224ac47d058965280162aa01ef0e6f247104ef` preserves v1 as
  `EXPERIMENT_INVALID` before outcome generation.
- PR #83 was closed unmerged and is not an execution basis.
- `historical-v1-manifest.json` binds all five v1 artifacts so a later mutation
  makes v2 preflight invalid.

## v2 readiness

The task cohort, source commit and hashes, sample size, context constructors,
system instruction, model snapshot and settings, condition-order rule, blinded
evaluation procedure, rubric, aggregation, terminal mapping, stopping rules,
and cost cap are specified prospectively in this directory.

The deterministic machinery proves source identity and exact reconstruction,
prompt identity and exact-once occurrence, absence of evaluator metadata in
generation contexts, constructor reproducibility, and absence of outcome
artifacts. It also refuses to pass unless this entire v2 package is tracked in a
clean Git commit.

## Remaining execution gate

OpenAI provider access is not available in the current Work environment. No
`OPENAI_API_KEY` is present, and the connected Platform account rejected the
secure API-key target lookup. Therefore the provider identity probe has not
passed and no experimental model call is authorized yet.

This is an execution-access block, not an empirical result and not evidence for
or against the MindShift hypothesis. Once an eligible credential is available,
the exact frozen commit must pass `preflight --require-api` before the single run.
