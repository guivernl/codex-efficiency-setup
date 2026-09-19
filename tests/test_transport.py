import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sync


class TransportTests(unittest.TestCase):
    def test_remote_files_are_pinned_to_one_commit(self):
        sha = 'a' * 40
        manifest = {'example': 'data'}
        with patch.object(sync, '_fetch', side_effect=[
            json.dumps({'object': {'sha': sha}}).encode(),
            json.dumps(manifest).encode(), b'instructions',
        ]) as fetch:
            self.assertEqual(sync.remote_source(), (manifest, b'instructions', sha))
        urls = [call.args[0] for call in fetch.call_args_list]
        self.assertIn('/git/ref/heads/main', urls[0])
        self.assertIn('/' + sha + '/defaults/manifest.json', urls[1])
        self.assertIn('/' + sha + '/defaults/AGENTS.md', urls[2])

    def test_fetch_failure_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as name:
            home = Path(name)
            config = home / 'config.toml'
            config.write_bytes(b'model = "local"\n')
            with patch.object(sync, 'remote_source', side_effect=sync.SyncError('offline')):
                with self.assertRaises(sync.SyncError):
                    sync.sync(home, apply=True, adopt=True)
            self.assertEqual(config.read_bytes(), b'model = "local"\n')
            self.assertFalse((home / 'efficiency-sync/state.json').exists())
            self.assertFalse((home / 'efficiency-sync/sync.lock').exists())

    def test_existing_lock_is_not_removed(self):
        with tempfile.TemporaryDirectory() as name:
            home = Path(name)
            state = home / 'efficiency-sync'
            state.mkdir()
            lock = state / 'sync.lock'
            lock.touch()
            with self.assertRaisesRegex(sync.SyncError, 'another sync'):
                sync.sync(home)
            self.assertTrue(lock.exists())
