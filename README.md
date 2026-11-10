# Optimizer

Optimizer is a small, offline toolkit and research notebook for **measuring** how well AI coding agents (Claude, GPT-6, xAI Grok, or any other) perform on real tasks, so that workflow changes can be judged on evidence rather than impressions.

> **Status in one sentence:** the measurement scaffold (run-record validation and a descriptive scorecard) is implemented and tested; **no benchmark has been run, there are no results, and no provider or workflow is established as better than another.** A polished repository is not a validated optimizer. The measurement system has to earn trust through real experiments.

## Implemented vs. proposed

| Item | Status |
| --- | --- |
| Run-record schema and validation (`scripts/scorecard.py`) | **Implemented**, covered by unit tests |
| Descriptive scorecard grouped by provider / model / harness / configuration | **Implemented**, covered by unit tests |
| Task, debugging, review, handoff and repo-instruction templates (`templates/`) | **Implemented** (text templates) |
| Dated source registry and research synthesis (`research/`) | **Implemented**, but a point-in-time survey (2026-10-18), not re-verified |
| Default workflow ([playbook](docs/PLAYBOOK.md)) and routing ideas ([providers](docs/PROVIDERS.md)) | **Proposed** hypotheses, untested |
| Frozen task suite and benchmark campaign | **Proposed**, not started ([readiness plan](docs/BENCHMARK_READINESS.md)) |
| Running agents, calling provider APIs, judging patches, pricing lookups | **Not implemented**, intentionally |
| Per-task breakdowns, matched-task warnings, statistics, dashboards | **Not implemented** |

## The problem

Advice on coding agents is abundant and mostly anecdotal or vendor-reported. Perceived speed can disagree with measured speed, cheap failed attempts can look like savings, and comparisons routinely mix model, harness, prompt and task differences. Optimizer exists to make small, honest comparisons possible: same task, same starting state, every attempt recorded, failures included.

## Measurement philosophy

- **Recommendations are not results.** Anything not backed by a recorded run is labeled a hypothesis.
- **Failures count.** Time and cost are reported across all attempts, including failed and time-limited ones.
- **Unknown stays unknown.** Missing tokens, cost or human time are `null`, never `0` and never inferred from a model name. Subtotals always show how many runs they cover.
- **Identify the whole configuration.** Model, harness (with client version) and workflow variant are separate fields. Different harnesses are different groups.
- **Matched comparisons only.** Compare groups only on the same tasks, acceptance criteria and starting commits. The scorecard is descriptive; it does not compute significance, control for task mix, or declare a winner.
- **No claim without matched evidence.** Do not say a provider or framework is faster or cheaper until representative, matched experiments support it.

## Supported comparisons

The scorecard treats `provider`, `model`, `harness` and `configuration` as free-text labels, so it can group runs from any provider, harness or workflow variant. There are **no provider integrations**: you run the agent yourself and record what you observed. The research notes cover Claude (Claude Code), GPT-6 (Codex) and xAI Grok (Grok Build); exact model IDs, client versions, pricing and account access have **not** been verified (see [provider notes](docs/PROVIDERS.md)).

## Quick start

Requirements: Python 3 and Git. No packages to install; no credentials or network access needed.

```sh
git clone https://github.com/bhntr81/optimizer.git
cd optimizer

python3 -m unittest discover -s tests -v   # run the tests
python3 scripts/scorecard.py benchmarks/runs.jsonl
```

Run both commands from the repository root. With the shipped (empty) dataset the scorecard prints `No runs recorded. No provider comparison or savings claim is available.`, which is the correct output today.

## Recording a benchmark task and run

1. Describe the task with the [task brief](templates/TASK.md): outcome, starting commit, observable acceptance criteria, verification commands, allowed work and stopping condition. Freeze it before any attempt.
2. Give one agent the brief, restore an isolated copy of the starting state for each attempt, and keep logs and diffs in `benchmarks/artifacts/` (git-ignored).
3. Copy `benchmarks/run.template.json` outside the repository, replace every `REPLACE` placeholder with an observed value, and set `accepted` to `true` or `false` after checking the frozen criteria. Keep unavailable `cost_usd`, `input_tokens`, `output_tokens` and `human_minutes` as `null`.
4. Validate, then append the record as one compact JSON line:

```sh
python3 scripts/scorecard.py --validate /path/to/completed-run.json
python3 -c 'import json,sys; print(json.dumps(json.load(open(sys.argv[1]))))' /path/to/completed-run.json >> benchmarks/runs.jsonl
```

Field definitions, the proposed pilot design and fairness rules are in the [measurement protocol](benchmarks/README.md). Do not put synthetic or practice records in `benchmarks/runs.jsonl`; use a scratch file and pass its path to the scorecard.

## Running and interpreting the scorecard

```sh
python3 scripts/scorecard.py path/to/runs.jsonl
```

Each group (`provider / model / harness / configuration`) reports:

| Line | Meaning |
| --- | --- |
| Runs, task revisions, accepted | Attempt count, number of distinct `task_id`+`task_revision` pairs, accepted count and rate |
| Median elapsed seconds | Median over **all** attempts, failures included |
| Elapsed seconds per accepted result | Total elapsed time of all attempts divided by accepted results; `n/a` if none were accepted |
| Reported cost subtotal and coverage | Sum of known costs and `known/total` runs. Subtotal is partial when coverage is below 100% |
| Cost USD per accepted result | Shown **only** if every run in the group has a known cost and at least one was accepted; otherwise `n/a` |
| Human minutes subtotal and coverage | Sum of recorded human time and how many runs reported it |

How to read it safely:

- Compare groups only if their task-revision counts and task sets match; the scorecard prints the count but **does not warn** when groups ran different tasks and does not list task IDs.
- A high acceptance rate on easy tasks is not comparable to a lower rate on hard ones. Split the JSONL by task (for example with `grep`) and run the scorecard on each slice.
- Input/output tokens are validated but **not summarized**.
- Cost and time are not combined into one score, and no variance or confidence interval is computed.
- The tool reads the file you give it. It cannot detect omitted runs, edited history, or a wrong `accepted` value.

## How acceptance is evaluated

Acceptance is **human-determined and recorded as a boolean**. A run is accepted only when the frozen acceptance criteria in the task brief pass and any required review passes. The scorecard does not run checks, inspect patches, or verify the flag; it only requires that `accepted` be `true` or `false` (not a placeholder or null). Weakening a test to make a patch pass does not count as acceptance. Automated acceptance evaluators are a proposed later stage.

## Current limitations

- No benchmark data exists; no model, harness or workflow ranking is supported.
- Task freezing, pre-registration of planned runs, and detection of missing runs are conventions described in [docs](docs/BENCHMARK_READINESS.md), not enforced by code.
- Model and harness versions, reasoning effort and cache state are recorded in free text (`model`, `harness`, `configuration`, `notes`), not validated fields.
- Research is a snapshot from 2026-10-18; several sources are mutable URLs and were not archived ([update list](research/UPDATES_NEEDED.md)). Pricing, quotas and exact model IDs are unverified.
- Vendor claims and community posts in the research are cited as such and are not local evidence.
- No license file is included yet.

## Planned development stages

All of these are proposed; see the [roadmap](docs/ROADMAP.md).

1. **Preparation (this stage):** accurate documentation, repository hygiene, scorecard verification, research update list, readiness plan.
2. **Pilot:** one task, one provider, one fully recorded run, to test the *process* (not to compare models).
3. **Baseline:** frozen six-task set across providers, three repeats each, only after the readiness gaps are closed.
4. **Ablations:** one workflow variable at a time (instructions, planning, reasoning effort, review, frameworks, repository maps).
5. **Automation:** adapters, acceptance evaluators and reporting, only for routines the earlier stages have proven worthwhile.

## Project map

| Path | Purpose |
| --- | --- |
| [docs/PLAYBOOK.md](docs/PLAYBOOK.md) | Proposed default workflow, debugging, context, review and cost levers |
| [docs/PROVIDERS.md](docs/PROVIDERS.md) | Claude / GPT-6 / Grok notes and a proposed routing experiment |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Staged plan and adoption criteria |
| [docs/BENCHMARK_READINESS.md](docs/BENCHMARK_READINESS.md) | Whether the framework can support the planned experiment, and the smallest pilot |
| [docs/records/](docs/records/) | Historical workflow records (not benchmark results) |
| [research/RESEARCH.md](research/RESEARCH.md) | Evidence strength, conflicts, GitHub shortlist, community leads |
| [research/sources.json](research/sources.json) | Dated source registry with limitations |
| [research/UPDATES_NEEDED.md](research/UPDATES_NEEDED.md) | Prioritized source verification before the first benchmark |
| [benchmarks/README.md](benchmarks/README.md) | Measurement protocol and record fields |
| [benchmarks/run.template.json](benchmarks/run.template.json) | Blank run record |
| [benchmarks/runs.jsonl](benchmarks/runs.jsonl) | The real dataset (currently empty) |
| [scripts/scorecard.py](scripts/scorecard.py), [tests/](tests/) | Validator, scorecard and tests (standard library only) |
| [templates/](templates/) | Task, debugging, review, handoff and repository-instruction templates |
| [AGENTS.md](AGENTS.md) | Instructions for coding agents working on this repository |
