# Codex efficiency instructions

A shared, public reference for useful Codex and ChatGPT working instructions.
This repository contains instructions, not an installer or background updater.

Its objective is the best model and reasoning combination for each task within
every applicable usage allowance, preserving headroom instead of running to
exhaustion. See [USAGE_POLICY.md](USAGE_POLICY.md). Instructions can reduce this
risk, but cannot guarantee uninterrupted access or enforce account-wide quotas.

## Use it on an installation

Tell Codex:

> Read the latest approved instructions at https://github.com/guivernl/codex-efficiency-setup and apply the relevant guidance to this installation. Follow BOOTSTRAP.md. Preserve all existing custom instructions and local settings; explain conflicts before changing anything.

Repeat that request whenever you want an installation to pick up approved changes.
A link does not create automatic synchronization. Each installation is updated only
when you authorize it. Updating this repository does not update existing tasks.

## What to read

- [defaults/AGENTS.md](defaults/AGENTS.md): portable efficiency guidance.
- [BOOTSTRAP.md](BOOTSTRAP.md): how to apply it without losing customizations.
- [CHATGPT_CUSTOM_INSTRUCTIONS.md](CHATGPT_CUSTOM_INSTRUCTIONS.md): text for ChatGPT.
- [MAINTENANCE.md](MAINTENANCE.md): how findings and model releases become proposals.
- [CHANGELOG.md](CHANGELOG.md): dated approved changes.

Choose model and reasoning for the task and verified allowance. Astra leading
with Luna on bounded work is an option, not a mandatory choice for every task.
Check usage when available, use targeted retrieval, retain project context, and
keep responses concise. These are preferences, not a promise that every surface
can select models, delegate work, read usage, or change persistent settings.

## Your existing instructions stay yours

None of these files should replace an entire local instruction document.
Codex must read existing guidance first, add only missing non-conflicting guidance,
and preserve custom text both inside and outside any older marked section.
Markers identify earlier additions; they are not permission to overwrite them.
Conflicts require your decision. Applying the same guidance again should do nothing.

Do not change model settings merely by copying instruction text. If the active
surface needs a separate setting change, explain it and obtain approval first.
No scripts, scheduled installers, plugin changes, restarts or spending changes are
part of applying this repository.

## Keeping it current

Review new findings and official model documentation, propose a pull request,
then let the owner approve and merge it. Only approved main is the reference for
normal use. A weekly research task may propose updates; it must not apply them to
your machines automatically. Scheduling that review is separate from this repo.

See [SECURITY.md](SECURITY.md). Never publish private configurations, credentials,
account or server identifiers, or task transcripts.
