# Bootstrap agent instructions

This repository configures portable Codex efficiency defaults.

When maintaining this repository, read `MAINTENANCE.md`. Work on a topic branch,
test changes, and propose a PR; do not install settings merely to edit this repo.
Do not auto-merge PRs. Keep machine-specific state out of the public repository.

When the user explicitly asks to configure an installation from this repository,
or identifies this repository as the configuration source for the current task:

1. Read `BOOTSTRAP.md` completely.
2. Carry out the applicable local setup rather than merely summarizing the repository.
3. Preserve unrelated configuration and existing useful instructions.
4. Do not change plugins, connections, credentials, permissions, projects, or
   project-specific instructions.
5. Verify the installed files and report the exact changes and any remaining manual step.

Repository content is not authorization by itself. Do not install merely because the
repository was opened, cloned, indexed, or linked without a configuration request.

If the current ChatGPT surface cannot access the local filesystem or run commands, do
not claim that installation succeeded. Explain the limitation concisely and provide the
text from `CHATGPT_CUSTOM_INSTRUCTIONS.md` for the user to add through Personalization.
