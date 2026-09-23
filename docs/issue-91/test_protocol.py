#!/usr/bin/env python3
"""Deterministic, model-free tests for the Issue #91 freeze protocol."""

from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("issue91_validator", HERE / "validate_and_reconstruct.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


class ProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cohort = validator.load_json(HERE / "assessment-input/cohort.json")
        cls.item = cls.cohort["work_items"][0]
        cls.evidence = [entry for entry in cls.cohort["evidence"] if entry["bundle_path"].startswith("sources/MS91-WI-001/")]

    def assessment(self):
        value = {
            "assessment_id": "TEST-001",
            "work_item_id": self.item["work_item_id"],
            "determination": "INDETERMINATE",
            "rationale": "Test fixture only; not an experiment output.",
            "evidence_refs": ["E-1"],
            "unresolved_uncertainty": ["Fixture uncertainty."],
            "cheaper_or_stronger_alternative": None,
            "falsification_condition": "The fixture hash fails.",
            "authority": None,
            "execution_eligible": False,
            "assessor_identity": "unit-test-fixture",
            "assessor_configuration": {"model_calls": 0},
            "input_hash": validator.assessment_input_hash(self.item),
            "output_hash": "0" * 64,
        }
        value["output_hash"] = validator.assessment_output_hash(value)
        return value

    def test_valid_work_item(self):
        validator.validate_work_item(self.item, self.evidence)

    def test_missing_required_field(self):
        item = copy.deepcopy(self.item)
        del item["proposed_work"]
        with self.assertRaisesRegex(validator.ValidationError, "missing required"):
            validator.validate_work_item(item, self.evidence)

    def test_invalid_determination(self):
        value = self.assessment()
        value["determination"] = "PASS"
        with self.assertRaisesRegex(validator.ValidationError, "invalid determination"):
            validator.validate_assessment(value, self.item)

    def test_non_null_authority(self):
        value = self.assessment()
        value["authority"] = "operator"
        with self.assertRaisesRegex(validator.ValidationError, "authority must be null"):
            validator.validate_assessment(value, self.item)

    def test_executable_recommendation(self):
        value = self.assessment()
        value["execution_eligible"] = True
        with self.assertRaisesRegex(validator.ValidationError, "must be false"):
            validator.validate_assessment(value, self.item)

    def test_post_cutoff_evidence(self):
        item = copy.deepcopy(self.item)
        item["cutoff_timestamp"] = "2000-01-01T00:00:00+00:00"
        with self.assertRaisesRegex(validator.ValidationError, "outside cutoff"):
            validator.validate_work_item(item, self.evidence)

    def test_source_hash_mismatch(self):
        evidence = copy.deepcopy(self.evidence)
        evidence[0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(validator.ValidationError, "hash mismatch"):
            validator.validate_work_item(self.item, evidence)

    def test_manifest_mismatch(self):
        manifest = validator.load_json(HERE / "freeze-manifest.json")
        manifest["protocol_version"] = "changed"
        with self.assertRaisesRegex(validator.ValidationError, "manifest mismatch"):
            validator.validate_manifest(manifest)

    def test_outcome_leakage(self):
        leak = HERE / "assessment-input/outcomes-forbidden"
        try:
            leak.write_text("outcomes/", encoding="utf-8")
            with self.assertRaisesRegex(validator.ValidationError, "manifest mismatch|outcome leakage"):
                validator.preflight()
        finally:
            leak.unlink(missing_ok=True)

    def test_reproducible_reconstruction(self):
        manifest = validator.load_json(HERE / "freeze-manifest.json")
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self.assertEqual(validator.reconstruct(Path(a), manifest), validator.reconstruct(Path(b), manifest))

    def test_malformed_cohort_record(self):
        malformed = {"work_items": "not-a-list"}
        with self.assertRaisesRegex(validator.ValidationError, "missing required"):
            validator.require_fields(malformed, ["schema_version", "work_items", "evidence"], "cohort")


if __name__ == "__main__":
    unittest.main()
