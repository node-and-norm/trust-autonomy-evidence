"""Post-output descriptive diagnostics; never modifies raw scores or calls Jev."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path

from experiments.jev.live_results_v1.verify import verify
from experiments.jev.evidence_v2.run import materials
from experiments.jev.run import encode, sha

HERE = Path(__file__).resolve().parent


def analyze():
    files, run, report = verify()
    cards, gold, questions, pairs, policy = materials()
    failed = []
    for row in run['records']:
        doc = json.loads(files[row['response_file']])
        for question, answer in doc['answers'].items():
            total = sum(answer['probabilities'].values())
            if not math.isclose(total, 1.0, abs_tol=1e-5):
                failed.append({'job_id':row['job_id'], 'repetition':row['repetition'],
                    'question_id':question, 'probability_sum':total,
                    'request_sha256':row['request_sha256'], 'response_sha256':row['response_sha256']})
    sections = []
    for rep in (1,2,3):
        for suite in sorted({c['suite'] for c in cards}):
            rows=[r for r in run['records'] if r['repetition']==rep and r['suite']==suite]
            constructs=[]
            for q in sorted(questions):
                selected=[r for r in rows if gold[r['job_id']].get(q)=='partially_supported']
                if not selected:
                    continue
                valid=[r for r in selected if r['status']=='ok']
                predictions=Counter(r['answers'][q]['choice'] for r in valid)
                constructs.append({'question_id':q,'scheduled_partial':len(selected),
                    'valid_partial':len(valid),'predictions':dict(predictions),
                    'disagreements':[{'job_id':r['job_id'],'response_file':r['response_file'],
                                      'choice':r['answers'][q]['choice']}
                                     for r in valid if r['answers'][q]['choice']!='partially_supported']})
            sections.append({'repetition':rep,'suite':suite,'constructs':constructs})
    return {'analysis_type':'post-output descriptive diagnostics; no adjusted scores or dispositions',
        'run_sha256':sha(files['run.json']), 'report_sha256':sha(files['report.json']),
        'probability_failures':failed,
        'invalid_requests':report['request_status_counts']['invalid'],
        'excluded_determinations':sum(len(gold[r['job_id']]) for r in run['records'] if r['status']=='invalid'),
        'partial_state_sections':sections}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    data=encode(analyze());path=HERE/'diagnostics.json'
    if args.check:
        if path.read_bytes()!=data:raise ValueError('Diagnostics differ from saved evidence')
        print('Follow-up diagnostics: PASS (no inference calls)')
    else:
        with path.open('xb') as file:file.write(data)


if __name__=='__main__':main()
