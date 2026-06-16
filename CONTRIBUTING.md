# Contributing to MindShift

MindShift is an independent, open-source cognition infrastructure project.
Contributions are welcome when they strengthen the project's focus: learning,
adaptation, validation, pattern recognition, recursive improvement, and reflexive
intelligence.

Before contributing, read [`CLAUDE.md`](CLAUDE.md) and [`docs/scope.md`](docs/scope.md).

## Principles for Contributions

Contributions should embody the same principles the project studies:

- **Reality First** — Claims remain subordinate to reality. Prefer ideas that can
  be tested and revised over ideas that merely sound complete.
- **Feedback Creates Learning** — Make the reasoning and its feedback loops
  explicit so others can engage with them.
- **Pattern Recognition** — Favor invariants and recurring structures that hold
  across contexts over one-off observations.
- **Recursive Improvement** — A change that improves how future work is done is
  worth more than a change that solves only today's instance.

## In Scope

- Concepts, models, and notes on learning, meta-learning, and reflexive
  intelligence.
- Refinements to the core runtime, principles, frameworks, and Grandmaster Mode.
- Clarifications, corrections, and improved explanations.
- Worked analyses that apply Grandmaster Mode and extract a meta-lesson.

## Out of Scope

MindShift focuses on cognition. The following are out of scope (see
[`docs/scope.md`](docs/scope.md)):

- Governance, authority, or legitimacy mechanisms
- Execution platforms or eligibility determination
- Agent frameworks

## The Decision Filter

Before proposing any change, run it through the
[thesis](docs/thesis.md) decision filter:

> Does this strengthen the loop that turns learning back on itself, or merely add
> information (or authority, or tooling) beside it?

If the change only adds something *beside* the loop, it does not belong here. This
is a required check, not a suggestion — every pull request must state how it
passes (the [PR template](.github/pull_request_template.md) prompts for it).

## How to Contribute

1. Create a topic branch for your change.
2. Keep changes focused and clearly described.
3. Confirm the change passes the decision filter above.
4. Add or update documentation under [`docs/`](docs/), and update the Repository
   Map in [`README.md`](README.md) when you add a new document.
5. Open a pull request explaining the change, the reasoning behind it, and how it
   passes the decision filter.

## Style

- Write clear, plain prose.
- Make feedback loops and assumptions explicit.
- Preserve and refine the core invariant; do not dilute it:

  > Learning becomes intelligence when it loops back on itself.
