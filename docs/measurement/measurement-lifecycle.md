# Layer 2 Measurement Lifecycle

**Status:** Proposed measurement procedure  
**Owner:** MindShift

## Scope

This lifecycle captures prospective blocker and preflight runs first, including future executions involving Issue #79, Issue #81 v2, and Issue #91. It does not re-run, rewrite, or enrich frozen historical records.

## Sequence

1. Bind the selected runner revision and immutable inputs before collection.
2. Capture environment and tool identity only where observed.
3. Execute the already-defined bounded run or preflight procedure.
4. Record exact operational status and, only if reached, execution disposition.
5. Capture expected and observed invariants separately.
6. Record blockers, deviations, retries, skipped steps, manual interventions, ambiguities, runtime, and resource observations.
7. Hash preserved evidence files and write a companion provenance manifest binding the InstrumentRunRecord digest.
8. Validate the record against the JSON Schema and retain both record and provenance manifest as separate artifacts.

## Terminal handling

A blocker before execution leaves `execution_disposition` null and requires a structured unknown or blocker reason. A completed, stopped, or inconclusive execution records the exact corresponding lifecycle disposition. No status-to-disposition inference is permitted.

## Non-authority

The collector records observations; it does not decide scientific truth, research-claim validity, legitimacy, permission, or execution eligibility. Instrument calibration and changes to future versions require the separate lifecycle process and append-only successor records.
