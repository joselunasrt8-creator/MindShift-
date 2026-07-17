# Contributing to MindShift

MindShift is a research framework for studying how observations become
transferable abstractions that improve future modeling.

Before contributing, read [`CLAUDE.md`](CLAUDE.md), [`docs/thesis.md`](docs/thesis.md),
and [`docs/scope.md`](docs/scope.md).

## In Scope

- Observations that reveal recurring patterns.
- Abstractions or distinctions that transfer across contexts.
- Worked examples that improve future modeling.
- Clarifications that preserve the canonical identity, question, and sequence.

## Out of Scope

- Runtime behavior.
- Infrastructure claims.
- Execution or agent capability.
- Authority, approval, legitimacy, execution eligibility, execution boundaries,
  proof, governed mutation, replay, or reconciliation.
- Schemas, services, packages, or machine objects for primitives.

## Decision Filter

Before proposing any change, run it through the
[thesis](docs/thesis.md) decision filter:

> Does this strengthen the study of how observations become transferable
> abstractions that improve future modeling?

If the change does not directly support the canonical identity, question, or
research sequence, it does not belong here.

## Useful Review Questions

1. What observation is being studied?
2. What pattern was identified?
3. What abstraction emerged?
4. What primitive or distinction transfers?
5. How does it improve future modeling?

## Canonical Terminology Review

For changes that affect canonical terminology, perform this bounded manual
review:

1. Compare the proposed text with [`docs/thesis.md`](docs/thesis.md), which is
   the canonical reference for terminology.
2. Identify every intentional wording difference from the thesis.
3. Check the affected summaries in [`README.md`](README.md),
   [`CLAUDE.md`](CLAUDE.md), and [`docs/scope.md`](docs/scope.md) for consistency.
4. In the pull request, record the paths reviewed and any accepted divergence,
   including why the differing wording is appropriate. If there is no accepted
   divergence, state that explicitly.

This is a static, human review procedure. Do not treat it as an executable
validator or expand it into repository-wide validation.

## How to Contribute

1. Create a topic branch for your change.
2. Keep changes focused and clearly described.
3. Confirm the change passes the decision filter above.
4. Update the Repository Map in [`README.md`](README.md) when adding, removing,
   or renaming documents.
5. Open a pull request explaining the change and how it supports the canonical
   research identity.
