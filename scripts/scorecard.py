#!/usr/bin/env python3
"""Validate observed coding-run records and summarize without API calls."""

import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
from statistics import median
import sys


TEXT_FIELDS = (
    "run_id", "task_id", "task_revision", "repo_commit", "provider", "model",
    "harness", "configuration", "evidence",
)
NUMERIC_FIELDS = ("elapsed_seconds", "human_minutes", "cost_usd", "input_tokens", "output_tokens")
GROUP_FIELDS = ("provider", "model", "harness", "configuration")


def validate(record):
    if not isinstance(record, dict):
        raise ValueError("record must be a JSON object")
    for field in TEXT_FIELDS:
        value = record.get(field)
        if not isinstance(value, str) or not value.strip() or value.strip() == "REPLACE":
            raise ValueError(f"{field} must contain an observed, non-placeholder value")
    if type(record.get("accepted")) is not bool:
        raise ValueError("accepted must be true or false")
    for field in NUMERIC_FIELDS:
        if field not in record:
            raise ValueError(f"missing {field}; use null for unavailable optional measurements")
        value = record[field]
        if value is None and field != "elapsed_seconds":
            continue
        if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
            raise ValueError(f"{field} must be a finite non-negative number")
        if field.endswith("_tokens") and type(value) is not int:
            raise ValueError(f"{field} must be an integer or null")
    if not isinstance(record.get("notes", ""), str):
        raise ValueError("notes must be a string")
    return record


def load_records(path):
    records = []
    seen = set()
    for number, line in enumerate(path.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = validate(json.loads(line))
            if record["run_id"] in seen:
                raise ValueError(f"duplicate run_id {record['run_id']!r}")
        except (ValueError, TypeError) as error:
            raise ValueError(f"line {number}: {error}") from error
        seen.add(record["run_id"])
        records.append(record)
    return records


def summarize(records):
    groups = defaultdict(list)
    for record in records:
        groups[tuple(record[field] for field in GROUP_FIELDS)].append(record)
    result = []
    for key, rows in sorted(groups.items()):
        accepted = sum(row["accepted"] for row in rows)
        costs = [row["cost_usd"] for row in rows if row["cost_usd"] is not None]
        human = [row["human_minutes"] for row in rows if row["human_minutes"] is not None]
        elapsed = sum(row["elapsed_seconds"] for row in rows)
        result.append({
            "group": key, "runs": len(rows), "accepted": accepted,
            "tasks": len({(row["task_id"], row["task_revision"]) for row in rows}),
            "acceptance_rate": accepted / len(rows),
            "median_elapsed_seconds": median(row["elapsed_seconds"] for row in rows),
            "seconds_per_accepted": elapsed / accepted if accepted else None,
            "known_cost_runs": len(costs), "known_cost_usd": sum(costs) if costs else None,
            "cost_per_accepted": sum(costs) / accepted if accepted and len(costs) == len(rows) else None,
            "known_human_runs": len(human), "human_minutes": sum(human) if human else None,
        })
    return result


def display(value):
    return "n/a" if value is None else f"{value:.2f}"


def render(records):
    if not records:
        return "No runs recorded. No provider comparison or savings claim is available."
    lines = ["Descriptive results only. Compare matched tasks and starting states."]
    for row in summarize(records):
        lines.extend([
            "", " / ".join(row["group"]),
            f"  Runs: {row['runs']}; task revisions: {row['tasks']}; accepted: {row['accepted']} ({row['acceptance_rate']:.1%})",
            f"  Median elapsed seconds (all attempts): {row['median_elapsed_seconds']:.2f}",
            f"  Elapsed seconds per accepted result (including failures): {display(row['seconds_per_accepted'])}",
            f"  Reported cost subtotal USD: {display(row['known_cost_usd'])}; coverage: {row['known_cost_runs']}/{row['runs']}",
            f"  Cost USD per accepted result: {display(row['cost_per_accepted'])}",
            f"  Human minutes subtotal: {display(row['human_minutes'])}; coverage: {row['known_human_runs']}/{row['runs']}",
        ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path, help="JSONL dataset, or a single JSON record with --validate")
    parser.add_argument("--validate", action="store_true", help="validate one JSON record without appending")
    args = parser.parse_args()
    try:
        if args.validate:
            validate(json.loads(args.path.read_text()))
            print("Record valid. Nothing appended.")
        else:
            print(render(load_records(args.path)))
    except (OSError, ValueError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
