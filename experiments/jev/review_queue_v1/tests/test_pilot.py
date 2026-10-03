import json
import shutil
import socket
import unittest
from unittest.mock import patch
from uuid import uuid4
from experiments.jev.review_queue_v1 import pilot as p


class PilotTests(unittest.TestCase):
    def test_generated_form_javascript_parses(self):
        import tempfile
        import subprocess
        from pathlib import Path
        from experiments.jev.review_queue_v1.forms import render
        node=shutil.which('node')
        if not node:self.skipTest('Node unavailable for static JavaScript syntax check')
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'form.html';render(path)
            script=path.read_text().split('<script>',1)[1].split('</script>',1)[0]
            result=subprocess.run([node,'--check'],input=script,text=True,capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)

    def test_selection_and_wire_boundaries(self):
        c=p.verify()
        self.assertEqual(len(c['units']),24)
        self.assertEqual(len(c['deterministic_queue']),22)
        self.assertEqual(sum(u['selection_bucket']=='agreement' for u in c['units']),12)
        for u in c['units']:
            self.assertEqual(set(u['state']),{'excerpt','original_question','provisional_reference','observed_choice'})

    def test_mock_is_network_free_and_preserves_schedule(self):
        out=p.HERE/'runs'/('test-'+uuid4().hex)
        try:
            with patch.object(socket.socket,'connect',side_effect=AssertionError('Network forbidden')):
                r=p.run('mock',out)
            self.assertEqual(len(r['records']),72)
            self.assertEqual(r['status'],'complete')
            self.assertIsNone(r['human_time_saving']);self.assertIsNone(r['review_quality'])
            self.assertEqual(r['records'][0]['request_sha256'],r['records'][24]['request_sha256'])
            with self.assertRaises(FileExistsError):p.run('dry-run',out)
        finally:shutil.rmtree(out,ignore_errors=True)

    def test_rejects_probability_deficit_nonfinite_and_wrong_labels(self):
        q={'q':{'criteria':{'A':'a','B':'b'}}}
        good={'model':'pinned','answers':{'q':{'type':'choice','choice':'A','confidence':1,'probabilities':{'A':1,'B':0}}}}
        self.assertEqual(p.validate(json.dumps(good).encode(),q),good)
        for probs in ({'A':.99,'B':0},{'A':float('nan'),'B':0},{'A':1,'C':0}):
            good['answers']['q']['probabilities']=probs
            with self.assertRaises(ValueError):p.validate(json.dumps(good).encode(),q)

    def test_interruption_preserves_pending_positions(self):
        class Interrupted:
            last_raw=last_http_status=None
            def evaluate(self,*a):raise KeyboardInterrupt()
            def close(self):pass
        out=p.HERE/'runs'/('test-'+uuid4().hex)
        try:
            with self.assertRaises(KeyboardInterrupt):p.run('live',out,Interrupted())
            r=json.loads((out/'run.json').read_bytes())
            self.assertEqual(r['status'],'interrupted')
            self.assertEqual(sum(x['status']=='planned' for x in r['records']),71)
        finally:shutil.rmtree(out,ignore_errors=True)

    def test_comparison_requires_actual_complete_records(self):
        from experiments.jev.review_queue_v1.forms import compare
        with self.assertRaises(ValueError):compare({}, {})
        cohort=p.verify()
        # Synthetic test fixture, never exported as human assessment.
        def fixture(mode,date):
            return {'mode':mode,'complete':True,'reviewer':'synthetic-test-only','prior_suggestion_exposure':'no',
              'source_run_sha256':cohort['source_run_sha256'],'records':[
               {'unit_id':u['id'],'active_seconds':2 if mode=='baseline' else 1,
                'reviewed_at':date,'notes':'synthetic test fixture',
                'answers':{q:next(iter(x['criteria'])) for q,x in cohort['questions'].items()},
                'helpfulness':'uncertain','missed_concern':'unassessed'} for u in cohort['units']]}
        a,b=fixture('baseline','2026-10-02T10:00:00Z'),fixture('assisted','2026-10-02T11:00:00Z')
        self.assertIsNone(compare(a,b)['net_seconds_difference'])
        self.assertEqual(compare(a,b,30)['net_seconds_difference'],-6)
        b['records'][0]['active_seconds']=float('nan')
        with self.assertRaises(ValueError):compare(a,b)
