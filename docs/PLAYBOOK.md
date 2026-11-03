# The working playbook

Status: proposed baseline, not a demonstrated optimum. Source IDs refer to [the registry](../research/sources.json).

## 1. Define the outcome

Write a short task brief with observable acceptance criteria, the repository, relevant examples, constraints, and the verification command. Clarify ambiguities that change behavior; let the agent resolve routine implementation details. For an exploratory task, define the decision or report that ends the exploration. [S01](https://code.claude.com/docs/en/best-practices)

Our default task size is one independently verifiable behavior. Split a large feature along working user flows, not arbitrary file counts. A typo needs neither an architecture document nor a planning ceremony. For a migration, write down the contracts and rollout constraints before editing.

## 2. Make the environment reproducible

Record the starting commit, runtime, dependency lockfile, setup command, and baseline check result. If a check already fails, capture that before the agent changes anything. Give the agent local build/test capability so it can obtain feedback directly. Keep a separate branch or worktree for each experimental attempt; preserve unrelated edits.

## 3. Give context in layers

Put durable, non-obvious repository rules and runnable commands in a concise instruction file. Keep changing task state in the task brief or handoff. Start with likely entry points, relevant tests, and one good example. Fetch additional code as needed. Search by symbol or behavior instead of dumping whole directories. For unfamiliar large repositories, try a concise dependency/symbol map. [S03](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), [S09](https://github.com/Aider-AI/aider/blob/main/aider/website/docs/repomap.md)

When a session repeats failed attempts or loses constraints, create a handoff with the current commit, facts, rejected hypotheses, verification results, and next action. Resume with that state plus relevant files. There is no validated universal context-percentage threshold for resetting.

## 4. Implement and check

Use one primary editor by default. Fix bugs from a reproducer; add a regression check when it captures meaningful behavior. For UI changes, inspect the rendered result and interaction states. For performance changes, record a baseline and rerun the same workload. A passing unit suite does not establish visual quality or performance.

Keep acceptance tests stable during evaluation. If an agent weakens a test to make a patch pass, review the requirement independently before accepting it. Run affected checks first, then the repository's required checks. Investigate failures caused by the change; avoid repeating successful suites without a reason.

## 5. Review where it pays

For consequential changes, give a fresh reviewer the task, diff, relevant contracts, and check outputs. Ask for reproducible defects and missing requirements. Do not frame the patch as already correct. A second model is an experiment, not independent proof: models can share blind spots.

Our escalation rule: after two attempts with the same failure and no new evidence, stop repeating the prompt. Improve the reproducer, inspect a missing dependency, or try another configuration. Two is a starting policy to evaluate, not a research-derived constant.

## 6. Finish with evidence

Deliver the changed behavior, validation performed, unresolved failures, and a reviewable diff. A task is accepted only when its frozen acceptance criteria and required review pass. Keep partial and failed runs in the dataset. Track human repair and review time as part of the workflow.

## Cost and speed levers, in order

| Lever | Trial | Failure signal |
| --- | --- | --- |
| Context | Remove irrelevant repeated instructions | More missed requirements |
| Tools | Expose only tools relevant to the task | Required evidence becomes inaccessible |
| Task scope | One complete behavior per task | Integration work is hidden between tasks |
| Reasoning | Compare default effort with a higher setting on hard tasks | More latency with no acceptance improvement |
| Review | Add an independent review to risky tasks | Cosmetic churn or duplicate findings |
| Caching | Keep stable API prefixes stable; variable data later | Low cache hits or unsupported adapter behavior |
| Concurrency | Independent work in isolated worktrees, when authorized | Merge conflicts, duplicated work, rising total cost |

OpenAI recommends testing leaner prompts and relevant tool sets for GPT-6; treat its internal measurements as vendor results, not projected savings here. [S05](https://developers.openai.com/api/docs/guides/latest-model)

Grok's API caching example demonstrates that changing early prompt content can destroy prefix reuse. Check usage fields and the API/SDK-specific mechanism in your integration; caching is distinct from semantic memory and does not make irrelevant context useful. [S07](https://docs.x.ai/cookbook/examples/prompt-caching)

## Avoid as defaults

- Massive universal prompts, compulsory reading of every document, and many overlapping skill packs.
- Maximum reasoning for every edit or automatic three-model debate for every task.
- Splitting tightly coupled edits across simultaneous writers.
- Scoring output volume, GitHub stars, or confidence as correctness.
- Infinite repair loops without new evidence.
- Counting only successful attempts when reporting cost or time.

These are project design choices to test. Longer instructions, planning, or additional agents can be useful when they address a measured failure.
