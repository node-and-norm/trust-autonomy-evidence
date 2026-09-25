import copy
import json
import os
import shutil
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from experiments.jev.adapter import LABELS, MockAdapter, JevAdapter, validate_response
from experiments.jev.run import HERE, ROOT, materials, run, sha, normalized, jobs


class ExperimentTests(unittest.TestCase):
    def setUp(self):
        (HERE/'runs').mkdir(exist_ok=True)
        self.parent = Path(tempfile.mkdtemp(dir=HERE/'runs'))
        self.out = self.parent/'result'
        self.network = patch.object(socket.socket, 'connect', side_effect=AssertionError('network forbidden'))
        self.network.start()

    def tearDown(self):
        self.network.stop()
        shutil.rmtree(self.parent)

    def test_dry_run_has_no_answers_and_covers_252(self):
        with patch('experiments.jev.run.JevAdapter', side_effect=AssertionError('SDK forbidden')):
            result = run('dry-run', self.out, include_mutations=True)
        self.assertEqual(result['planned_requests'], 24)
        self.assertEqual(result['summary']['evaluated_base_determinations'], 0)
        self.assertTrue(all(not r['rows'] for r in result['records']))
        self.assertEqual(len(list(self.out.glob('*.request.json'))), 24)
        self.assertFalse(list(self.out.glob('*.response.json')))
        with self.assertRaises(FileExistsError):
            run('dry-run', self.out)

    def test_mock_outputs_hashes_calibration_and_disagreements(self):
        result = run('mock', self.out, include_mutations=True)
        self.assertEqual(result['summary']['evaluated_base_determinations'], 252)
        self.assertEqual(result['resolved_models'], ['mock-only'])
        self.assertEqual(len(result['mutation_results']), 12)
        self.assertEqual(sum(m['exact_delta_match'] for m in result['mutation_results']), 3)
        for record in result['records']:
            self.assertEqual(record['response_sha256'], sha((self.out/(record['job_id']+'.response.json')).read_bytes()))
            self.assertEqual(record['request_sha256'], sha((self.out/(record['job_id']+'.request.json')).read_bytes()))
        rows = [json.loads(l) for l in (self.out/'comparisons.jsonl').read_text().splitlines()]
        self.assertEqual(len(rows), 504)
        self.assertTrue(all(abs(r['brier_multiclass']-0.8)<1e-9 for r in rows))
        self.assertGreater(len(json.loads((self.out/'disagreements.json').read_text())), 0)
        import jsonschema
        jsonschema.validate(result, json.loads((HERE/'run.schema.json').read_text()))

    def test_missing_key_blocked_without_sdk(self):
        with patch.dict(os.environ, {'TYPESAFE_API_KEY': ''}):
            result = run('live', self.out)
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['reason'], 'missing TYPESAFE_API_KEY')
        self.assertEqual(result['records'], [])

    def test_no_gold_in_requests_and_mapping_complete(self):
        cases, oracle, qs, mutations, _ = materials()
        self.assertEqual(len(qs), 21)
        self.assertEqual(sum(q['assessment']=='control' for q in qs.values()), 9)
        state = normalized(cases[0])
        self.assertNotIn('title', state)
        self.assertNotIn('purpose', state)
        self.assertNotIn('case_id', state)
        self.assertNotIn('expected', state)
        planned = jobs(cases, oracle, mutations, True)
        for jid, case, expected, mutation in planned[12:]:
            if mutation['expected_deltas']:
                self.assertNotEqual(expected, oracle[mutation['base_case_id']])
        self.assertEqual(normalized(planned[18][1]), normalized(cases[0]))  # title invariant

    def test_response_rejections(self):
        good = json.loads(MockAdapter().evaluate({}, {'q': {}}, 'requested'))
        validate_response(json.dumps(good).encode(), {'q'})
        changes = [lambda d: d['answers'].clear(),
                   lambda d: d.update(model=''),
                   lambda d: d['answers']['q'].update(confidence=True),
                   lambda d: d['answers']['q'].update(confidence=float('nan')),
                   lambda d: d['answers']['q'].update(choice='invented'),
                   lambda d: d['answers']['q'].update(type='noul'),
                   lambda d: d['answers']['q']['probabilities'].update(supported=-1),
                   lambda d: d['answers']['q']['probabilities'].update(supported=0.9)]
        for change in changes:
            doc=copy.deepcopy(good); change(doc)
            with self.assertRaises(ValueError):
                validate_response(json.dumps(doc).encode(), {'q'})

    def test_invalid_response_retained_no_false_agreement(self):
        class Bad(MockAdapter):
            def evaluate(self, *args):
                return b'{"model":"test","answers":{}}'
        result=run('mock', self.out, adapter=Bad())
        self.assertEqual(result['status'], 'incomplete')
        self.assertEqual(result['summary']['errors'], 12)
        self.assertEqual(result['summary']['evaluated_base_determinations'], 0)
        self.assertEqual(len(list(self.out.glob('*.response.json'))), 12)

    def test_output_cannot_touch_core(self):
        with self.assertRaises(ValueError):
            run('dry-run', ROOT/'oracles'/'accidental')

    def test_question_tampering_rejected(self):
        original=Path.read_bytes
        def changed(path):
            data=original(path)
            return data+b' ' if path == HERE/'questions-v1.json' else data
        with patch.object(Path, 'read_bytes', changed), self.assertRaises(ValueError):
            materials()

    def test_sealed_fixture_tampering_rejected(self):
        original = Path.read_bytes
        def changed(path):
            data = original(path)
            return data + b' ' if path == ROOT/'fixtures/synthetic/cases.json' else data
        with patch.object(Path, 'read_bytes', changed), self.assertRaises(ValueError):
            materials()

    def test_mutation_detects_unexpected_extra_changes(self):
        from experiments.jev.run import mutation_comparisons
        qs = {'control__access': {'assessment': 'control', 'field': 'access'},
              'control__authority': {'assessment': 'control', 'field': 'authority'}}
        def record(name, labels):
            return {'job_id': name, 'status': 'ok', 'state_sha256': name,
                    'rows': [{'question_id': q, 'choice': label,
                              'probabilities': {l: float(l == label) for l in LABELS}}
                             for q, label in zip(qs, labels)]}
        records = [record('base', ['supported', 'supported']),
                   record('mut', ['unsupported', 'unsupported'])]
        mutation = {'mutation_id': 'mut', 'base_case_id': 'base',
                    'expected_deltas': [{'assessment': 'control', 'field': 'access',
                                         'from': 'supported', 'to': 'unsupported'}]}
        result = mutation_comparisons(records, [mutation], qs)[0]
        self.assertFalse(result['exact_delta_match'])
        self.assertEqual(len(result['observed_deltas']), 2)

    def test_sdk_invalid_and_error_bodies_preserved_without_retries(self):
        try:
            import httpx2
            import typesafe_sdk
        except ImportError:
            self.skipTest('optional SDK not installed')
        for status, raw in [(200, b'{}'), (429, b'{"error":"rate limit"}')]:
            calls = []
            def respond(request):
                calls.append(request)
                return httpx2.Response(status, content=raw)
            with patch.dict(os.environ, {'TYPESAFE_API_KEY': 'test-only-key'}):
                adapter = JevAdapter(transport=httpx2.MockTransport(respond))
                out = self.parent / str(status)
                result = run('live', out, adapter=adapter)
            self.assertEqual(result['status'], 'incomplete')
            self.assertEqual(len(calls), 12)
            self.assertTrue(all(r['response_sha256'] == sha(raw) for r in result['records']))
            self.assertEqual((out/'TAE-SYN-001.response.json').read_bytes(), raw)


    def test_sdk_transport_contract(self):
        try:
            import httpx2
            import typesafe_sdk
        except ImportError:
            self.skipTest('optional SDK not installed')
        requests=[]
        def respond(request):
            requests.append(request)
            payload=json.loads(request.content)
            return httpx2.Response(200, content=MockAdapter().evaluate(payload['state'], payload['questions'], payload['model']))
        with patch.dict(os.environ, {'TYPESAFE_API_KEY':'test-only-key','TYPESAFE_BASE_URL':'https://invalid.example'}):
            adapter=JevAdapter(transport=httpx2.MockTransport(respond))
            try:
                raw=adapter.evaluate({'test':'state'}, {'q': {'type':'choice','instructions':'test','criteria': {l:l for l in LABELS}}}, 'jev-1.13.0')
                validate_response(raw, {'q'})
            finally:
                adapter.close()
        self.assertEqual(str(requests[0].url), 'https://api.typesafe.ai/v1/systemone')
        self.assertEqual(json.loads(requests[0].content)['model'], 'jev-1.13.0')
        self.assertEqual(len(requests), 1)


if __name__ == '__main__':
    unittest.main()
