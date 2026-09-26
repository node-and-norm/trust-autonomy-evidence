"""All completed entries here are artificial fixtures, never author review."""
import csv
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import socket
from experiments.jev.author_audit_v1 import audit as a

class AuditTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.out=Path(self.temp.name)/'workbook'; a.export(self.out)

    def fixture(self):
        key=json.loads((self.out/'KEY.json').read_bytes())
        for n in (1,2):
            path=self.out/f'PASS_{n}.csv'
            rows=list(csv.DictReader(io.StringIO(path.read_text())))
            for row in rows:
                row.update(state=key[row['unit_id']]['occurrences'][0]['reference'],rationale='SYNTHETIC TEST FIXTURE ONLY')
            self.write_rows(path,rows)
        path=self.out/'PAIRS.csv'; rows=list(csv.DictReader(io.StringIO(path.read_text())))
        for row in rows: row.update(decision='retain',rationale='SYNTHETIC TEST FIXTURE ONLY')
        self.write_rows(path,rows)
        cover=json.loads((self.out/'COVER.json').read_bytes())
        cover.update(author='TEST FIXTURE, NOT A REVIEWER',route_confirmed=True,
            pass_1_completed_at='2000-01-01T12:00:00Z',pass_2_completed_at='2000-01-08T12:00:00Z')
        for n in (1,2): cover[f'pass_{n}_sha256']=a.sha((self.out/f'PASS_{n}.csv').read_bytes())
        (self.out/'COVER.json').write_bytes(a.encode(cover))

    def write_rows(self,path,rows):
        stream=io.StringIO(newline=''); writer=csv.DictWriter(stream,fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows); path.write_text(stream.getvalue())

    def test_complete_coverage_and_reproducibility(self):
        self.assertEqual(a.build(),a.build())
        key=json.loads(a.build()['KEY.json'])
        self.assertEqual(len(key),216)
        self.assertEqual(sum(len(v['occurrences']) for v in key.values()),1654)
        self.assertEqual(len(json.loads(a.build()['PAIR_PACKET.json'])),60)
        self.assertTrue(all(len({o['reference'] for o in v['occurrences']})==1 for v in key.values()))

    def test_blank_workbook_never_passes(self):
        result=a.check(self.out); self.assertEqual(result['status'],'PENDING')
        self.assertIsNone(result['author_consistency']['agreement'])

    def test_fixture_completeness_and_no_network(self):
        self.fixture()
        with patch.object(socket.socket,'connect',side_effect=AssertionError('network forbidden')):
            result=a.check(self.out)
        self.assertEqual(result['errors'],[])
        self.assertEqual(result['author_consistency']['agreement'],1)

    def test_source_tampering_and_overwrite_rejected(self):
        self.fixture(); (self.out/'UNITS.json').write_text('[]')
        self.assertIn('changed source UNITS.json',a.check(self.out)['errors'])
        with self.assertRaises(FileExistsError): a.export(self.out)
        with self.assertRaises(ValueError): a.export(a.HERE/'forbidden')

    def test_delay_and_exposure_gate(self):
        self.fixture(); path=self.out/'COVER.json'; cover=json.loads(path.read_bytes())
        cover.update(pass_2_completed_at='2000-01-02T12:00:00Z',live_output_exposure='unknown')
        path.write_bytes(a.encode(cover)); self.assertGreaterEqual(len(a.check(self.out)['errors']),2)

    def test_missing_and_duplicate_units_rejected(self):
        self.fixture(); path=self.out/'PASS_1.csv'; rows=list(csv.DictReader(io.StringIO(path.read_text())))
        rows[1]=rows[0]; self.write_rows(path,rows)
        self.assertIn('pass 1 coverage invalid',a.check(self.out)['errors'])

    def test_disagreement_requires_issue_and_no_material_defect(self):
        self.fixture(); path=self.out/'PASS_1.csv'; rows=list(csv.DictReader(io.StringIO(path.read_text())))
        row=rows[0]; row['state']=next(s for s in sorted(a.STATES) if s!=row['state'])
        self.write_rows(path,rows); coverpath=self.out/'COVER.json'; cover=json.loads(coverpath.read_bytes()); cover['pass_1_sha256']=a.sha(path.read_bytes()); coverpath.write_bytes(a.encode(cover))
        self.assertTrue(any('unaddressed' in e for e in a.check(self.out)['errors']))
        issue={'issue_id':'test-only','target':row['unit_id'],'evidence':'test','alternative_interpretation':'test',
               'rationale':'test','action':'test','disposition':'CONSTRUCT_AMBIGUITY','material':False,'status':'documented_limitation'}
        (self.out/'ISSUES.json').write_bytes(a.encode([issue])); self.assertEqual(a.check(self.out)['errors'],[])
        issue['material']=True; (self.out/'ISSUES.json').write_bytes(a.encode([issue])); self.assertTrue(a.check(self.out)['errors'])

    def test_freeze(self): a.verify()

if __name__=='__main__': unittest.main()
