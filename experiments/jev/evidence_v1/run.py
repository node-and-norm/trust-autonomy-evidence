"""Credential-free frozen documentary experiment. No live transport is available."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from experiments.jev.adapter import LABELS, MockAdapter, validate_response
from experiments.jev.run import ROOT, encode, load, sha

HERE = Path(__file__).resolve().parent


def verify():
    freeze_path = HERE / 'freeze.json'
    frozen_bytes = freeze_path.read_bytes()
    relative = freeze_path.relative_to(ROOT).as_posix()
    committed = subprocess.check_output(['git', 'show', 'HEAD:'+relative], cwd=ROOT)
    if committed != frozen_bytes:
        raise ValueError('freeze differs from committed Git anchor')
    freeze = json.loads(frozen_bytes)
    for namespace in ('materials', 'preserved'):
        for name, digest in freeze[namespace].items():
            path = (ROOT / name).resolve()
            if ROOT not in path.parents or sha(path.read_bytes()) != digest:
                raise ValueError('freeze mismatch: '+name)
    return freeze


def materials():
    verify()
    cards, gold, questions, pairs, policy = [load(HERE/name) for name in
        ('cards.json','gold.json','questions.json','pairs.json','policy.json')]
    ids = [c['id'] for c in cards]
    if len(set(ids)) != len(ids) or set(ids) != set(gold):
        raise ValueError('case inventory differs from gold')
    for card in cards:
        topics = [d['topic'] for d in card['state']['documents']]
        if len(topics) != len(set(topics)) or set(topics) != set(gold[card['id']]):
            raise ValueError('document and question inventory mismatch')
        if not set(topics) <= set(questions) or not set(gold[card['id']].values()) <= set(LABELS):
            raise ValueError('unknown question or reference label')
    if policy['label_order'] != list(LABELS) or policy['live_enabled']:
        raise ValueError('unexpected policy')
    return cards, gold, questions, pairs, policy


def request(card, questions, policy):
    # Allowlist projection: local ID, suite, gold, provenance and pairs are absent.
    topics = {d['topic'] for d in card['state']['documents']}
    return {'model': policy['requested_model'], 'state': card['state'],
            'questions': {q: questions[q]['question'] for q in questions if q in topics}}


def summary(rows, scheduled):
    matrix = {a:{b:0 for b in LABELS} for a in LABELS}
    counts = {a:scheduled.count(a) for a in LABELS}
    for row in rows:
        matrix[row['gold']][row['choice']] += 1
    n = len(rows)
    matches = sum(r['choice']==r['gold'] for r in rows)
    return {'scheduled':len(scheduled),'valid':n,'coverage':n/len(scheduled) if scheduled else None,
        'agreements':matches,'agreement':matches/n if n else None,
        'disagreements':n-matches,'disagreement_rate':(n-matches)/n if n else None,
        'brier_mean':sum(sum((r['probabilities'][l]-int(l==r['gold']))**2 for l in LABELS) for r in rows)/n if n else None,
        'confusion_matrix_gold_rows':matrix,'scheduled_gold_counts':counts,
        'recall':{l:{'correct':matrix[l][l],'valid_gold':sum(matrix[l].values()),
            'value':matrix[l][l]/sum(matrix[l].values()) if sum(matrix[l].values()) else None} for l in LABELS}}


def metrics(records, gold):
    rows = []
    for r in records:
        if r['status']=='ok':
            rows.extend({'question':q,'gold':gold[r['job_id']][q],**a} for q,a in r['answers'].items())
    scheduled = [label for r in records for label in gold[r['job_id']].values()]
    qids = sorted({q for r in records for q in gold[r['job_id']]})
    return {'overall':summary(rows,scheduled),'per_construct':{
        q:summary([r for r in rows if r['question']==q],
            [gold[r['job_id']][q] for r in records if q in gold[r['job_id']]]) for q in qids}}


def paired(records, pairs, repetitions):
    by_id={(r['job_id'],r['repetition']):r for r in records}
    results=[]
    for rep in range(1,repetitions+1):
        for pair in pairs:
            a,b=(by_id.get((pair[k],rep)) for k in ('base','variant'))
            row={**pair,'repetition':rep,'status':'not_evaluated','reason':'missing_or_invalid'}
            if a and b:
                row['input_identical']=a['request_sha256']==b['request_sha256']
            if a and b and a['status']==b['status']=='ok':
                if a['resolved_model'] != b['resolved_model']:
                    row['reason']='resolved_model_mismatch'
                else:
                    observed={q:[a['answers'][q]['choice'],b['answers'][q]['choice']]
                        for q in a['answers'] if a['answers'][q]['choice']!=b['answers'][q]['choice']}
                    row.update(status='evaluated',reason=None,resolved_model=a['resolved_model'],observed_deltas=observed,
                        exact_delta_match=observed==pair['expected_deltas'],
                        choice_invariance_failure=bool(observed),
                        max_probability_shift=max(abs(a['answers'][q]['probabilities'][l]-b['answers'][q]['probabilities'][l])
                            for q in a['answers'] for l in LABELS))
            results.append(row)
    return results


def repetition_results(records):
    groups={}
    for r in records:
        groups.setdefault(r['job_id'],[]).append(r)
    result=[]
    for jid,group in groups.items():
        valid=[r for r in group if r['status']=='ok']
        versions={r['resolved_model'] for r in valid}
        row={'job_id':jid,'scheduled':len(group),'valid':len(valid),'status':'not_evaluated'}
        if len(valid)==len(group) and len(valid)>1 and len(versions)==1:
            row.update(status='evaluated',resolved_model=valid[0]['resolved_model'],
                changed_questions=[q for q in valid[0]['answers'] if len({r['answers'][q]['choice'] for r in valid})>1],
                max_probability_shift=max(max(r['answers'][q]['probabilities'][l] for r in valid)-
                    min(r['answers'][q]['probabilities'][l] for r in valid) for q in valid[0]['answers'] for l in LABELS))
        result.append(row)
    return result


def report(records, cards, gold, pairs, policy, mode):
    versions=sorted({r['resolved_model'] for r in records if r.get('resolved_model')})
    statuses={s:sum(r['status']==s for r in records) for s in ('planned','ok','invalid','error','interrupted')}
    # Never aggregate scores across resolved versions. Coverage of a version includes
    # the full scheduled suite; all missing/other-version positions remain visible.
    sections=[]
    for rep in [1,2,3,'pooled_secondary']:
        for suite in sorted({c['suite'] for c in cards}):
            selected=[r for r in records if r['suite']==suite and (rep=='pooled_secondary' or r['repetition']==rep)]
            for version in versions or [None]:
                scoped=[r if r.get('resolved_model')==version else {**r,'status':'version_excluded'} for r in selected]
                sections.append({'repetition':rep,'suite':suite,'resolved_model':version,**metrics(scoped,gold)})
    pairs_out=paired(records,pairs,policy['repetitions'])
    pair_summary=[]
    for rep in (1,2,3):
        for suite in sorted({p['suite'] for p in pairs}):
            for version in versions or [None]:
                group=[p for p in pairs_out if p['repetition']==rep and p['suite']==suite]
                valid=[p for p in group if p['status']=='evaluated' and p['resolved_model']==version]
                pair_summary.append({'repetition':rep,'suite':suite,'resolved_model':version,'scheduled':len(group),
                    'evaluable':len(valid),'exact_delta_matches':sum(p['exact_delta_match'] for p in valid),
                    'exact_delta_rate':sum(p['exact_delta_match'] for p in valid)/len(valid) if valid else None,
                    'choice_invariance_failures':sum(p['choice_invariance_failure'] for p in valid) if suite!='mutation' else None})
    return {'mode':mode,'interpretation':'OFFLINE PLUMBING ONLY; no Jev performance inference',
        'requested_model':policy['requested_model'],'resolved_versions':versions,
        'scheduled_requests':len(records),'attempted':sum(r['status']!='planned' for r in records),
        'request_status_counts':statuses,'missing_resolved_version':sum(r['status']!='planned' and not r.get('resolved_model') for r in records),
        'sections':sections,'pair_summary':pair_summary,'pairs':pairs_out,'repetitions':repetition_results(records)}


def adjudications(records, gold, run_id):
    result=[]
    for r in records:
        if r['status']=='planned':
            continue
        questions = gold[r['job_id']]
        for q in questions:
            if r['status']=='ok' and r['answers'][q]['choice']==questions[q]:
                continue
            result.append({'record_id':f"{r['job_id']}-r{r['repetition']}-{q}",
                'run_id':run_id,'job_id':r['job_id'],'repetition':r['repetition'],'question_id':q,
                'status':'open','disposition':'UNRESOLVED','evidence_refs':[
                    f"cards.json#{r['job_id']}/{q}",f"questions.json#{q}",f"provenance.json#{r['job_id']}",
                    r['request_file']], 'reviewers':[],'rationale':'','supersedes':None})
    return result


def validate_adjudication(item):
    import jsonschema
    jsonschema.Draft202012Validator(load(HERE/'adjudication.schema.json')).validate(item)
    if item['status']=='closed' and len({r['identity'].strip().casefold() for r in item['reviewers']})!=2:
        raise ValueError('two distinct reviewers required')


def run(mode, output, adapter=None):
    if mode not in ('dry-run','mock'):
        raise ValueError('this phase has no live mode')
    cards,gold,questions,pairs,policy=materials()
    output=Path(output).resolve()
    runs=(HERE/'runs').resolve()
    # Reject symlink redirects out of the experiment as well as overwrite attempts.
    if runs != HERE/'runs' or runs not in output.parents:
        raise ValueError('output must be a new directory under evidence_v1/runs')
    output.mkdir(parents=True,exist_ok=False)
    adapter=adapter or (MockAdapter() if mode=='mock' else None)
    meta={'mode':mode,'status':'running','freeze_sha256':sha((HERE/'freeze.json').read_bytes()),
        'git_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'requested_model':policy['requested_model'],'sdk_version':getattr(adapter,'sdk_version',None),
        'records':[]}
    # All requests are planned before any output is observed. Persist schedule so an
    # interrupted run retains its full denominator and never resumes selectively.
    for rep in range(1,policy['repetitions']+1):
        for card in cards:
            name=f"{card['id']}-r{rep}"
            wire=encode(request(card,questions,policy))
            (output/(name+'.request.json')).write_bytes(wire)
            meta['records'].append({'job_id':card['id'],'suite':card['suite'],'repetition':rep,
                'request_file':name+'.request.json','request_sha256':sha(wire),
                'response_file':None,'response_sha256':None,'resolved_model':None,'status':'planned'})
    def save():
        (output/'run.json').write_bytes(encode(meta))
    save()
    try:
        if mode=='mock':
            for r in meta['records']:
                wire=load(output/r['request_file'])
                try:
                    raw=adapter.evaluate(wire['state'],wire['questions'],wire['model'])
                except (KeyboardInterrupt, SystemExit):
                    r.update(status='interrupted')
                    raise
                except Exception as exc:
                    r.update(status='error',error_type=type(exc).__name__)
                else:
                    name=r['request_file'].replace('.request.json','.response.json')
                    (output/name).write_bytes(raw)
                    r.update(response_file=name,response_sha256=sha(raw))
                    try:
                        parsed=json.loads(raw)
                        if isinstance(parsed,dict) and isinstance(parsed.get('model'),str) and parsed['model'].strip():
                            r['resolved_model']=parsed['model']
                        doc=validate_response(raw,set(wire['questions']))
                    except (ValueError,TypeError,KeyError) as exc:
                        r.update(status='invalid',error_type=type(exc).__name__)
                    else:
                        r.update(status='ok',resolved_model=doc['model'],answers=doc['answers'])
                save()
        meta['status']='dry-run' if mode=='dry-run' else ('incomplete' if any(r['status']!='ok' for r in meta['records']) else 'complete')
    except BaseException:
        meta['status']='interrupted'
        raise
    finally:
        save()
        (output/'report.json').write_bytes(encode(report(meta['records'],cards,gold,pairs,policy,mode)))
        (output/'adjudications.json').write_bytes(encode(adjudications(meta['records'],gold,output.name)))
        if adapter:
            adapter.close()
    return meta


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',choices=('dry-run','mock'),default='dry-run')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run(args.mode,args.output)
    print(json.dumps({'mode':result['mode'],'status':result['status'],'scheduled':len(result['records'])}))
    return 0 if result['status'] in ('complete','dry-run') else 2

if __name__=='__main__':
    raise SystemExit(main())
