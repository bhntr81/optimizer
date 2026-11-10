# Roadmap

## Built

- Initial official-doc, GitHub, and Reddit research with source limitations.
- Portable task, debugging, review, handoff, and instruction templates.
- Offline run validation and a descriptive scorecard with tests.

- Phase 2 (2026-11-10): README rewritten to match the implementation, public-repo hygiene pass, scorecard checked against a scratch dataset, [research update list](../research/UPDATES_NEEDED.md) and [readiness assessment](BENCHMARK_READINESS.md).

## Next: pilot, then baseline

First run the one-task, one-provider pilot described in [BENCHMARK_READINESS](BENCHMARK_READINESS.md) to test the measurement process. Proceed to the baseline below only after the pilot's gaps are resolved.

### Baseline

Select a representative target repository and six tasks: a bug, a feature, a refactor, a UI change, a performance change, and a test repair. Replace inapplicable categories rather than inventing a workload. Freeze task acceptance and starting commits. Record actual model and client versions.

Run each provider with the same brief and starting state. Use three repeats per task/configuration as an initial pilot: 54 runs for six tasks, three providers, three repeats. This is a proposed experiment size, not work already performed or a statistical guarantee. Start with one task per provider if cost is constrained.

## Then: ablate workflow choices

1. Lean instructions versus existing instructions.
2. Direct implementation versus a short plan.
3. Default reasoning versus higher reasoning on hard tasks.
4. Single implementer versus implementer plus fresh review.
5. Native baseline versus one pinned framework: Superpowers or GSD.
6. Targeted file discovery versus a repository map on unfamiliar code.

Change one variable at a time; retain failed runs and review effort. A candidate becomes the default only after it preserves acceptance quality and improves measured time or measured cost on relevant tasks. Report mixed results by task class.

## Later: automate only proven routines

Add provider adapters after model access, credential handling, and budget are established. Preserve execution traces, run IDs, actual usage, and immutable task definitions. Add automated acceptance evaluators for selected repositories. Consider a dashboard once real records exist. Recheck volatile provider docs before adding flags or API parameters.
