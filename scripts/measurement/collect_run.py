#!/usr/bin/env python3
"""Validate and seal a prospective InstrumentRunRecord with a companion manifest.

No research instrument is executed. Unknown observations are not inferred.
The record is never rewritten; only the separate provenance manifest is written.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from datetime import datetime
from pathlib import Path
from typing import Any


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def is_rfc3339_timestamp(value: str) -> bool:
    pattern = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})"
    if re.fullmatch(pattern, value) is None:
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def matches_type(value: Any, kind: str) -> bool:
    if kind == "object":
        return isinstance(value, dict)
    if kind == "array":
        return isinstance(value, list)
    if kind == "string":
        return isinstance(value, str)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind == "null":
        return value is None
    raise ValueError(f"unsupported schema type: {kind}")


def validate(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    kind = schema.get("type")
    if isinstance(kind, list):
        if not any(matches_type(instance, item) for item in kind):
            raise ValueError(f"{path}: expected one of {kind}")
    elif kind and not matches_type(instance, kind):
        raise ValueError(f"{path}: expected {kind}")

    if "const" in schema and instance != schema["const"]:
        raise ValueError(f"{path}: const mismatch")
    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"{path}: enum mismatch")

    if isinstance(instance, dict):
        missing = sorted(set(schema.get("required", [])) - set(instance))
        if missing:
            raise ValueError(f"{path}: missing required properties {missing}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(properties))
            if extras:
                raise ValueError(f"{path}: additional properties {extras}")
        for key, value in instance.items():
            if key in properties:
                validate(value, properties[key], f"{path}.{key}")
        if "minProperties" in schema and len(instance) < schema["minProperties"]:
            raise ValueError(f"{path}: too few properties")
    elif isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ValueError(f"{path}: too few items")
        if schema.get("uniqueItems"):
            encoded = [canonical_bytes(item) for item in instance]
            if len(encoded) != len(set(encoded)):
                raise ValueError(f"{path}: duplicate items")
        if "items" in schema:
            for index, value in enumerate(instance):
                validate(value, schema["items"], f"{path}[{index}]")
    elif isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ValueError(f"{path}: string too short")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, instance) is None:
            raise ValueError(f"{path}: pattern mismatch")
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if not math.isfinite(instance):
            raise ValueError(f"{path}: non-finite numbers are not valid JSON values")
        if instance < schema.get("minimum", float("-inf")):
            raise ValueError(f"{path}: below minimum")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--schema", type=Path, default=Path(__file__).resolve().parents[2] / "docs/measurement/schemas/instrument-run-record.schema.json")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    try:
        raw = args.record.read_bytes()
        record = json.loads(raw.decode("utf-8"))
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        validate(record, schema)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        parser.error(f"record/schema validation failed: {exc}")

    for timestamp_field in ("started_at", "ended_at"):
        timestamp = record[timestamp_field]
        if timestamp is not None and not is_rfc3339_timestamp(timestamp):
            parser.error(
                f"{timestamp_field} must be an RFC 3339 timestamp with timezone"
            )

    # Unknown values must be justified, and blocked pre-execution runs cannot
    # claim an execution disposition. This is a contract invariant beyond the
    # schema's vocabulary checks.
    unknown_subjects = {item["subject"] for item in record["unknowns"]}
    nullable_observations = {
        "instrument.version": record["instrument"]["version"],
        "started_at": record["started_at"],
        "ended_at": record["ended_at"],
        "inputs.repository": record["inputs"]["repository"],
        "inputs.commit_sha": record["inputs"]["commit_sha"],
        "inputs.manifest_sha256": record["inputs"]["manifest_sha256"],
        "environment.python_version": record["environment"]["python_version"],
        "environment.platform": record["environment"]["platform"],
        "environment.provider_identity": record["environment"]["provider_identity"],
        "environment.tool_state": record["environment"]["tool_state"],
        "expected.disposition": record["expected"]["disposition"],
        "observed.disposition": record["observed"]["disposition"],
        "resources.duration_ms": record["resources"]["duration_ms"],
        "resources.tokens": record["resources"]["tokens"],
        "resources.bytes": record["resources"]["bytes"],
        "resources.cost": record["resources"]["cost"],
    }
    for subject, value in nullable_observations.items():
        if value is None and subject not in unknown_subjects:
            parser.error(f"{subject} is null but has no corresponding unknown entry")
    for item in record["unknowns"]:
        if not item["reason"].strip():
            parser.error(f"unknown {item['subject']} requires a non-empty reason")
    blocker_statuses = {
        "PROVIDER_IDENTITY_BLOCKED",
        "ASSESSMENT_BLOCKED",
        "EXPERIMENT_INVALID",
        "BLOCKED_BY_REPOSITORY_PERMISSIONS",
    }
    if record["run_status"] in blocker_statuses and record["execution_disposition"] is not None:
        parser.error("blocked run must have null execution_disposition")
    if record["run_status"] == "PREFLIGHT_PASS" and record["execution_disposition"] is not None:
        parser.error("preflight-only run must have null execution_disposition")

    # Terminal run states must bind to the exact lifecycle disposition.
    # This prevents operational labels from drifting away from the recorded
    # execution outcome.
    terminal_dispositions = {
        "RUN_COMPLETED": "completed",
        "RUN_STOPPED": "stopped",
        "RUN_INCONCLUSIVE": "inconclusive",
    }
    expected_disposition = terminal_dispositions.get(record["run_status"])
    if expected_disposition is not None and record["execution_disposition"] != expected_disposition:
        parser.error(
            f"{record['run_status']} requires execution_disposition={expected_disposition!r}"
        )
    if expected_disposition is not None:
        required_observations = {
            "started_at": record["started_at"],
            "ended_at": record["ended_at"],
            "expected.disposition": record["expected"]["disposition"],
            "observed.disposition": record["observed"]["disposition"],
        }
        missing = [name for name, value in required_observations.items() if value is None]
        if missing:
            parser.error(
                f"{record['run_status']} requires non-null observations: {', '.join(missing)}"
            )

        if record["observed"]["disposition"] != record["execution_disposition"]:
            parser.error(
                f"{record['run_status']} requires observed.disposition to match "
                "execution_disposition"
            )

        if not record["observed"]["invariants"]:
            parser.error(f"{record['run_status']} requires at least one observed invariant")
    if record["run_status"] not in terminal_dispositions and record["execution_disposition"] is not None:
        parser.error("non-terminal or pre-execution status must have null execution_disposition")

    manifest = {
        "manifest_version": "1.0.0",
        "record_path": args.record.as_posix(),
        "record_sha256": sha256(canonical_bytes(record)),
        "record_byte_sha256": sha256(raw),
        "schema_path": args.schema.as_posix(),
        "schema_sha256": sha256(args.schema.read_bytes()),
        "canonicalization": "json.dumps(sort_keys=True,separators=(',',':')) + LF",
    }
    manifest["manifest_hash"] = sha256(canonical_bytes(manifest))
    output = args.manifest or args.record.with_name(args.record.stem + ".provenance.json")
    if output.resolve() == args.record.resolve():
        parser.error("provenance manifest must not overwrite the record")
    output.write_bytes(canonical_bytes(manifest))
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
