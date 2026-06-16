# Worked Example — Retrospectives That Don't Change Behavior

A worked application of [Grandmaster Mode](../grandmaster-mode.md).

**Situation:** A team holds a retrospective at the end of every cycle. People are
candid, action items are written down — and yet the same problems resurface
cycle after cycle. The ritual runs; the team does not improve.

---

## Stage 1 — Surface Observation

- **Recurring pattern:** the same three or four issues appear in nearly every
  retro. The list is stable; the outcomes are not changing.
- **Friction point:** action items are generated, then decay. By the next cycle
  no one remembers whether the last set was done.
- **Anomaly:** there *is* a feedback loop (the retro), but it is **open** — signal
  is produced and then dropped. Reflection happens; adaptation does not.
- **Map:** the constraint is not insight generation (the team has plenty). The
  bottleneck is the missing link between insight and the next cycle's behavior.

> What pattern keeps repeating? Issues recur because nothing carries forward.
> What assumption distorts clarity? "Holding a retro" is being mistaken for
> "learning from it."

## Stage 2 — Define Purpose

- **Bateson:** the team is stuck at Learning I (correcting individual symptoms),
  never reaching Learning II (improving how it learns). Each retro restarts from
  zero instead of building on the last.
- **Dilts:** changes are attempted at the *behavior* level ("do X next time"),
  but the binding constraint is at the *capability/process* level — the team has
  no process for closing a loop.
- **Actual objective:** not "have a retro" but "change the next cycle." The ritual
  is a proxy that has been mistaken for the goal.

> What problem is actually being solved? Currently: the need to *feel* reflective.
> What level of learning is present? Surface (Learning I) — symptom correction,
> no learning about the learning.

## Stage 3 — Determine Next Step

- **80/20:** the leverage is not a better retro template; it is *closing the
  loop*. One closure mechanism outweighs any amount of better discussion.
- **PDCA:** the team runs Plan → Do but skips Check → Act. The broken link is
  Check→Act — verifying the prior change and acting on the result.
- **Smallest useful experiment:** carry exactly **one** action item forward as the
  first agenda item of the next retro, and verify whether it was done and what it
  changed. Nothing else changes.

> If the decision were inverted — if the team never held a retro but always
> verified last cycle's single change — would it improve faster? Almost certainly
> yes. Closure beats insight volume.

## Stage 4 — Strategic Board Analysis

| Candidate move | Risk | Reward | Tempo | Alignment |
| --- | --- | --- | --- | --- |
| A. Better-structured retro template | Low | Low | Low | Low — adds beside the loop |
| B. Carry-forward + verify one action | Low | High | High | High — closes the loop |
| C. Metrics dashboard for action items | Med | Med | Low | Low — tooling, not closure |

**Best move: B.** It directly closes the open loop at the lowest cost and the
highest tempo, and it is the only move aligned with the thesis (it strengthens
the loop rather than adding something beside it).

---

## Output

```text
♟️ Position Summary
   A retro ritual runs every cycle but is an open loop: reflection without
   adaptation. The same issues recur because nothing carries forward.

♜ Candidate Moves
   A. Better retro template
   B. Carry forward and verify one action item
   C. Action-item metrics dashboard

🧠 Best Move + Reasoning
   B. Closing the loop is the 80/20 lever. The missing link is Check→Act, not
   insight. Verifying one carried-forward action turns reflection into recursion
   at minimal cost and maximal tempo.

🏁 Meta-Lesson + Recommended Action
   A learning ritual without a closure check produces reflection, not recursion —
   information beside the loop, not in it. Recommended action: make the first item
   of every retro the verification of the previous retro's single committed
   change.
```

---

## Meta-Lesson → Refinement of the Method

The diagnosis applies to **Grandmaster Mode itself.** As originally written, the
method ends at "Meta-Lesson + Recommended Action" — it *produces* a recommended
action but never *checks* whether the previous analysis's action was carried out
or what it taught. That is precisely the open-loop failure this example diagnoses:
the method could generate insight forever without ever closing a cycle.

**Refinement fed back into [`grandmaster-mode.md`](../grandmaster-mode.md):** add a
**Closure Check** — every analysis should also verify the prior cycle's
recommended action and fold its result into the current observation. This makes
the method enforce on itself the recursion it asks of everything else.

This is the roadmap's Tier 1 working as intended: the practice improved the
protocol.
