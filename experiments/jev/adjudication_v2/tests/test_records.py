"""Synthetic record fixtures only: these tests perform no human adjudication."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from jsonschema.exceptions import ValidationError
from experiments.jev.adjudication_v2 import records as r


class RecordTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        request = r.encode({'questions': {'authority': 'Synthetic fixture question'}})
        response = b'{"fixture":true}'
        (self.root/'request.json').write_bytes(request)
        (self.root/'response.json').write_bytes(response)
        self.run = self.root/'run.json'
        self.run.write_bytes(r.encode({'mode':'mock','records':[{
            'job_id':'fixture','repetition':1,'status':'invalid',
            'request_file':'request.json','request_sha256':r.sha(request),
            'response_file':'response.json','response_sha256':r.sha(response),
            'resolved_model':'synthetic-test-only'}]}))
        self.original = {'record_id':'fixture-r1-authority','run_id':'fixture-run',
            'job_id':'fixture','repetition':1,'question_id':'authority',
            'status':'open','disposition':'UNRESOLVED','evidence_refs':['request.json'],
            'reviewers':[],'rationale':'','supersedes':None}
        self.item = r.migrate([self.original],self.run,'2026-09-25T12:00:00Z')[0]

    def closed(self):
        item = copy.deepcopy(self.item)
        item['record'].update(status='closed',disposition='INSUFFICIENT_EVIDENCE',
            rationale='Synthetic test decision, not a real review.',reviewers=[
                {'identity':name,'blind_notes':'Synthetic fixture only.',
                 'reconciliation':'Synthetic fixture only.'}
                for name in ('Fixture A','Fixture B')])
        item['reviewer_dates']=[{'identity':name,'blind_reviewed_at':'2026-09-25T10:00:00Z',
            'reconciled_at':'2026-09-25T11:00:00Z'} for name in ('Fixture A','Fixture B')]
        item['reviewed_at']='2026-09-25T11:30:00Z'
        item['downstream']={'status':'no_change','rationale':'Fixture requires no change.','changes':[]}
        return item

    def test_import_preserves_source_and_does_not_invent_review(self):
        before = {p.name:p.read_bytes() for p in self.root.iterdir()}
        r.validate_all([self.item],self.run)
        self.assertEqual(self.item['source']['record'],self.original)
        self.assertEqual(self.item['record']['status'],'open')
        self.assertIsNone(self.item['reviewed_at'])
        self.assertEqual(self.item['reviewer_dates'],[])
        self.assertEqual(self.item['downstream']['status'],'not_assessed')
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})

    def test_closed_legacy_record_is_retained_but_reopened(self):
        original=self.closed()['record']
        imported=r.migrate([original],self.run,'2026-09-25T12:00:00Z')[0]
        self.assertEqual(imported['source']['record'],original)
        self.assertEqual(imported['record']['disposition'],'UNRESOLVED')
        self.assertEqual(imported['record']['reviewers'],[])

    def test_two_dated_reviews_and_no_change_can_close(self):
        r.validate_all([self.closed()],self.run)

    def test_incomplete_or_inconsistent_closure_rejected(self):
        edits=[lambda x:x.update(reviewed_at=None),
               lambda x:x.update(reviewer_dates=[]),
               lambda x:x['reviewer_dates'][1].update(identity=' fixture a '),
               lambda x:x['reviewer_dates'][0].update(reconciled_at='2026-09-25T09:00:00Z'),
               lambda x:x['reviewer_dates'][0].update(reconciled_at='2026-09-25T12:00:00Z'),
               lambda x:x['downstream'].update(status='not_assessed'),
               lambda x:x['record'].update(rationale='  '),
               lambda x:x.update(created_at='2026-09-25T12:00:00')]
        for edit in edits:
            with self.subTest(edit=edit):
                item=self.closed(); edit(item)
                with self.assertRaises((ValueError,ValidationError)):
                    r.validate_all([item],self.run)

    def test_downstream_applied_requires_date_and_hash(self):
        item=self.closed()
        item['downstream']={'status':'change_applied','rationale':'Synthetic correction.',
            'changes':[{'kind':'new_versioned_experiment','target':'fixture-v-next',
                'description':'Synthetic test only.','evidence_refs':['fixture-note'],
                'changed_at':None,'before_sha256':None,'after_sha256':None}]}
        with self.assertRaises(ValueError): r.validate(item)
        item['downstream']['changes'][0].update(changed_at='2026-09-26T12:00:00Z',after_sha256='a'*64)
        r.validate(item)
        item['downstream']['status']='change_proposed'
        with self.assertRaises(ValueError): r.validate(item)

    def test_raw_response_or_run_tampering_rejected(self):
        (self.root/'response.json').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'artifact hash'): r.validate_all([self.item],self.run)
        self.run.write_bytes(self.run.read_bytes()+b'\n')
        with self.assertRaisesRegex(ValueError,'run bytes'): r.validate_all([self.item],self.run)

    def test_source_or_evidence_identity_tampering_rejected(self):
        item=copy.deepcopy(self.item); item['source']['record']['rationale']='changed'
        with self.assertRaisesRegex(ValueError,'original adjudication'): r.validate(item)
        item=copy.deepcopy(self.item); item['record']['question_id']='another'
        with self.assertRaisesRegex(ValueError,'source identity'): r.validate(item)
        original=copy.deepcopy(self.original); original['question_id']='absent'
        with self.assertRaisesRegex(ValueError,'question absent'): r.migrate([original],self.run,'2026-09-25T12:00:00Z')

    def test_no_response_error_attempt_is_preserved(self):
        run=r.load(self.run); run['records'][0].update(status='error',response_file=None,response_sha256=None,resolved_model=None)
        self.run.write_bytes(r.encode(run))
        imported=r.migrate([self.original],self.run,'2026-09-25T12:00:00Z')
        r.validate_all(imported,self.run)
        self.assertIsNone(imported[0]['source']['response_file'])

    def test_no_planned_or_duplicate_requests(self):
        run=r.load(self.run); run['records'][0]['status']='planned'
        self.run.write_bytes(r.encode(run))
        with self.assertRaises(ValueError): r.migrate([self.original],self.run,'2026-09-25T12:00:00Z')
        run['records'].append(run['records'][0]); self.run.write_bytes(r.encode(run))
        with self.assertRaises(ValueError): r.RunContext(self.run)

    def test_supersession_requires_preserved_chain(self):
        next_item=self.closed()
        next_item['record'].update(record_id='fixture.v2.2',supersedes=self.item['record']['record_id'])
        next_item['created_at']='2026-09-26T12:00:00Z'
        r.validate_all([self.item,next_item],self.run)
        with self.assertRaises(ValueError): r.validate_all([next_item],self.run)
        with self.assertRaises(ValueError): r.validate_all([self.item,self.item],self.run)
        first=copy.deepcopy(self.item); first['record']['supersedes']='fixture.v2.2'
        with self.assertRaises(ValueError): r.validate_all([first,next_item],self.run)

    def test_artifact_path_escape_rejected(self):
        run=r.load(self.run); run['records'][0]['response_file']='../outside.json'
        self.run.write_bytes(r.encode(run))
        with self.assertRaisesRegex(ValueError,'directly inside'): r.migrate([self.original],self.run,'2026-09-25T12:00:00Z')

    def test_frozen_amendment_and_original_experiment(self):
        r.verify()


if __name__=='__main__':
    unittest.main()
