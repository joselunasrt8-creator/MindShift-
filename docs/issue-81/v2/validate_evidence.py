#!/usr/bin/env python3
"""Validate v1 preservation, prospective ordering, and the blocked v2 record."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FREEZE = "bd40efaacced05290e4c48d31a92f9e4f3655400"
V1_BLOBS = {
    "docs/issue-81/protocol.md": "ace1422f87757f65905ba5a976348d2ae33690cf",
    "docs/issue-81/task-set.json": "c027b3fcab614e3155205553647c41e76849c05b",
    "docs/issue-81/source-manifest.json": "c43236b3b1b185a14ada4243afe9031aa11cf26f",
    "docs/issue-81/validate_protocol.py": "cfd586944a6f2e6736ae0646dc91200c76756cb2",
    "docs/issue-81/experiment-record.md": "d8df5f343d2fb4938ae84d465e0c4cfbc2ef27a6",
}
FROZEN_HASHES = {
    "protocol.md": "4003570bcdc0190d0c444f966239693783d960acf8d8de893111fb0087bd2fcf",
    "task-set.json": "1894d261ed7d6e873c63a6d25af281473b2adf1d11d561b9ebe75bdef3c21f22",
    "source-manifest.json": "d527c5f4758d01dcf4ec85f08e98f4c0b147fcf2fcb8e9d76096db3e61c97d33",
    "construct_and_validate.py": "a4e0283e325ee4652730e00b32c81f44ff340c38b4eef569b1deae2ef63eba0a",
}


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


for path, expected in V1_BLOBS.items():
    assert git("rev-parse", f"HEAD:{path}") == expected, f"v1 changed: {path}"
for name, expected in FROZEN_HASHES.items():
    assert hashlib.sha256((HERE / name).read_bytes()).hexdigest() == expected, name
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
