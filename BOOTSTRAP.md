# Installation bootstrap

Follow this procedure when the user has explicitly asked to configure their current
installation from this repository.

## 1. Confirm capability

Determine whether the current surface has local filesystem and command execution access.

- In a local Codex task, continue with the installation.
- In Chat or Work without local execution access, do not claim to have configured the
  computer. Provide `CHATGPT_CUSTOM_INSTRUCTIONS.md` and explain that Personalization is
  the remaining manual step.

Do not request information already available from the environment. Do not ask the user
to choose an operating system when it can be detected locally.

## 2. Inspect before execution

Read the applicable installer and the files it consumes:

- Windows: `install.ps1` and `defaults/AGENTS.md`
- macOS or Linux: `install.sh` and `defaults/AGENTS.md`

Stop if the checked-out files differ materially from the documented behavior, attempt
to transmit local data, or contain credentials.

## 3. Install

Run the installer appropriate for the current operating system from the repository root.

Windows:

```powershell
.\install.ps1
```

macOS or Linux:

```sh
sh ./install.sh
```

Respect `CODEX_HOME` when it is already defined. Otherwise use the normal Codex home.
The installer must preserve unrelated settings and create timestamped backups before
modifying existing files.

## 4. Verify

Verify all of the following without exposing private configuration values:

- The global `AGENTS.md` contains exactly one managed block between
  `codex-efficiency-setup:start` and `codex-efficiency-setup:end`.
- Top-level Codex configuration selects `gpt-6-astra`, low reasoning, and
  `service_tier = "default"`.
- Existing unrelated configuration remains present.
- No plugin, MCP server, connection, credential, permission, project, or project-specific
  instruction was changed.

When the app exposes a read-only usage-limit capability, read it after installation and
report the remaining percentage and reset time. Calculate remaining percentage as
`100 - usedPercent`. Do not redeem a reset credit, purchase credits, or modify spending
controls.

Do not print tokens, environment-variable values, OAuth data, or full configuration files.

## 5. Report

Report:

- Which files were changed.
- Where backups were created.
- Which defaults are now active.
- The verified remaining Work/Codex allowance and reset time, when available.
- That a new Codex task/session is required to load the global instructions.
- Whether Chat/Work Personalization still requires the manual text in
  `CHATGPT_CUSTOM_INSTRUCTIONS.md`.
