# Reproducible Research Validation

## Purpose and scope

Run the deterministic, model-free checks for the Issue #81 v1 preregistration, Issue #81 v2 context construction and freeze evidence, and Issue #91 reconstruction preparation from one command.

From the repository root:

```bash
python scripts/validate.py
```

Requirements:

- Python 3.10 or newer.
- Git installed and available on `PATH`.
- A complete, non-shallow clone of this repository.
- The required historical commits and their trees/blobs retained in the local object database.
- No third-party Python packages, network access, or model/API calls are required.

The entry point rejects optimized Python because the frozen Issue #81 validators use Python assertions as protocol checks. It also rejects shallow clones because Issue #81 v2 explicitly checks that its freeze commit is an ancestor of the checked-out `HEAD`.

For a shallow clone, fetch the complete history before running:

```bash
git fetch --unshallow --tags
```

The GitHub Actions workflow uses `actions/checkout` with `fetch-depth: 0` for the same reason.

## Exact Git-history dependencies

The validators intentionally resolve historical Git objects. A working-tree copy of a source file is not a substitute for the commit/path identity recorded by the experiment.

| Validator | Git operation | Required identity / condition |
| --- | --- | --- |
| `docs/issue-81/validate_protocol.py` | `git show <source_commit>:<path>` | Source commit `d31d7630c5c2189dc350626215f2ba0c65b667a0`; every source path and SHA-256 in `docs/issue-81/source-manifest.json`. |
| `docs/issue-81/v2/construct_and_validate.py` | `git show <source_commit>:<path>` | Same source commit `d31d7630c5c2189dc350626215f2ba0c65b667a0`; every source path and SHA-256 in `docs/issue-81/v2/source-manifest.json`. |
| `docs/issue-81/v2/validate_evidence.py` | `git rev-parse HEAD:<path>`; `git merge-base --is-ancestor <freeze> HEAD` | The exact v1/v2 blob pins listed below must be present at the checked-out `HEAD`; freeze commit `56886b7bb7018d729dc4a65651c7e635878dc697` must be an ancestor of `HEAD`. |
| `docs/issue-91/validate_and_reconstruct.py` | `git show -s --format=%cI <commit>`; `git show <commit>:<path>` | The four evidence-source commits and paths listed below must resolve, with commit timestamps matching the frozen cohort records. |

### Issue #81 v1 blob pins

The Issue #81 v2 evidence validator compares `HEAD:<path>` against these exact blob IDs:

| Path | Blob SHA |
| --- | --- |
| `docs/issue-81/protocol.md` | `ace1422f87757f65905ba5a976348d2ae33690cf` |
| `docs/issue-81/task-set.json` | `c027b3fcab614e3155205553647c41e76849c05b` |
| `docs/issue-81/source-manifest.json` | `c43236b3b1b185a14ada4243afe9031aa11cf26f` |
| `docs/issue-81/validate_protocol.py` | `cfd586944a6f2e6736ae0646dc91200c76756cb2` |
| `docs/issue-81/experiment-record.md` | `d8df5f343d2fb4938ae84d465e0c4cfbc2ef27a6` |

### Issue #81 v2 blob pins

| Path | Blob SHA |
| --- | --- |
| `docs/issue-81/v2/protocol.md` | `c48c3f597fde3932c6dcb38c06a41d35733fc5b6` |
| `docs/issue-81/v2/task-set.json` | `d62de2cc38739bf59a991c6922afb9ef8a080277` |
| `docs/issue-81/v2/source-manifest.json` | `b49ef2b7e0b02d0a59371e67c29e4f028bb54964` |
| `docs/issue-81/v2/construct_and_validate.py` | `9265673905d22fa88be787e084a445e35fa38625` |

The v2 evidence validator also requires commit `56886b7bb7018d729dc4a65651c7e635878dc697` to be an ancestor of the checked-out `HEAD`. Its `git merge-base --is-ancestor` command succeeds with exit status 0 and empty stdout; a nonzero exit means the ancestry condition is not established.

### Issue #91 source commits

The frozen cohort references these historical source identities:

| Work item / evidence | Commit | Source path |
| --- | --- | --- |
| MS91-WI-001 E-1; MS91-WI-002 E-2 | `34a99ff520a840fbf44a044e7a25e86b87a2512a` | `docs/reference-execution/v1.0/freeze-record.md` |
| MS91-WI-002 E-1 | `388c49a6d31c9f630dd1ce15cb7f752fd212cd20` | `docs/reference-execution/transcripts/MIT-6.1200J-Lecture-11/transcript.md` |
| MS91-WI-003 E-1 | `7cb679b8e1de8f27df6cad661c2b43673221d9ba` | `docs/issue-81/protocol.md` |
| MS91-WI-004 E-1 | `bd40efaacced05290e4c48d31a92f9e4f3655400` | `docs/issue-81/v2/protocol.md` |
| MS91-WI-004 E-2 | `bd40efaacced05290e4c48d31a92f9e4f3655400` | `docs/issue-81/v2/construct_and_validate.py` |
| MS91-WI-004 E-3 | `bd40efaacced05290e4c48d31a92f9e4f3655400` | `docs/issue-81/v2/task-set.json` |
| MS91-WI-004 E-4 | `bd40efaacced05290e4c48d31a92f9e4f3655400` | `docs/issue-81/v2/source-manifest.json` |

Issue #91 also verifies each recorded commit timestamp against Git's committer timestamp and compares the bytes returned by `git show` with the frozen assessment-input bundle.

### What “full history” means here

For the aggregate entry point, the repository must not be shallow and must contain the listed commit objects, their relevant trees/blobs, and the ancestry chain needed to establish the Issue #81 v2 freeze commit as an ancestor of `HEAD`. The Issue #91 validator itself resolves the listed commit objects by ID; it does not independently require every unrelated historical commit to be present. The aggregate command uses a full clone as the reproducible, supported environment.

## Validation sequence

The entry point runs, in order:

1. Issue #81 v1 static preregistration validation.
2. Issue #81 v2 context construction and byte-equivalence preflight.
3. Issue #81 v2 preservation, freeze-identity, and blocked-run evidence validation.
4. Issue #91 frozen cohort, provenance, cutoff, leakage, and deterministic reconstruction preflight.
5. Issue #91 unit tests.
6. README local-link and image-reference checks, plus UTF-8 verification of `docs/grandmaster-mode.md`.

The checks are deterministic and model-free. The command prints reports to stdout and does not create experiment outcomes, score files, determination files, or reconstructed assessor bundles.

## Preservation boundary

The Issue #81 manifests, protocols, source files, validators, preflight records, and execution records are frozen evidence. The Issue #91 validator is itself bound by `docs/issue-91/freeze-manifest.json`. This maintenance work therefore does not rewrite those files or regenerate their manifests.

The Issue #91 test isolates its adversarial input in a temporary copy of `assessment-input/`; it does not write into the committed frozen input tree.

A future correction to any manifest-bound validator or frozen experiment artifact requires a separately versioned successor and a new freeze decision. Do not update a pinned blob merely to make the current validator pass.
