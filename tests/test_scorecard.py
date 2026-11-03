"""Synthetic records exercise accounting; these are not provider benchmarks."""

import copy
import json
from pathlib import Path
import tempfile
import unittest

from scripts.scorecard import load_records, render, summarize, validate


def record(**updates):
    result = {
        "run_id": "synthetic-1", "task_id": "fixture", "task_revision": "v1",
        "repo_commit": "fixture", "provider": "synthetic", "model": "fixture",
        "harness": "fixture-v1", "configuration": "baseline", "accepted": True,
        "elapsed_seconds": 60, "human_minutes": None, "cost_usd": None,
        "input_tokens": None, "output_tokens": None, "evidence": "synthetic fixture",
    }
    result.update(updates)
    return result


class ScorecardTests(unittest.TestCase):
    def test_unknown_usage_is_not_zero(self):
        row = summarize([record()])[0]
        self.assertIsNone(row["known_cost_usd"])
        self.assertIsNone(row["cost_per_accepted"])
        self.assertIsNone(row["human_minutes"])

    def test_failures_count_in_cost_and_time(self):
        rows = [record(cost_usd=2), record(run_id="synthetic-2", accepted=False, cost_usd=3, elapsed_seconds=120)]
        result = summarize(rows)[0]
        self.assertEqual(result["cost_per_accepted"], 5)
        self.assertEqual(result["seconds_per_accepted"], 180)
        self.assertEqual(result["acceptance_rate"], 0.5)

    def test_partial_cost_is_not_complete_cost(self):
        result = summarize([record(cost_usd=2), record(run_id="synthetic-2")])[0]
        self.assertEqual(result["known_cost_runs"], 1)
        self.assertIsNone(result["cost_per_accepted"])

    def test_no_acceptance_has_no_unit_cost(self):
        result = summarize([record(accepted=False, cost_usd=0)])[0]
        self.assertIsNone(result["cost_per_accepted"])
        self.assertIsNone(result["seconds_per_accepted"])

    def test_invalid_measurements(self):
        for field, value in [("elapsed_seconds", None), ("cost_usd", -1),
                             ("input_tokens", True), ("input_tokens", 1.5),
                             ("cost_usd", float("nan")), ("elapsed_seconds", float("inf")),
                             ("accepted", 1), ("model", "REPLACE")]:
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                validate(record(**{field: value}))

    def test_groups_do_not_mix_models_or_harnesses(self):
        self.assertEqual(len(summarize([record(), record(model="other"), record(harness="other")])), 3)

    def test_duplicate_ids_and_line_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "runs.jsonl"
            path.write_text(json.dumps(record()) + "\n" + json.dumps(record()))
            with self.assertRaisesRegex(ValueError, "line 2: duplicate"):
                load_records(path)
            path.write_text("\n{broken}\n")
            with self.assertRaisesRegex(ValueError, "line 2"):
                load_records(path)

    def test_empty_dataset(self):
        self.assertIn("No runs recorded", render([]))

    def test_template_requires_completion(self):
        template = json.loads((Path(__file__).resolve().parents[1] / "benchmarks/run.template.json").read_text())
        with self.assertRaises(ValueError):
            validate(template)


if __name__ == "__main__":
    unittest.main()
