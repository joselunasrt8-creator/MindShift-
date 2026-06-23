/**
 * Static MindShift runtime graph manifest.
 *
 * This file is intentionally non-operative: it exports deterministic topology
 * data only. It does not read files, call APIs, execute workflows, or mutate
 * repository/runtime state.
 */

export type RuntimeGraphNode = {
  id: string;
  label: string;
  artifact: string;
  authority: 'observation' | 'manual-approval' | 'boundary-review' | 'evidence' | 'interpretation';
};

export type RuntimeGraphEdge = {
  from: string;
  to: string;
  invariant: string;
};

export const runtimeGraphNodes: RuntimeGraphNode[] = [
  {
    id: 'intent-candidate',
    label: 'Intent Candidate',
    artifact: 'runtime/intents/README.md',
    authority: 'observation',
  },
  {
    id: 'authority-record',
    label: 'Authority Record',
    artifact: 'runtime/authority/README.md',
    authority: 'manual-approval',
  },
  {
    id: 'execution-boundary',
    label: 'Execution Boundary Checklist',
    artifact: 'runtime/execution-boundary/README.md',
    authority: 'boundary-review',
  },
  {
    id: 'proof-closure',
    label: 'Proof Closure',
    artifact: 'runtime/proof/README.md',
    authority: 'evidence',
  },
  {
    id: 'learning-log',
    label: 'Learning Log',
    artifact: 'runtime/learning/README.md',
    authority: 'interpretation',
  },
];

export const runtimeGraphEdges: RuntimeGraphEdge[] = [
  {
    from: 'intent-candidate',
    to: 'authority-record',
    invariant: 'issue creation does not create authority',
  },
  {
    from: 'authority-record',
    to: 'execution-boundary',
    invariant: 'approval makes a bounded action reviewable, not executed',
  },
  {
    from: 'execution-boundary',
    to: 'proof-closure',
    invariant: 'eligibility is not proof; proof follows separately scoped action',
  },
  {
    from: 'proof-closure',
    to: 'learning-log',
    invariant: 'learning interprets proof and creates no new authority',
  },
  {
    from: 'learning-log',
    to: 'intent-candidate',
    invariant: 'new observations require a fresh candidate and review cycle',
  },
];
