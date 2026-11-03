# Provider notes

Reviewed 2026-10-18. Distinguish the **model**, the **coding harness**, and the **subscription/API billing surface**. A web chat comparison does not isolate model quality from tooling.

## Claude

Claude Code supplies repository access and an execution loop. Its guidance emphasizes observable verification and selective planning; CLAUDE.md carries recurring project guidance. Use a small file and put task-specific state elsewhere. [Claude Code best practices](https://code.claude.com/docs/en/best-practices)

Starting trial: Claude Code with the task brief and normal tool access, using the exact model available in your account. Record that model ID and harness version. For longer work, save incremental progress and verify user-visible functionality between slices. [Long-running harnesses](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)

This repo's CLAUDE.md imports AGENTS.md. Check instruction-loading behavior when copying templates into other clients. No Claude model ranking or pricing is assumed here.

## GPT-6 / Codex

The requested family is GPT-6. Official documentation explicitly discusses GPT-6 Astra; use an exact model ID exposed by your client rather than treating the conversational label “GPT-6” as an API identifier. Preserve that selection in experiments. [Official model guide](https://developers.openai.com/api/docs/guides/latest-model)

Use concise outcome-level instructions, retain consequential invariants, and define completion. The GPT-6 Astra guidance recommends revisiting old skills and AGENTS.md rules that force unnecessary reading, testing, or premature review pauses. For this project, local checks are explicitly authorized so routine verification can continue. [Official GPT-6 instruction guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

Starting trial: one Codex implementer with the ordinary configuration currently available to you. Compare reasoning effort on difficult tasks instead of hardcoding maximum effort everywhere. No API integration or provider settings are changed by this repository.

## xAI Grok

Grok Build is xAI's coding-agent surface. The official repository describes terminal, headless, and editor integration, file references, and resumable sessions. Use its own current docs for installation and configuration. [Official getting-started guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/01-getting-started.md), [product overview](https://docs.x.ai/build/overview)

Starting trial: run the same acceptance-defined tasks through Grok Build, recording the actual model ID and tool configuration. If using a different Grok client, explicitly provide the task and repository instructions; do not assume all clients load AGENTS.md or a GROK.md file automatically.

For API experiments, separate prefix-cache behavior from model performance. Preserve stable prefixes and use the current SDK's supported conversation-state mechanism. The cookbook and lower-level caching docs describe different integration surfaces; do not mix parameters blindly. [Caching cookbook](https://docs.x.ai/cookbook/examples/prompt-caching), [cache mechanics](https://docs.x.ai/developers/advanced-api-usage/prompt-caching/how-it-works)

## Proposed routing experiment

| Task | Initial assignment | Escalation to test |
| --- | --- | --- |
| Small bug / feature | Any one available provider | Switch only after a diagnosed failure |
| Architectural ambiguity | One planning pass, then implementation | Compare concise plan versus direct execution |
| Difficult debugging | Agent with a reliable reproducer | Fresh context or a second provider with the evidence |
| Consequential patch | Implementer plus fresh review | Compare same-model versus cross-provider reviewer |
| Mechanical edit | Cheapest configuration that passes your checks | Stronger model only if acceptance degrades |

These are hypotheses. We do not assign “Claude plans, GPT codes, Grok researches” as a fixed hierarchy without matched local results. Account access, quotas, exact prices, and installed versions remain unverified.
