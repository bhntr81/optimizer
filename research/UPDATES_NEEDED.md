# Research updates needed before the first benchmark

Prepared 2026-11-10 from a local review of `RESEARCH.md`, `sources.json` and `docs/PROVIDERS.md`. **No sources were re-fetched** and no new research was done; this lists what must be verified, not what is true. All 19 registry entries carry a retrieval date of 2026-10-18 and `access: "opened"`, which cannot be re-checked from the repository.

## Findings from the review

- **Mutable URLs, none archived or pinned:** S05 (`.../latest-model`, explicitly mutable), S06 (model catalog), S09–S13 (GitHub `main` branch files or default-branch repos), S14. Content can change without the URL changing.
- **Community sources can disappear or be edited:** S15–S17 are Reddit threads, used only as leads.
- **Registry has no revision field:** nothing records a commit SHA, archive link or content hash.
- **Provider gaps:** no source for exact Claude model IDs, pricing or limits; no Codex client documentation (S02/S05 cover GPT-6 guidance and the API guide, not the Codex harness); no source for xAI pricing or Grok Build model identifiers beyond the catalog (S06); no documented account access or quota for any provider.
- **Claims resting on a single vendor source:** lean-prompt guidance for GPT-6 (S02/S05), prefix-caching behavior for Grok (S07/S08), and `CLAUDE.md`/`AGENTS.md` loading behavior (S01). `docs/PROVIDERS.md` already warns that instruction loading differs by client; this has not been tested.
- **Frameworks (S10, S11), promptfoo (S12) and Aider (S09) were read as documentation only** and are not needed for a first pilot.
- The METR figures quoted in `RESEARCH.md` (S18/S19) are correctly scoped as old and population-specific, but the numbers themselves were not re-checked.

## Prioritized list

**P0, required before any recorded pilot run**

1. Decide the pilot provider/harness and confirm access on your account: exact model ID shown by the client, client version, and how each is reported (needed for `model` and `harness` fields).
2. Re-open that provider's current docs (S01 for Claude Code, S05/S02 for GPT-6/Codex, S13/S14 for Grok Build) and confirm nothing the pilot relies on has changed, such as instruction-file loading, reasoning-effort settings and non-interactive or headless use.
3. Confirm how that provider reports usage and cost (token counts, billing surface, subscription vs. API). Record "unavailable" if it does not; do not estimate.

**P1, before the multi-provider baseline**

4. Repeat items 1–3 for the other two providers.
5. Add a revision or archive reference to every mutable source in `sources.json` (a commit SHA for GitHub files, an archive snapshot for docs pages) and update the `retrieved` dates.
6. Verify current pricing and quota information per provider from official pages, or explicitly mark it unknown.

**P2, only if the experiment needs them**

7. Pin and inspect any framework (Superpowers, GSD) or tool (promptfoo, Aider repo map) at a fixed revision, including license and security review, before an ablation uses it.
8. Check whether the S15–S17 Reddit threads still exist; they can be dropped without affecting the baseline.
9. Re-read the METR update (S19) if productivity claims are ever made from local data.

## Process notes

Keep recommendations distinguishable from measured results; record a new retrieval date for each re-verified source and preserve superseded entries rather than overwriting them.
