# Roadmap — Future / Optional Work

This roadmap is deliberately small. Every item is run through the
[decision filter](thesis.md): *does it strengthen the loop that turns learning
back on itself, or merely add something beside it?* Items that only add beside the
loop are recorded in Tier 3 as guardrails, not tasks.

## Tier 1 — Strengthens the loop (recommended)

### 1. Worked Grandmaster Mode examples
- Add `docs/examples/` with two or three analyses that run a real problem through
  the four stages and end in a `🏁 Meta-Lesson`.
- Each example must feed back: the meta-lesson should propose a refinement to
  [`grandmaster-mode.md`](grandmaster-mode.md) itself, closing the recursion — the
  practice improving the protocol.
- *Why:* the distinctive value is the practice, not the theory. Demonstrations are
  higher-leverage than new concepts.

### 2. Make the decision filter operational in the contribution flow
- Reference the [thesis](thesis.md) decision filter directly in the PR template and
  [`CONTRIBUTING.md`](../CONTRIBUTING.md) as a required check.
- *Why:* turns scope-defense into a standing feedback loop, not a one-time doc.

## Tier 2 — Maintenance / integrity (as needed)

### 3. Periodic compression review
- On any substantive addition, re-run the test: *what remains if every framework
  is removed?* If the answer changed, the thesis drifted — revert or refactor.

### 4. License confirmation
- Currently MIT. Decide explicitly: MIT vs. Apache-2.0 vs. a Creative Commons
  license (defensible for a docs-heavy project).

## Tier 3 — Explicitly NOT to be built (guardrails, not tasks)

Recorded so they are never mistaken for roadmap. See [`scope.md`](scope.md).

- Execution / agent capability
- Governance / authority / legitimacy / eligibility
- Tooling or a product (PKM app, LLM wrapper)
- More "essential" frameworks (framework accretion dilutes the thesis)
- Completeness or scientific-validity claims

## Sequencing

Tier 1.1 first — a single worked example is the smallest useful experiment — then
Tier 1.2. Tiers 2 and 3 are continuous, not scheduled.
