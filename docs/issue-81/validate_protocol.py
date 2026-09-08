#!/usr/bin/env python3
"""Static preregistration checks. This script never invokes a model."""

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / name).read_text(encoding="utf-8"))


manifest = load("source-manifest.json")
tasks = load("task-set.json")
protocol = (HERE / "protocol.md").read_text(encoding="utf-8")

assert manifest["schema_version"] == "1.0.0"
assert tasks["frozen_status"] == "PREREGISTERED_NO_OUTCOMES"
source_ids = set()
for source in manifest["sources"]:
    assert source["source_id"] not in source_ids
    source_ids.add(source["source_id"])
    payload = subprocess.check_output(
        ["git", "show", f'{manifest["source_commit"]}:{source["path"]}'], cwd=ROOT
    )
    assert hashlib.sha256(payload).hexdigest() == source["sha256"], source["path"]

assert len(tasks["tasks"]) == 4
assert len({task["task_id"] for task in tasks["tasks"]}) == 4
for task in tasks["tasks"]:
    assert task["prompt"] and task["information_requirements"]
    assert task["evaluation_dimensions"] and task["bounded_reference"]
    assert task["source_ids"] and set(task["source_ids"]) <= source_ids

required = [
    "same verified source IDs and exact bytes",
    "ORDINARY_RAW_V1",
    "MINDSHIFT_STRUCTURED_V1",
    "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED",
    "NO_MEASURABLE_IMPROVEMENT",
    "MINDSHIFT_CONTEXT_DEGRADED_OUTPUT",
    "INDETERMINATE",
    "EXPERIMENT_INVALID",
    "No treatment/control output",
    "invalid outcomes are admissible",
    "not a MindShift runtime",
]
normalized_protocol = " ".join(protocol.split())
for phrase in required:
    assert phrase in normalized_protocol, phrase

reserved = [HERE / "outputs", HERE / "results", HERE / "determination.json"]
assert not any(path.exists() for path in reserved)
print("Issue #81 preregistration validation: PASS (no model execution performed)")
