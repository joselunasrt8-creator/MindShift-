#!/usr/bin/env python3
"""Validate v1 preservation, prospective ordering, and the blocked v2 record."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FREEZE = "56886b7bb7018d729dc4a65651c7e635878dc697"
V1_BLOBS = {
    "docs/issue-81/protocol.md": "ace1422f87757f65905ba5a976348d2ae33690cf",
    "docs/issue-81/task-set.json": "c027b3fcab614e3155205553647c41e76849c05b",
    "docs/issue-81/source-manifest.json": "c43236b3b1b185a14ada4243afe9031aa11cf26f",
    "docs/issue-81/validate_protocol.py": "cfd586944a6f2e6736ae0646dc91200c76756cb2",
    "docs/issue-81/experiment-record.md": "d8df5f343d2fb4938ae84d465e0c4cfbc2ef27a6",
}
FROZEN_BLOBS = {
    "protocol.md": "c48c3f597fde3932c6dcb38c06a41d35733fc5b6",
    "task-set.json": "d62de2cc38739bf59a991c6922afb9ef8a080277",
    "source-manifest.json": "b49ef2b7e0b02d0a59371e67c29e4f028bb54964",
    "construct_and_validate.py": "9265673905d22fa88be787e084a445e35fa38625",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for path, expected in V1_BLOBS.items():
    assert git("rev-parse", f"HEAD:{path}") == expected, f"v1 changed: {path}"
if not __debug__:
    raise SystemExit("Issue #81 v2 evidence validation refuses optimized Python")

for name, expected in FROZEN_BLOBS.items():
    assert git("rev-parse", f"HEAD:docs/issue-81/v2/{name}") == expected, name
assert git("merge-base", "--is-ancestor", FREEZE, "HEAD") == ""

preflight = json.loads((HERE / "preflight.json").read_text())
provenance = json.loads((HERE / "run-provenance.json").read_text())
assert preflight["result"] == "PASS" and preflight["model_calls_performed"] == 0
assert len(preflight["tasks"]) == 4
for task in preflight["tasks"]:
    assert task["source_hashes_match"] and task["source_bytes_match"]
    assert task["nothing_omitted_or_duplicated"] and task["task_byte_identical"]
    assert task["control_task_occurrences"] == task["treatment_task_occurrences"] == 1
    assert not task["evaluator_metadata_reachable_by_constructor"]

assert provenance["frozen_protocol_commit"] == FREEZE
assert provenance["preflight_result"] == "PASS"
assert provenance["run_status"] == "PROVIDER_IDENTITY_BLOCKED"
assert provenance["model_calls_performed"] == provenance["completed_pairs"] == 0
assert provenance["raw_outputs"] == provenance["evaluations"] == 0
assert provenance["empirical_terminal_determination"] is None
assert not provenance["issue_closure_permitted"]
for forbidden in ("outputs", "blinded", "scores", "determination.json"):
    assert not (HERE / forbidden).exists(), forbidden

print("Issue #81 v2 evidence validation: PASS (provider-blocked; no empirical outcome)")
