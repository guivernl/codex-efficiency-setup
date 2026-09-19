#!/usr/bin/env python3
"""Safely synchronize the approved Codex efficiency defaults."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import tomllib
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = "guivernl/codex-efficiency-setup"
START = "<!-- codex-efficiency-setup:start -->"
END = "<!-- codex-efficiency-setup:end -->"
KEYS = ("model", "model_reasoning_effort", "service_tier")
STATE_DIR = "efficiency-sync"


class SyncError(Exception):
    pass


def _fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "codex-efficiency-sync", "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.read(1_000_001)
    except (urllib.error.URLError, TimeoutError) as exc:
        raise SyncError(f"source fetch failed: {exc}") from exc


def remote_source() -> tuple[dict, bytes, str]:
    ref = json.loads(_fetch(f"https://api.github.com/repos/{REPO}/git/ref/heads/main"))
    sha = ref["object"]["sha"]
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise SyncError("GitHub returned an invalid commit identifier")
    base = f"https://raw.githubusercontent.com/{REPO}/{sha}/"
    manifest = json.loads(_fetch(base + "defaults/manifest.json"))
    agents = _fetch(base + "defaults/AGENTS.md")
    return manifest, agents, sha


def local_source(source: Path) -> tuple[dict, bytes, str]:
    manifest = json.loads((source / "defaults" / "manifest.json").read_text(encoding="utf-8"))
    agents = (source / "defaults" / "AGENTS.md").read_bytes()
    try:
        sha = subprocess.run(["git", "-C", str(source), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except Exception:
        sha = "local"
    return manifest, agents, sha


def _semver(value: object, label: str) -> tuple[int, int, int]:
    if not isinstance(value, str) or not re.fullmatch(r"(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)", value):
        raise SyncError(f"{label} must be a stable semantic version")
    return tuple(map(int, value.split(".")))


def check_codex_version(minimum: str, executable: str | None = None) -> None:
    minimum_tuple = _semver(minimum, "minimum_codex_version")
    executable = executable or shutil.which("codex")
    if not executable:
        candidates = [Path.home() / ".local" / "bin" / "codex"]
        local_appdata = os.environ.get("LOCALAPPDATA")
        if local_appdata:
            candidates.append(Path(local_appdata) / "Programs" / "OpenAI" / "Codex" / "bin" / "codex.exe")
            bundled_root = Path(local_appdata) / "OpenAI" / "Codex" / "bin"
            if bundled_root.is_dir():
                bundled = sorted(bundled_root.glob("*/codex.exe"), key=lambda p: p.stat().st_mtime, reverse=True)
                candidates.extend(bundled)
        executable = next((str(path) for path in candidates if path.is_file()), None)
    if not executable:
        raise SyncError("Codex CLI was not found; cannot verify minimum version")
    try:
        result = subprocess.run([executable, "--version"], check=True, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise SyncError(f"could not verify Codex CLI version: {exc}") from exc
    match = re.search(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?!\d)", result.stdout + " " + result.stderr)
    version_tuple = tuple(map(int, match.groups()[:3])) if match else None
    prerelease = match.group(4) if match else None
    if not match or version_tuple < minimum_tuple or (version_tuple == minimum_tuple and prerelease):
        raise SyncError(f"Codex CLI {minimum} or newer is required")


def validate_source(manifest: object, agents: bytes) -> tuple[str, dict[str, str], str, str]:
    if not isinstance(manifest, dict) or set(manifest) != {"schema", "version", "minimum_codex_version", "settings", "agents_file"}:
        raise SyncError("manifest fields are invalid")
    if type(manifest["schema"]) is not int or manifest["schema"] != 1:
        raise SyncError("unsupported manifest schema or version")
    _semver(manifest["version"], "manifest version")
    minimum_version = _semver(manifest["minimum_codex_version"], "minimum_codex_version")
    if minimum_version < (0, 154, 0):
        raise SyncError("minimum_codex_version cannot be lower than 0.154.0")
    if manifest["agents_file"] != "AGENTS.md":
        raise SyncError("manifest may only name defaults/AGENTS.md")
    settings = manifest["settings"]
    if not isinstance(settings, dict) or set(settings) != set(KEYS) or not all(isinstance(v, str) and v for v in settings.values()):
        raise SyncError("manifest settings must contain only the three approved string keys")
    if len(agents) > 100_000:
        raise SyncError("instruction file is too large")
    try:
        agents.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SyncError("instruction file must be UTF-8") from exc
    if START in agents.decode() or END in agents.decode():
        raise SyncError("source instruction file must not contain managed markers")
    content_hash = hashlib.sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode() + b"\0" + agents).hexdigest()
    return manifest["version"], settings, hashlib.sha256(agents).hexdigest(), content_hash


def replace_block(existing: str, body: str, previous_hash: str | None) -> str:
    starts, ends = existing.count(START), existing.count(END)
    if starts != ends or starts > 1:
        raise SyncError("global AGENTS.md has malformed or duplicate managed markers")
    block = f"{START}\n{body.rstrip()}\n{END}"
    if starts:
        a, b = existing.index(START), existing.index(END)
        if a >= b:
            raise SyncError("global AGENTS.md has reversed managed markers")
        old_block = existing[a:b + len(END)]
        if previous_hash and hashlib.sha256(old_block.encode("utf-8")).hexdigest() != previous_hash:
            raise SyncError("managed AGENTS.md block was modified locally")
        return existing[:a] + block + existing[b + len(END):]
    if previous_hash:
        raise SyncError("previously managed AGENTS.md block was removed locally")
    if existing:
        return existing.rstrip("\r\n") + "\n\n" + block + "\n"
    return block + "\n"


def _toml_update(raw: bytes, desired: dict[str, str]) -> tuple[bytes, dict[str, str]]:
    try:
        text = raw.decode("utf-8")
        parsed = tomllib.loads(text)
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise SyncError(f"config.toml is invalid UTF-8/TOML: {exc}") from exc
    lines = text.splitlines(keepends=True)
    top_end = next((i for i, line in enumerate(lines) if re.match(r"^\s*\[", line)), len(lines))
    found: dict[str, int] = {}
    for i, line in enumerate(lines[:top_end]):
        stripped = line.lstrip()
        if stripped.startswith("#"):
            continue
        m = re.match(r"^\s*([A-Za-z0-9_-]+)\s*=", line)
        q = re.match(r'^\s*["\']([^"\']+)["\']\s*=', line)
        if q and q.group(1) in KEYS:
            raise SyncError("quoted managed TOML keys are unsupported")
        if m and m.group(1) in KEYS:
            key = m.group(1)
            if key in found:
                raise SyncError(f"duplicate managed key: {key}")
            found[key] = i
            val_match = re.match(r"^(\s*[^=]+?\s*=\s*)(.*?)(\r?\n)?$", line)
            if not val_match or not val_match.group(2).strip():
                raise SyncError(f"ambiguous managed value: {key}")
            if "\"" in val_match.group(2) and val_match.group(2).count('"') % 2:
                raise SyncError(f"multiline managed value is unsupported: {key}")
    missing = []
    for key, value in desired.items():
        if not re.fullmatch(r"[A-Za-z0-9_.+-]+", value):
            raise SyncError(f"unsafe setting value: {key}")
        if key in found:
            i = found[key]
            line = lines[i]
            m = re.match(r"^(\s*[^=]+?\s*=\s*)(.*?)(\s+#.*)?(\r?\n)?$", line)
            if not m:
                raise SyncError(f"ambiguous managed assignment: {key}")
            lines[i] = f'{m.group(1)}"{value}"{m.group(3) or ""}{m.group(4) or ""}'
        else:
            missing.append(f'{key} = "{value}"\n')
    lines = missing + lines
    updated = "".join(lines).encode("utf-8")
    try:
        final = tomllib.loads(updated.decode("utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise SyncError(f"updated config.toml would be invalid: {exc}") from exc
    before_unmanaged = {k: v for k, v in parsed.items() if k not in KEYS}
    after_unmanaged = {k: v for k, v in final.items() if k not in KEYS}
    if before_unmanaged != after_unmanaged:
        raise SyncError("config.toml contains ambiguous text near a managed key; unrelated values would change")
    return updated, {k: final[k] for k in KEYS}


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


def _validate_state(state: object) -> dict:
    fields = {"schema", "values", "agents_block_sha256", "source_sha256", "version", "commit"}
    if (not isinstance(state, dict) or set(state) != fields or type(state.get("schema")) is not int or state["schema"] != 1
            or not isinstance(state.get("values"), dict) or set(state["values"]) != set(KEYS)
            or not all(isinstance(v, str) and re.fullmatch(r"[A-Za-z0-9_.+-]+", v) for v in state["values"].values())
            or not isinstance(state.get("commit"), str) or not state["commit"]):
        raise SyncError("managed state file is invalid")
    if state["commit"] != "local" and not re.fullmatch(r"[0-9a-f]{40}", state["commit"]):
        raise SyncError("managed state file is invalid")
    for key in ("agents_block_sha256", "source_sha256"):
        if not isinstance(state.get(key), str) or not re.fullmatch(r"[0-9a-f]{64}", state[key]):
            raise SyncError("managed state file is invalid")
    _semver(state.get("version"), "managed state version")
    return state


def sync(codex_home: Path, source: Path | None = None, apply: bool = False, adopt: bool = False, codex_executable: str | None = None) -> list[str]:
    codex_home = codex_home.resolve()
    state_dir = codex_home / STATE_DIR
    state_dir.mkdir(parents=True, exist_ok=True)
    if os.name != "nt":
        os.chmod(state_dir, 0o700)
    lock = state_dir / "sync.lock"
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise SyncError("another sync is running (or a stale sync.lock exists)") from exc
    os.close(lock_fd)
    try:
        manifest, source_agents, commit = local_source(source) if source else remote_source()
        version, settings, _, source_hash = validate_source(manifest, source_agents)
        check_codex_version(manifest["minimum_codex_version"], codex_executable)
        overrides_path = state_dir / "overrides.json"
        overrides: dict = {}
        if overrides_path.exists():
            try:
                overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
            except Exception as exc:
                raise SyncError("overrides.json is invalid") from exc
            if not isinstance(overrides, dict) or set(overrides) - set(KEYS) or not all(isinstance(v, str) and v for v in overrides.values()):
                raise SyncError("overrides may contain only approved setting keys with string values")
        desired = {**settings, **overrides}
        state_path = state_dir / "state.json"
        try:
            state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else None
        except (OSError, ValueError) as exc:
            raise SyncError("managed state file is invalid") from exc
        if state is not None:
            state = _validate_state(state)
            if state["version"] == version and state["source_sha256"] != source_hash:
                raise SyncError("source content changed without a manifest version bump")
        config_path, agents_path = codex_home / "config.toml", codex_home / "AGENTS.md"
        config_raw = config_path.read_bytes() if config_path.exists() else b""
        try:
            current_toml = tomllib.loads(config_raw.decode("utf-8")) if config_raw else {}
        except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
            raise SyncError(f"config.toml is invalid UTF-8/TOML: {exc}") from exc
        for key in KEYS:
            current = current_toml.get(key)
            if state and current != state["values"].get(key) and not (key in overrides and current == overrides[key]):
                raise SyncError(f"local drift detected for {key}; matching override required")
            if not state and current is not None and not adopt and current != overrides.get(key):
                raise SyncError(f"existing {key} requires --adopt or a matching override")
        updated_config, values = _toml_update(config_raw, desired)
        if values != desired:
            raise SyncError("managed settings do not match approved desired values")
        old_agents = agents_path.read_bytes() if agents_path.exists() else b""
        try:
            agents_text = old_agents.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise SyncError("AGENTS.md must be UTF-8") from exc
        updated_agents = replace_block(agents_text, source_agents.decode("utf-8"), state.get("agents_block_sha256") if state else None).encode("utf-8")
        block = updated_agents[updated_agents.index(START.encode()):updated_agents.index(END.encode()) + len(END)].decode("utf-8")
        new_state = {"schema": 1, "values": values, "agents_block_sha256": hashlib.sha256(block.encode()).hexdigest(), "source_sha256": source_hash, "version": version, "commit": commit}
        changes = {}
        for path, data in ((config_path, updated_config), (agents_path, updated_agents), (state_path, (json.dumps(new_state, sort_keys=True, indent=2) + "\n").encode())):
            old = path.read_bytes() if path.exists() else None
            if old != data:
                changes[path] = (old, data)
        if not changes:
            return []
        if not apply:
            return [f"would update {p.name}" for p in changes]
        backups = state_dir / "backups"
        backups.mkdir(parents=True, exist_ok=True)
        if os.name != "nt":
            os.chmod(backups, 0o700)
        stamp = f"{time.strftime('%Y%m%d-%H%M%S')}-{time.time_ns()}"
        for path, (old, _) in changes.items():
            if old is not None:
                _atomic_write(backups / f"{stamp}-{path.name}.bak", old)
        written: list[tuple[Path, bytes | None]] = []
        try:
            for path, (old, data) in changes.items():
                _atomic_write(path, data)
                written.append((path, old))
        except Exception:
            for path, old in reversed(written):
                if old is None:
                    path.unlink(missing_ok=True)
                else:
                    _atomic_write(path, old)
            raise
        return [f"updated {p.name}" for p in changes]
    finally:
        lock.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--source", type=Path, help="local repository source (development and tests)")
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    parser.add_argument("--adopt", action="store_true", help="authorize applying managed defaults over existing root settings")
    parser.add_argument("--codex-executable", help="Codex CLI path to use for minimum-version verification")
    args = parser.parse_args()
    try:
        result = sync(args.codex_home, args.source, args.apply, args.adopt, args.codex_executable)
    except (SyncError, OSError, ValueError, KeyError) as exc:
        parser.error(str(exc))
    print("No changes needed." if not result else "\n".join(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
