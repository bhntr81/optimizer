# Benchmark readiness assessment

Prepared 2026-11-10. This is an assessment and a plan. **Nothing here has been executed**, no benchmark has been run, and the real dataset (`benchmarks/runs.jsonl`) is empty.

## Can the current framework support the roadmap experiment?

The roadmap proposes six frozen tasks × three providers × three repeats = 54 runs.

**Verdict: it can *record and summarize* 54 runs, but it cannot *enforce* the integrity of the experiment or compare repeats and tasks on its own.** Several controls would exist only as manual discipline. That is acceptable for a one-run pilot and risky for 54 runs.

| Requirement | What exists today | Gap |
| --- | --- | --- |
| **Freezing tasks** | `task_id`, `task_revision` and `repo_commit` are required strings; [TASK.md](../templates/TASK.md) defines the brief | Nothing stores or hashes the frozen brief or acceptance checks, and nothing detects edits after the fact |
| **Measuring acceptance** | Required boolean `accepted`, set by a human against the brief | Not verified by code; no record of which checks ran or who judged |
| **Counting failed attempts** | Scorecard counts failures in acceptance rate, median time and per-accepted time and cost; time-limit failures must be recorded as failures | No registry of planned runs, so omitted failures are undetectable |
| **Recording time and cost** | Required `elapsed_seconds`; optional `human_minutes`, `cost_usd`, tokens (null when unknown); coverage shown | Time is typed by hand (no start/end timestamps); tokens are validated but not summarized |
| **Recording model and harness versions** | Free-text `model`, `harness` (documented to include client version), `configuration`, `notes` | Not validated; reasoning effort, cache state, OS and date are only convention |
| **Controlling the environment** | [Protocol](../benchmarks/README.md): isolated copy per attempt, same tools, randomized order, record cache state | Entirely manual |
| **Comparing repeats** | Repeats are just more runs in the same group | No per-task view, no matched-task warning, no variance; task-level comparison needs manual slicing of the JSONL |
| **Protecting against cherry-picking** | Failures are preserved by convention; the dataset is plain text in Git | No enforcement; see below |

## Proposed controls (conventions to adopt, not features that exist)

1. **Freeze tasks.** Store each task brief and acceptance command under a per-task directory, commit it, and record the commit hash and a SHA-256 of the brief in the run's `task_revision` or `evidence`. Never edit a frozen task; create a new revision.
2. **Measure acceptance.** Write acceptance as commands or a short checklist before the first attempt. Run exactly those checks, save their output as evidence, and record `accepted` only from them plus any required review. Do not change criteria after seeing results.
3. **Count failures.** Pre-register the run plan (run IDs, task, provider, configuration, order) in a Git commit *before* running. Every planned run gets exactly one record, including aborted, timed-out and infrastructure failures. Compare planned and recorded counts before reporting.
4. **Record time and cost.** Note start and end timestamps in `evidence` logs; enter `elapsed_seconds` from them. Use provider- or runtime-reported usage and cost only; otherwise `null`.
5. **Record versions.** Put the client name and version in `harness`, the exact model ID in `model`, and reasoning effort, cache state, OS and date in `configuration`/`notes`.
6. **Control the environment.** Fresh worktree or clone at the frozen commit per attempt, same dependencies and tool access, same time limit, randomized configuration order.
7. **Compare repeats.** Report per task, never pooled across different tasks. Show every run, not only summary lines. Treat differences as descriptive until there are enough runs.
8. **Resist cherry-picking.** Commit the pre-registration, append-only results and evidence index before analysis; do not delete or rewrite records; report all runs, including failures and null measurements; state analysis choices before looking at data.

## Gaps worth closing before the 54-run campaign (proposed, not started)

- Scorecard: per-task breakdown, a warning when compared groups have different task sets, token totals.
- A small checker that compares a pre-registered run plan against `runs.jsonl`.
- Optional structured fields for reasoning effort and cache state.

None of these is required for the pilot. Adding them should not alter the existing scorecard behavior without tests.

## Smallest useful pilot (not launched)

**One task, one provider, one complete recorded run.** Its purpose is to test the *measurement process*, not to compare models. Do not publish or interpret its result as performance.

1. Choose one small, real, independently verifiable task (the bug or test-repair category fits well) in a repository you control, with a baseline check that passes or has a recorded known failure.
2. Choose the provider/harness you already use and have access to, to keep setup noise out of the test; complete research updates P0 in [UPDATES_NEEDED](../research/UPDATES_NEEDED.md) for it.
3. Fill in [TASK.md](../templates/TASK.md); freeze it and commit it. Write acceptance checks first.
4. Pre-register the single run (run ID and configuration) in a commit.
5. Run in an isolated copy, with timestamps, logs and diff saved to `benchmarks/artifacts/`.
6. Apply the frozen acceptance checks, then record one JSON line via the steps in the README. Validate it with `--validate`, append it, and run the scorecard.
7. Review: Were any fields hard to fill? Was anything unrecorded or ambiguous? Could another person reproduce the run from the evidence? Fix the process, then decide whether to proceed.

**Pilot success means the process worked and the record is trustworthy, not that the agent did well.** A failed run is a valid pilot outcome and must be kept.
