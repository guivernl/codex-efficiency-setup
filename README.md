# Codex efficiency setup

Portable, privacy-safe defaults for new Codex and ChatGPT installations.

This repository intentionally contains no credentials, account identifiers,
machine paths, project names, plugin inventories, or complete user configuration
files.

## What it configures

- GPT-5.6 Terra as the default Codex model for routine work.
- Medium reasoning effort.
- Standard processing (`service_tier = "default"`), so Fast mode is not the default.
- Concise global Codex working agreements that favor targeted retrieval, proportionate
  tool use, reusable project context, economical delegation, and concise reporting.

The installers preserve unrelated settings. Before changing an existing file, they
create a timestamped backup in the same directory.

## Install on Windows

Clone or download this repository, open PowerShell in the repository directory, and run:

```powershell
.\install.ps1
```

If your Codex home is in a nonstandard location:

```powershell
.\install.ps1 -CodexHome "D:\path\to\.codex"
```

## Install on macOS or Linux

Clone or download this repository, then run:

```sh
sh ./install.sh
```

To use a nonstandard Codex home:

```sh
CODEX_HOME=/path/to/.codex sh ./install.sh
```

Start a new Codex task after installation. Codex loads global `AGENTS.md`
instructions when a new task/session begins.

## ChatGPT and Work

Codex reads the installed global `AGENTS.md`. Chat and Work do not use that file.
For those surfaces, append the text in [CHATGPT_CUSTOM_INSTRUCTIONS.md](CHATGPT_CUSTOM_INSTRUCTIONS.md)
to **Settings → Personalize**, preserving any useful instructions already present.

Project-specific instructions should stay inside their relevant ChatGPT Project or
repository. They should not be copied into the global file.

## Uninstall or roll back

The installer labels its addition inside `AGENTS.md` with managed comment markers.
Remove that marked block to remove the global efficiency instructions. Restore a
timestamped `.bak-*` file if you want to revert all changes from an installation.

## Security

Review scripts before running them. Do not commit your complete `config.toml`, tokens,
OAuth data, plugin connection data, hostnames, personal project names, or files copied
from your Codex home.

Codex's supported global and project instruction hierarchy is documented in the
[official OpenAI documentation](https://developers.openai.com/es-419/docs/agent-configuration/agents-md).

