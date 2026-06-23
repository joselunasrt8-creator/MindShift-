# MindShift

## Cognition Infrastructure for Learning, Adaptation, and Recursive Improvement

MindShift is an independent, open-source exploration of how systems learn, adapt, validate, and improve over time.

It began with a single observation:

> Learning becomes intelligence when it loops back on itself.

The project explores recursive learning systems, feedback loops, pattern recognition, reflection, meta-learning, and cognitive architecture.

Rather than asking:

> What should I learn?

MindShift asks:

> How does learning itself improve?

---

## MindShift Runtime

MindShift includes a non-operative runtime documentation model that reconciles the cognitive loop with an artifact lifecycle for bounded intent, authority, execution-boundary review, proof closure, and learning.

The cognitive loop remains:

```text
Observe → Model → Validate → Learn → Improve → Repeat
```

The artifact lifecycle is:

```text
Issue → Intent Candidate → Manual Approval → Authority Record → Execution Boundary Checklist → Eligible / NULL → Separately Scoped Action → Proof Closure → Learning Log → New Observation
```

The runtime does not create authority, execute actions, create proof, determine future eligibility automatically, perform releases, or operate external systems. Learning closes the loop only by producing a new observation for a future separately approved cycle.

Runtime documentation:

- [`runtime/RUNTIME.md`](runtime/RUNTIME.md)
- [`runtime/lifecycle/README.md`](runtime/lifecycle/README.md)
- [`runtime/lifecycle/manual-runbook.md`](runtime/lifecycle/manual-runbook.md)
- [`runtime/intents/README.md`](runtime/intents/README.md)
- [`runtime/authority/README.md`](runtime/authority/README.md)
- [`runtime/execution-boundary/README.md`](runtime/execution-boundary/README.md)
- [`runtime/proof/README.md`](runtime/proof/README.md)
- [`runtime/learning/README.md`](runtime/learning/README.md)

The manual runbook explains how to move through the non-operative lifecycle
without confusing documentation artifacts with authority, execution,
eligibility, or proof.

---

## Core Question

```text
How do systems learn, adapt, validate, and improve over time?
```

This question applies to:

- Individuals
- Teams
- Organizations
- AI systems
- Multi-agent systems
- Learning environments

---

## Foundational Principles

### Reality First

All models remain subordinate to reality.

```text
Assumption → Test → Validation → Revision
```

### Feedback Creates Learning

Without feedback, improvement stalls.

```text
Action → Feedback → Adaptation
```

### Pattern Recognition Matters

Understanding emerges from recognizing relationships across observations. Seek
patterns, invariants, feedback loops, leverage points, and recurring structures.

### Learning About Learning

The highest-leverage improvements often come from improving the learning process itself.

### Recursive Improvement

Every cycle should improve future cycles.

---

## Framework Areas

MindShift draws from and integrates concepts including:

- First Principles Thinking
- Pattern Recognition
- Learning Systems
- Meta-Learning
- Reflexive Intelligence
- Bateson Levels of Learning
- Dilts Logical Levels
- Cybernetics
- Kaizen / PDCA
- OODA Loops
- Systems Thinking
- Flow Theory
- Feedback Systems
- Cognitive Architecture
- Recursive Improvement

See [`docs/frameworks.md`](docs/frameworks.md) for how each lens is used.

---

## What MindShift Is

- A cognition infrastructure project
- A recursive learning framework
- A collection of learning systems
- An exploration of reflexive intelligence
- A research space for cognition and adaptation

## What MindShift Is Not

- A governance system
- An execution platform
- An agent framework
- A legitimacy or eligibility protocol
- A replacement for machine learning
- A large language model
- A productivity or certification system
- A claim of scientific completeness

MindShift focuses on **cognition**. It does not create authority, govern
execution, validate legitimacy, or determine execution eligibility.

---

## Repository Map

| Path | Purpose |
| --- | --- |
| [`README.md`](README.md) | Project overview (this file) |
| [`CLAUDE.md`](CLAUDE.md) | Repository-level operating guide and Grandmaster Mode |
| [`docs/thesis.md`](docs/thesis.md) | The center: the invariant, canonical compression, and decision filter |
| [`docs/core-runtime.md`](docs/core-runtime.md) | The Observe → Improve loop in depth |
| [`docs/principles.md`](docs/principles.md) | Operating principles |
| [`docs/frameworks.md`](docs/frameworks.md) | The framework lenses MindShift integrates |
| [`docs/grandmaster-mode.md`](docs/grandmaster-mode.md) | The four-stage analysis method |
| [`docs/examples/`](docs/examples/) | Worked Grandmaster Mode analyses that feed back into the method |
| [`runtime/RUNTIME.md`](runtime/RUNTIME.md) | Canonical non-operative runtime lifecycle and boundary invariants |
| [`runtime/lifecycle/README.md`](runtime/lifecycle/README.md) | Runtime lifecycle index and closure rule |
| [`runtime/lifecycle/manual-runbook.md`](runtime/lifecycle/manual-runbook.md) | Contributor-facing manual guide and boundary map for the non-operative runtime lifecycle |
| [`runtime/intents/README.md`](runtime/intents/README.md) | Intent candidate documentation and handoff boundary |
| [`runtime/authority/README.md`](runtime/authority/README.md) | Authority record documentation for bounded manual approval |
| [`runtime/execution-boundary/README.md`](runtime/execution-boundary/README.md) | Execution-boundary checklist documentation for Eligible / NULL review |
| [`runtime/proof/README.md`](runtime/proof/README.md) | Proof closure documentation after separately scoped action |
| [`runtime/learning/README.md`](runtime/learning/README.md) | Learning log documentation for new observations |
| [`docs/lineage.md`](docs/lineage.md) | Historical context and the recurring invariant |
| [`docs/scope.md`](docs/scope.md) | Boundaries: what MindShift is and is not |
| [`docs/roadmap.md`](docs/roadmap.md) | Future / optional work, filtered against the thesis |
| [`docs/reviews/`](docs/reviews/) | Periodic compression reviews checking the repo against its thesis |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to contribute |
| [`LICENSE`](LICENSE) | Apache-2.0 License |

---

## Project Thesis

Information is becoming abundant.

Learning is becoming the differentiator.

The future advantage is not access to answers.

It is the ability to learn, adapt, validate, and improve faster than the environment changes.

```text
Observe → Model → Validate → Learn → Improve → Repeat
```

Learning how to learn remains one of the most powerful recursive advantages available to any system.

The [reframing audit](docs/reviews/mindshift-reframing-audit.md) compresses MindShift as **Abstraction Discovery Infrastructure**:

```text
Reality → Pattern → Abstraction → Transfer
```
