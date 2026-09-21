#!/usr/bin/env python3
"""Build v2 contexts in memory and prove the frozen matched invariants."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SYSTEM_INSTRUCTION = (
    "Answer the user's task using only the provided repository sources. Do not "
    "use external knowledge. Preserve uncertainty and distinguish candidate "
    "output from authority, permission, legitimacy, execution eligibility, or "
    "validated findings."
)
NEUTRAL_WRAPPER = (
    "The following repository sources are the complete allowed source "
    "information. Use only them. Cite source paths. Treat model output as "
    "candidate output, not authority."
)
SETTINGS = {
    "temperature": 0,
    "top_p": 1,
    "completions": 1,
    "tools": False,
    "retrieval": False,
    "conversation_history": False,
    "shared_prompt_cache": False,
    "max_output_tokens": 2000,
}
GROUPS = (
    ("STALE OR SUPERSEDED", ("supersed", "retir", "withdraw", "stale")),
    ("CONTRADICTIONS", ("contradict", "conflict")),
    ("ASSUMPTIONS AND LIMITATIONS", ("assum", "unknown", "limitation", "uncertain")),
    ("LINEAGE AND PRIOR OBSERVATIONS", ("prior", "histor", "lineage", "observation", "evidence")),
    ("SUPPORTED FINDINGS", ("finding", "result", "evaluation")),
    ("CURRENT STATE", ()),
)
HEADING = re.compile(br"(?m)^#{1,6}[^\r\n]*(?:\r?\n|$)")


@dataclass(frozen=True)
class Source:
    source_id: str
    path: str
    commit: str
    sha256: str
    payload: bytes


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def git_bytes(commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=ROOT)


def sources_by_id(manifest: dict) -> dict[str, Source]:
    result = {}
    for item in manifest["sources"]:
        payload = git_bytes(manifest["source_commit"], item["path"])
        assert hashlib.sha256(payload).hexdigest() == item["sha256"], item["path"]
        assert item["source_id"] not in result
        result[item["source_id"]] = Source(
            item["source_id"], item["path"], manifest["source_commit"],
            item["sha256"], payload
        )
    return result


def delimiter(source: Source, byte_range: str | None = None) -> bytes:
    suffix = f" | bytes={byte_range}" if byte_range else ""
    return (
        f"--- SOURCE: {source.source_id} | {source.path} | {source.commit} | "
        f"{source.sha256}{suffix} ---"
    ).encode()


def task_suffix(prompt: str) -> bytes:
    return b"\n\n--- TASK ---\n\n" + prompt.encode("utf-8")


def construct_control(selected: list[Source], prompt: str) -> tuple[bytes, list[bytes]]:
    chunks = [source.payload for source in selected]
    body = b"\n\n".join(
        delimiter(source) + b"\n\n" + source.payload for source in selected
    )
    return NEUTRAL_WRAPPER.encode() + b"\n\n" + body + task_suffix(prompt), chunks


def split_source(source: Source) -> list[tuple[int, int, bytes, bytes]]:
    starts = [match.start() for match in HEADING.finditer(source.payload)]
    boundaries = [0] + [start for start in starts if start != 0] + [len(source.payload)]
    segments = []
    for start, end in zip(boundaries, boundaries[1:]):
        payload = source.payload[start:end]
        match = HEADING.match(payload)
        heading = match.group(0).lower() if match else b""
        segments.append((start, end, heading, payload))
    return segments


def group_for(heading: bytes) -> str:
    text = heading.decode("utf-8", errors="strict")
    for name, keywords in GROUPS[:-1]:
        if any(keyword in text for keyword in keywords):
            return name
    return "CURRENT STATE"


def construct_treatment(selected: list[Source], prompt: str) -> tuple[bytes, list[bytes]]:
    grouped: dict[str, list[tuple[Source, int, int, bytes]]] = {
        name: [] for name, _ in GROUPS
    }
    reconstructed: dict[str, list[bytes]] = {source.source_id: [] for source in selected}
    for source in selected:
        for start, end, heading, payload in split_source(source):
            grouped[group_for(heading)].append((source, start, end, payload))
            reconstructed[source.source_id].append(payload)

    sections = []
    for name, _ in GROUPS:
        entries = grouped[name]
        if entries:
            content = b"\n\n".join(
                delimiter(source, f"{start}:{end}") + b"\n\n" + payload
                for source, start, end, payload in entries
            )
        else:
            content = b"No source segment classified by the frozen rule."
        sections.append(b"=== " + name.encode() + b" ===\n\n" + content)
    context = (
        NEUTRAL_WRAPPER.encode() + b"\n\n"
        + b"\n\n".join(sections) + task_suffix(prompt)
    )
    chunks = [b"".join(reconstructed[source.source_id]) for source in selected]
    return context, chunks


def validate() -> dict:
    manifest = load_json("source-manifest.json")
    task_set = load_json("task-set.json")
    protocol = (HERE / "protocol.md").read_bytes()
    assert manifest["schema_version"] == "2.0.0"
    assert task_set["schema_version"] == "2.0.0"
    assert task_set["frozen_status"] == "PREREGISTERED_NO_OUTCOMES"
    assert task_set["pairs_per_task"] == 1
    assert len(task_set["tasks"]) == 4
    source_map = sources_by_id(manifest)
    assert len(source_map) == len(manifest["sources"])
    assert len({task["task_id"] for task in task_set["tasks"]}) == 4

    forbidden_paths = [HERE / "outputs", HERE / "blinded", HERE / "scores"]
    assert not any(path.exists() for path in forbidden_paths)
    assert not (HERE / "determination.json").exists()
    assert b"PREREGISTERED_NO_OUTCOMES" in protocol
    assert protocol.count(b"MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED") == 1

    records = []
    for task in task_set["tasks"]:
        # Constructors receive this projection only. Evaluator-only metadata is
        # therefore unreachable rather than filtered after construction.
        generation = {key: task[key] for key in ("task_id", "prompt", "source_ids")}
        ids = generation["source_ids"]
        assert len(ids) == len(set(ids)) and set(ids) <= set(source_map)
        selected = [
            source_map[item["source_id"]]
            for item in manifest["sources"]
            if item["source_id"] in ids
        ]
        selected_ids = [source.source_id for source in selected]
        assert ids == selected_ids, (
            f"{generation['task_id']}: source_ids must follow frozen manifest order"
        )
        control, control_chunks = construct_control(selected, generation["prompt"])
        treatment, treatment_chunks = construct_treatment(selected, generation["prompt"])
        expected = [source.payload for source in selected]
        prompt_bytes = generation["prompt"].encode()
        assert control_chunks == expected
        assert treatment_chunks == expected
        assert control.count(prompt_bytes) == 1
        assert treatment.count(prompt_bytes) == 1
        assert control.endswith(task_suffix(generation["prompt"]))
        assert treatment.endswith(task_suffix(generation["prompt"]))
        records.append({
            "task_id": generation["task_id"],
            "source_ids": ids,
            "source_hashes_match": True,
            "source_bytes_match": True,
            "nothing_omitted_or_duplicated": True,
            "task_byte_identical": True,
            "control_task_occurrences": 1,
            "treatment_task_occurrences": 1,
            "evaluator_metadata_reachable_by_constructor": False,
            "control_context_sha256": hashlib.sha256(control).hexdigest(),
            "treatment_context_sha256": hashlib.sha256(treatment).hexdigest(),
            "control_context_bytes": len(control),
            "treatment_context_bytes": len(treatment),
        })
    return {
        "schema_version": "2.0.0",
        "result": "PASS",
        "model_calls_performed": 0,
        "independent_variable": "source-context organization only",
        "system_instruction_sha256": hashlib.sha256(SYSTEM_INSTRUCTION.encode()).hexdigest(),
        "inference_settings": SETTINGS,
        "tasks": records,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, help="write canonical JSON report")
    args = parser.parse_args()
    report = validate()
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
