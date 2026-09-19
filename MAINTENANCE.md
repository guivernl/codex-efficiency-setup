# Maintaining the shared instructions

## New findings

Record the observation, affected surface/version, evidence or official source,
proposed instruction change, and tradeoffs. Remove all private details.
Ask Codex: "Propose this finding to the efficiency instructions repository."

Only general, reusable guidance belongs here. Keep machine-specific configuration
and project context on the relevant installation.

## Model releases and weekly review

Use official OpenAI documentation and release notes. Check availability, supported
features, lead reasoning quality, delegated execution suitability, and documented
usage cost. Do not invent savings or select a model solely because it is newer.

A separately authorized weekly Codex review can research and propose changes.
It should check existing PRs, avoid duplicates, and remain quiet when no actionable
change exists. It must not merge proposals or update installations automatically.

## Publish through a pull request

1. Create a topic branch and make a small, clear documentation change.
2. Add dated sources and a CHANGELOG.md entry.
3. Check consistency across README, portable guidance and ChatGPT text.
4. Check relative links, privacy, and the preserve-and-merge rule.
5. Explain what changes, why, and any capabilities that are surface-dependent.
6. The owner reviews and merges; other installations use it when next instructed.

No Python scripts, installers, machine-specific setup, or automated deployment
belong in this repository. No CI runner or programming-language requirement is
needed for reading these instructions.

Protecting main with required PRs is an optional owner decision. Repository text
does not enforce approval or grant permission to change GitHub security settings.

## Source reference

[Official Codex instruction guidance](https://developers.openai.com/es-419/docs/agent-configuration/agents-md)
was consulted on 2026-09-19. Verify current documentation when proposing changes;
do not assume all ChatGPT surfaces read local Codex instruction files.
