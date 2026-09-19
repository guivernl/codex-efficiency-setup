# Security policy

This repository must remain safe to clone publicly.

Do not commit:

- API keys, access tokens, OAuth data, cookies, or account identifiers.
- Complete user `config.toml` files.
- Hostnames, IP addresses, usernames, home-directory paths, or personal project names.
- Plugin connection state, private MCP server configuration, or environment-variable values.

Report a security issue privately through GitHub's security advisory feature rather
than opening a public issue containing sensitive data.

## Synchronization trust boundary

Clients trust `main` for three allowed settings and global instruction text. Text
can influence agent behavior and needs careful review. Protect main with required
PRs/checks and protect the owner account. Clients cannot verify owner approval.

Updater code does not self-update; code/schema changes need a reviewed reinstall.
No local settings are uploaded. Local backups can contain sensitive configuration
and must never be published. Keep overrides and state private as well.

File updates roll back on ordinary errors, but are not transactional across power
loss. After interruption, pause scheduling and restore consistent files/state from
the local backups before resuming. No automatic app restart is performed.
