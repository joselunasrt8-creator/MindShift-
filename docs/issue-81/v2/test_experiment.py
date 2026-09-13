import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("experiment.py")
SPEC = importlib.util.spec_from_file_location("ms81_v2_experiment", MODULE_PATH)
experiment = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = experiment
SPEC.loader.exec_module(experiment)


class DeterministicExperimentTests(unittest.TestCase):
    def test_v1_manifest_preserves_all_historical_artifacts(self):
        verified = experiment.verify_v1_preserved()
        self.assertEqual(5, len(verified))

    def test_all_context_pairs_are_information_equivalent(self):
        tasks = experiment.load(experiment.TASKS)["tasks"]
        self.assertEqual(4, len(tasks))
        for task in tasks:
            sources = experiment.read_sources(task)
            proof = experiment.prove_equivalence(
                task,
                experiment.control_context(task, sources),
                experiment.treatment_context(task, sources),
            )
            self.assertEqual(1, proof["control_task_occurrences"])
            self.assertEqual(1, proof["treatment_task_occurrences"])
            self.assertTrue(proof["source_bytes_reconstruct_exactly_once"])
            self.assertFalse(proof["treatment_only_factual_content"])

    def test_condition_order_contains_each_condition_once_per_pair(self):
        for task in experiment.load(experiment.TASKS)["tasks"]:
            for replicate in range(1, 4):
                self.assertEqual(
                    {"control", "treatment"},
                    set(experiment.condition_order(task["task_id"], replicate)),
                )

    def test_terminal_mapping_is_bounded(self):
        base = {
            "valid_pairs": 12,
            "measures_complete": True,
            "blinding_preserved": True,
            "bootstrap_95": (6, 10),
            "correctness_linear_weighted_kappa": 0.8,
            "task_medians": {"a": 8, "b": 6, "c": 7, "d": 9},
            "preference_treatment": 8,
            "preference_control": 3,
            "treatment_unsupported_plus_stale": 2,
            "control_unsupported_plus_stale": 3,
        }
        self.assertEqual(
            "MINDSHIFT_CONTEXT_IMPROVEMENT_SUPPORTED",
            experiment.terminal_state(base),
        )
        degraded = dict(base, bootstrap_95=(-12, -6), task_medians={"a": -8, "b": -7, "c": 0, "d": 1})
        self.assertEqual("MINDSHIFT_CONTEXT_DEGRADED_OUTPUT", experiment.terminal_state(degraded))
        indeterminate = dict(base, correctness_linear_weighted_kappa=0.2)
        self.assertEqual("INDETERMINATE", experiment.terminal_state(indeterminate))

    def test_cost_calculation_is_conservative_uncached_price(self):
        self.assertAlmostEqual(
            0.00056,
            experiment.usage_cost_usd({"prompt_tokens": 1000, "completion_tokens": 100}),
        )


if __name__ == "__main__":
    unittest.main()
