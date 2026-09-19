import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sync


ROOT = Path(__file__).resolve().parents[1]


class SyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.home = Path(self.temp.name) / "codex"
        self.home.mkdir()
        self.real_version_check = sync.check_codex_version
        self.version_check = patch.object(sync, "check_codex_version").start()
        self.addCleanup(patch.stopall)

    def tearDown(self):
        self.temp.cleanup()

    def apply(self, **kwargs):
        return sync.sync(self.home, ROOT, apply=True, **kwargs)

    def test_idempotent_and_preserves_unrelated_settings(self):
        config = self.home / "config.toml"
        config.write_text('other = "keep"\n[projects."x"]\nmodel = "project-model"\n', encoding="utf-8")
        self.apply()
        first = config.read_bytes()
        self.assertEqual(tomllib_load(config)["other"], "keep")
        self.assertEqual(tomllib_load(config)["projects"]["x"]["model"], "project-model")
        self.assertEqual(sync.sync(self.home, ROOT, apply=True), [])
        self.assertEqual(config.read_bytes(), first)

    def test_dry_run_does_not_write(self):
        result = sync.sync(self.home, ROOT)
        self.assertTrue(result)
        self.assertFalse((self.home / "config.toml").exists())
        self.assertFalse((self.home / "AGENTS.md").exists())

    def test_malformed_toml_refused(self):
        (self.home / "config.toml").write_text('model = "ok"\nmodel = "dup"\n')
        with self.assertRaises(sync.SyncError):
            self.apply(adopt=True)

    def test_mixed_present_missing_root_keys(self):
        config = self.home / "config.toml"
        config.write_text('model = "old"\nother = "keep"\n[section]\nvalue = 7\n')
        self.apply(adopt=True)
        parsed = tomllib_load(config)
        self.assertEqual(parsed["model"], "gpt-6-astra")
        self.assertEqual(parsed["model_reasoning_effort"], "low")
        self.assertEqual(parsed["service_tier"], "default")
        self.assertEqual(parsed["other"], "keep")
        self.assertEqual(parsed["section"]["value"], 7)

    def test_multiline_lookalike_fails_closed(self):
        config = self.home / "config.toml"
        config.write_text('note = """start\nmodel = "fake"\nend"""\n')
        with self.assertRaisesRegex(sync.SyncError, "ambiguous"):
            self.apply()
        self.assertIn('model = "fake"', config.read_text())

    def test_marker_errors_and_modified_managed_block_refused(self):
        (self.home / "AGENTS.md").write_text(f"{sync.START}\nwrong\n")
        with self.assertRaisesRegex(sync.SyncError, "markers"):
            self.apply()
        (self.home / "AGENTS.md").write_text(f"{sync.END}\n{sync.START}\n")
        with self.assertRaisesRegex(sync.SyncError, "reversed"):
            self.apply()
        (self.home / "AGENTS.md").write_text("user text\n")
        self.apply()
        path = self.home / "AGENTS.md"
        content = path.read_text()
        start = content.index(sync.START)
        end = content.index(sync.END) + len(sync.END)
        path.write_text(content[:start] + content[end:])
        with self.assertRaisesRegex(sync.SyncError, "removed locally"):
            self.apply()
        path.write_text(content)
        path.write_text(path.read_text().replace("Minimize", "Change"))
        with self.assertRaisesRegex(sync.SyncError, "modified locally"):
            self.apply()

    def test_drift_requires_matching_override(self):
        self.apply()
        path = self.home / "config.toml"
        path.write_text(path.read_text().replace('model = "gpt-6-astra"', 'model = "local-choice"'))
        with self.assertRaisesRegex(sync.SyncError, "drift"):
            self.apply()
        path.write_text("\n".join(line for line in path.read_text().splitlines() if not line.startswith("model =")) + "\n")
        with self.assertRaisesRegex(sync.SyncError, "drift"):
            self.apply()
        path.write_text('model = "local-choice"\n' + "\n".join(line for line in path.read_text().splitlines() if not line.startswith("model =")) + "\n")
        overrides = self.home / sync.STATE_DIR / "overrides.json"
        overrides.write_text(json.dumps({"model": "local-choice"}))
        self.apply()

    def test_invalid_override_and_manifest_refused(self):
        (self.home / sync.STATE_DIR).mkdir()
        (self.home / sync.STATE_DIR / "overrides.json").write_text('{"plugins": "bad"}')
        with self.assertRaisesRegex(sync.SyncError, "overrides"):
            self.apply()
        manifest = json.loads((ROOT / "defaults/manifest.json").read_text())
        manifest["settings"]["extra"] = "bad"
        with self.assertRaisesRegex(sync.SyncError, "manifest"):
            sync.validate_source(manifest, (ROOT / "defaults/AGENTS.md").read_bytes())
        manifest = json.loads((ROOT / "defaults/manifest.json").read_text())
        manifest["minimum_codex_version"] = "0.1.0"
        with self.assertRaisesRegex(sync.SyncError, "lower than 0.154.0"):
            sync.validate_source(manifest, (ROOT / "defaults/AGENTS.md").read_bytes())

    def test_first_adoption_requires_flag(self):
        (self.home / "config.toml").write_text('model = "gpt-5.5"\n')
        with self.assertRaisesRegex(sync.SyncError, "--adopt"):
            self.apply()
        self.apply(adopt=True)
        self.assertEqual(tomllib_load(self.home / "config.toml")["model"], "gpt-6-astra")

    def test_minimum_version_enforced(self):
        self.version_check.stop()
        with patch.object(sync.shutil, "which", return_value="codex"), patch.object(
            sync.subprocess, "run", return_value=type("Result", (), {"stdout": "codex-cli 0.153.9", "stderr": ""})()
        ):
            with self.assertRaisesRegex(sync.SyncError, "0.154.0 or newer"):
                self.real_version_check("0.154.0", "codex")

    def test_version_floor_prerelease_rules(self):
        self.version_check.stop()
        for reported, accepted in (("0.154.0-alpha.9", False), ("0.154.0", True), ("0.155.0-alpha.9.2", True)):
            with self.subTest(reported=reported), patch.object(sync.shutil, "which", return_value="codex"), patch.object(
                sync.subprocess, "run", return_value=type("Result", (), {"stdout": f"codex-cli {reported}", "stderr": ""})()
            ):
                if accepted:
                    self.real_version_check("0.154.0", "codex")
                else:
                    with self.assertRaisesRegex(sync.SyncError, "0.154.0 or newer"):
                        self.real_version_check("0.154.0", "codex")

    def test_codex_version_fallback(self):
        local_bin = self.home / ".local" / "bin"
        local_bin.mkdir(parents=True)
        executable = local_bin / "codex"
        executable.write_text("")
        self.version_check.stop()
        with patch.object(sync.shutil, "which", return_value=None), patch.object(sync.Path, "home", return_value=self.home), patch.object(
            sync.subprocess, "run", return_value=type("Result", (), {"stdout": "codex-cli 0.200.0", "stderr": ""})()
        ) as run:
            self.real_version_check("0.154.0")
            self.assertEqual(run.call_args.args[0][0], str(executable))

    def test_windows_bundled_codex_discovery(self):
        appdata = self.home / "appdata"
        old_exe = appdata / "OpenAI" / "Codex" / "bin" / "old" / "codex.exe"
        new_exe = appdata / "OpenAI" / "Codex" / "bin" / "new" / "codex.exe"
        old_exe.parent.mkdir(parents=True)
        new_exe.parent.mkdir(parents=True)
        old_exe.write_text("")
        new_exe.write_text("")
        sync.os.utime(old_exe.parent, (1, 1))
        sync.os.utime(new_exe.parent, (2, 2))
        self.version_check.stop()
        with patch.object(sync.shutil, "which", return_value=None), patch.dict(sync.os.environ, {"LOCALAPPDATA": str(appdata)}), patch.object(
            sync.subprocess, "run", return_value=type("Result", (), {"stdout": "codex-cli 0.200.0", "stderr": ""})()
        ) as run:
            self.real_version_check("0.154.0")
            self.assertEqual(run.call_args.args[0][0], str(new_exe))

    def test_invalid_state_and_unbumped_source_refused(self):
        state_dir = self.home / sync.STATE_DIR
        state_dir.mkdir()
        (state_dir / "state.json").write_text('{"schema": true}')
        with self.assertRaisesRegex(sync.SyncError, "state"):
            self.apply()

        (state_dir / "state.json").unlink()
        self.apply()
        source = Path(self.temp.name) / "source"
        import shutil
        shutil.copytree(ROOT / "defaults", source / "defaults")
        with (source / "defaults" / "AGENTS.md").open("a", encoding="utf-8") as f:
            f.write("new source content\n")
        with self.assertRaisesRegex(sync.SyncError, "version bump"):
            sync.sync(self.home, source, apply=True)

    def test_transaction_rolls_back_written_file(self):
        original = sync._atomic_write
        count = 0

        def fail_second(path, data):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("simulated failure")
            return original(path, data)

        with patch.object(sync, "_atomic_write", side_effect=fail_second):
            with self.assertRaises(OSError):
                self.apply()
        self.assertFalse((self.home / "config.toml").exists())
        self.assertFalse((self.home / "AGENTS.md").exists())


def tomllib_load(path):
    import tomllib
    return tomllib.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
