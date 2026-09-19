# Safely apply these instructions

Follow this only when the user explicitly asks to apply the repository's guidance.
Read approved main, not a pending proposal, unless the user asks to review that proposal.

## Inspect first

Read README.md and defaults/AGENTS.md. For ChatGPT also read
CHATGPT_CUSTOM_INSTRUCTIONS.md. Inspect applicable existing global and project
instructions using the current surface's supported capabilities. Do not assume
every installation uses the same paths, model choices, or features.

Keep private configuration local. Do not print or upload full settings or credentials.

## Merge, never replace

- Preserve every existing custom instruction, including custom text inside any
  old codex-efficiency-setup marked block.
- Compare meaning, not just wording. Do not duplicate guidance already present.
- Add only missing, non-conflicting guidance to the appropriate global document.
- Leave project-specific guidance in its existing project; do not copy it globally.
- If guidance conflicts, explain both choices and ask before changing either.
- Do not delete obsolete-looking text without the user's approval.
- Before an authorized edit, make a private rollback copy of the affected document.
  Never commit that copy or its contents to this public repository.
- Make a minimal edit, inspect the diff, and confirm custom guidance remains intact.

If the relevant document is unavailable, do not invent its contents or claim a
successful merge. Provide the proposed addition for the user to apply manually.

## Settings are separate

Instructions cannot guarantee a model switch, delegation, usage access or Fast-mode
change. Verify what the current surface supports. Explain any needed settings change
and obtain explicit approval; do not silently change existing preferences.

Do not alter credentials, connections, plugins, permissions, spending, projects,
or project instructions. Do not install scripts, timers or background services.
Never restart or interrupt active tasks merely to apply guidance.

## Verify and report

Report which document was changed, which guidance was added, where the private
backup is, and any conflict or manual step. If nothing is missing, say no changes
were needed. Existing conversations may retain loaded instructions; do not promise
immediate changes to the current task.

This procedure is repeated only on request. It creates no automatic update mechanism.
