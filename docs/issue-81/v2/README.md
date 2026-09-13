# Issue #81 v2 execution package

This directory is the prospective Phase 1 package for the matched context-only
experiment specified by Issue #81. It does not contain empirical outcomes.

The v1 record one directory above remains historical `EXPERIMENT_INVALID`
evidence and is protected by `historical-v1-manifest.json`.

## Before any model call

1. Review and commit every file in this directory.
2. Record that exact commit SHA in Issue #81 or its pull request.
3. From a clean checkout of that commit, run:

   ```bash
   python3 -m unittest docs/issue-81/v2/test_experiment.py
   python3 docs/issue-81/v2/experiment.py preflight
   OPENAI_API_KEY=... python3 docs/issue-81/v2/experiment.py preflight --require-api
   ```

The first command tests deterministic machinery. The second proves the local
equivalence invariants without contacting a model. The third performs only the
frozen provider-identity probe. Do not run the experiment unless all three pass.

## Execute once

From the same clean checkout and with the same credential environment:

```bash
OPENAI_API_KEY=... python3 docs/issue-81/v2/experiment.py run
```

The default output directory is `docs/issue-81/v2/execution/`. The runner uses
create-only evidence writes and refuses to reuse an existing execution
directory. Do not retry a partial run as though it were a new prospective run.
