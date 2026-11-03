# Measurement protocol

This is an offline measurement scaffold. It does not call providers, execute patches, or automatically evaluate acceptance. No real model results are included.

## Fair pilot

Freeze the task, acceptance checks, starting commit, and environment before each comparison. Restore an isolated copy for each attempt. Use the same tool capabilities where possible; otherwise label the comparison as a complete workflow comparison rather than model-only. Randomize configuration order to reduce learning and cache effects. Record warm/cold cache conditions and harness versions in notes.

Try three repetitions per task/configuration initially and keep every failure. Expand the sample before drawing strong conclusions. The scorecard is descriptive: it does not calculate significance, control for task mix, or declare a winner. Compare only matched task sets and report results by task category.

Measure elapsed wall time from the start of work through final acceptance or stopping. Include planning, model calls, tests, retries, review, and repair. Separately measure active human review/repair time; it may overlap elapsed time, so do not add the two blindly. Record provider-reported cost only. Subscription time does not imply a marginal dollar charge of zero.

## Recording a run

Copy `run.template.json` to a temporary file. Replace every placeholder, including null acceptance, then fill in observed measurements. Keep unavailable tokens and costs null. Set `accepted` only after evaluating the frozen criteria. A time-limit failure is a failed run, not an omitted result.

```sh
python3 scripts/scorecard.py --validate /path/to/completed-run.json
```

After validation, append the compact record:

```sh
python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' /path/to/completed-run.json >> benchmarks/runs.jsonl
python3 scripts/scorecard.py benchmarks/runs.jsonl
```

Keep experiment logs/diffs in `benchmarks/artifacts/` (ignored by Git); record their paths in `evidence`. Export sanitized evidence separately when sharing. Do not include credentials or private prompts in a public dataset.

## Record fields

| Field | Meaning |
| --- | --- |
| run_id | Unique attempt ID |
| task_id / task_revision | Frozen task and acceptance revision |
| repo_commit | Starting commit; exact commit for real repository experiments |
| provider / model / harness / configuration | Exact identity and workflow variant; include client version in harness |
| accepted | Boolean from checks and required review |
| elapsed_seconds | Measured end-to-end duration, including failed attempts |
| human_minutes | Measured active human effort, or null |
| cost_usd / input_tokens / output_tokens | Runtime/billing-supplied values, otherwise null |
| evidence | Log, diff, and acceptance evidence reference |
| notes | Environment, failures, cache condition, tool differences, or interventions |

Input/output tokens are reported as separate observed fields. This scaffold does not infer totals, cached billing, reasoning-token accounting, or monetary charges from them.

## Interpreting the report

Reports group by provider, exact model, harness, and configuration. They show run count, distinct task revisions, acceptance rate, median elapsed time across all attempts, elapsed seconds per accepted result including failed attempts, human-time coverage, and cost coverage. Cost per accepted result is shown only when every run in that group has a known cost and at least one was accepted. Zero accepted results produce `n/a`.

Do not compare groups with different tasks as if they were controlled experiments. A cheap failed attempt is not a successful optimization. Review any claimed gain alongside acceptance quality and human effort.
