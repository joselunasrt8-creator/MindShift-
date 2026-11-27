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
                {"subject": "started_at", "reason": "Execution could not begin"},
                {"subject": "ended_at", "reason": "Execution could not begin"},
                {"subject": "inputs.commit_sha", "reason": "No repository checkout was available"}
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

    def test_rejects_blocker_with_execution_disposition(self):
        record = self.valid_record()
        record["execution_disposition"] = "completed"
        with tempfile.TemporaryDirectory() as temp:
            record_path = Path(temp) / "record.json"
            record_path.write_text(json.dumps(record), encoding="utf-8")
            result = subprocess.run([sys.executable, str(COLLECTOR), str(record_path)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
