import json
import socket
import shutil
import tempfile
import unittest
from unittest.mock import patch
from experiments.jev.evidence_v2 import run as r,author
from experiments.jev.evidence_v1 import run as old
from experiments.jev.run import encode

class SuccessorTests(unittest.TestCase):
    def test_reproduction_freeze_and_inventory(self):
        c,g,q,p,policy=r.materials()
        self.assertEqual(len(c),94);self.assertEqual(sum(map(len,g.values())),1654)
        for name,value in author.build().items():self.assertEqual(encode(value),(r.HERE/name).read_bytes(),name)
        self.assertEqual(g,old.materials()[1])
        self.assertEqual(policy['review_route'],'author_reviewed_ai_assisted_v1')

    def test_pairs_and_unchanged_topics(self):
        c,g,q,p,policy=r.materials(); by={x['id']:x for x in c}
        for pair in p:
            a,b=pair['base'],pair['variant']
            delta={k:[g[a][k],g[b][k]] for k in g[a] if g[a][k]!=g[b][k]}
            self.assertEqual(delta,pair['expected_deltas'])
            if pair['suite']=='mutation':
                before={d['topic']:d['text'] for d in by[a]['state']['documents']}
                after={d['topic']:d['text'] for d in by[b]['state']['documents']}
                self.assertEqual({k for k in before if before[k]!=after[k]},set(delta))

    def test_every_material_issue_implemented_and_no_stale_text(self):
        c,g,q,p,policy=r.materials()
        text='\n'.join(d['text'] for x in c for d in x['state']['documents'])
        for oldtext in author.REPLACEMENTS:self.assertNotIn(oldtext,text)
        self.assertNotIn('object the proposed action',text)
        self.assertIn('recommended cancellation',text)
        self.assertIn('recorded a review note requesting cancellation',text)
        self.assertIn('partially_supported',q['control__access']['question']['instructions'])
        self.assertIn('documented precursor only',q['control__comprehension']['question']['instructions'])
        self.assertIn('attestation only',q['control__exercise']['question']['instructions'])
        self.assertIn('threshold failure',q['trust__reliability']['question']['instructions'])
        self.assertIn('at least two',q['trust__capability']['question']['instructions'])

    def test_wire_and_repetitions(self):
        c,g,q,p,policy=r.materials()
        for card in c:
            wire=r.request(card,q,policy)
            self.assertEqual(set(wire),{'state','questions','model'})
            self.assertNotIn('reference_labels',wire['state'])
        self.assertEqual(policy['repetitions'],3)
        with self.assertRaises(ValueError):r.run('live',r.HERE/'runs/not-allowed')

    def test_network_free_mock_and_dry(self):
        (r.HERE/'runs').mkdir(exist_ok=True)
        directory=r.HERE/'runs'/('test-'+next(tempfile._get_candidate_names()))
        self.addCleanup(lambda:shutil.rmtree(directory,ignore_errors=True))
        with patch.object(socket.socket,'connect',side_effect=AssertionError('network forbidden')):
            dry=r.run('dry-run',directory/'dry');mock=r.run('mock',directory/'mock')
        self.assertEqual(len(dry['records']),282);self.assertEqual(len(mock['records']),282)
        report=json.loads((directory/'mock/report.json').read_bytes())
        self.assertEqual(report['experiment_version'],'jev-tae-evidence-v2')
        self.assertEqual(report['review_route'],'author_reviewed_ai_assisted_v1')
        self.assertTrue(all(x['status']=='ok' for x in mock['records']))
        with self.assertRaises(FileExistsError):r.run('mock',directory/'mock')

if __name__=='__main__':unittest.main()
