# Research synthesis

Research date: 2026-10-18. This is a curated initial survey, not an exhaustive crawl or an independent benchmark. Searches covered official provider documentation, first-party project repositories, and Reddit accounts. Pages in [sources.json](sources.json) were opened; entries record their evidence class and limitations. Mutable pages were not archived or pinned to a commit.

## Evidence rules

- **Official guidance:** reliable for intended product behavior; performance claims remain vendor-reported.
- **Project documentation:** reliable for the project's design and stated features; popularity does not prove improvement.
- **Empirical study:** interpret within its models, participants, tasks, and dates.
- **Firsthand community report:** a source for that author's experience only; generate hypotheses, not technical guarantees.
- **Project proposal:** our synthesis, awaiting measured local evidence.

## Findings worth adopting as the baseline

| Finding | Evidence | Decision |
| --- | --- | --- |
| Precise completion and verification help guide work | [Claude docs](https://code.claude.com/docs/en/best-practices) | Use an acceptance-defined brief |
| Repeated global instructions can waste context | [GPT-6 guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | Keep durable instructions short and scoped |
| Selective retrieval and durable notes support long work | [Anthropic context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Retrieve relevant files and save handoffs |
| Long tasks benefit from incremental state and checks | [Anthropic harness design](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | Finish and validate one usable slice at a time |
| Prompt prefix changes can undermine caching | [xAI cookbook](https://docs.x.ai/cookbook/examples/prompt-caching) | Test stable-prefix layout in API integrations |

These decisions are a synthesis, not a controlled comparison of Claude, GPT-6, and Grok.

## GitHub shortlist

| Project | What to learn or test | Adoption decision |
| --- | --- | --- |
| [obra/superpowers](https://github.com/obra/superpowers) | Composable planning, debugging, testing, and review workflows | Trial one relevant workflow; measure overhead before adopting the full framework |
| [gsd-build/get-shit-done](https://github.com/gsd-build/get-shit-done/blob/main/docs/README.md) | Specification and context-oriented project structure | Candidate for larger projects with durable state; compare against a small brief and handoff |
| [Aider repository map](https://github.com/Aider-AI/aider/blob/main/aider/website/docs/repomap.md) | Compact symbols and dependency-based selection | Try when orientation in an unfamiliar repository is the bottleneck |
| [promptfoo](https://github.com/promptfoo/promptfoo) | Repeatable prompt/provider evaluation and assertions | Potential future evaluator; text-output tests alone do not validate repository edits |
| [xai-org/grok-build](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/01-getting-started.md) | Native Grok coding harness and execution surfaces | Candidate Grok baseline; verify local version and access before use |

No repository was installed, executed, security-audited, or benchmarked. Source licenses must be checked before incorporating third-party code. Pin a revision when beginning framework experiments; current default branches can change.

## Reddit: useful leads, conflicting results

1. A [Claude Code workflow author](https://www.reddit.com/r/ClaudeAI/comments/1taelgl/what_improved_my_claude_code_workflow_stop/) describes improved predictability from tickets and persistent environments. The post also promotes the author's service. Keep the ticket hypothesis; do not treat it as independent product evidence.
2. A [Grok discussion from September 2026](https://www.reddit.com/r/grok/comments/1wqtnpg/is_anyone_actually_using_grok_for_coding/) contains both readability praise and cost/value disappointment. It provides no matched benchmark, so it cannot establish a model winner.
3. A [June 2026 Grok Build report](https://www.reddit.com/r/grok/comments/1u8ddar/grok_build_feedback_from_a_few_days_of_use/) alleges resource and permission issues, while replies report positive experiences. Versions and setups differ. Use this as a reason to record environment, process cleanup, and actual client behavior during trials; it does not establish a current Grok defect.

These are firsthand anecdotes only. Technical recommendations above are anchored to primary documentation. Search coverage is biased by indexing, self-selection, model changes, and promotion. No Reddit comment was treated as verified pricing or API documentation.

## Conflicts to resolve experimentally

**Lean prompts versus elaborate frameworks.** Superpowers and GSD offer structured workflows; current GPT-6 guidance cautions against excessive process. Both can be useful in different tasks. Compare one framework at a time with the same acceptance criteria, and include planning/review time.

**Larger context versus better retrieval.** Context capacity is not evidence that every file should be loaded. Try a short map or targeted retrieval first. Expand when missing information explains failures.

**Perceived speed versus measured speed.** METR's early-2025 randomized study found experienced maintainers took 19% longer with the studied AI tools. That result concerns older tools and a specific population, not today's three-provider comparison. Its [2026 follow-up](https://metr.org/blog/2026-02-24-uplift-update/) discusses changes in the environment and experiment design, so the old figure must not be generalized into a current slowdown claim. Track actual acceptance time and human effort. [Original study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/)

**More agents versus coordination cost.** Our proposed default is one writer. Trial isolated parallel tasks only when dependencies allow it, and count integration and review work. No multi-agent superiority is established by this survey.

## Open questions

- Which exact models, harness versions, and billing surfaces will be compared?
- Which real repository and task mix best represent the user's work?
- Is the primary bottleneck implementation, review, debugging, context recovery, or rate limits?
- Does cross-provider review discover more meaningful defects than a fresh same-model review?
- Which framework improves acceptance enough to cover its process overhead?

Refresh provider documentation before configuring clients. Revisit recommendations after meaningful model or harness updates and after each local experiment batch.
