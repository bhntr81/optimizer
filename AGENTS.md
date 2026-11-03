# Project guidance

This repository studies coding workflows for Claude, GPT-6, and xAI Grok.

- Keep recommendations distinguishable from measured results. Cite external claims and record retrieval dates in research/sources.json.
- Read docs/PLAYBOOK.md for workflow changes; benchmarks/README.md for scorecard changes. Load other documents only when relevant.
- Use Python standard library for local measurement tools. Check with `python3 -m unittest discover -s tests -v`.
- Local tests use disposable fixtures and require no credentials or production access. Run and repair affected checks autonomously.
- Preserve failed experiment records. Unknown tokens or cost stay null; never infer billing from a model name.
- Do not claim a framework or provider is faster until representative matched experiments support it.
- Keep provider-specific configuration separate from portable task instructions.
- Append a concise final usage line with tool-call count; exact tokens/cost only when runtime supplied, otherwise unavailable.

## Shared optimizer and prompt-writing workflow

Follow `/home/kali/Programming/Projects/AGENTS.md`: use the `coder_optimization` playbook and
task/review guidance; assign a dedicated prompt-writing agent to read the latest
output and write the next bounded prompt, then have the primary agent execute
and verify it within the authorized scope. Preserve this project's specific
constraints and model requirements. This standing workflow supersedes older
wording that made optimizer guidance optional; it adds no runtime dependency.
