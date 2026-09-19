# Approved configuration lifecycle

## Review, do not chase model names

Review official OpenAI model documentation, Codex release notes, configuration
reference, and AGENTS.md guidance weekly. Record the review date and direct source
links. Confirm availability on the actual intended surfaces; a model announcement
alone is not evidence that every installation can use it. Compare lead reasoning,
bounded execution quality, supported reasoning levels, and documented usage cost.
Do not invent usage ratios or choose a new model solely because it is newer.

Use a topic branch and a pull request. Never auto-merge, bypass failing checks, or
change permissions, spending, authentication, plugins, or remote connections.
Read existing open PRs first to avoid duplicate work. If no actionable change is
found, keep the review quiet; do not manufacture a release to record activity.

## Findings from everyday work

Ask Codex: "Propose this finding to the efficiency setup repository."
State the observed behavior, reproducible test, affected versions/surfaces, source,
proposed change, risks, and rollback. Remove private paths, hostnames, account IDs,
credentials, raw configurations and task transcripts before publishing. Use the
issue template for uncertain findings; use a PR for validated improvements.

## Publishing settings

1. Edit `defaults/manifest.json` and/or `defaults/AGENTS.md` on a topic branch.
2. Increment the manifest version for every distributed content change.
3. Add a dated entry to `CHANGELOG.md`, including sources and migration notes.
4. Run `python -m unittest discover -s tests -v` and test a disposable Codex home.
5. Review diffs for privacy, compatibility, unrelated settings, and rollback.
6. The repository owner approves and merges the PR into `main`.
7. Enrolled installations pick up `main` at the next daily check. Never restart
   running tasks automatically. Open a new task or restart manually as needed.

The updater is locally installed code, not remotely executed code. Changes to
`sync.py` or the scheduler require a separately reviewed local reinstall. A schema
change must not silently cause old clients to accept a broader set of settings.

`main` is the distribution channel, not an approval system by itself. Configure
GitHub branch protection/rulesets to require PRs and passing CI if available. This
repository does not grant an agent permission to change GitHub security settings.
Protect the owner's GitHub account with strong authentication: malicious text in
the managed instruction block is also a supply-chain risk.

## Routine schedule

- Per installation: opt-in daily check at 09:00 in that machine's timezone.
- Research: weekly Codex task; requires its host/app and authentication to be available.
- Before substantial work: a user or agent may invoke the installed updater;
  there is no universal pre-task hook installed by this repository.

ChatGPT Personalization and cloud/temporary instances are not synchronized by the
local filesystem updater. Apply the portable instructions manually there, or
explicitly bootstrap each new persistent Codex home.

## Sources reviewed 2026-09-19

- [Global and project instructions](https://developers.openai.com/es-419/docs/agent-configuration/agents-md)
- [Configuration reference](https://developers.openai.com/es-419/docs/config-file/config-reference)

Settings loaded into an existing conversation may remain unchanged. Treat new
tasks as the activation boundary; this updater never claims to switch the current
task's model or replace already-loaded instructions.
