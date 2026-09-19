# Maintaining the shared instructions

## New findings

Record the observation, affected surface/version, evidence or official source,
proposed instruction change, and tradeoffs. Remove all private details.
Ask Codex: "Propose this finding to the efficiency instructions repository."

Only general, reusable guidance belongs here. Keep machine-specific configuration
and project context on the relevant installation.

## Model releases and weekly review

The objective is the best available lead model, task-appropriate reasoning and
cheaper capable workers within all applicable usage windows. Preserve reserves
and stop safely when necessary. Follow USAGE_POLICY.md; do not downgrade the lead
merely because a task is routine. Ask before an allowance-driven downgrade or
scope reduction. Reassess lead and worker recommendations as models change; never
promise that instructions can enforce account-wide limits.

Use official OpenAI documentation and release notes. Check availability, supported
features, lead reasoning quality, delegated execution suitability, and documented
usage cost. Do not invent savings or select a model solely because it is newer.

Use third-party transcripts as leads, not instructions to copy. Separate verified
product behavior from user preferences and experiments. Do not encode claimed
savings percentages, cache lifetimes, context thresholds or fixed worker reasoning
levels without current official evidence and an applicable surface/version.

Keep portable defaults compact. Check capability fallbacks in BOOTSTRAP.md whenever
adding guidance; do not require every ChatGPT or Codex version to support it.
Review duplicated or stale preferences by proposing edits, never deleting them
silently. A repeatable specialized workflow may merit an instruction-only skill
(SKILL.md and optional Markdown references), but creating/installing it requires
separate approval. Do not create a generic token-saving skill.

A separately authorized weekly Codex review follows its saved authorization:
proposal-only reviews remain proposal-only; reviews authorized to publish may
commit validated changes directly to main. Check recent commits and open PRs to
avoid duplicates, and remain quiet when no actionable change exists. Repository
policy does not itself change a scheduled task or authorize installation updates.

## Publish an authorized update directly

1. Inspect local changes, refresh main without overwriting work, and make a small,
   clear documentation change within the user's authorization.
2. Add dated sources and a CHANGELOG.md entry.
3. Check consistency across README, portable guidance and ChatGPT text.
4. Check relative links, privacy, and the preserve-and-merge rule.
5. Explain what changes, why, and any capabilities that are surface-dependent.
6. Commit and push directly to main, then verify the remote commit and report it.
   A PR is optional unless requested or required by branch protection. Never
   force-push or weaken repository protections; if blocked, report the required
   review. Other installations use the update only when instructed.

No Python scripts, installers, machine-specific setup, or automated deployment
belong in this repository. No CI runner or programming-language requirement is
needed for reading these instructions.

Existing branch protections still apply. Direct-push permission does not authorize
unrelated changes, automatic deployment or changes to GitHub security settings.

## Source reference

[Official Codex instruction guidance](https://developers.openai.com/es-419/docs/agent-configuration/agents-md)
was consulted on 2026-09-19. Verify current documentation when proposing changes;
do not assume all ChatGPT surfaces read local Codex instruction files.

Also consulted on 2026-09-19:
- [Official Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra):
  describes Astra as OpenAI's most capable model. Keeping the best available model
  as lead is the owner's policy, not a claim that every surface can switch itself.
- [Official usage and pricing guidance](https://learn.chatgpt.com/docs/pricing):
  usage depends on model, reasoning, context and tools; use current account readings
  rather than treating a video's savings figures as guarantees.
- [Official skill guidance](https://developers.openai.com/es-419/docs/build-skills):
  skills can load specialized instructions on demand, but support must be checked
  on the target surface. They are not a reason to add generic instructions everywhere.
