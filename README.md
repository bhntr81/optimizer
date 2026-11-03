# coder_optimization

A practical lab for better coding with **Claude, GPT-6, and xAI Grok**. Optimize for accepted, maintainable changes per unit of time and money. Research baseline: **2026-10-18**.

## Start here

1. Read the [playbook](docs/PLAYBOOK.md) and [provider notes](docs/PROVIDERS.md).
2. Fill out the [task brief](templates/TASK.md) for one real task.
3. Give one coding agent the brief and the relevant repository paths.
4. Verify the result against the brief, then record a run using the [measurement protocol](benchmarks/README.md).
5. Change one workflow variable and repeat on the same task set.

```sh
cd /home/kali/Projects/coder_optimization
python3 -m unittest discover -s tests -v
python3 scripts/scorecard.py benchmarks/runs.jsonl
```

The scorecard uses Python's standard library, makes no API calls, and starts with no results. It summarizes manually recorded experiments; it does not run coding agents or judge their patches.

## Project map

| File | Purpose |
| --- | --- |
| [PLAYBOOK](docs/PLAYBOOK.md) | Default workflow, debugging, context, review, and cost decisions |
| [PROVIDERS](docs/PROVIDERS.md) | Claude / GPT-6 / Grok differences and proposed routing |
| [RESEARCH](research/RESEARCH.md) | Evidence strength, conflicting advice, GitHub shortlist, Reddit findings |
| [Sources](research/sources.json) | Dated source registry with limitations and links |
| [Experiments](benchmarks/README.md) | Fair comparisons and measurement definitions |
| [Roadmap](docs/ROADMAP.md) | Next experiments and adoption criteria |
| [Templates](templates/) | Task, handoff, review, debugging, and repository instructions |

## Current status

Local Git project and initial research synthesis created. No provider benchmarking has been performed. No universal best model or workflow is established. Frameworks were researched, not installed or executed. This project contains original templates and links, not vendored third-party frameworks. There is no remote repository or deployment.

The initial recommendation is deliberately small: clear outcome, relevant context, one implementer, observable verification, and measured escalation. Both [Anthropic's guidance](https://code.claude.com/docs/en/best-practices) and [OpenAI's GPT-6 guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) support reducing unnecessary context and making completion concrete. The details here are working hypotheses until tested on your repositories.
