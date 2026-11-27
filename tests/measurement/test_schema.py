"""Standard-library schema and collector contract tests."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "docs/measurement/schemas/instrument-run-record.schema.json"
COLLECTOR = ROOT / "scripts/measurement/collect_run.py"


class InstrumentRunRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))

    def valid_record(self):
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
            "inputs": {"repository": None, "commit_sha": None, "manifest_sha256": None, "items": []},
            "environment": {"python_version": "3.12", "platform": "test", "provider_identity": None, "tool_state": "offline"},
            "expected": {"disposition": None, "invariants": []},
            "observed": {"disposition": "BLOCKED_BY_REPOSITORY_PERMISSIONS", "invariants": [], "discrepancies": []},
            "blockers": [{"code": "BLOCKED_BY_REPOSITORY_PERMISSIONS", "reason": "Repository access unavailable"}],
            "friction": {"retries": 0, "skipped_steps": [], "manual_interventions": [], "ambiguities": []},
            "resources": {"duration_ms": None, "tokens": None, "bytes": None, "cost": None},
            "evidence": [],
            "unknowns": [
                {"subject": "instrument.version", "reason": "No released instrument version was assigned"},
                {"subject": "started_at", "reason": "Execution could not begin"},
                {"subject": "ended_at", "reason": "Execution could not begin"},
                {"subject": "inputs.repository", "reason": "No repository checkout was available"},
                {"subject": "inputs.commit_sha", "reason": "No repository checkout was available"},
                {"subject": "inputs.manifest_sha256", "reason": "No input manifest was available"},
                {"subject": "environment.provider_identity", "reason": "Provider identity was not available"},
                {"subject": "expected.disposition", "reason": "No expected disposition was declared"},
                {"subject": "observed.disposition", "reason": "No runner disposition was returned"},
                {"subject": "resources.duration_ms", "reason": "The run did not start"},
                {"subject": "resources.tokens", "reason": "Token usage was not observable"},
                {"subject": "resources.bytes", "reason": "Byte usage was not measured"},
                {"subject": "resources.cost", "reason": "Cost was not measured"}
            ],
            "authority": None
        }

    def test_blocked_record_validates_without_external_dependencies(self):
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            manifest_path = Path(temp) / "record.provenance.json"
            record_path.write_text(json.dumps(self.valid_record()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path), "--manifest", str(manifest_path)],
                capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(manifest_path.is_file())
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["record_sha256"]), 64)

    def test_rejects_unrecognized_top_level_field(self):
        record = self.valid_record()
        record["scientific_conclusion"] = "SUPPORTED"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run([sys.executable, str(COLLECTOR), str(record_path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_rejects_null_without_structured_unknown(self):
        record = self.valid_record()
        record["environment"]["provider_identity"] = None
        record["unknowns"] = [item for item in record["unknowns"] if item["subject"] != "environment.provider_identity"]
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run([sys.executable, str(COLLECTOR), str(record_path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_rejects_blocker_with_execution_disposition(self):
        record = self.valid_record()
        record["execution_disposition"] = "completed"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run([sys.executable, str(COLLECTOR), str(record_path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_terminal_status_requires_matching_disposition(self):
        for status, disposition in (
            ("RUN_COMPLETED", "completed"),
            ("RUN_STOPPED", "stopped"),
            ("RUN_INCONCLUSIVE", "inconclusive"),
        ):
            with self.subTest(status=status):
                record = self.valid_record()
                record["run_status"] = status
                record["execution_disposition"] = disposition
                record["started_at"] = "2026-11-27T05:00:00Z"
                record["ended_at"] = "2026-11-27T05:00:01Z"
                record["expected"]["disposition"] = disposition
                record["observed"]["disposition"] = disposition
                record["observed"]["invariants"] = ["terminal disposition observed"]
                record["unknowns"] = [
                    item for item in record["unknowns"]
                    if item["subject"] not in {
                        "started_at", "ended_at",
                        "expected.disposition", "observed.disposition",
                    }
                ]
                with tempfile.TemporaryDirectory() as temp:
                    record_path = Path(temp) / "record.json"
                    record_path.write_text(json.dumps(record), encoding="utf-8")
                    manifest_path = Path(temp) / "record.provenance.json"
                    result = subprocess.run(
                        [sys.executable, str(COLLECTOR), str(record_path),
                         "--manifest", str(manifest_path)],
                        capture_output=True, text=True, check=False
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(manifest_path.is_file())

    def test_rejects_terminal_record_missing_required_observations(self):
        record = self.valid_record()
        record["run_status"] = "RUN_COMPLETED"
        record["execution_disposition"] = "completed"
        record["started_at"] = "2026-11-27T05:00:00Z"
        record["ended_at"] = "2026-11-27T05:00:01Z"
        record["expected"]["disposition"] = "completed"
        record["observed"]["disposition"] = "completed"
        record["observed"]["invariants"] = []
        record["unknowns"] = [
            item for item in record["unknowns"]
            if item["subject"] not in {
                "started_at", "ended_at",
                "expected.disposition", "observed.disposition",
            }
        ]
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("requires at least one observed invariant", result.stderr)


    def test_rejects_terminal_observed_disposition_mismatch(self):
        record = self.valid_record()
        record["run_status"] = "RUN_COMPLETED"
        record["execution_disposition"] = "completed"
        record["started_at"] = "2026-11-27T05:00:00Z"
        record["ended_at"] = "2026-11-27T05:00:01Z"
        record["expected"]["disposition"] = "completed"
        record["observed"]["disposition"] = "stopped"
        record["observed"]["invariants"] = ["terminal outcome observed"]
        record["unknowns"] = [
            item for item in record["unknowns"]
            if item["subject"] not in {
                "started_at", "ended_at",
                "expected.disposition", "observed.disposition",
            }
        ]
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("observed.disposition to match", result.stderr)

    def test_rejects_invalid_timestamp(self):
        record = self.valid_record()
        record["started_at"] = "yesterday"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("RFC 3339 timestamp", result.stderr)

    def test_rejects_non_finite_number(self):
        record = self.valid_record()
        record["resources"]["cost"] = float("nan")
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("non-finite numbers", result.stderr)

    def test_rejects_mismatched_terminal_disposition(self):
        record = self.valid_record()
        record["run_status"] = "RUN_COMPLETED"
        record["execution_disposition"] = "stopped"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)

    def test_rejects_disposition_on_unknown_status(self):
        record = self.valid_record()
        record["run_status"] = "UNKNOWN"
        record["execution_disposition"] = "completed"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(COLLECTOR), str(record_path)],
                capture_output=True, text=True, check=False
            )
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
