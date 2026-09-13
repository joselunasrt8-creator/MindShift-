#!/usr/bin/env python3
"""Prospective v2 matched context-effect experiment for MindShift Issue #81.

The preflight is deterministic except for the optional provider-availability
probe. The run command refuses to overwrite any empirical artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import random
import re
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PROTOCOL = HERE / "protocol.md"
TASKS = HERE / "task-set.json"
SOURCES = HERE / "source-manifest.json"
MODEL = HERE / "model-settings.json"
V1_MANIFEST = HERE / "historical-v1-manifest.json"
V1_RECORD = HERE.parent / "experiment-record.md"

SYSTEM_INSTRUCTION = (
    "Answer the user's task using only the provided repository sources. Do not use external "
    "knowledge. Cite source paths for material claims. Preserve uncertainty and distinguish "
    "candidate output from authority, permission, legitimacy, execution eligibility, or "
    "validated findings."
)
SOURCE_INSTRUCTION = (
    "The following repository sources are the complete allowed source information. Use only "
    "them. Cite source paths. Treat model output as candidate output, not authority."
)
CATEGORIES = (
    "CURRENT STATE",
    "OBSERVATIONS",
    "PRIOR OBSERVATIONS",
    "SUPPORTED FINDINGS",
    "ASSUMPTIONS",
    "CONTRADICTIONS",
    "STALE OR SUPERSEDED",
)
CLASSIFIERS = (
    (re.compile(br"supersed|retir|withdraw|stale", re.I), "STALE OR SUPERSEDED"),
    (re.compile(br"contradict|conflict", re.I), "CONTRADICTIONS"),
    (re.compile(br"assum|unknown|limitation|uncertain", re.I), "ASSUMPTIONS"),
    (re.compile(br"prior|histor|lineage", re.I), "PRIOR OBSERVATIONS"),
    (re.compile(br"observation|evidence", re.I), "OBSERVATIONS"),
    (re.compile(br"finding|result|evaluation", re.I), "SUPPORTED FINDINGS"),
)
HEADING = re.compile(br"(?m)^#{1,6}[ \t]+[^\r\n]*(?:\r?\n|$)")
TERMINALS = {
    "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED",
    "NO_MEASURABLE_IMPROVEMENT",
    "MINDSHIFT_CONTEXT_DEGRADED_OUTPUT",
    "INDETERMINATE",
    "EXPERIMENT_INVALID",
}
RUBRIC_KEYS = (
    "correctness",
    "relevant_used",
    "critical_omissions",
    "unsupported_claims",
    "stale_context_errors",
    "contradictions",
    "uncertainty_calibration",
    "decision_usefulness",
)


class ExperimentError(RuntimeError):
    def __init__(self, state: str, detail: str):
        super().__init__(detail)
        self.state = state
        self.detail = detail


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def require_frozen_checkout() -> None:
    status = git("status", "--porcelain", "--untracked-files=all", "--", str(HERE.relative_to(ROOT)))
    if status:
        raise ExperimentError(
            "EXPERIMENT_INVALID",
            "v2 package is not frozen in the recorded commit; commit all v2 artifacts before preflight",
        )


def verify_v1_preserved() -> dict[str, str]:
    manifest = load(V1_MANIFEST)
    verified: dict[str, str] = {}
    for item in manifest["artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file() or digest(path.read_bytes()) != item["sha256"]:
            raise ExperimentError("EXPERIMENT_INVALID", f"v1 historical artifact changed: {item['path']}")
        verified[item["path"]] = item["sha256"]
    if "EXPERIMENT_INVALID" not in V1_RECORD.read_text(encoding="utf-8"):
        raise ExperimentError("EXPERIMENT_INVALID", "v1 terminal determination is not preserved")
    return verified


def write_once(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("xb") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ExperimentError("EXPERIMENT_INVALID", f"refusing to overwrite evidence: {path}") from exc


@dataclass(frozen=True)
class Source:
    source_id: str
    path: str
    commit: str
    sha256: str
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


def source_index() -> dict[str, dict[str, Any]]:
    manifest = load(SOURCES)
    records = manifest["sources"]
    if len(records) != len({item["source_id"] for item in records}):
        raise ExperimentError("EXPERIMENT_INVALID", "duplicate source ID")
    return {item["source_id"]: item for item in records}


def read_sources(task: dict[str, Any]) -> tuple[Source, ...]:
    manifest = load(SOURCES)
    indexed = source_index()
    if len(task["source_ids"]) != len(set(task["source_ids"])):
        raise ExperimentError("EXPERIMENT_INVALID", f"duplicate task source: {task['task_id']}")
    result: list[Source] = []
    for source_id in task["source_ids"]:
        if source_id not in indexed:
            raise ExperimentError("EXPERIMENT_INVALID", f"unmanifested source: {source_id}")
        item = indexed[source_id]
        try:
            payload = subprocess.check_output(
                ["git", "show", f'{manifest["source_commit"]}:{item["path"]}'], cwd=ROOT
            )
        except subprocess.CalledProcessError as exc:
            raise ExperimentError("EXPERIMENT_INVALID", f"missing frozen source: {source_id}") from exc
        actual = digest(payload)
        if actual != item["sha256"]:
            raise ExperimentError("EXPERIMENT_INVALID", f"source hash mismatch: {source_id}")
        result.append(Source(source_id, item["path"], manifest["source_commit"], actual, payload))
    if len(result) != len(task["source_ids"]):
        raise ExperimentError("EXPERIMENT_INVALID", "source omission")
    return tuple(result)


def shared_prefix(sources: tuple[Source, ...]) -> bytes:
    body = bytearray(SOURCE_INSTRUCTION.encode())
    body.extend(b"\n\n## SOURCE PROVENANCE\n")
    for source in sources:
        body.extend(
            f"- {source.source_id} | {source.path} | {source.commit} | {source.sha256}\n".encode()
        )
    return bytes(body)


def control_context(task: dict[str, Any], sources: tuple[Source, ...]) -> Context:
    body = bytearray(shared_prefix(sources))
    for source in sources:
        body.extend(f"\n--- SOURCE: {source.source_id} | {source.path} ---\n".encode())
        body.extend(source.payload)
    body.extend(b"\n\n--- TASK ---\n")
    body.extend(task["prompt"].encode())
    return Context("control", task["task_id"], task["prompt"], sources, (), bytes(body))


def split_source(source: Source, source_ordinal: int) -> tuple[Segment, ...]:
    starts = sorted(set([0] + [match.start() for match in HEADING.finditer(source.payload)]))
    result: list[Segment] = []
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
        result.append(Segment(source.source_id, source.path, source_ordinal, ordinal, category, payload))
    return tuple(result)


def treatment_context(task: dict[str, Any], sources: tuple[Source, ...]) -> Context:
    segments = tuple(segment for index, source in enumerate(sources) for segment in split_source(source, index))
    body = bytearray(shared_prefix(sources))
    for category in CATEGORIES:
        body.extend(f"\n## {category}\n".encode())
        for segment in (item for item in segments if item.category == category):
            body.extend(
                f"--- SEGMENT: {segment.source_id} | {segment.path} | {segment.segment_ordinal} ---\n".encode()
            )
            body.extend(segment.payload)
    body.extend(b"\n\n--- TASK ---\n")
    body.extend(task["prompt"].encode())
    return Context("treatment", task["task_id"], task["prompt"], sources, segments, bytes(body))


def prove_equivalence(task: dict[str, Any], control: Context, treatment: Context) -> dict[str, Any]:
    prompt = task["prompt"].encode()
    if control.prompt != treatment.prompt or control.prompt != task["prompt"]:
        raise ExperimentError("EXPERIMENT_INVALID", "task prompt mismatch")
    if control.payload.count(prompt) != 1 or treatment.payload.count(prompt) != 1:
        raise ExperimentError("EXPERIMENT_INVALID", "task prompt is not exact-once in both conditions")
    left = [(item.source_id, item.path, item.commit, item.sha256, item.payload) for item in control.sources]
    right = [(item.source_id, item.path, item.commit, item.sha256, item.payload) for item in treatment.sources]
    if left != right:
        raise ExperimentError("EXPERIMENT_INVALID", "source identity or bytes differ")
    sources = treatment.sources
    reconstructed = {source.source_id: bytearray() for source in sources}
    expected_ordinal = {source.source_id: 0 for source in sources}
    for segment in sorted(treatment.segments, key=lambda item: (item.source_ordinal, item.segment_ordinal)):
        if segment.segment_ordinal != expected_ordinal[segment.source_id]:
            raise ExperimentError("EXPERIMENT_INVALID", "segment omitted or duplicated")
        reconstructed[segment.source_id].extend(segment.payload)
        expected_ordinal[segment.source_id] += 1
    if any(bytes(reconstructed[source.source_id]) != source.payload for source in sources):
        raise ExperimentError("EXPERIMENT_INVALID", "treatment source reconstruction mismatch")
    forbidden = [
        task["bounded_reference"].encode(),
        canonical(task["information_requirements"]).strip(),
        " | ".join(task["information_requirements"]).encode(),
        b"Quality score:",
        b"MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED",
    ]
    if any(value and value in control.payload for value in forbidden):
        raise ExperimentError("EXPERIMENT_INVALID", "evaluator metadata leaked into control")
    if any(value and value in treatment.payload for value in forbidden):
        raise ExperimentError("EXPERIMENT_INVALID", "evaluator metadata leaked into treatment")
    if control.payload != control_context(task, control.sources).payload:
        raise ExperimentError("EXPERIMENT_INVALID", "control contains unauthorized material")
    if treatment.payload != treatment_context(task, treatment.sources).payload:
        raise ExperimentError("EXPERIMENT_INVALID", "treatment contains unauthorized material")
    return {
        "task_id": task["task_id"],
        "source_ids_equal": True,
        "source_hashes_equal": True,
        "source_bytes_reconstruct_exactly_once": True,
        "treatment_only_factual_content": False,
        "system_instruction_sha256": digest(SYSTEM_INSTRUCTION.encode()),
        "task_prompt_sha256": digest(prompt),
        "control_task_occurrences": 1,
        "treatment_task_occurrences": 1,
        "evaluator_metadata_absent": True,
        "control_sha256": digest(control.payload),
        "treatment_sha256": digest(treatment.payload),
        "control_utf8_bytes": len(control.payload),
        "treatment_utf8_bytes": len(treatment.payload),
    }


def artifact_hashes() -> dict[str, str]:
    return {
        path.name: digest(path.read_bytes())
        for path in (PROTOCOL, TASKS, SOURCES, MODEL, V1_MANIFEST, Path(__file__))
    }


def no_outcomes(output: Path) -> None:
    forbidden = (
        output / "raw",
        output / "evaluation",
        output / "scores",
        output / "preferences",
        output / "sealed" / "condition-key.json",
        output / "per-task-effects.json",
        output / "aggregate-result.json",
        output / "determination.json",
    )
    if any(path.exists() for path in forbidden):
        raise ExperimentError("EXPERIMENT_INVALID", "v2 outcome artifacts already exist")


def call_openai(payload: dict[str, Any], api_key: str, attempts: int = 3) -> tuple[dict[str, Any], bytes, int]:
    body = canonical(payload)
    last: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            load(MODEL)["endpoint"],
            data=body,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        started = time.perf_counter()
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                raw = response.read()
            elapsed = round((time.perf_counter() - started) * 1000)
            return json.loads(raw), raw, elapsed
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            last = RuntimeError(f"HTTP {exc.code}: {detail[:500]}")
            if exc.code not in (408, 409, 429, 500, 502, 503, 504) or attempt + 1 == attempts:
                break
            delay = min(30, 2 ** attempt * 3)
            time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(min(30, 2 ** attempt * 3))
    raise ExperimentError("EXPERIMENT_INVALID", f"provider request failed after frozen retries: {last}")


def api_payload(system: str, user: str, seed: int, max_tokens: int | None = None) -> dict[str, Any]:
    model = load(MODEL)
    return {
        "model": model["model"],
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": model["temperature"],
        "top_p": model["top_p"],
        "max_tokens": max_tokens or model["max_output_tokens"],
        "seed": seed,
    }


def response_text(response: dict[str, Any]) -> str:
    try:
        text = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise ExperimentError("EXPERIMENT_INVALID", "provider response lacks message content") from exc
    if not isinstance(text, str) or not text.strip():
        raise ExperimentError("EXPERIMENT_INVALID", "empty provider output")
    return text


def verify_response_model(response: dict[str, Any], stage: str) -> None:
    expected = load(MODEL)["model"]
    if response.get("model") != expected:
        raise ExperimentError(
            "EXPERIMENT_INVALID",
            f"{stage} model identity mismatch: {response.get('model')!r} != {expected!r}",
        )


def usage_cost_usd(usage: dict[str, Any] | None) -> float:
    if not isinstance(usage, dict):
        raise ExperimentError("EXPERIMENT_INVALID", "provider usage is missing")
    prompt_tokens = usage.get("prompt_tokens")
    completion_tokens = usage.get("completion_tokens")
    if not isinstance(prompt_tokens, int) or not isinstance(completion_tokens, int):
        raise ExperimentError("EXPERIMENT_INVALID", "provider token usage is incomplete")
    settings = load(MODEL)
    return (
        prompt_tokens * settings["pricing_usd_per_million_input_tokens"]
        + completion_tokens * settings["pricing_usd_per_million_output_tokens"]
    ) / 1_000_000


def provider_probe(api_key: str) -> dict[str, Any]:
    expected = load(MODEL)["model"]
    response, raw, latency = call_openai(
        api_payload(
            "Return only the token READY.",
            "This is a provider-availability probe, not an experimental task. Return READY.",
            810000,
            8,
        ),
        api_key,
    )
    returned = response.get("model")
    verify_response_model(response, "provider probe")
    if response_text(response).strip() != "READY":
        raise ExperimentError("EXPERIMENT_INVALID", "provider probe did not follow bounded instruction")
    return {
        "state": "PASS",
        "selected_model": expected,
        "returned_model": returned,
        "system_fingerprint": response.get("system_fingerprint"),
        "usage": response.get("usage"),
        "latency_ms": latency,
        "raw_response_sha256": digest(raw),
    }


def preflight(output: Path, api_key: str | None = None) -> dict[str, Any]:
    require_frozen_checkout()
    no_outcomes(output)
    v1_hashes = verify_v1_preserved()
    task_set = load(TASKS)
    if task_set["frozen_status"] != "FROZEN_BEFORE_OUTCOMES" or len(task_set["tasks"]) != 4:
        raise ExperimentError("EXPERIMENT_INVALID", "task cohort is not frozen")
    if len({task["task_id"] for task in task_set["tasks"]}) != 4:
        raise ExperimentError("EXPERIMENT_INVALID", "task IDs are not unique")
    model = load(MODEL)
    if model["generation_replicates_per_task"] != 3 or model["maximum_total_cost_usd"] != 5:
        raise ExperimentError("EXPERIMENT_INVALID", "sample size or cost cap changed")
    proofs = []
    max_bytes = 0
    for task in task_set["tasks"]:
        sources = read_sources(task)
        proof = prove_equivalence(task, control_context(task, sources), treatment_context(task, sources))
        max_bytes = max(max_bytes, proof["control_utf8_bytes"], proof["treatment_utf8_bytes"])
        proofs.append(proof)
    if max_bytes + model["max_output_tokens"] > model["context_window_tokens"]:
        raise ExperimentError("EXPERIMENT_INVALID", "context exceeds conservative byte-bound window check")
    provider = provider_probe(api_key) if api_key else {"state": "NOT_RUN_NO_CREDENTIAL"}
    return {
        "schema_version": "2.0.0",
        "experiment": "MS81-V2",
        "state": "PASS" if api_key else "DETERMINISTIC_PASS_PROVIDER_NOT_PROBED",
        "repository_commit": git("rev-parse", "HEAD"),
        "repository_tree": git("rev-parse", "HEAD^{tree}"),
        "source_commit": load(SOURCES)["source_commit"],
        "artifact_hashes": artifact_hashes(),
        "sample": {"tasks": 4, "replicates_per_task": 3, "pairs": 12, "outputs": 24},
        "system_instruction_sha256": digest(SYSTEM_INSTRUCTION.encode()),
        "equivalence_proofs": proofs,
        "rubric_frozen": True,
        "terminal_rules_frozen": True,
        "prior_v2_outcomes_absent": True,
        "v1_preserved": True,
        "v1_artifact_hashes": v1_hashes,
        "provider_probe": provider,
    }


def generation_seed(task_ordinal: int, replicate: int) -> int:
    return load(MODEL)["seed_base"] + task_ordinal * 100 + replicate


def condition_order(task_id: str, replicate: int) -> tuple[str, str]:
    bit = hashlib.sha256(f"MS81-V2|{task_id}|{replicate}".encode()).digest()[0] & 1
    return ("control", "treatment") if bit == 0 else ("treatment", "control")


def scoring_prompt(task: dict[str, Any], sources: tuple[Source, ...], answer: str, evaluation_id: str) -> str:
    source_text = "\n\n".join(
        f"--- SOURCE: {source.source_id} | {source.path} ---\n{source.payload.decode('utf-8')}"
        for source in sources
    )
    return f"""Evaluation ID: {evaluation_id}

Score the anonymous answer using only the frozen sources, task, requirements, bounded reference, and rubric below. You are not told the experimental condition. Do not infer or mention it. Return one JSON object and no markdown.

TASK:
{task['prompt']}

INFORMATION REQUIREMENTS:
{json.dumps(task['information_requirements'], ensure_ascii=False)}

BOUNDED REFERENCE:
{task['bounded_reference']}

RUBRIC (all integers 0..4):
- correctness: 0 materially wrong, 4 fully correct within sources
- relevant_used: 0 none, 4 more than 75% used correctly
- critical_omissions: count of missing required items, capped at 4
- unsupported_claims: count of material claims not entailed by sources, capped at 4
- stale_context_errors: count of explicit stale/superseded material treated as current, capped at 4
- contradictions: count of internal or explicit source contradictions, capped at 4
- uncertainty_calibration: 0 overclaims, 4 appropriately bounded
- decision_usefulness: 0 unusable, 4 directly useful for the task

Required JSON keys: {', '.join(RUBRIC_KEYS)}, rationale. Rationale must be concise and source-grounded.

ANONYMOUS ANSWER:
{answer}

FROZEN SOURCES:
{source_text}
"""


def parse_score(response: dict[str, Any]) -> dict[str, Any]:
    text = response_text(response).strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    try:
        score = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ExperimentError("EXPERIMENT_INVALID", "evaluator returned invalid JSON") from exc
    for key in RUBRIC_KEYS:
        if not isinstance(score.get(key), int) or not 0 <= score[key] <= 4:
            raise ExperimentError("EXPERIMENT_INVALID", f"invalid rubric value: {key}")
    if not isinstance(score.get("rationale"), str):
        raise ExperimentError("EXPERIMENT_INVALID", "missing scoring rationale")
    score["quality_score"] = quality_score(score)
    return score


def quality_score(score: dict[str, Any]) -> float:
    positives = score["correctness"] + score["relevant_used"] + score["uncertainty_calibration"] + score["decision_usefulness"]
    penalties = score["critical_omissions"] + score["unsupported_claims"] + score["stale_context_errors"] + score["contradictions"]
    return max(0.0, min(100.0, 6.25 * (positives - penalties)))


def needs_adjudication(a: dict[str, Any], b: dict[str, Any]) -> bool:
    counts = ("critical_omissions", "unsupported_claims", "stale_context_errors", "contradictions")
    return abs(a["quality_score"] - b["quality_score"]) > 15 or any(abs(a[key] - b[key]) >= 2 for key in counts)


def final_score(scores: list[dict[str, Any]]) -> dict[str, Any]:
    expected = 3 if needs_adjudication(scores[0], scores[1]) else 2
    if len(scores) != expected:
        raise ExperimentError("EXPERIMENT_INVALID", "adjudication custody mismatch")
    merged = {key: statistics.median([score[key] for score in scores]) for key in RUBRIC_KEYS}
    merged["quality_score"] = statistics.median([score["quality_score"] for score in scores])
    return merged


def weighted_kappa(left: list[int], right: list[int]) -> float:
    if len(left) != len(right) or not left:
        raise ExperimentError("EXPERIMENT_INVALID", "kappa inputs invalid")
    n = len(left)
    observed = sum(abs(a - b) / 4 for a, b in zip(left, right)) / n
    left_counts = [left.count(value) / n for value in range(5)]
    right_counts = [right.count(value) / n for value in range(5)]
    expected = sum(left_counts[i] * right_counts[j] * abs(i - j) / 4 for i in range(5) for j in range(5))
    return 1.0 if expected == 0 and observed == 0 else (0.0 if expected == 0 else 1 - observed / expected)


def bootstrap(pair_effects: dict[str, list[float]]) -> tuple[float, float]:
    settings = load(MODEL)
    rng = random.Random(settings["bootstrap_seed"])
    task_ids = sorted(pair_effects)
    values = []
    for _ in range(settings["bootstrap_resamples"]):
        medians = []
        for task_id in task_ids:
            effects = pair_effects[task_id]
            sample = [rng.choice(effects) for _ in effects]
            medians.append(statistics.median(sample))
        values.append(statistics.mean(medians))
    values.sort()
    return values[math.floor(0.025 * (len(values) - 1))], values[math.ceil(0.975 * (len(values) - 1))]


def terminal_state(aggregate: dict[str, Any]) -> str:
    if aggregate["valid_pairs"] < 11 or not aggregate["measures_complete"] or not aggregate["blinding_preserved"]:
        return "EXPERIMENT_INVALID"
    low, high = aggregate["bootstrap_95"]
    if aggregate["correctness_linear_weighted_kappa"] < 0.40 or (low < -5 and high > 5):
        return "INDETERMINATE"
    if (
        low >= 5
        and min(aggregate["task_medians"].values()) >= -5
        and aggregate["preference_treatment"] > aggregate["preference_control"]
        and aggregate["treatment_unsupported_plus_stale"] <= aggregate["control_unsupported_plus_stale"]
    ):
        return "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED"
    if high <= -5 or sum(value < -5 for value in aggregate["task_medians"].values()) >= 2:
        return "MINDSHIFT_CONTEXT_DEGRADED_OUTPUT"
    return "NO_MEASURABLE_IMPROVEMENT"


def run(output: Path, api_key: str) -> str:
    if output.exists():
        raise ExperimentError("EXPERIMENT_INVALID", "v2 execution directory already exists")
    prospective = preflight(output, api_key)
    output.mkdir(parents=True, exist_ok=False)
    write_once(output / "preflight-result.json", canonical(prospective))
    manifest = {
        "schema_version": "2.0.0",
        "experiment": "MS81-V2",
        "repository_commit": git("rev-parse", "HEAD"),
        "repository_tree": git("rev-parse", "HEAD^{tree}"),
        "source_commit": load(SOURCES)["source_commit"],
        "artifact_hashes": artifact_hashes(),
        "model_settings": load(MODEL),
        "system_instruction": SYSTEM_INSTRUCTION,
        "system_instruction_sha256": digest(SYSTEM_INSTRUCTION.encode()),
        "condition_order_rule": "low SHA-256 bit of MS81-V2|task-id|replicate",
        "blinding": "anonymous UUID evaluation IDs; key opened after scores and preferences seal",
        "started_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "preflight_sha256": digest(canonical(prospective)),
    }
    write_once(output / "run-manifest.json", canonical(manifest))

    running_cost_usd = usage_cost_usd(prospective["provider_probe"]["usage"])

    def accept_response(response: dict[str, Any], stage: str) -> float:
        nonlocal running_cost_usd
        verify_response_model(response, stage)
        cost = usage_cost_usd(response.get("usage"))
        running_cost_usd += cost
        if running_cost_usd > load(MODEL)["maximum_total_cost_usd"]:
            raise ExperimentError("EXPERIMENT_INVALID", "frozen maximum total cost exceeded")
        return cost

    tasks = load(TASKS)["tasks"]
    records: list[dict[str, Any]] = []
    condition_key: list[dict[str, Any]] = []
    for task_ordinal, task in enumerate(tasks, 1):
        sources = read_sources(task)
        contexts = {
            "control": control_context(task, sources),
            "treatment": treatment_context(task, sources),
        }
        for replicate in range(1, 4):
            seed = generation_seed(task_ordinal, replicate)
            for execution_order, condition in enumerate(condition_order(task["task_id"], replicate), 1):
                context = contexts[condition]
                request = api_payload(SYSTEM_INSTRUCTION, context.payload.decode("utf-8"), seed)
                response, raw, latency = call_openai(request, api_key)
                request_cost = accept_response(response, "generation")
                evaluation_id = "E-" + uuid.uuid4().hex
                record = {
                    "artifact_class": "EMPIRICAL_OUTCOME",
                    "task_id": task["task_id"],
                    "replicate": replicate,
                    "condition": condition,
                    "execution_order": execution_order,
                    "seed": seed,
                    "request_sha256": digest(canonical(request)),
                    "context_sha256": digest(context.payload),
                    "response_sha256": digest(raw),
                    "returned_model": response.get("model"),
                    "system_fingerprint": response.get("system_fingerprint"),
                    "usage": response.get("usage"),
                    "estimated_cost_usd": request_cost,
                    "latency_ms": latency,
                    "text": response_text(response),
                    "evaluation_id": evaluation_id,
                }
                basename = f"{task['task_id']}-R{replicate:02d}-O{execution_order}"
                write_once(output / "raw" / f"{basename}.provider.json", raw)
                write_once(output / "raw" / f"{basename}.record.json", canonical(record))
                anonymous = {
                    "evaluation_id": evaluation_id,
                    "task_id": task["task_id"],
                    "response": record["text"],
                    "usage": record["usage"],
                    "latency_ms": latency,
                }
                write_once(output / "evaluation" / "anonymous" / f"{evaluation_id}.json", canonical(anonymous))
                condition_key.append({
                    "evaluation_id": evaluation_id,
                    "task_id": task["task_id"],
                    "replicate": replicate,
                    "condition": condition,
                    "execution_order": execution_order,
                })
                records.append(record)

    key_payload = canonical(condition_key)
    write_once(output / "sealed" / "condition-key.json", key_payload)
    write_once(output / "sealed" / "condition-key.sha256", (digest(key_payload) + "\n").encode())

    score_records: dict[str, list[dict[str, Any]]] = {}
    initial_correctness = ([], [])
    for record in sorted(records, key=lambda item: item["evaluation_id"]):
        task = next(item for item in tasks if item["task_id"] == record["task_id"])
        sources = read_sources(task)
        scores = []
        for evaluator_pass in (1, 2):
            request = api_payload(
                "You are a blinded evaluator. Follow the supplied frozen rubric exactly and return only valid JSON.",
                scoring_prompt(task, sources, record["text"], record["evaluation_id"]),
                820000 + evaluator_pass,
                900,
            )
            response, raw, latency = call_openai(request, api_key)
            request_cost = accept_response(response, "evaluation")
            parsed = parse_score(response)
            parsed.update({
                "evaluation_id": record["evaluation_id"],
                "evaluator_pass": evaluator_pass,
                "returned_model": response.get("model"),
                "system_fingerprint": response.get("system_fingerprint"),
                "usage": response.get("usage"),
                "estimated_cost_usd": request_cost,
                "latency_ms": latency,
                "raw_response_sha256": digest(raw),
            })
            write_once(output / "scores" / "raw" / f"{record['evaluation_id']}-P{evaluator_pass}.provider.json", raw)
            write_once(output / "scores" / f"{record['evaluation_id']}-P{evaluator_pass}.json", canonical(parsed))
            scores.append(parsed)
            initial_correctness[evaluator_pass - 1].append(parsed["correctness"])
        if needs_adjudication(scores[0], scores[1]):
            request = api_payload(
                "You are a blinded adjudicator. Independently apply the supplied frozen rubric and return only valid JSON.",
                scoring_prompt(task, sources, record["text"], record["evaluation_id"]),
                820003,
                900,
            )
            response, raw, latency = call_openai(request, api_key)
            request_cost = accept_response(response, "adjudication")
            parsed = parse_score(response)
            parsed.update({
                "evaluation_id": record["evaluation_id"],
                "evaluator_pass": 3,
                "returned_model": response.get("model"),
                "system_fingerprint": response.get("system_fingerprint"),
                "usage": response.get("usage"),
                "estimated_cost_usd": request_cost,
                "latency_ms": latency,
                "raw_response_sha256": digest(raw),
            })
            write_once(output / "scores" / "raw" / f"{record['evaluation_id']}-P3.provider.json", raw)
            write_once(output / "scores" / f"{record['evaluation_id']}-P3.json", canonical(parsed))
            scores.append(parsed)
        score_records[record["evaluation_id"]] = scores

    final_scores = {evaluation_id: final_score(scores) for evaluation_id, scores in score_records.items()}
    write_once(output / "scores" / "final-scores.json", canonical(final_scores))

    preferences: dict[str, str] = {}
    for task in tasks:
        sources = read_sources(task)
        source_text = "\n\n".join(
            f"--- SOURCE: {source.source_id} | {source.path} ---\n{source.payload.decode('utf-8')}"
            for source in sources
        )
        for replicate in range(1, 4):
            pair = [item for item in records if item["task_id"] == task["task_id"] and item["replicate"] == replicate]
            pair.sort(key=lambda item: item["evaluation_id"])
            first, second = pair
            prompt = f"""Choose which anonymous answer better satisfies the task using the supplied sources. Ignore style unless it affects correctness or usefulness. Return only JSON with keys preference (X, Y, or TIE) and rationale. You are not told either experimental condition.

TASK: {task['prompt']}
BOUNDED REFERENCE: {task['bounded_reference']}
INFORMATION REQUIREMENTS: {json.dumps(task['information_requirements'])}

ANSWER X ({first['evaluation_id']}):
{first['text']}

ANSWER Y ({second['evaluation_id']}):
{second['text']}

SOURCES:
{source_text}
"""
            request = api_payload("You are a blinded pairwise evaluator. Return only valid JSON.", prompt, 830000 + replicate, 500)
            response, raw, latency = call_openai(request, api_key)
            request_cost = accept_response(response, "pairwise preference")
            text = response_text(response).strip()
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError as exc:
                raise ExperimentError("EXPERIMENT_INVALID", "pair evaluator returned invalid JSON") from exc
            if parsed.get("preference") not in ("X", "Y", "TIE"):
                raise ExperimentError("EXPERIMENT_INVALID", "pair evaluator preference invalid")
            preferred_id = "TIE" if parsed["preference"] == "TIE" else (first if parsed["preference"] == "X" else second)["evaluation_id"]
            pair_id = f"{task['task_id']}-R{replicate:02d}"
            result = {
                "pair_id": pair_id,
                "answer_x": first["evaluation_id"],
                "answer_y": second["evaluation_id"],
                "preferred_evaluation_id": preferred_id,
                "rationale": parsed.get("rationale"),
                "usage": response.get("usage"),
                "estimated_cost_usd": request_cost,
                "latency_ms": latency,
                "raw_response_sha256": digest(raw),
            }
            write_once(output / "preferences" / "raw" / f"{pair_id}.provider.json", raw)
            write_once(output / "preferences" / f"{pair_id}.json", canonical(result))
            preferences[pair_id] = preferred_id

    key = {item["evaluation_id"]: item for item in condition_key}
    pair_effects: dict[str, list[float]] = {task["task_id"]: [] for task in tasks}
    preference_counts = {"treatment": 0, "control": 0, "tie": 0}
    condition_penalties = {"treatment": 0.0, "control": 0.0}
    for task in tasks:
        for replicate in range(1, 4):
            pair_ids = [item["evaluation_id"] for item in condition_key if item["task_id"] == task["task_id"] and item["replicate"] == replicate]
            by_condition = {key[item]["condition"]: item for item in pair_ids}
            effect = final_scores[by_condition["treatment"]]["quality_score"] - final_scores[by_condition["control"]]["quality_score"]
            pair_effects[task["task_id"]].append(effect)
            preferred = preferences[f"{task['task_id']}-R{replicate:02d}"]
            if preferred == "TIE":
                preference_counts["tie"] += 1
            else:
                preference_counts[key[preferred]["condition"]] += 1
            for condition, evaluation_id in by_condition.items():
                condition_penalties[condition] += final_scores[evaluation_id]["unsupported_claims"] + final_scores[evaluation_id]["stale_context_errors"]

    task_medians = {task_id: statistics.median(values) for task_id, values in pair_effects.items()}
    interval = bootstrap(pair_effects)
    generation_metrics: dict[str, dict[str, float]] = {}
    for condition in ("control", "treatment"):
        selected = [record for record in records if record["condition"] == condition]
        generation_metrics[condition] = {
            "outputs": len(selected),
            "context_utf8_bytes_total": sum(
                len((control_context if condition == "control" else treatment_context)(
                    next(task for task in tasks if task["task_id"] == record["task_id"]),
                    read_sources(next(task for task in tasks if task["task_id"] == record["task_id"])),
                ).payload)
                for record in selected
            ),
            "prompt_tokens_total": sum(record["usage"]["prompt_tokens"] for record in selected),
            "completion_tokens_total": sum(record["usage"]["completion_tokens"] for record in selected),
            "latency_ms_total": sum(record["latency_ms"] for record in selected),
            "estimated_cost_usd": sum(record["estimated_cost_usd"] for record in selected),
        }
    aggregate = {
        "valid_pairs": 12,
        "total_pairs": 12,
        "measures_complete": True,
        "blinding_preserved": True,
        "pair_effects": pair_effects,
        "task_medians": task_medians,
        "aggregate_mean_task_median_effect": statistics.mean(task_medians.values()),
        "bootstrap_95": interval,
        "correctness_linear_weighted_kappa": weighted_kappa(*initial_correctness),
        "preference_treatment": preference_counts["treatment"],
        "preference_control": preference_counts["control"],
        "preference_ties": preference_counts["tie"],
        "treatment_unsupported_plus_stale": condition_penalties["treatment"],
        "control_unsupported_plus_stale": condition_penalties["control"],
        "generation_metrics": generation_metrics,
        "total_experiment_estimated_cost_usd": running_cost_usd,
    }
    determination = terminal_state(aggregate)
    if determination not in TERMINALS:
        raise ExperimentError("EXPERIMENT_INVALID", "terminal mapping produced an unauthorized state")
    write_once(output / "per-task-effects.json", canonical({"pair_effects": pair_effects, "task_medians": task_medians}))
    write_once(output / "aggregate-result.json", canonical(aggregate))
    write_once(output / "determination.json", canonical({
        "experiment": "MS81-V2",
        "terminal_determination": determination,
        "claim_boundary": "Frozen model, tasks, sources, constructors, and evaluator only",
        "completed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }))
    limitations = """# MS81 v2 limitations

- Four repository-specific tasks limit external validity.
- Three replicates per task provide only bounded Phase 1 evidence.
- Provider-side nondeterminism may remain despite temperature zero and paired seeds.
- The treatment uses lexical heading classification; labels are hypotheses, not validated truth states.
- Treatment contexts are longer because structural syntax is part of the intervention.
- The same model snapshot generated and blindly evaluated outputs; model-as-judge bias may remain.
- Public-repository familiarity cannot be completely excluded, although generation was instructed to use only supplied sources.
- A supported result would not establish cross-model transfer, production readiness, authority, legitimacy, permission, or economic value.
"""
    write_once(output / "limitations.md", limitations.encode())
    summary = f"""# MindShift Issue #81 v2 execution summary

**Terminal determination:** `{determination}`

**Repository commit:** `{manifest['repository_commit']}`

**Model:** `{load(MODEL)['model']}`

**Pairs:** 12 / 12 complete

**Aggregate mean task-median effect:** {aggregate['aggregate_mean_task_median_effect']:.2f}

**95% task-stratified paired bootstrap interval:** [{interval[0]:.2f}, {interval[1]:.2f}]

**Blinded preferences:** treatment {preference_counts['treatment']}, control {preference_counts['control']}, ties {preference_counts['tie']}

See `preflight-result.json`, `run-manifest.json`, `raw/`, `evaluation/`,
`scores/`, `preferences/`, `per-task-effects.json`, `aggregate-result.json`,
`determination.json`, and `limitations.md` for the complete preserved package.
"""
    write_once(output / "execution-summary.md", summary.encode())
    return determination


def cli() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("preflight")
    check.add_argument("--output", type=Path, default=HERE / "execution")
    check.add_argument("--require-api", action="store_true")
    execute = sub.add_parser("run")
    execute.add_argument("--output", type=Path, default=HERE / "execution")
    args = parser.parse_args()
    try:
        if args.command == "preflight":
            key = os.environ.get("OPENAI_API_KEY") if args.require_api else None
            if args.require_api and not key:
                raise ExperimentError("EXPERIMENT_INVALID", "OPENAI_API_KEY is unavailable")
            print(json.dumps(preflight(args.output, key), indent=2, sort_keys=True))
        else:
            key = os.environ.get("OPENAI_API_KEY")
            if not key:
                raise ExperimentError("EXPERIMENT_INVALID", "OPENAI_API_KEY is unavailable")
            print(run(args.output, key))
    except ExperimentError as exc:
        print(exc.state)
        print(exc.detail, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(cli())
