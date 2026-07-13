# MindShift — Repository Operating Guide

This file orients contributors working in this repository. It defines the
surviving MindShift identity, its boundaries, and the analysis method used here.

## What MindShift Is

MindShift is a research framework for studying how observations become
transferable abstractions that improve future modeling.

The canonical research question is:

```text
How can observations be converted into transferable abstractions that improve future modeling?
```

The canonical research sequence is:

```text
Observation → Pattern → Abstraction → Primitive → Transfer
```

## What MindShift Is Not

MindShift is not independent infrastructure, a deterministic runtime, execution
infrastructure, legitimacy infrastructure, authority infrastructure, governance
infrastructure, or an agent framework.

MindShift does not own execution, authority, approval, legitimacy, execution
eligibility, execution boundaries, proof closure, governed mutation, or replay.
Repository governance may use external mechanisms, including ContinuityOS, but
that governance is not MindShift functionality.

## Operating Principles

- **Reality First** — Models remain subordinate to reality.
- **Pattern Recognition** — Seek recurring structures across observations.
- **Abstraction Formation** — Compress patterns into abstractions that can be
  reused beyond the original case.
- **Transfer Test** — Treat transfer across contexts as the test of usefulness.
- **Learning Reflection** — Each analysis should improve future modeling, not
  merely explain the present.

## MindShift Grandmaster Mode

When analyzing any problem, project, framework, decision, or situation, operate
through the following stages.

### Stage 1 — Surface Observation

- Identify: patterns, biases, anomalies, friction points, recurring structures.
- Map: feedback loops, constraints, bottlenecks, leverage points.
- Ask: What pattern keeps repeating? What assumption may be distorting clarity?

### Stage 2 — Define Purpose

- Analyze using optional learning and systems lenses.
- Determine: actual objective, intended outcome, and level of learning occurring.
- Ask: What problem is actually being solved? What level of learning is present?

### Stage 3 — Determine Next Research Move

- Determine: the highest-leverage research question, smallest useful observation,
  and primary bottleneck to abstraction transfer.
- Ask: If this interpretation were inverted, what might be learned?

### Stage 4 — Transfer Analysis

- Evaluate: candidate abstractions, transfer scope, limits, and model-improvement
  value.
- Select the abstraction or distinction most likely to improve future modeling.

### Output Format

```text
♟️ Position Summary
♜ Candidate Abstractions
🧠 Transfer Analysis
🏁 Meta-Lesson
```

Before a new analysis, run the **Closure Check**: verify whether the previous
analysis improved future modeling and fold that result into the current
observation. The canonical specification of this method, including the Closure
Check, lives in [`docs/grandmaster-mode.md`](docs/grandmaster-mode.md); this
section is a summary.

## Conventions for This Repository

- Keep contributions aligned with the scope above: research on observation,
  patterns, abstraction, primitive extraction, transfer, and model improvement.
- Prefer clear prose and explicit reasoning traces.
- Preserve the canonical identity, question, and sequence.
- Documentation lives in [`docs/`](docs/). Update the Repository Map in
  [`README.md`](README.md) when adding, removing, or renaming documents.
