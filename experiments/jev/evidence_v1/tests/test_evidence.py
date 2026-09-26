import copy
import json
import shutil
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import jsonschema
from experiments.jev.adapter import LABELS, MockAdapter
from experiments.jev.run import ROOT, encode, load, sha, materials as v1_materials
from experiments.jev.evidence_v1 import run as harness
from experiments.jev.evidence_v1.author import build


class EvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (harness.HERE/'runs').mkdir(exist_ok=True)
        cls.parent=Path(tempfile.mkdtemp(dir=harness.HERE/'runs'))
        cls.network=patch.object(socket.socket,'connect',side_effect=AssertionError('network forbidden'))
        cls.network.start()
        cls.cards,cls.gold,cls.questions,cls.pairs,cls.policy=harness.materials()
        cls.dry=harness.run('dry-run',cls.parent/'dry')
        cls.mock=harness.run('mock',cls.parent/'mock')
        cls.report=load(cls.parent/'mock/report.json')

    @classmethod
    def tearDownClass(cls):
        cls.network.stop()
        shutil.rmtree(cls.parent)

    def test_freeze_and_reproducible_authorship(self):
        frozen=harness.verify()
        self.assertGreater(len(frozen['preserved']),20)
        for name,data in build().items():
            self.assertEqual(encode(data),(harness.HERE/name).read_bytes(),name)
        v1_materials()  # also verifies the original sealed oracle and v1 freeze

    def test_tampering_materials_and_freeze_rejected(self):
        original=Path.read_bytes
        def tamper(path):
            data=original(path)
            return data+b' ' if path==harness.HERE/'cards.json' else data
        with patch.object(Path,'read_bytes',tamper),self.assertRaises(ValueError):
            harness.verify()
        def tamper_freeze(path):
            data=original(path)
            return data+b' ' if path==harness.HERE/'freeze.json' else data
        with patch.object(Path,'read_bytes',tamper_freeze),self.assertRaises(ValueError):
            harness.verify()

    def test_inventory_and_holdout_novelty(self):
        self.assertEqual(len(self.cards),94)
        self.assertEqual(sum(len(x) for x in self.gold.values()),1654)
        self.assertEqual(len(self.pairs),60)
        by_suite={s:[c for c in self.cards if c['suite']==s] for s in {c['suite'] for c in self.cards}}
        self.assertEqual({s:len(c) for s,c in by_suite.items()},
            {'reconstruction':12,'mutation':9,'boundary':3,'invariance':48,'authority':16,'holdout':6})
        baseline={encode(sorted(c['state']['documents'],key=lambda d:d['topic'])) for c in by_suite['reconstruction']}
        holdouts=[encode(sorted(c['state']['documents'],key=lambda d:d['topic'])) for c in by_suite['holdout']]
        self.assertEqual(len(set(holdouts)),6)
        self.assertFalse(set(holdouts)&baseline)
        for c in by_suite['holdout']:
            self.assertEqual(set(self.gold[c['id']].values()),set(LABELS))

    def test_wire_boundary_and_frozen_repetitions(self):
        self.assertEqual(len(self.dry['records']),282)
        self.assertFalse(list((self.parent/'dry').glob('*.response.json')))
        by_id={}
        for r in self.dry['records']:
            raw=(self.parent/'dry'/r['request_file']).read_bytes()
            wire=json.loads(raw)
            self.assertEqual(set(wire),{'state','questions','model'})
            self.assertEqual(set(wire['state'])-{'incidental_context'},{'packet_kind','documents'})
            for d in wire['state']['documents']:
                self.assertEqual(set(d),{'topic','text'})
            for forbidden in ('trust_signals','control_signals','source_case','source_path','expected_deltas','advisory_only','pre_action_complete'):
                self.assertNotIn(forbidden,raw.decode())
            self.assertEqual(sha(raw),r['request_sha256'])
            by_id.setdefault(r['job_id'],set()).add(r['request_sha256'])
        self.assertTrue(all(len(v)==1 for v in by_id.values()))
        self.assertEqual([r['repetition'] for r in self.dry['records']],[1]*94+[2]*94+[3]*94)
        self.assertEqual(load(self.parent/'dry/report.json')['request_status_counts']['planned'],282)

    def test_mock_is_uniform_no_oracle_in_adapter(self):
        self.assertEqual(self.mock['status'],'complete')
        self.assertEqual(self.report['resolved_versions'],['mock-only'])
        self.assertEqual(self.report['request_status_counts']['ok'],282)
        for r in self.mock['records']:
            self.assertEqual(sha((self.parent/'mock'/r['response_file']).read_bytes()),r['response_sha256'])
            self.assertTrue(all(a['choice']=='indeterminate' and set(a['probabilities'].values())=={0.2} for a in r['answers'].values()))
        for section in self.report['sections']:
            self.assertAlmostEqual(section['overall']['brier_mean'],0.8)
        mutation=[p for p in self.report['pairs'] if p['suite']=='mutation']
        self.assertTrue(all(not p['exact_delta_match'] for p in mutation))
        self.assertEqual(len(mutation),27)
        self.assertTrue(all(p['exact_delta_match'] for p in self.report['pairs'] if p['suite']!='mutation'))

    def test_hand_calculated_metrics_and_empty_states(self):
        probs=lambda choice:{l:float(l==choice) for l in LABELS}
        rows=[{'gold':'supported','choice':'supported','probabilities':probs('supported')},
              {'gold':'unsupported','choice':'supported','probabilities':probs('supported')}]
        score=harness.summary(rows,['supported','unsupported','indeterminate'])
        self.assertEqual(score['agreement'],0.5)
        self.assertEqual(score['disagreement_rate'],0.5)
        self.assertEqual(score['brier_mean'],1)
        self.assertEqual(score['coverage'],2/3)
        self.assertEqual(score['recall']['unsupported']['value'],0)
        self.assertIsNone(score['recall']['indeterminate']['value'])
        self.assertEqual(score['scheduled_gold_counts']['indeterminate'],1)
        self.assertEqual(sum(sum(r.values()) for r in score['confusion_matrix_gold_rows'].values()),2)
        self.assertIsNone(harness.summary([],[])['agreement'])

    def test_mutation_exact_delta_and_extra_change(self):
        pair=next(p for p in self.pairs if p['suite']=='mutation')
        records=copy.deepcopy([r for r in self.mock['records'] if r['repetition']==1 and r['job_id'] in (pair['base'],pair['variant'])])
        by_id={r['job_id']:r for r in records}
        for q,(before,after) in pair['expected_deltas'].items():
            by_id[pair['base']]['answers'][q]['choice']=before
            by_id[pair['variant']]['answers'][q]['choice']=after
        self.assertTrue(harness.paired(records,[pair],1)[0]['exact_delta_match'])
        other=next(q for q in records[0]['answers'] if q not in pair['expected_deltas'])
        by_id[pair['variant']]['answers'][other]['choice']='unsupported'
        self.assertFalse(harness.paired(records,[pair],1)[0]['exact_delta_match'])
        by_id[pair['variant']]['resolved_model']='different-version'
        self.assertEqual(harness.paired(records,[pair],1)[0]['reason'],'resolved_model_mismatch')
        by_id[pair['variant']]['status']='invalid'
        self.assertEqual(harness.paired(records,[pair],1)[0]['status'],'not_evaluated')

    def test_invariance_facts_and_paraphrases(self):
        cards={c['id']:c for c in self.cards}
        for pair in self.pairs:
            if pair['suite']!='invariance':
                continue
            a,b=cards[pair['base']],cards[pair['variant']]
            self.assertEqual(self.gold[a['id']],self.gold[b['id']])
            self.assertNotEqual(encode(a['state']),encode(b['state']))
            da={d['topic']:d['text'] for d in a['state']['documents']}
            db={d['topic']:d['text'] for d in b['state']['documents']}
            if b['id'].endswith('paraphrase'):
                for q in da:
                    if q!='control__access':
                        self.assertTrue(db[q].endswith(da[q]))
            else:
                self.assertEqual(da,db)
        for verb in ('review','recommend','object'):
            self.assertEqual(self.gold[f'A-{verb}-1']['control__authority'],'unsupported')
        for verb in ('delay','suspend','cancel','override','approval-required'):
            self.assertEqual(self.gold[f'A-{verb}-0']['control__authority'],'partially_supported')
            self.assertEqual(self.gold[f'A-{verb}-1']['control__authority'],'supported')

    def test_adjudication_schema_and_independent_review_gate(self):
        items=load(self.parent/'mock/adjudications.json')
        self.assertGreater(len(items),0)
        validator=jsonschema.Draft202012Validator(load(harness.HERE/'adjudication.schema.json'))
        for item in items:
            validator.validate(item)
        item=copy.deepcopy(items[0])
        item.update(status='closed',disposition='EVIDENCE_TRANSLATION_DEFECT',rationale='Translation introduced an unsupported event.')
        with self.assertRaises(jsonschema.ValidationError):
            harness.validate_adjudication(item)
        item['reviewers']=[{'identity':'reviewer-one','blind_notes':'Independent note','reconciliation':'Agreed'}]*2
        with self.assertRaises((jsonschema.ValidationError,ValueError)):
            harness.validate_adjudication(item)
        item['reviewers'][1]={'identity':'reviewer-two','blind_notes':'Second independent note','reconciliation':'Agreed'}
        harness.validate_adjudication(item)

    def test_failure_accounting_no_retry_and_live_rejected(self):
        class BadAdapter:
            calls=0
            def evaluate(self,*args):
                self.calls+=1
                if self.calls==1:
                    return b'{"model":"mock-only","answers":{}}'
                raise RuntimeError('secret must not be logged')
            def close(self):
                pass
        adapter=BadAdapter()
        card=self.cards[0]
        subset=([card],{card['id']:self.gold[card['id']]},self.questions,[],self.policy)
        with patch.object(harness,'materials',return_value=subset):
            result=harness.run('mock',self.parent/'bad',adapter)
        self.assertEqual(adapter.calls,3)
        self.assertEqual([r['status'] for r in result['records']],['invalid','error','error'])
        self.assertNotIn('secret',(self.parent/'bad/run.json').read_text())
        report=load(self.parent/'bad/report.json')
        self.assertEqual(report['scheduled_requests'],3)
        self.assertTrue(all(s['overall']['valid']==0 for s in report['sections']))
        with self.assertRaises(ValueError):
            harness.run('live',self.parent/'live')
        with self.assertRaises(FileExistsError):
            harness.run('dry-run',self.parent/'dry')
        with self.assertRaises(ValueError):
            harness.run('dry-run',Path('/tmp/forbidden-evidence-output'))

    def test_interruption_preserves_scheduled_denominator(self):
        class InterruptAdapter:
            def evaluate(self,*args):
                raise KeyboardInterrupt()
            def close(self):
                pass
        card=self.cards[0]
        with patch.object(harness,'materials',return_value=([card],{card['id']:self.gold[card['id']]},self.questions,[],self.policy)):
            with self.assertRaises(KeyboardInterrupt):
                harness.run('mock',self.parent/'interrupted',InterruptAdapter())
        result=load(self.parent/'interrupted/run.json')
        self.assertEqual(result['status'],'interrupted')
        self.assertEqual(len(result['records']),3)
        self.assertEqual(load(self.parent/'interrupted/report.json')['scheduled_requests'],3)

    def test_mixed_models_never_pooled(self):
        records=copy.deepcopy(self.mock['records'][:2])
        records[1]['resolved_model']='other-version'
        rep=harness.report(records,self.cards[:2],self.gold,[],self.policy,'mock')
        self.assertEqual(rep['resolved_versions'],['mock-only','other-version'])
        sections=[s for s in rep['sections'] if s['repetition']==1]
        self.assertTrue(all(s['overall']['valid']==21 and s['overall']['scheduled']==42 for s in sections))

if __name__=='__main__':
    unittest.main()
