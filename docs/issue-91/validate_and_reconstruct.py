#!/usr/bin/env python3
"""Deterministically validate and reconstruct the Issue #91 blinded bundle.

This program performs no network or model calls and makes no recommendation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INPUT = HERE / "assessment-input"
OUTCOMES = HERE / "outcomes"
DETERMINATIONS = {"CONTINUE", "DEFER", "STOP", "INDETERMINATE"}


class ValidationError(ValueError):
    """A structural or protocol admissibility failure."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"invalid JSON {path}: {exc}") from exc


def parse_time(value: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"invalid timestamp: {value!r}") from exc
    if parsed.tzinfo is None:
        raise ValidationError("timestamp must include an offset")
    return parsed


def git_bytes(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{path}"], cwd=ROOT, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as exc:
        raise ValidationError(f"unresolved source identity: {commit}:{path}") from exc


def git_timestamp(commit: str) -> datetime:
    try:
        value = subprocess.check_output(
            ["git", "show", "-s", "--format=%cI", commit], cwd=ROOT, text=True
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise ValidationError(f"unresolved source commit: {commit}") from exc
    return parse_time(value)


def require_fields(record: dict[str, Any], required: list[str], kind: str) -> None:
    if not isinstance(record, dict):
        raise ValidationError(f"malformed {kind}: expected object")
    missing = sorted(set(required) - set(record))
    if missing:
        raise ValidationError(f"missing required {kind} fields: {missing}")


def validate_work_item(item: dict[str, Any], evidence: list[dict[str, Any]]) -> None:
    schema = load_json(HERE / "schemas/work-item.schema.json")
    required = schema["required"]
    require_fields(item, required, "work item")
    if set(item) != set(required):
        raise ValidationError("work item contains unrecognized fields")
    if not isinstance(item["work_item_id"], str) or not item["work_item_id"].startswith("MS91-WI-"):
        raise ValidationError("invalid work_item_id")
    scalar_strings = ["repository", "proposed_work", "target_uncertainty", "downstream_decision", "reconstruction_procedure"]
    if any(not isinstance(item[key], str) or not item[key] for key in scalar_strings):
        raise ValidationError("malformed work item string")
    for key in ("expected_evidence", "known_prerequisites", "known_blockers", "known_alternatives", "evidence_refs", "excluded_post_cutoff_material", "known_limitations"):
        if not isinstance(item[key], list) or any(not isinstance(v, str) or not v for v in item[key]):
            raise ValidationError(f"malformed work item list: {key}")
    if not item["expected_evidence"] or not item["evidence_refs"]:
        raise ValidationError("work item evidence cannot be empty")
    if item["estimated_cost"] is not None and not isinstance(item["estimated_cost"], str):
        raise ValidationError("malformed estimated_cost")
    cutoff = parse_time(item["cutoff_timestamp"])
    refs = item["evidence_refs"]
    if len(refs) != len(set(refs)) or set(refs) != set(item["evidence_hashes"]):
        raise ValidationError("invalid or unresolved evidence references")
    matches = [entry for entry in evidence if entry.get("evidence_id") in refs]
    if len(matches) != len(refs):
        raise ValidationError("invalid or unresolved evidence references")
    for entry in matches:
        require_fields(entry, ["evidence_id", "repository", "commit", "commit_timestamp", "path", "bundle_path", "sha256"], "evidence")
        if set(entry) != {"evidence_id", "repository", "commit", "commit_timestamp", "path", "bundle_path", "sha256"}:
            raise ValidationError("malformed evidence record")
        if entry["repository"] != item["repository"]:
            raise ValidationError("source identity mismatch")
        recorded_commit_time = parse_time(entry["commit_timestamp"])
        resolved_commit_time = git_timestamp(entry["commit"])
        if recorded_commit_time != resolved_commit_time:
            raise ValidationError("source identity/timestamp mismatch")
        if recorded_commit_time > cutoff:
            raise ValidationError("evidence outside cutoff boundary")
        source = git_bytes(entry["commit"], entry["path"])
        bundle = INPUT / entry["bundle_path"]
        if not bundle.is_file() or bundle.is_symlink():
            raise ValidationError("invalid evidence bundle path")
        digest = sha256(source)
        if digest != entry["sha256"] or digest != item["evidence_hashes"][entry["evidence_id"]] or bundle.read_bytes() != source:
            raise ValidationError("source identity/hash mismatch")
    primary = item["source_issue_or_artifact"]
    require_fields(primary, ["identity", "commit", "path", "sha256"], "primary source")
    if primary["commit"] != matches[0]["commit"] or primary["path"] != matches[0]["path"] or primary["sha256"] != matches[0]["sha256"]:
        raise ValidationError("source identity/hash mismatch")
    if git_timestamp(primary["commit"]) != cutoff:
        raise ValidationError("primary source commit does not define cutoff")


def assessment_input_hash(item: dict[str, Any]) -> str:
    return sha256(canonical_bytes(item))


def assessment_output_hash(assessment: dict[str, Any]) -> str:
    return sha256(canonical_bytes({key: value for key, value in assessment.items() if key != "output_hash"}))


def validate_assessment(assessment: dict[str, Any], item: dict[str, Any]) -> None:
    schema = load_json(HERE / "schemas/assessment.schema.json")
    required = schema["required"]
    require_fields(assessment, required, "assessment")
    if set(assessment) != set(required):
        raise ValidationError("assessment contains unrecognized fields")
    if assessment["determination"] not in DETERMINATIONS:
        raise ValidationError("invalid determination")
    if assessment["authority"] is not None:
        raise ValidationError("authority must be null")
    if assessment["execution_eligible"] is not False:
        raise ValidationError("execution_eligible must be false")
    if assessment["work_item_id"] != item["work_item_id"]:
        raise ValidationError("assessment work item mismatch")
    if not set(assessment["evidence_refs"]) <= set(item["evidence_refs"]):
        raise ValidationError("invalid or unresolved evidence references")
    if assessment["input_hash"] != assessment_input_hash(item):
        raise ValidationError("assessment input hash mismatch")
    if assessment["output_hash"] != assessment_output_hash(assessment):
        raise ValidationError("assessment output hash mismatch")


def inventory(base: Path) -> dict[str, str]:
    result = {}
    for path in sorted(base.rglob("*")):
        if path.is_symlink():
            raise ValidationError(f"links forbidden in bundle: {path}")
        if path.is_file():
            result[path.relative_to(base).as_posix()] = sha256(path.read_bytes())
    return result


def manifest_digest(manifest: dict[str, Any]) -> str:
    return sha256(canonical_bytes({key: value for key, value in manifest.items() if key != "manifest_hash"}))


def validate_manifest(manifest: dict[str, Any]) -> None:
    if manifest.get("manifest_hash") != manifest_digest(manifest):
        raise ValidationError("manifest mismatch")
    bindings = manifest.get("bindings", {})
    for relative, expected in bindings.items():
        path = HERE / relative
        if not path.is_file() or path.is_symlink() or sha256(path.read_bytes()) != expected:
            raise ValidationError(f"manifest mismatch: {relative}")


def reconstruct(destination: Path, manifest: dict[str, Any]) -> dict[str, str]:
    if destination.exists() and any(destination.iterdir()):
        raise ValidationError("reconstruction destination must be empty")
    destination.mkdir(parents=True, exist_ok=True)
    expected = manifest["assessment_bundle"]
    actual = inventory(INPUT)
    input_expected = {key.removeprefix("assessment-input/"): value for key, value in expected.items() if key.startswith("assessment-input/")}
    if actual != input_expected:
        raise ValidationError("manifest mismatch: assessment input inventory")
    for relative in sorted(actual):
        source = INPUT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    schema_source = HERE / "schemas/assessment.schema.json"
    shutil.copyfile(schema_source, destination / "assessment.schema.json")
    result = inventory(destination)
    expected_result = dict(input_expected)
    expected_result["assessment.schema.json"] = sha256(schema_source.read_bytes())
    if result != expected_result:
        raise ValidationError("reconstructed bundle mismatch")
    return result


def preflight() -> dict[str, Any]:
    manifest = load_json(HERE / "freeze-manifest.json")
    validate_manifest(manifest)
    cohort = load_json(INPUT / "cohort.json")
    require_fields(cohort, ["schema_version", "status", "temporal_rule", "work_items", "evidence"], "cohort")
    if set(cohort) != {"schema_version", "status", "temporal_rule", "work_items", "evidence"}:
        raise ValidationError("malformed cohort record")
    if cohort["status"] != "FROZEN_NO_ASSESSMENTS" or not isinstance(cohort["work_items"], list) or not isinstance(cohort["evidence"], list):
        raise ValidationError("malformed cohort record")
    ids = [item.get("work_item_id") for item in cohort["work_items"] if isinstance(item, dict)]
    if len(ids) != len(cohort["work_items"]) or len(ids) != len(set(ids)) or ids != manifest["cohort_identities"]:
        raise ValidationError("malformed cohort records or manifest mismatch")
    for item in cohort["work_items"]:
        scoped = [entry for entry in cohort["evidence"] if entry.get("bundle_path", "").startswith(f"sources/{item['work_item_id']}/")]
        validate_work_item(item, scoped)
    if sorted(entry["sha256"] for entry in cohort["evidence"]) != sorted(manifest["source_hashes"]):
        raise ValidationError("manifest mismatch: source hashes")
    outcome_hashes = set(load_json(OUTCOMES / "manifest.json")["outcomes"][i]["sha256"] for i in range(len(ids)))
    for path in INPUT.rglob("*"):
        if path.is_symlink() or (path.is_file() and (b"outcomes/" in path.read_bytes() or any(value.encode() in path.read_bytes() for value in outcome_hashes))):
            raise ValidationError("outcome leakage")
    forbidden = [INPUT / name for name in ("assessments.json", "results.json", "determination.json")]
    if any(path.exists() for path in forbidden):
        raise ValidationError("continuation assessments already generated")
    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        one = reconstruct(Path(first), manifest)
        two = reconstruct(Path(second), manifest)
        if one != two:
            raise ValidationError("reconstruction is not reproducible")
        bundle_hash = sha256(canonical_bytes(one))
    return {
        "schema_version": "1.0.0",
        "result": "PASS",
        "terminal_determination": "FROZEN_FOR_BLINDED_ASSESSMENT",
        "model_calls_performed": 0,
        "cohort_size": len(ids),
        "cohort_identities": ids,
        "checks": {
            "work_items_validate": True,
            "source_identities_and_hashes_resolve": True,
            "cutoff_constraints_pass": True,
            "outcome_material_reachable": False,
            "reconstruction_byte_identical": True,
            "manifest_bound_identities_match": True,
            "continuation_assessments_generated": False
        },
        "manifest_hash": manifest["manifest_hash"],
        "assessment_bundle_inventory_hash": bundle_hash
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path)
    parser.add_argument("--reconstruct", type=Path)
    args = parser.parse_args()
    report = preflight()
    if args.reconstruct:
        reconstruct(args.reconstruct, load_json(HERE / "freeze-manifest.json"))
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
