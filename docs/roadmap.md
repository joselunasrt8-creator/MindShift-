# Roadmap — Future / Optional Work

This roadmap is deliberately small. Every item is run through the
[decision filter](thesis.md): *does it strengthen the loop that turns learning
back on itself, or merely add something beside it?* Items that only add beside the
loop are recorded in Tier 3 as guardrails, not tasks.

## Tier 1 — Strengthens the loop (recommended)

### 1. Worked Grandmaster Mode examples
- Add [`docs/examples/`](examples/) with analyses that run a real problem through
  the four stages and end in a `🏁 Meta-Lesson`.
- Each example must feed back: the meta-lesson should propose a refinement to
  [`grandmaster-mode.md`](grandmaster-mode.md) itself, closing the recursion — the
  practice improving the protocol.
- *Why:* the distinctive value is the practice, not the theory. Demonstrations are
  higher-leverage than new concepts.
- **Status:** started. First example —
  [retrospectives that don't change behavior](examples/retrospectives-that-dont-change-behavior.md) —
  produced the **Closure Check** refinement to the method. The pattern is
  established; add further examples as new problems arise.

### 2. Make the decision filter operational in the contribution flow
- Reference the [thesis](thesis.md) decision filter directly in the PR template and
  [`CONTRIBUTING.md`](../CONTRIBUTING.md) as a required check.
- *Why:* turns scope-defense into a standing feedback loop, not a one-time doc.
- **Status:** done. The filter is a required check in
  [`CONTRIBUTING.md`](../CONTRIBUTING.md) and a checkbox in the
  [PR template](../.github/pull_request_template.md).

## Tier 2 — Maintenance / integrity (as needed)

### 3. Periodic compression review
- On any substantive addition, re-run the test: *what remains if every framework
  is removed?* If the answer changed, the thesis drifted — revert or refactor.
- Record each review under [`docs/reviews/`](reviews/). First review:
  [2026-06-16](reviews/2026-06-16-compression-review.md) — verdict: no drift; fixed
  a divergence between the method spec and its summary in `CLAUDE.md`.

### 4. License confirmation
- **Decided: Apache-2.0** (see [`LICENSE`](../LICENSE) and [`NOTICE`](../NOTICE)).
  Chosen over MIT for its explicit patent grant and over Creative Commons because
  the project may include code as well as prose.

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
