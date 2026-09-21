#!/usr/bin/env python3
"""Validate v1 preservation, prospective ordering, and the blocked v2 record."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FREEZE = "91cb3907c3ac2f219e9885c8277db94f63db16e9"
V1_BLOBS = {
    "docs/issue-81/protocol.md": "ace1422f87757f65905ba5a976348d2ae33690cf",
    "docs/issue-81/task-set.json": "c027b3fcab614e3155205553647c41e76849c05b",
    "docs/issue-81/source-manifest.json": "c43236b3b1b185a14ada4243afe9031aa11cf26f",
    "docs/issue-81/validate_protocol.py": "cfd586944a6f2e6736ae0646dc91200c76756cb2",
    "docs/issue-81/experiment-record.md": "d8df5f343d2fb4938ae84d465e0c4cfbc2ef27a6",
}
FROZEN_PATHS = (
    "docs/issue-81/v2/protocol.md",
    "docs/issue-81/v2/task-set.json",
    "docs/issue-81/v2/source-manifest.json",
    "docs/issue-81/v2/construct_and_validate.py",
)


def fail(message: str) -> None:
    raise SystemExit(f"Issue #81 v2 evidence validation FAILED: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def git(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.STDOUT
        ).strip()
    except subprocess.CalledProcessError as exc:
        fail(f"git {' '.join(args)} failed: {exc.output.strip()}")


for path, expected in V1_BLOBS.items():
    require(git("rev-parse", f"HEAD:{path}") == expected, f"v1 changed: {path}")

git("merge-base", "--is-ancestor", FREEZE, "HEAD")
for path in FROZEN_PATHS:
    require(
        git("rev-parse", f"HEAD:{path}") == git("rev-parse", f"{FREEZE}:{path}"),
        f"post-freeze mutation: {path}",
    )

preflight = json.loads((HERE / "preflight.json").read_text())
provenance = json.loads((HERE / "run-provenance.json").read_text())
try:
    regenerated = json.loads(
        subprocess.check_output(
            [sys.executable, str(HERE / "construct_and_validate.py")],
            cwd=ROOT,
            text=True,
        )
    )
except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
    fail(f"preflight regeneration failed: {exc}")

require(regenerated == preflight, "stored preflight differs from frozen constructor output")
require(preflight.get("result") == "PASS", "preflight did not pass")
require(preflight.get("model_calls_performed") == 0, "preflight performed model calls")
require(len(preflight.get("tasks", [])) == 4, "expected four preflight tasks")
for task in preflight["tasks"]:
    require(task.get("source_hashes_match") is True, f"{task.get('task_id')}: source hashes")
    require(task.get("source_bytes_match") is True, f"{task.get('task_id')}: source bytes")
    require(
        task.get("nothing_omitted_or_duplicated") is True,
        f"{task.get('task_id')}: omission/duplication",
    )
    require(task.get("task_byte_identical") is True, f"{task.get('task_id')}: task mismatch")
    require(
        task.get("control_task_occurrences") == 1
        and task.get("treatment_task_occurrences") == 1,
        f"{task.get('task_id')}: task occurrence count",
    )
    require(
        task.get("evaluator_metadata_reachable_by_constructor") is False,
        f"{task.get('task_id')}: evaluator metadata leakage",
    )

require(provenance.get("frozen_protocol_commit") == FREEZE, "wrong freeze commit")
require(provenance.get("preflight_result") == "PASS", "provenance preflight state")
require(provenance.get("run_status") == "PROVIDER_IDENTITY_BLOCKED", "wrong run status")
require(
    provenance.get("model_calls_performed") == 0
    and provenance.get("completed_pairs") == 0,
    "empirical generation occurred",
)
require(
    provenance.get("raw_outputs") == 0 and provenance.get("evaluations") == 0,
    "empirical artifacts exist",
)
require(
    provenance.get("empirical_terminal_determination") is None,
    "fabricated empirical terminal determination",
)
require(provenance.get("issue_closure_permitted") is False, "issue closure incorrectly permitted")
for forbidden in ("outputs", "blinded", "scores", "determination.json"):
    require(not (HERE / forbidden).exists(), f"forbidden empirical artifact: {forbidden}")

print("Issue #81 v2 evidence validation: PASS (provider-blocked; no empirical outcome)")
