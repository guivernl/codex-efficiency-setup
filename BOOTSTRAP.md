# Installation bootstrap

Only follow when explicitly asked to configure an installation. Repository
maintenance is not installation authorization.

1. Confirm local file/command access. Without it provide
   `CHATGPT_CUSTOM_INSTRUCTIONS.md` for manual Personalization; do not claim setup.
2. Read `README.md`, `sync.py`, the applicable installer, `defaults/manifest.json`,
   and `defaults/AGENTS.md` completely. For recurring sync also read `install-sync.py`.
   Verify Python 3.11+ and the manifest's Codex compatibility floor.
3. Use approved main, not a pending PR except explicitly authorized disposable
   testing. Inspect useful local values and agree overrides before adoption.
4. One-time: run `install.ps1` or `sh install.sh`. For explicitly requested ongoing
   sync: `python install-sync.py --adopt --schedule` (python3 on Linux).
   Respect `CODEX_HOME` or pass a home. Don't enroll out-of-scope/retiring machines.
5. Verify one managed block, manifest values plus overrides, valid TOML, private
   backups, unchanged unrelated settings, and the requested schedule. Scheduling
   errors are not success. Never silently change privileges, enable lingering,
   restart apps or alter connections to repair scheduling.
6. Report version, files, backups, schedule, activation boundaries and manual steps.
   New tasks load new instructions; an explicit current model may override defaults.

Read shared usage before substantial work when available; remaining allowance is
100 minus usedPercent. Note reset time. Never redeem credits, change spending,
expose credentials or full configuration, or alter plugins, permissions, project
instructions, authentication or connections as part of this setup.
