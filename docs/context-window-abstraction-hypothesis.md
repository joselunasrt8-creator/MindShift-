# Candidate Hypothesis: From Information Availability to Reusable Abstractions

## Research Status

This document is exploratory. Its statements are labeled as **observations**,
**candidate abstractions**, **research questions**, **hypotheses**, or **future
empirical work**. It does not report validated findings.

## Problem Statement

**Candidate abstraction — Information availability** is the information that a
system can access within a task's available context. Access can include source
material, prior task state, or retrieved content; it does not by itself show
that the information has been integrated or can be used in a new setting.

**Candidate abstraction — Reusable understanding** is the ability to apply a
principle derived from one setting to a materially different setting while
preserving the relevant relation or constraint. This is a proposed capability,
not a claim about any particular system.

**Research question — Why distinguish them?** Information availability concerns
what is present for a task. Reusable understanding concerns whether a
generalized principle can be formed and transferred beyond the originating
material. A system may have access to information without demonstrating that
transfer; this distinction therefore warrants separate study.

## Candidate Hypothesis

> **Candidate hypothesis:** Scaling context windows increases information
> availability, but transforming information into reusable principles requires
> an explicit abstraction process.

This hypothesis proposes a distinction between context scaling and abstraction
scaling. It does not establish that either effect occurs, identify a mechanism,
or prescribe a system design.

## Conceptual Model

**Candidate abstraction — Canonical diagram**

```text
Context Window
        ↓
Working Information
        ↓
Abstraction Process
        ↓
Reusable Principles
```

```text
More Context
        ≠
More Understanding
```

The inequality is a research framing: additional available context and reusable
understanding are distinct variables to measure, rather than quantities this
document treats as equivalent.

## Proposed Bottleneck Shift

**Research hypothesis — Bottleneck shift**

```text
Small Context Era
Scarcity:
Information
        ↓
Large Context Era
Scarcity:
Reusable Abstractions
```

This diagram proposes a possible transition in the primary constraint on task
performance. It requires validation across defined tasks, systems, and context
conditions. In particular, it does not assert that information is universally
scarce in small-context settings or that reusable abstractions are universally
the limiting factor in large-context settings.

## Operational Definitions

| Term | Operational definition |
| --- | --- |
| **Context window** | The bounded set of input tokens or equivalent task material that a system can process together during one evaluated step. |
| **Working information** | The subset of available task material selected, retained, or referenced while producing an evaluated response. Its use must be evidenced by a predefined trace, annotation, or task-specific measurement. |
| **Explicit abstraction** | A documented operation that identifies one or more relations from source material, states a generalized principle, specifies its conditions or limits, and records the source-to-principle link. |
| **Reusable principle** | A generalized statement with stated applicability conditions that can be evaluated on an unseen task distinct from its source material. |
| **Transfer** | Application of a reusable principle to an unseen target task that differs from the source task according to a predefined difference criterion, followed by a predefined performance assessment. |
| **Reusable abstraction** | An abstraction represented as a reusable principle and evaluated for transfer on one or more unseen target tasks. |

These definitions specify candidate measurement boundaries. Future studies may
revise them before use, but should record revisions so results remain
interpretable.

## Research Questions

- **Research question:** Does larger context alone improve reusable
  understanding under a predefined transfer assessment?
- **Research question:** Which abstraction operations, if any, create reusable
  principles more reliably than alternatives?
- **Research question:** Can explicit abstraction outperform context scaling on
  transfer tasks under comparable task budgets?
- **Research question:** How do source diversity, task difficulty, and the
  definition of target-task difference affect measured transfer?
- **Research question:** Does an explicit abstraction record improve
  long-horizon consistency or reduce repeated reasoning on comparable tasks?

## Validation Roadmap

**Future empirical work — Study design.** Define a task set with source and
unseen target tasks, a context budget, a transfer assessment, and a rule for
what counts as a materially different target task. Keep models, prompts,
information sources, and evaluation criteria documented for each comparison.

**Future empirical work — Context-only workflows.** Evaluate workflows that
receive larger or smaller context budgets without requiring a recorded
abstraction step. Measure task performance and transfer performance separately.

**Future empirical work — Explicit-abstraction workflows.** Evaluate workflows
that produce a source-linked generalized principle with applicability conditions
before the target task. Compare them with context-only workflows under a
predefined comparable budget.

**Future empirical work — Outcome measures.** Assess transfer performance,
long-horizon consistency, and repeated reasoning reduction using measures
specified before evaluation. For repeated reasoning reduction, define both the
unit of reasoning and the permitted reuse mechanism before collecting results.

**Future empirical work — Analysis.** Report task-level variation, failure
cases, and conditions that limit transfer. Separate measured outcomes from
interpretations of the bottleneck hypothesis.

## Boundaries

This document:

- proposes a candidate abstraction;
- does not claim empirical validation;
- does not claim novelty has been established; and
- identifies future research.

It is a conceptual input for future **Architectural Boundary Research**. It does
not define an architecture, runtime behavior, execution process, or governance
mechanism.
