from __future__ import annotations

import base64
import contextlib
import io
from pathlib import Path
import re
import tempfile
import unittest
from unittest import mock

import importlib.util


SCRIPT = Path(__file__).resolve().parents[1] / "install-sync.py"
SPEC = importlib.util.spec_from_file_location("install_sync", SCRIPT)
install_sync = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(install_sync)


class EnrolmentTests(unittest.TestCase):
    def test_enrollment_copies_updater_without_implicit_adoption(self) -> None:
        with tempfile.TemporaryDirectory(prefix="repo with spaces ") as raw:
            root = Path(raw)
            source = root / "source repo"
            home = root / "codex home"
            source.mkdir()
            (source / "sync.py").write_text("# reviewed\n", encoding="utf-8")
            result = install_sync._enroll(source, home)

            self.assertEqual(result.read_text(encoding="utf-8"), "# reviewed\n")
            self.assertEqual(result, home / "efficiency-sync" / "sync.py")

    def test_adoption_passes_explicit_source_apply_adopt_and_codex_home(self) -> None:
        source = Path("repo with spaces")
        script = Path("home with spaces") / "efficiency-sync" / "sync.py"
        home = Path("home with spaces")
        with mock.patch.object(install_sync, "_run") as run:
            install_sync._adopt(script, source, home)
        self.assertEqual(run.call_args.args[0], [
                install_sync.sys.executable,
                str(script), "--source", str(source.resolve()), "--apply", "--adopt",
                "--codex-home", str(home),
        ])

    def test_refuses_to_overwrite_an_existing_different_updater(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            source = root / "repo"
            destination = root / "home" / "efficiency-sync"
            source.mkdir()
            destination.mkdir(parents=True)
            (source / "sync.py").write_text("new", encoding="utf-8")
            (destination / "sync.py").write_text("old", encoding="utf-8")
            with self.assertRaises(install_sync.SetupError):
                install_sync._enroll(source, root / "home")


class SchedulerTests(unittest.TestCase):
    def test_windows_action_quotes_paths_and_persists_run_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="python install ") as raw:
            script = Path(raw) / "codex home" / "efficiency-sync" / "sync.py"
            home = Path(raw) / "codex home"
            executable = Path(raw) / "python.exe"
            with mock.patch.object(install_sync.sys, "executable", str(executable)):
                command = install_sync._windows_schedule_command(script, home)
            self.assertEqual(command[0], "powershell.exe")
            ps = base64.b64decode(command[-1]).decode("utf-16le")
            self.assertIn("-Daily -At '9:00 AM'", ps)
            self.assertIn("-StartWhenAvailable -WakeToRun:$false", ps)
            self.assertIn("-LogonType Interactive -RunLevel Limited", ps)
            action_encoded = re.search(r"-EncodedCommand ([A-Za-z0-9+/=]+)", ps)
            self.assertIsNotNone(action_encoded)
            action = base64.b64decode(action_encoded.group(1)).decode("utf-16le")
            self.assertIn(str(executable), action)
            self.assertIn(str(script.parent), action)
            self.assertIn("logs", action)
            self.assertIn("efficiency-sync.log", action)
            self.assertIn("--codex-home", action)
            self.assertIn("codex home", action)

    def test_linux_units_quote_spaces_and_enable_persistent_delayed_daily_timer(self) -> None:
        with tempfile.TemporaryDirectory(prefix="repo with spaces ") as raw:
            root = Path(raw)
            paths = install_sync._linux_units(
                root / "codex home" / "sync.py", root / "home with space", root / "units"
            )
            service_path, service, timer_path, timer = paths
            expected_script = str(root / "codex home" / "sync.py").replace("\\", "\\\\")
            self.assertIn(f'"{expected_script}"', service)
            expected_home = str(root / "home with space").replace("\\", "\\\\")
            self.assertIn(f'"{expected_home}"', service)
            self.assertIn("OnCalendar=*-*-* 09:00:00", timer)
            self.assertIn("Persistent=true", timer)
            self.assertIn("RandomizedDelaySec=10min", timer)
            self.assertTrue(service_path.name.endswith(".service"))
            self.assertTrue(timer_path.name.endswith(".timer"))

    def test_linux_schedule_registers_only_user_timer(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            script = root / "sync.py"
            home = root / "codex"
            unit_dir = root / "systemd" / "user"
            with mock.patch.object(install_sync, "_run") as run:
                install_sync._install_linux_schedule(script, home, unit_dir)
            self.assertEqual(run.call_args_list[0].args[0], ["systemctl", "--user", "daemon-reload"])
            self.assertEqual(run.call_args_list[1].args[0], [
                "systemctl", "--user", "enable", "--now", "codex-efficiency-sync.timer"
            ])
            self.assertTrue((unit_dir / "codex-efficiency-sync.timer").exists())

    def test_macos_schedule_fails_before_enrolment(self) -> None:
        with mock.patch.object(install_sync.platform, "system", return_value="Darwin"), \
             mock.patch.object(install_sync, "_enroll") as enroll:
            status = install_sync.main(["--schedule"])
        self.assertEqual(status, 1)
        enroll.assert_not_called()

    def test_schedule_requires_explicit_adoption(self) -> None:
        with mock.patch.object(install_sync.platform, "system", return_value="Linux"), \
             mock.patch.object(install_sync, "_enroll") as enroll, \
             mock.patch.object(install_sync, "_preflight_linux") as preflight:
            status = install_sync.main(["--schedule"])
        self.assertEqual(status, 1)
        enroll.assert_not_called()
        preflight.assert_not_called()

    def test_enrollment_failure_does_not_print_success(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            (root / "sync.py").write_text("# reviewed", encoding="utf-8")
            stdout = io.StringIO()
            with mock.patch.object(install_sync.platform, "system", return_value="Linux"), \
                 mock.patch.object(install_sync, "_enroll", side_effect=install_sync.SetupError("failed")), \
                 contextlib.redirect_stdout(stdout):
                status = install_sync.main(["--source", str(root), "--codex-home", str(root / "home")])
        self.assertEqual(status, 1)
        self.assertNotIn("Enrolled", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
