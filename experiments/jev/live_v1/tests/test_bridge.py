import json
import os
from pathlib import Path
import shutil
import socket
import unittest
from unittest.mock import patch
from uuid import uuid4

from experiments.jev.adapter import MockAdapter
from experiments.jev.evidence_v2 import run as frozen
from experiments.jev.live_v1 import run as bridge
from experiments.jev.live_v1.transport import Transport
from experiments.jev.run import encode, sha


class BridgeTests(unittest.TestCase):
    def setUp(self):
        self.parent = bridge.HERE/'runs'/('test-'+uuid4().hex)
        self.block = patch.object(socket.socket, 'connect', side_effect=AssertionError('network forbidden'))
        self.block.start()

    def tearDown(self):
        self.block.stop()
        shutil.rmtree(self.parent, ignore_errors=True)

    def test_schedule_equals_frozen_projection_and_mock(self):
        result = bridge.run('mock', self.parent/'mock')
        self.assertEqual(len(result['records']), 282)
        self.assertEqual(result['status'], 'complete')
        cards, gold, questions, pairs, policy = frozen.materials()
        for row, card in zip(result['records'], cards*3):
            body = (self.parent/'mock'/row['request_file']).read_bytes()
            self.assertEqual(body, encode(frozen.request(card, questions, policy)))
        report = json.loads((self.parent/'mock'/'report.json').read_bytes())
        expected = frozen.report(result['records'], cards, gold, pairs, policy, 'mock')
        self.assertEqual(report['sections'], expected['sections'])
        self.assertEqual(report['pair_summary'], expected['pair_summary'])
        with self.assertRaises(FileExistsError):
            bridge.run('dry-run', self.parent/'mock')

    def test_optional_sdk_not_needed_for_dry_run(self):
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': ''}):
            result = bridge.run('dry-run', self.parent/'dry')
        self.assertTrue(all(r['status'] == 'planned' for r in result['records']))

    def sdk(self, handler):
        try:
            import httpx2
        except ImportError:
            self.skipTest('optional SDK not installed')
        with patch.dict(os.environ, {'TYPESAFE_API_KEY':'test-only',
                                    'TYPESAFE_BASE_URL':'https://invalid.example'}):
            return Transport(transport=httpx2.MockTransport(handler))

    def test_http_errors_and_invalid_bodies_retained_single_attempt(self):
        try:
            import httpx2
        except ImportError:
            self.skipTest('optional SDK not installed')
        for status, body in [(429, b'{"error":"test"}'), (200, b'{}')]:
            calls = []
            def respond(request):
                calls.append(request)
                self.assertEqual(str(request.url), 'https://api.typesafe.ai/v1/systemone')
                return httpx2.Response(status, content=body)
            result = bridge.run('live', self.parent/str(status), adapter=self.sdk(respond))
            self.assertEqual(len(calls), 282)
            self.assertEqual(result['status'], 'incomplete')
            for row in result['records']:
                self.assertEqual(row['response_sha256'], sha(body))
                self.assertEqual(row['status'], 'error' if status == 429 else 'invalid')
                self.assertEqual(json.loads((self.parent/str(status)/row['http_request_file']).read_bytes()),
                                 json.loads((self.parent/str(status)/row['request_file']).read_bytes()))

    def test_interruption_preserves_schedule_and_pending_denominator(self):
        class Interrupted:
            last_raw = last_http_status = last_request_id = None
            def evaluate(self, payload, callback):
                raise KeyboardInterrupt()
            def close(self):
                pass
        with self.assertRaises(KeyboardInterrupt):
            bridge.run('live', self.parent/'interrupt', adapter=Interrupted())
        result = json.loads((self.parent/'interrupt'/'run.json').read_bytes())
        self.assertEqual(len(result['records']), 282)
        self.assertEqual(result['records'][0]['status'], 'interrupted')
        self.assertEqual(sum(r['status']=='planned' for r in result['records']), 281)

    def test_preflight_only_calls_models(self):
        try:
            import httpx2
        except ImportError:
            self.skipTest('optional SDK not installed')
        calls = []
        def respond(request):
            calls.append((request.method, str(request.url)))
            return httpx2.Response(200, json={'models': []})
        adapter = self.sdk(respond)
        try:
            self.assertEqual(adapter.preflight(), [])
        finally:
            adapter.close()
        self.assertEqual(calls, [('GET', 'https://api.typesafe.ai/v1/models')])

    def test_manifest_tamper_rejected(self):
        with patch.object(bridge, 'load', return_value={'sha256':{'experiments/jev/live_v1/run.py':'wrong'}}):
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                bridge.verify()


if __name__ == '__main__':
    unittest.main()
