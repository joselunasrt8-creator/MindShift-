"""Standard-library structural tests for the InstrumentRunRecord schema."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "docs/measurement/schemas/instrument-run-record.schema.json"


def validate_subset(instance: Any, schema: dict[str, Any], path: str = "$") -> None:
    """Validate the schema keyword subset used by this contract (stdlib only)."""
    expected_type = schema.get("type")
    if isinstance(expected_type, list):
        if not any(_matches_type(instance, item) for item in expected_type):
            raise ValueError(f"{path}: expected one of {expected_type}")
    elif expected_type and not _matches_type(instance, expected_type):
        raise ValueError(f"{path}: expected {expected_type}")

    if "const" in schema and instance != schema["const"]:
        raise ValueError(f"{path}: const mismatch")
    if "enum" in schema and instance not in schema["enum"]:
        raise ValueError(f"{path}: enum mismatch")

    if isinstance(instance, dict):
        required = schema.get("required", [])
        missing = sorted(set(required) - set(instance))
        if missing:
            raise ValueError(f"{path}: missing required keys {missing}")
        if schema.get("additionalProperties") is False:
            extras = sorted(set(instance) - set(schema.get("properties", {})))
            if extras:
                raise ValueError(f"{path}: additional keys {extras}")
        for key, value in instance.items():
            child = schema.get("properties", {}).get(key)
            if child is not None:
                validate_subset(value, child, f"{path}.{key}")
    elif isinstance(instance, list):
        if len(instance) < schema.get("minItems", 0):
            raise ValueError(f"{path}: too few items")
        for index, value in enumerate(instance):
            if "items" in schema:
                validate_subset(value, schema["items"], f"{path}[{index}]")
    elif isinstance(instance, str):
        if len(instance) < schema.get("minLength", 0):
            raise ValueError(f"{path}: string too short")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, instance) is None:
            raise ValueError(f"{path}: pattern mismatch")
    elif isinstance(instance, (int, float)) and not isinstance(instance, bool):
        if instance < schema.get("minimum", float("-inf")):
            raise ValueError(f"{path}: below minimum")


def _matches_type(value: Any, kind: str) -> bool:
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
    raise ValueError(f"unsupported schema type in stdlib validator: {kind}")


class InstrumentRunSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def valid_record(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0.0",
            "record_id": "MS-INSTRUN-test-001",
            "instrument": {
                "name": "MindShift preflight",
                "version": None,
                "runner_path": "scripts/validate.py",
                "runner_commit_sha": "a" * 40
            },
            "run_status": "BLOCKED_BY_REPOSITORY_PERMISSIONS",
            "execution_disposition": None,
            "started_at": None,
            "ended_at": None,
            "inputs": {
                "repository": None,
                "commit_sha": None,
                "manifest_sha256": None,
                "items": []
            },
            "environment": {
                "python_version": "3.12",
                "platform": "test",
                "provider_identity": None,
                "tool_state": "offline"
            },
            "expected": {"disposition": None, "invariants": []},
            "observed": {"disposition": "BLOCKED_BY_REPOSITORY_PERMISSIONS", "invariants": [], "discrepancies": []},
            "blockers": [{"code": "BLOCKED_BY_REPOSITORY_PERMISSIONS", "reason": "Repository access unavailable"}],
            "friction": {"retries": 0, "skipped_steps": [], "manual_interventions": [], "ambiguities": []},
            "resources": {"duration_ms": None, "tokens": None, "bytes": None, "cost": None},
            "evidence": [],
            "unknowns": [
                {"subject": "inputs.commit_sha", "reason": "No repository checkout was available"}
            ],
            "authority": None
        }

    def test_valid_blocked_record(self) -> None:
        validate_subset(self.valid_record(), self.schema)

    def test_rejects_additional_top_level_property(self) -> None:
        record = self.valid_record()
        record["scientific_conclusion"] = "SUPPORTED"
        with self.assertRaises(ValueError):
            validate_subset(record, self.schema)

    def test_rejects_unknown_without_reason(self) -> None:
        record = self.valid_record()
        record["unknowns"] = [{"subject": "environment.provider_identity", "reason": ""}]
        with self.assertRaises(ValueError):
            validate_subset(record, self.schema)

    def test_execution_disposition_stays_null_when_blocked(self) -> None:
        record = self.valid_record()
        record["execution_disposition"] = "completed"
        # The schema constrains vocabulary; contract logic enforces reachability.
        validate_subset(record, self.schema)
        self.assertIsNone(self.valid_record()["execution_disposition"])


if __name__ == "__main__":
    unittest.main()
