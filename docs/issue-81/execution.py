#!/usr/bin/env python3
"""Deterministic, fail-closed execution machinery for frozen Issue #81.

This module does not select a provider and does not make a model call unless the
operator explicitly invokes ``generate`` with a preflighted, immutable run
manifest.  Synthetic test data is always marked and cannot be used as evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import secrets
import statistics
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PROTOCOL = HERE / "protocol.md"
TASK_SET = HERE / "task-set.json"
SOURCE_MANIFEST = HERE / "source-manifest.json"
FROZEN_COMMIT = "7cb679b8e1de8f27df6cad661c2b43673221d9ba"
FROZEN_TREE = "8a445bd8b5792e705dd4bb5dd7a370a352db42cf"
SYSTEM_INSTRUCTION = (
    "Answer the user's task using only the provided repository sources. Do not use external "
    "knowledge. Preserve uncertainty and distinguish candidate output from authority, permission, "
    "legitimacy, execution eligibility, or validated findings."
)
SOURCE_INSTRUCTION = (
    "The following repository sources are the complete allowed source information. Use only them. "
    "Cite source paths. Treat model output as candidate output, not authority."
)
CATEGORIES = (
    "CURRENT STATE", "OBSERVATIONS", "PRIOR OBSERVATIONS", "SUPPORTED FINDINGS",
    "ASSUMPTIONS", "CONTRADICTIONS", "STALE OR SUPERSEDED",
)
RESERVED_OUTCOME_PATHS = (HERE / "outputs", HERE / "results", HERE / "determination.json")
REQUIRED_MODEL_FIELDS = (
    "provider", "snapshot", "immutable_snapshot", "temperature_control", "seed_control",
    "token_accounting", "context_window_tokens", "tokenizer",
)


class PreflightError(RuntimeError):
    """A bounded preflight failure carrying the required terminal blocker."""

    def __init__(self, state: str, detail: str):
        super().__init__(detail)
        self.state = state
        self.detail = detail


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def frozen_identities() -> dict[str, str]:
    return {
        "protocol_sha256": sha256(PROTOCOL.read_bytes()),
        "task_set_sha256": sha256(TASK_SET.read_bytes()),
        "source_manifest_sha256": sha256(SOURCE_MANIFEST.read_bytes()),
        "frozen_commit": FROZEN_COMMIT,
        "frozen_tree": FROZEN_TREE,
    }


@dataclass(frozen=True)
class Source:
    source_id: str
    path: str
    source_commit: str
    expected_hash: str
    payload: bytes


@dataclass(frozen=True)
class Segment:
    source_id: str
    path: str
    source_ordinal: int
    segment_ordinal: int
    category: str
    payload: bytes


@dataclass(frozen=True)
class Context:
    condition: str
    task_id: str
    prompt: str
    sources: tuple[Source, ...]
    segments: tuple[Segment, ...]
    payload: bytes


def task_by_id(task_id: str, tasks: dict[str, Any] | None = None) -> dict[str, Any]:
    records = (tasks or load_json(TASK_SET))["tasks"]
    matches = [task for task in records if task["task_id"] == task_id]
    if len(matches) != 1:
        raise PreflightError("EXPERIMENT_INVALID", f"unknown or duplicate task: {task_id}")
    return matches[0]


def read_sources(task: dict[str, Any], manifest: dict[str, Any] | None = None) -> tuple[Source, ...]:
    manifest = manifest or load_json(SOURCE_MANIFEST)
    indexed = {item["source_id"]: item for item in manifest["sources"]}
    result = []
    for source_id in task["source_ids"]:
        if source_id not in indexed:
            raise PreflightError("EXPERIMENT_INVALID", f"unmanifested source: {source_id}")
        item = indexed[source_id]
        try:
            payload = subprocess.check_output(
                ["git", "show", f'{manifest["source_commit"]}:{item["path"]}'], cwd=ROOT
            )
        except subprocess.CalledProcessError as exc:
            raise PreflightError("EXPERIMENT_INVALID", f"missing frozen source: {source_id}") from exc
        actual = sha256(payload)
        if actual != item["sha256"]:
            raise PreflightError("EXPERIMENT_INVALID", f"source hash mismatch: {source_id}")
        result.append(Source(source_id, item["path"], manifest["source_commit"], actual, payload))
    return tuple(result)


def control_context(task: dict[str, Any], sources: tuple[Source, ...]) -> Context:
    body = bytearray(SOURCE_INSTRUCTION.encode())
    for source in sources:
        body.extend(f"\n\n--- SOURCE: {source.path} ---\n\n".encode())
        body.extend(source.payload)
    body.extend(b"\n\n--- TASK ---\n\n")
    body.extend(task["prompt"].encode())
    return Context("control", task["task_id"], task["prompt"], sources, (), bytes(body))


HEADING = re.compile(br"(?m)^#{1,6}[ \t]+[^\r\n]*(?:\r?\n|$)")
CLASSIFIERS = (
    (re.compile(br"supersed|retir|withdraw|stale", re.I), "STALE OR SUPERSEDED"),
    (re.compile(br"contradict|conflict", re.I), "CONTRADICTIONS"),
    (re.compile(br"assum|unknown|limitation|uncertain", re.I), "ASSUMPTIONS"),
    (re.compile(br"prior|histor|lineage", re.I), "PRIOR OBSERVATIONS"),
    (re.compile(br"observation|evidence", re.I), "OBSERVATIONS"),
    (re.compile(br"finding|result|evaluation", re.I), "SUPPORTED FINDINGS"),
)


def split_source(source: Source, source_ordinal: int) -> tuple[Segment, ...]:
    matches = list(HEADING.finditer(source.payload))
    starts = ([0] if not matches or matches[0].start() else [0]) + [m.start() for m in matches]
    starts = sorted(set(starts))
    segments = []
    for ordinal, start in enumerate(starts):
        end = starts[ordinal + 1] if ordinal + 1 < len(starts) else len(source.payload)
        payload = source.payload[start:end]
        heading_match = HEADING.match(payload)
        heading = heading_match.group(0) if heading_match else b""
        category = "CURRENT STATE"
        for pattern, candidate in CLASSIFIERS:
            if pattern.search(heading):
                category = candidate
                break
        segments.append(Segment(source.source_id, source.path, source_ordinal, ordinal, category, payload))
    return tuple(segments)


def treatment_context(task: dict[str, Any], sources: tuple[Source, ...]) -> Context:
    segments = tuple(seg for i, source in enumerate(sources) for seg in split_source(source, i))
    body = bytearray(SOURCE_INSTRUCTION.encode())
    for category in CATEGORIES:
        body.extend(f"\n\n## {category}\n".encode())
        selected = [seg for seg in segments if seg.category == category]
        if not selected:
            body.extend(b"No source segment classified by the frozen rule.\n")
        for seg in selected:
            body.extend(
                f"\n--- SEGMENT: {seg.source_id} | {seg.path} | {seg.segment_ordinal} ---\n".encode()
            )
            body.extend(seg.payload)
    body.extend(b"\n\n## TASK RELEVANCE\nTask focus: ")
    body.extend(task["prompt"].encode())
    body.extend(b"\n\n## LINEAGE AND PROVENANCE\n")
    for source in sources:
        body.extend(
            f"- {source.source_id} | {source.path} | {source.source_commit} | {source.expected_hash}\n".encode()
        )
    body.extend(b"\n--- TASK ---\n\n")
    body.extend(task["prompt"].encode())
    return Context("treatment", task["task_id"], task["prompt"], sources, segments, bytes(body))


def prove_equivalence(control: Context, treatment: Context, task: dict[str, Any]) -> dict[str, Any]:
    if control.task_id != treatment.task_id or control.prompt != treatment.prompt or control.prompt != task["prompt"]:
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "task prompt mismatch")
    control_identity = [(s.source_id, s.expected_hash, s.payload) for s in control.sources]
    treatment_identity = [(s.source_id, s.expected_hash, s.payload) for s in treatment.sources]
    if control_identity != treatment_identity:
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "source identity, order, hash, or bytes differ")
    if control.payload != control_context(task, control.sources).payload:
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "control does not match the frozen constructor")
    if treatment.payload != treatment_context(task, treatment.sources).payload:
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "treatment contains text outside the frozen transformation")
    reconstructed: dict[str, bytearray] = {s.source_id: bytearray() for s in treatment.sources}
    expected_ordinals: dict[str, int] = {s.source_id: 0 for s in treatment.sources}
    for segment in treatment.segments:
        if segment.source_id not in reconstructed or segment.segment_ordinal != expected_ordinals[segment.source_id]:
            raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "segment omitted, duplicated, or reordered")
        reconstructed[segment.source_id].extend(segment.payload)
        expected_ordinals[segment.source_id] += 1
    if any(bytes(reconstructed[s.source_id]) != s.payload for s in treatment.sources):
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "source-byte reconstruction failed")
    forbidden = [
        task["bounded_reference"].encode(),
        canonical_json(task["information_requirements"])[:-1],
        " | ".join(task["information_requirements"]).encode(),
    ]
    if any(value and value in treatment.payload for value in forbidden):
        raise PreflightError("CONTEXT_EQUIVALENCE_FAILED", "treatment contains evaluator-only metadata")
    return {
        "task_id": control.task_id,
        "source_ids": [s.source_id for s in control.sources],
        "source_hashes": [s.expected_hash for s in control.sources],
        "source_bytes_sha256": sha256(b"".join(s.payload for s in control.sources)),
        "segments": len(treatment.segments),
        "every_source_byte_exactly_once": True,
        "identical_task_prompt": True,
        "evaluator_metadata_absent": True,
    }


def context_hashes() -> tuple[dict[str, str], list[dict[str, Any]]]:
    hashes, proofs = {}, []
    for task in load_json(TASK_SET)["tasks"]:
        sources = read_sources(task)
        control, treatment = control_context(task, sources), treatment_context(task, sources)
        proofs.append(prove_equivalence(control, treatment, task))
        hashes[task["task_id"]] = {
            "control_sha256": sha256(control.payload), "treatment_sha256": sha256(treatment.payload),
            "control_utf8_bytes": len(control.payload), "treatment_utf8_bytes": len(treatment.payload),
        }
    return hashes, proofs


def constructor_hash() -> str:
    return sha256(Path(__file__).read_bytes())


def validate_model(model: dict[str, Any], maximum_context_bytes: int) -> None:
    missing = [field for field in REQUIRED_MODEL_FIELDS if field not in model]
    if missing:
        raise PreflightError("MODEL_REQUIREMENTS_UNSATISFIED", "missing model fields: " + ", ".join(missing))
    if not model["snapshot"] or not all(model[field] is True for field in (
        "immutable_snapshot", "temperature_control", "seed_control", "token_accounting"
    )):
        raise PreflightError("MODEL_REQUIREMENTS_UNSATISFIED", "model lacks frozen eligibility capabilities")
    # Exact tokenizer eligibility must be established by the provider adapter. A conservative
    # byte upper bound prevents silently accepting an obviously undersized window here.
    if int(model["context_window_tokens"]) < maximum_context_bytes + 2000:
        raise PreflightError("MODEL_REQUIREMENTS_UNSATISFIED", "context overflow under conservative preflight bound")


def prior_outcomes_absent() -> None:
    if any(path.exists() for path in RESERVED_OUTCOME_PATHS):
        raise PreflightError("EXPERIMENT_INVALID", "reserved outcome artifact already exists")


def verify_frozen_state() -> None:
    if git("rev-parse", FROZEN_COMMIT + "^{tree}") != FROZEN_TREE:
        raise PreflightError("EXPERIMENT_INVALID", "frozen preregistration tree identity mismatch")
    changed = git("diff", "--name-only", FROZEN_COMMIT, "--", "docs/issue-81/protocol.md",
                  "docs/issue-81/task-set.json", "docs/issue-81/source-manifest.json",
                  "docs/issue-81/validate_protocol.py")
    if changed:
        raise PreflightError("EXPERIMENT_INVALID", "frozen preregistration mutated after merge")
    subprocess.run([sys.executable, str(HERE / "validate_protocol.py")], cwd=ROOT, check=True,
                   stdout=subprocess.DEVNULL)
    prior_outcomes_absent()


def prepare_manifest(model: dict[str, Any], executor: str, timestamp: str) -> dict[str, Any]:
    verify_frozen_state()
    hashes, proofs = context_hashes()
    maximum = max(item[f"{condition}_utf8_bytes"] for item in hashes.values() for condition in ("control", "treatment"))
    validate_model(model, maximum)
    tasks = [task["task_id"] for task in load_json(TASK_SET)["tasks"]]
    manifest = {
        "schema_version": "1.0.0", "artifact_class": "EMPIRICAL_RUN",
        "experiment": "MS81", "protocol_version": "1.0.0", **frozen_identities(),
        "repository_commit": git("rev-parse", "HEAD"), "repository_tree": git("rev-parse", "HEAD^{tree}"),
        "constructor": {"version": "ORDINARY_RAW_V1+MINDSHIFT_STRUCTURED_V1", "sha256": constructor_hash()},
        "model": model,
        "generation": {"temperature": 0, "top_p": 1, "completions": 1, "output_token_cap": 2000,
                       "tools": False, "retrieval": False, "history": False, "prompt_cache": False},
        "seed_strategy": "810000 + task ordinal * 100 + replicate ordinal; identical within pair",
        "replicates": 20, "task_order": tasks,
        "condition_order": "low SHA-256 bit of MS81|task_id|replicate (0 control first; 1 treatment first)",
        "timestamp": timestamp, "executor": executor,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "context_hashes": hashes, "equivalence_proofs": proofs,
        "preflight": {"contamination": "PASS", "source_integrity": "PASS", "task_integrity": "PASS",
                      "context_equivalence": "PASS", "treatment_non_leakage": "PASS",
                      "context_size": "PASS_CONSERVATIVE_BYTE_BOUND", "model_eligibility": "PASS",
                      "custody": "PASS", "scoring": "PASS", "terminal": "PASS",
                      "prior_real_outcomes": "ABSENT", "state": "EXPERIMENT_EXECUTION_READY"},
    }
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> None:
    required = ("experiment", "protocol_version", "repository_commit", "repository_tree",
                "task_set_sha256", "source_manifest_sha256", "constructor", "model", "generation",
                "seed_strategy", "replicates", "task_order", "condition_order", "timestamp", "executor",
                "environment", "context_hashes", "preflight", "artifact_class")
    missing = [key for key in required if not manifest.get(key)]
    if missing or manifest.get("artifact_class") != "EMPIRICAL_RUN":
        raise PreflightError("EXECUTION_INFRASTRUCTURE_INCOMPLETE", "incomplete run manifest: " + ", ".join(missing))


def write_once(path: Path, payload: bytes, mode: int = 0o444) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, mode)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)


def pair_order(task_id: str, replicate: int) -> tuple[str, str]:
    bit = hashlib.sha256(f"MS81|{task_id}|{replicate}".encode()).digest()[-1] & 1
    return ("control", "treatment") if bit == 0 else ("treatment", "control")


def quality_score(correctness: int, relevant_used: int, omissions: int, unsupported: int,
                  stale: int, contradictions: int) -> float:
    values = (correctness, relevant_used, omissions, unsupported, stale, contradictions)
    if any(not isinstance(v, int) or not 0 <= v <= 4 for v in values):
        raise ValueError("all rubric values must be integer 0..4")
    raw = 12.5 * correctness + 12.5 * relevant_used - 6.25 * (omissions + unsupported + stale + contradictions)
    return min(100.0, max(0.0, raw))


def aggregate_pair_effects(effects: dict[str, list[float]]) -> tuple[dict[str, float], float]:
    if set(effects) != {f"MS81-T0{i}" for i in range(1, 5)} or any(len(v) != 20 for v in effects.values()):
        raise ValueError("exactly 20 pair effects for each of four frozen tasks required")
    medians = {task: float(statistics.median(values)) for task, values in effects.items()}
    return medians, statistics.mean(medians.values())


def final_item_score(evaluator_scores: list[dict[str, int]]) -> float:
    """Apply the frozen adjudication trigger and median-of-available rule."""
    if len(evaluator_scores) not in (2, 3):
        raise ValueError("two evaluator scores and, when triggered, one adjudicator score required")
    totals = [quality_score(**score) for score in evaluator_scores]
    count_names = ("omissions", "unsupported", "stale", "contradictions")
    needs_adjudication = abs(totals[0] - totals[1]) > 15 or any(
        abs(evaluator_scores[0][name] - evaluator_scores[1][name]) >= 2 for name in count_names
    )
    if needs_adjudication != (len(evaluator_scores) == 3):
        raise ValueError("adjudicator presence does not match the frozen trigger")
    return float(statistics.median(totals))


def percentile(values: list[float], p: float) -> float:
    ordered = sorted(values)
    index = (len(ordered) - 1) * p
    low, high = int(index), min(int(index) + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (index - low)


def bootstrap_interval(task_medians: dict[str, float]) -> tuple[float, float]:
    values = [task_medians[key] for key in sorted(task_medians)]
    if len(values) != 4:
        raise ValueError("four task medians required")
    means = []
    for n in range(4 ** 4):
        digits, x = [], n
        for _ in range(4):
            digits.append(x % 4); x //= 4
        means.append(statistics.mean(values[i] for i in digits))
    return percentile(means, .025), percentile(means, .975)


def terminal_state(*, valid: bool, valid_pairs: int, total_pairs: int, blinded: bool,
                   measures_complete: bool, kappa: float, task_medians: dict[str, float],
                   preference_treatment: int, preference_control: int) -> str:
    if not valid or total_pairs != 80 or valid_pairs < 72 or not blinded or not measures_complete:
        return "EXPERIMENT_INVALID"
    low, high = bootstrap_interval(task_medians)
    if (low < -5 and high > 5) or kappa < .40:
        return "INDETERMINATE"
    if low >= 5 and min(task_medians.values()) >= -5 and preference_treatment > preference_control:
        return "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED"
    if high <= -5 or sum(value < -5 for value in task_medians.values()) >= 2:
        return "MINDSHIFT_CONTEXT_DEGRADED_OUTPUT"
    return "NO_MEASURABLE_IMPROVEMENT"


def create_custody(batch_dir: Path, response_records: Iterable[dict[str, Any]]) -> None:
    records = list(response_records)
    if any(record.get("artifact_class") != "EMPIRICAL_RUN" for record in records):
        raise PreflightError("EXPERIMENT_INVALID", "synthetic or untyped response cannot enter empirical custody")
    public, key = [], []
    for record in records:
        evaluation_id = "E-" + secrets.token_hex(16)
        write_once(batch_dir / "evaluation" / f"{evaluation_id}.json", canonical_json({
            "evaluation_id": evaluation_id, "task_id": record["task_id"], "response": record["response"]
        }))
        public.append(evaluation_id)
        key.append({"evaluation_id": evaluation_id, "task_id": record["task_id"],
                    "replicate": record["replicate"], "condition": record["condition"],
                    "execution_order": record["execution_order"]})
    secrets.SystemRandom().shuffle(public)
    write_once(batch_dir / "evaluation-order.json", canonical_json(public))
    key_payload = canonical_json(key)
    write_once(batch_dir / "sealed" / "condition-key.json", key_payload, 0o400)
    write_once(batch_dir / "sealed" / "condition-key.sha256", (sha256(key_payload) + "\n").encode(), 0o400)


def generate(manifest_path: Path, batch_dir: Path, provider_command: list[str]) -> None:
    """Execute later via a JSON-stdin/JSON-stdout provider adapter; never called by preflight."""
    manifest_payload = manifest_path.read_bytes()
    manifest = json.loads(manifest_payload)
    validate_manifest(manifest)
    if manifest["preflight"]["state"] != "EXPERIMENT_EXECUTION_READY":
        raise PreflightError("EXECUTION_INFRASTRUCTURE_INCOMPLETE", "manifest did not pass preflight")
    write_once(batch_dir / "run-manifest.json", manifest_payload)
    records = []
    failures = []
    tasks = load_json(TASK_SET)["tasks"]
    for task_ordinal, task in enumerate(tasks, 1):
        sources = read_sources(task)
        contexts = {"control": control_context(task, sources), "treatment": treatment_context(task, sources)}
        for replicate in range(1, 21):
            seed = 810000 + task_ordinal * 100 + replicate
            pair_records = []
            for execution_order, condition in enumerate(pair_order(task["task_id"], replicate), 1):
                request = {"system": SYSTEM_INSTRUCTION, "user": contexts[condition].payload.decode("utf-8"),
                           "model": manifest["model"]["snapshot"], "temperature": 0, "top_p": 1,
                           "max_output_tokens": 2000, "seed": seed, "tools": [], "retrieval": False}
                attempts = []
                response = None
                completed = None
                for attempt in (1, 2):
                    completed = subprocess.run(provider_command, input=canonical_json(request), capture_output=True)
                    attempts.append({"attempt": attempt, "returncode": completed.returncode,
                                     "stderr_sha256": sha256(completed.stderr)})
                    if completed.returncode == 0:
                        try:
                            response = json.loads(completed.stdout)
                            break
                        except json.JSONDecodeError:
                            attempts[-1]["invalid_json"] = True
                if response is None or completed is None:
                    failure = {"task_id": task["task_id"], "replicate": replicate, "condition": condition,
                               "execution_order": execution_order, "request_sha256": sha256(canonical_json(request)),
                               "attempts": attempts, "status": "PERSISTENT_FAILURE"}
                    write_once(batch_dir / "failures" / f"{task['task_id']}-{replicate:02d}-{execution_order}.json",
                               canonical_json(failure))
                    failures.append(failure)
                    continue
                record = {"artifact_class": "EMPIRICAL_RUN", "task_id": task["task_id"], "replicate": replicate,
                          "condition": condition, "execution_order": execution_order, "request_sha256": sha256(canonical_json(request)),
                          "response": response, "raw_response_sha256": sha256(completed.stdout), "attempts": attempts}
                basename = f"{task['task_id']}-{replicate:02d}-{execution_order}"
                write_once(batch_dir / "raw" / f"{basename}.response", completed.stdout)
                write_once(batch_dir / "raw" / f"{basename}.json",
                           canonical_json(record))
                pair_records.append(record)
            if len(pair_records) == 2:
                records.extend(pair_records)
            elif pair_records:
                failures.append({"task_id": task["task_id"], "replicate": replicate,
                                 "status": "INCOMPLETE_PAIR_EXCLUDED"})
    invalid_pairs = len({(item["task_id"], item["replicate"]) for item in failures})
    status = {"total_pairs": 80, "valid_pairs": 80 - invalid_pairs, "invalid_pairs": invalid_pairs,
              "failures": failures,
              "state": "EXPERIMENT_INVALID" if invalid_pairs > 8 else "GENERATION_COMPLETE_BLINDING_READY"}
    write_once(batch_dir / "generation-status.json", canonical_json(status))
    if invalid_pairs > 8:
        raise PreflightError("EXPERIMENT_INVALID", "more than 10% of pairs are invalid")
    create_custody(batch_dir, records)


def cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    preflight = sub.add_parser("preflight")
    preflight.add_argument("--model", type=Path, required=True)
    preflight.add_argument("--executor", required=True)
    preflight.add_argument("--timestamp", required=True, help="UTC ISO-8601 timestamp fixed by the executor")
    preflight.add_argument("--output", type=Path, required=True)
    run = sub.add_parser("generate")
    run.add_argument("--manifest", type=Path, required=True)
    run.add_argument("--batch-dir", type=Path, required=True)
    run.add_argument("provider_command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            manifest = prepare_manifest(load_json(args.model), args.executor, args.timestamp)
            write_once(args.output, canonical_json(manifest))
            print("EXPERIMENT_EXECUTION_READY")
        else:
            if not args.provider_command:
                raise PreflightError("EXECUTION_INFRASTRUCTURE_INCOMPLETE", "provider command required")
            generate(args.manifest, args.batch_dir, args.provider_command)
    except PreflightError as exc:
        print(exc.state)
        print(exc.detail, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
