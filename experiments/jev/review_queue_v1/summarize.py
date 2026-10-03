"""Prespecified descriptive workflow measurements; human benefit remains unmeasured."""
from collections import Counter
from datetime import datetime
import json
from pathlib import Path
import statistics

from .pilot import verify, validate
from experiments.jev.run import sha,encode


def summarize(path):
    path=Path(path);c=verify();r=json.loads((path/'run.json').read_bytes())
    expected=[(rep,u) for rep in (1,2,3) for u in c['units']]
    if len(r['records'])!=len(expected):raise ValueError('Wrong schedule')
    for row,(rep,u) in zip(r['records'],expected):
        if (row['unit_id'],row['repetition'])!=(u['id'],rep):raise ValueError('Wrong scheduled position')
        raw=(path/row['request_file']).read_bytes()
        payload={'model':'jev-1.13.0','state':u['state'],'questions':c['questions']}
        if sha(raw)!=row['request_sha256'] or raw!=encode(payload):raise ValueError('Request changed')
        if row.get('response_file'):
            raw=(path/row['response_file']).read_bytes()
            if sha(raw)!=row['response_sha256']:raise ValueError('Response changed')
            if row['status']=='ok' and validate(raw,c['questions'])['answers']!=row['answers']:raise ValueError('Answers changed')
        if row.get('http_request_file'):
            raw=(path/row['http_request_file']).read_bytes()
            if sha(raw)!=row['http_request_sha256'] or json.loads(raw)!=payload:raise ValueError('SDK body changed')
    times=[x['elapsed_seconds'] for x in r['records'] if 'elapsed_seconds' in x]
    versions=sorted({x['resolved_model'] for x in r['records'] if x['resolved_model']})
    counts=[]
    for rep in (1,2,3):
        for v in versions:
            rows=[x for x in r['records'] if x['repetition']==rep and x['status']=='ok' and x['resolved_model']==v]
            counts.append({'repetition':rep,'resolved_model':v,'valid':len(rows),'scheduled':24,
                'choices':{q:dict(Counter(x['answers'][q]['choice'] for x in rows)) for q in c['questions']}})
    repeated=[]
    for u in c['units']:
        rows=[x for x in r['records'] if x['unit_id']==u['id']]
        valid=all(x['status']=='ok' for x in rows) and len({x['resolved_model'] for x in rows})==1
        repeated.append({'unit_id':u['id'],'evaluable':valid,'changed_questions':
            [q for q in c['questions'] if len({x['answers'][q]['choice'] for x in rows})>1] if valid else None})
    return {'mode':r['mode'],'scheduled':72,'statuses':dict(Counter(x['status'] for x in r['records'])),
        'resolved_versions':versions,'median_attempt_seconds':statistics.median(times) if times else None,
        'summed_attempt_seconds':sum(times),
        'scheduled_execution_seconds':(datetime.fromisoformat(r['finished_at'])-datetime.fromisoformat(r['started_at'])).total_seconds(),
        'timing_boundary':'Execution timestamps exclude initial corpus verification and human/setup/checking overhead.',
        'sections':counts,'repetitions':repeated,'deterministic_source_requests':len(c['deterministic_queue']),
        'human_time_saving':None,'review_quality':None,
        'interpretation':'Diagnostic assistance only; no independent adjudication, causal speedup or accuracy claim.'}
