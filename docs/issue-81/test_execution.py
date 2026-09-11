#!/usr/bin/env python3
"""Synthetic-only regression tests for Issue #81 execution preparation."""

import importlib.util
import json
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("ms81_execution", HERE / "execution.py")
execution = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
sys.modules[SPEC.name] = execution
SPEC.loader.exec_module(execution)


class ExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tasks = execution.load_json(execution.TASK_SET)
        cls.task = cls.tasks["tasks"][0]
        cls.sources = execution.read_sources(cls.task)

    def test_exact_control_construction(self):
        context = execution.control_context(self.task, self.sources)
        expected = execution.SOURCE_INSTRUCTION.encode()
        for source in self.sources:
            expected += f"\n\n--- SOURCE: {source.path} ---\n\n".encode() + source.payload
        expected += b"\n\n--- TASK ---\n\n" + self.task["prompt"].encode()
        self.assertEqual(context.payload, expected)
        self.assertNotIn(self.task["bounded_reference"].encode(), context.payload)

    def test_exact_treatment_categories_order_and_no_hints(self):
        context = execution.treatment_context(self.task, self.sources)
        positions = [context.payload.index(f"## {category}".encode()) for category in execution.CATEGORIES]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(context.payload.count(b"## TASK RELEVANCE"), 1)
        self.assertEqual(context.payload.count(b"## LINEAGE AND PROVENANCE"), 1)
        self.assertNotIn(self.task["bounded_reference"].encode(), context.payload)
        self.assertNotIn(json.dumps(self.task["information_requirements"], separators=(",", ":")).encode(), context.payload)

    def test_information_equivalence_and_source_byte_preservation(self):
        control = execution.control_context(self.task, self.sources)
        treatment = execution.treatment_context(self.task, self.sources)
        proof = execution.prove_equivalence(control, treatment, self.task)
        self.assertTrue(proof["every_source_byte_exactly_once"])
        reconstructed = {source.source_id: b"" for source in self.sources}
        for segment in treatment.segments:
            reconstructed[segment.source_id] += segment.payload
        self.assertEqual([reconstructed[s.source_id] for s in self.sources], [s.payload for s in self.sources])

    def test_duplicate_or_missing_segment_fails_closed(self):
        control = execution.control_context(self.task, self.sources)
        treatment = execution.treatment_context(self.task, self.sources)
        damaged = replace(treatment, segments=treatment.segments[:-1])
        with self.assertRaisesRegex(execution.PreflightError, "reconstruction"):
            execution.prove_equivalence(control, damaged, self.task)

    def test_treatment_only_answer_hint_fails(self):
        control = execution.control_context(self.task, self.sources)
        treatment = execution.treatment_context(self.task, self.sources)
        leaked = replace(treatment, payload=treatment.payload + self.task["bounded_reference"].encode())
        with self.assertRaisesRegex(execution.PreflightError, "outside the frozen transformation"):
            execution.prove_equivalence(control, leaked, self.task)

    def test_source_hash_mismatch_rejected(self):
        manifest = execution.load_json(execution.SOURCE_MANIFEST)
        manifest["sources"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(execution.PreflightError, "hash mismatch"):
            execution.read_sources(self.task, manifest)

    def test_task_mismatch_rejected(self):
        control = execution.control_context(self.task, self.sources)
        treatment = execution.treatment_context(self.task, self.sources)
        changed = dict(self.task, prompt=self.task["prompt"] + " changed")
        with self.assertRaisesRegex(execution.PreflightError, "prompt mismatch"):
            execution.prove_equivalence(control, treatment, changed)

    def test_context_overflow_and_model_capabilities_rejected(self):
        eligible = {field: True for field in execution.REQUIRED_MODEL_FIELDS}
        eligible.update(provider="synthetic", snapshot="dated-snapshot", tokenizer="synthetic", context_window_tokens=1)
        with self.assertRaisesRegex(execution.PreflightError, "overflow"):
            execution.validate_model(eligible, 100)
        eligible["context_window_tokens"] = 10000
        eligible["seed_control"] = False
        with self.assertRaisesRegex(execution.PreflightError, "capabilities"):
            execution.validate_model(eligible, 100)

    def test_run_manifest_completeness(self):
        with self.assertRaisesRegex(execution.PreflightError, "incomplete"):
            execution.validate_manifest({"artifact_class": "EMPIRICAL_RUN"})

    def test_scoring_normalization_penalties_and_bounds(self):
        self.assertEqual(execution.quality_score(0, 0, 0, 0, 0, 0), 0)
        self.assertEqual(execution.quality_score(4, 4, 0, 0, 0, 0), 100)
        self.assertEqual(execution.quality_score(2, 2, 1, 1, 0, 0), 37.5)
        self.assertEqual(execution.quality_score(4, 4, 4, 4, 4, 4), 0)
        self.assertEqual(execution.quality_score(4, 4, 1, 0, 0, 0), 93.75)
        with self.assertRaises(ValueError):
            execution.quality_score(5, 0, 0, 0, 0, 0)

    def test_pair_effect_and_aggregation(self):
        self.assertEqual(75 - 50, 25)
        effects = {f"MS81-T0{i}": [float(i)] * 20 for i in range(1, 5)}
        medians, aggregate = execution.aggregate_pair_effects(effects)
        self.assertEqual(medians["MS81-T03"], 3)
        self.assertEqual(aggregate, 2.5)

    def test_adjudication_and_median_rule(self):
        low = dict(correctness=1, relevant_used=1, omissions=2, unsupported=0, stale=0, contradictions=0)
        high = dict(correctness=4, relevant_used=4, omissions=0, unsupported=0, stale=0, contradictions=0)
        middle = dict(correctness=3, relevant_used=3, omissions=0, unsupported=0, stale=0, contradictions=0)
        with self.assertRaisesRegex(ValueError, "adjudicator"):
            execution.final_item_score([low, high])
        self.assertEqual(execution.final_item_score([low, high, middle]), 75)

    def terminal(self, medians, **changes):
        args = dict(valid=True, valid_pairs=80, total_pairs=80, blinded=True,
                    measures_complete=True, kappa=.8, task_medians=medians,
                    preference_treatment=45, preference_control=30)
        args.update(changes)
        return execution.terminal_state(**args)

    def test_all_terminal_states(self):
        self.assertEqual(self.terminal({str(i): 10 for i in range(4)}), "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED")
        self.assertEqual(self.terminal({str(i): -10 for i in range(4)}), "MINDSHIFT_CONTEXT_DEGRADED_OUTPUT")
        self.assertEqual(self.terminal({str(i): 1 for i in range(4)}), "NO_MEASURABLE_IMPROVEMENT")
        self.assertEqual(self.terminal({"0": -20, "1": 20, "2": -20, "3": 20}), "INDETERMINATE")
        self.assertEqual(self.terminal({str(i): 10 for i in range(4)}, valid=False), "EXPERIMENT_INVALID")

    def test_synthetic_cannot_enter_empirical_custody(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(execution.PreflightError, "synthetic"):
                execution.create_custody(Path(directory), [{"artifact_class": "SYNTHETIC_FIXTURE"}])

    def test_blinded_custody_names_and_sealed_key(self):
        records = [{"artifact_class": "EMPIRICAL_RUN", "task_id": "MS81-T01", "replicate": 1,
                    "condition": "control", "execution_order": 1, "response": {"text": "synthetic placeholder"}}]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            execution.create_custody(root, records)
            names = [path.name for path in (root / "evaluation").iterdir()]
            self.assertEqual(len(names), 1)
            self.assertNotIn("control", names[0])
            public = json.loads((root / "evaluation" / names[0]).read_text())
            self.assertNotIn("condition", public)
            self.assertEqual((root / "sealed" / "condition-key.json").stat().st_mode & 0o777, 0o400)

    def test_pair_order_is_deterministic(self):
        self.assertEqual(execution.pair_order("MS81-T01", 1), execution.pair_order("MS81-T01", 1))


if __name__ == "__main__":
    unittest.main()
