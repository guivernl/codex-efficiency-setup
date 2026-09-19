#!/usr/bin/env python3
"""Enroll the reviewed local efficiency updater and optionally schedule it."""

from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile


TASK_NAME = "Codex Efficiency Sync"
UNIT_BASENAME = "codex-efficiency-sync"


class SetupError(RuntimeError):
    pass


def _run(command: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            command,
            input=input_text,
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        details = getattr(exc, "stderr", None) or str(exc)
        raise SetupError(f"Command failed: {command[0]} ({details.strip()})") from exc


def _codex_home(value: str | None) -> Path:
    if value:
        return Path(value).expanduser().resolve()
    env_home = os.environ.get("CODEX_HOME")
    if env_home:
        return Path(env_home).expanduser().resolve()
    if os.name == "nt":
        profile = os.environ.get("USERPROFILE")
        if not profile:
            raise SetupError("USERPROFILE is unavailable; pass --codex-home explicitly")
        return (Path(profile) / ".codex").resolve()
    home = os.environ.get("HOME")
    if not home:
        raise SetupError("HOME is unavailable; pass --codex-home explicitly")
    return (Path(home) / ".codex").resolve()


def _enroll(source: Path, codex_home: Path) -> Path:
    source_script = source / "sync.py"
    if not source_script.is_file():
        raise SetupError(f"Reviewed local updater not found: {source_script}")

    install_dir = codex_home / "efficiency-sync"
    installed_script = install_dir / "sync.py"
    install_dir.mkdir(parents=True, exist_ok=True)
    source_bytes = source_script.read_bytes()
    if installed_script.exists():
        if installed_script.read_bytes() != source_bytes:
            raise SetupError(
                f"An existing, different updater is at {installed_script}; "
                "review or move it before enrolling this version"
            )
    else:
        with tempfile.NamedTemporaryFile(dir=install_dir, prefix="sync-", delete=False) as temp:
            temp_path = Path(temp.name)
            temp.write(source_bytes)
        try:
            os.replace(temp_path, installed_script)
        finally:
            temp_path.unlink(missing_ok=True)

    return installed_script


def _adopt(script: Path, source: Path, codex_home: Path) -> None:
    _run([
        sys.executable,
        str(script),
        "--source",
        str(source.resolve()),
        "--apply",
        "--adopt",
        "--codex-home",
        str(codex_home),
    ])


def _ps_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _windows_schedule_command(script: Path, codex_home: Path) -> list[str]:
    action_body = "\n".join([
        "$ErrorActionPreference = 'Stop'",
        f"$logDirectory = Join-Path {_ps_quote(str(script.parent))} 'logs'",
        "$logPath = Join-Path $logDirectory 'efficiency-sync.log'",
        "New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null",
        "$syncArguments = @(",
        f"  {_ps_quote(str(script))}, '--apply', '--codex-home', {_ps_quote(str(codex_home))}",
        ")",
        "$syncExit = 1",
        "try {",
        "  $ErrorActionPreference = 'Continue'",
        f"  $output = & {_ps_quote(sys.executable)} @syncArguments 2>&1",
        "  if ($null -ne $LASTEXITCODE) { $syncExit = $LASTEXITCODE }",
        "} catch { $output = $_; $syncExit = 1 }",
        "$ErrorActionPreference = 'Stop'",
        "$timestamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'",
        "\"[$timestamp] exit=$syncExit\" | Out-File -FilePath $logPath -Append -Encoding utf8",
        "$output | Out-File -FilePath $logPath -Append -Encoding utf8",
        "exit $syncExit",
    ])
    action_encoded = base64.b64encode(action_body.encode("utf-16le")).decode("ascii")
    action_arguments = f"-NoProfile -NonInteractive -WindowStyle Hidden -EncodedCommand {action_encoded}"
    ps = "\n".join([
        "$ErrorActionPreference = 'Stop'",
        f"$taskName = {_ps_quote(TASK_NAME)}",
        "if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {",
        "  throw \"A scheduled task named '$taskName' already exists; inspect it before replacing it.\"",
        "}",
        f"$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument {_ps_quote(action_arguments)}",
        "$trigger = New-ScheduledTaskTrigger -Daily -At '9:00 AM'",
        "$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -WakeToRun:$false -MultipleInstances IgnoreNew",
        "$identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name",
        "$principal = New-ScheduledTaskPrincipal -UserId $identity -LogonType Interactive -RunLevel Limited",
        "Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Description 'Codex efficiency sync; enrolled from a reviewed local updater.' | Out-Null",
    ])
    encoded = base64.b64encode(ps.encode("utf-16le")).decode("ascii")
    return ["powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded]


def _linux_units(script: Path, codex_home: Path, unit_dir: Path) -> tuple[Path, str, Path, str]:
    def systemd_arg(value: str) -> str:
        # systemd does not invoke a shell; quote each argument using its own parser.
        if any(ord(character) < 32 for character in value):
            raise SetupError("Newlines and control characters are not supported in scheduled paths")
        return '"' + (value.replace("\\", "\\\\").replace('"', '\\"')
                       .replace("%", "%%").replace("$", "$$")) + '"'

    python = systemd_arg(sys.executable)
    sync = systemd_arg(str(script))
    home = systemd_arg(str(codex_home))
    service = "\n".join([
        "[Unit]",
        "Description=Apply reviewed Codex efficiency defaults",
        "",
        "[Service]",
        "Type=oneshot",
        f"ExecStart={python} {sync} --apply --codex-home {home}",
        "",
    ])
    timer = "\n".join([
        "[Unit]",
        "Description=Daily Codex efficiency synchronization",
        "",
        "[Timer]",
        "OnCalendar=*-*-* 09:00:00",
        "Persistent=true",
        "RandomizedDelaySec=10min",
        "Unit=codex-efficiency-sync.service",
        "",
        "[Install]",
        "WantedBy=timers.target",
        "",
    ])
    return (
        unit_dir / f"{UNIT_BASENAME}.service", service,
        unit_dir / f"{UNIT_BASENAME}.timer", timer,
    )


def _preflight_linux(unit_dir: Path, script: Path, codex_home: Path) -> None:
    bus = os.environ.get("DBUS_SESSION_BUS_ADDRESS")
    runtime = os.environ.get("XDG_RUNTIME_DIR")
    has_user_bus = bool(bus) or bool(runtime and (Path(runtime) / "bus").exists())
    if not has_user_bus:
        raise SetupError("No systemd user bus is available; open a user session and retry")
    _run(["systemctl", "--user", "show-environment"])
    service_path, service, timer_path, timer = _linux_units(script, codex_home, unit_dir)
    for path, content in ((service_path, service), (timer_path, timer)):
        if path.exists() and path.read_text(encoding="utf-8") != content:
            raise SetupError(f"A different schedule already exists at {path}; inspect it before replacing it")


def _preflight_windows() -> None:
    ps = "\n".join([
        "$ErrorActionPreference = 'Stop'",
        f"$taskName = {_ps_quote(TASK_NAME)}",
        "if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {",
        "  throw \"A scheduled task named '$taskName' already exists; inspect it before replacing it.\"",
        "}",
    ])
    encoded = base64.b64encode(ps.encode("utf-16le")).decode("ascii")
    _run(["powershell.exe", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded])


def _install_linux_schedule(script: Path, codex_home: Path, unit_dir: Path) -> None:
    service_path, service, timer_path, timer = _linux_units(script, codex_home, unit_dir)
    unit_dir.mkdir(parents=True, exist_ok=True)
    for path, content in ((service_path, service), (timer_path, timer)):
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    _run(["systemctl", "--user", "daemon-reload"])
    _run(["systemctl", "--user", "enable", "--now", f"{UNIT_BASENAME}.timer"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent,
                        help="local repository containing reviewed sync.py")
    parser.add_argument("--codex-home", help="Codex home (defaults to CODEX_HOME or ~/.codex)")
    parser.add_argument("--adopt", action="store_true",
                        help="explicitly apply the reviewed local defaults during initial enrollment")
    parser.add_argument("--schedule", action="store_true",
                        help="opt in to a daily 09:00 local user schedule")
    args = parser.parse_args(argv)

    try:
        system = platform.system()
        if args.schedule and system == "Darwin":
            raise SetupError("Automatic scheduling is not supported on macOS")
        if args.schedule and not args.adopt:
            raise SetupError("--schedule requires --adopt so the local defaults are explicitly enrolled first")
        if system not in {"Windows", "Linux", "Darwin"}:
            raise SetupError(f"Unsupported operating system: {system}")

        source = args.source.expanduser().resolve()
        codex_home = _codex_home(args.codex_home)
        if not (source / "sync.py").is_file():
            raise SetupError(f"Reviewed local updater not found: {source / 'sync.py'}")

        unit_dir: Path | None = None
        if args.schedule and system == "Linux":
            config_home = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
            unit_dir = config_home / "systemd" / "user"
            _preflight_linux(unit_dir, codex_home / "efficiency-sync" / "sync.py", codex_home)
        elif args.schedule and system == "Windows":
            # Existing tasks are never overwritten, even if their settings are opaque.
            _preflight_windows()

        installed_script = _enroll(source, codex_home)
        if args.adopt:
            _adopt(installed_script, source, codex_home)
        if args.schedule and system == "Windows":
            _run(_windows_schedule_command(installed_script, codex_home))
        elif args.schedule and system == "Linux":
            assert unit_dir is not None
            _install_linux_schedule(installed_script, codex_home, unit_dir)
        print(f"Enrolled reviewed updater in {codex_home / 'efficiency-sync'}")
        if args.schedule:
            print("Daily 09:00 local synchronization was scheduled.")
        else:
            print("No schedule was requested; future synchronization is manual.")
        return 0
    except (SetupError, OSError) as exc:
        print(f"Setup failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
