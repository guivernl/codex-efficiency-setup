# Codex efficiency setup

Portable, privacy-safe settings with owner-approved updates.

> Configure this installation from https://github.com/guivernl/codex-efficiency-setup

Codex follows [BOOTSTRAP.md](BOOTSTRAP.md), inspects the code, preserves unrelated
settings and verifies installation. A bare link is not authorization to modify a
machine. Editing this repository is not an installation request.

## Defaults

Astra leads planning, integration and review; Luna handles suitable bounded work.
Read shared usage before substantial work when available. Use targeted retrieval,
concise successful outputs, useful diagnostics, and existing project context.

`defaults/manifest.json` versions three managed root settings: `model`,
`model_reasoning_effort`, and `service_tier` (Astra, low, standard by default).
`defaults/AGENTS.md` supplies the managed instruction block. Named agents, global
worker settings and project overrides remain local; explicitly selected workers
can override the delegation recommendation. New managed keys require reviewed code.

## One-time installation

Requires Python 3.11+ and a Codex CLI meeting the manifest's minimum version.
Review the scripts first. From an approved checkout:

```powershell
# Windows, no schedule
.\install.ps1
```

```sh
# Linux/macOS, no schedule
sh ./install.sh
```

Both honor `CODEX_HOME`; PowerShell also accepts `-CodexHome`. These adopt the three
managed settings. Put intentional local choices in overrides before installation.
Unrelated instructions, credentials, connections, plugins, permissions and project
configuration are not changed.

## Approved daily updates

From an **approved, reviewed checkout**:

```sh
# Use python3 on Linux where python is not installed.
python install-sync.py --adopt --schedule
```

Pass `--codex-home PATH` for a separate home. Omit `--schedule` for manual updates.
Enroll once per Codex home/user, not once per binary sharing that home. Initial
adoption applies the reviewed checkout; scheduled checks resolve `main` to a commit
and fetch immutable configuration data at that commit.

- Windows: daily 09:00 local, current interactive user, no password stored, no wake;
  catches up when available. Laptop must be powered on and user logged in.
- Linux: daily 09:00 local plus up to ten minutes jitter, persistent systemd user
  timer. Running after logout/reboot requires a running user manager, commonly
  administrator-approved lingering; this installer does not enable it.
- macOS: manual updater only; automatic scheduling is not implemented.

The daily updater calls no models and uploads no local configuration. It fetches
data, not executable code. Updater-code changes require a reviewed reinstall.

Manual preview (default) and application:

```sh
python /path/to/codex-home/efficiency-sync/sync.py --codex-home /path/to/codex-home
python /path/to/codex-home/efficiency-sync/sync.py --codex-home /path/to/codex-home --apply
```

There is no universal pre-task hook. An authorized agent may invoke a check before
substantial work. Existing tasks may retain loaded settings; start a new task or
restart manually as needed. No automatic restarts, CLI upgrades or spending changes.

## Local overrides and conflicts

Create `<Codex home>/efficiency-sync/overrides.json` locally, never in this repo:

```json
{"model_reasoning_effort": "medium"}
```

Only the same three managed keys are accepted. After manually editing a managed
setting, add a matching override or sync stops rather than overwriting the edit.
Local edits/removal of the managed instruction block also stop synchronization.
Keep extra instructions outside the markers. Resolve conflicts manually; do not
blindly delete the state record to silence an error.

## Review, status and rollback

Follow [MAINTENANCE.md](MAINTENANCE.md). Weekly research proposes PRs; the owner
approves and merges to `main`. Clients then pick up that data. The weekly AI review
must be scheduled separately in the Codex app; repo files alone don't schedule it.

Protect `main` with required PRs/checks where available. Clients trust the branch:
they cannot distinguish an approved merge from an owner's direct push. Instruction
text is trusted configuration even though it is not executable code.

`<Codex home>/efficiency-sync/state.json` records applied version/commit. Private
rollback copies are in `backups`; they may contain sensitive configuration and must
never be uploaded. No automatic backup pruning is performed. Inspect a stale
`sync.lock` after a crash; remove it only after confirming no sync process is running.

Pause Linux updates with `systemctl --user disable --now codex-efficiency-sync.timer`.
On Windows disable **Codex Efficiency Sync** in Task Scheduler. Check task history
or the user journal for failures. Disable scheduling before rollback, then restore
matching configuration, instructions and state backups. If previous state did not
exist, remove the new state record after restoring the original files.

## ChatGPT and Work

Local file sync does not update Personalization. On surfaces without local access,
manually append [CHATGPT_CUSTOM_INSTRUCTIONS.md](CHATGPT_CUSTOM_INSTRUCTIONS.md),
retaining useful existing instructions. Keep project-specific context in Projects.

See [SECURITY.md](SECURITY.md): never publish credentials, account/server IDs, private
paths, complete configs, connection state or raw task transcripts.
