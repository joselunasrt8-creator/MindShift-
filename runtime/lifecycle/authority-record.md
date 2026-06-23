# Authority Record Template

Authority records document explicit maintainer approval for a bounded action.
They are non-operative records and do not execute the approved action.

## Authority ID

`authority-<short-description>-<date>`

## Linked Intent Candidate

<!-- Link to the issue or document that proposed the intent candidate. -->

## Approved Action

<!-- Describe the bounded action that may proceed to boundary review. -->

## Scope

<!-- State exact files, directories, systems, or artifacts in scope. -->

## Constraints

<!-- State non-goals and preserved invariants. -->

## Expiry

<!-- State when this authority expires or must be re-approved. -->

## Expected Proof

<!-- State what evidence must exist after any separately scoped action. -->

## Status

`APPROVED | NULL | EXPIRED`

Authority does not equal execution. This record does not trigger workflows,
mutate systems, create proof, or grant authority to future actions.
