"""Deterministic offline workbooks; never impersonates the author or calls models."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess

from experiments.jev.evidence_v1.run import materials
from experiments.jev.adjudication_v2.records import verify as verify_previous
from experiments.jev.run import ROOT, encode, sha

HERE = Path(__file__).resolve().parent
from experiments.jev.adapter import LABELS
STATES = set(LABELS)


def build():
    cards, gold, questions, pairs, policy = materials()
    groups = {}
    for card in cards:
        for doc in card['state']['documents']:
            key = (doc['topic'], doc['text'])
            groups.setdefault(key, []).append((card['id'],gold[card['id']][doc['topic']]))
    units, key = [], {}
    for i, ((topic, text), uses) in enumerate(sorted(groups.items()),1):
        uid = f'U{i:03d}'
        units.append({'unit_id':uid,'topic':topic,'text':text,'question':questions[topic]['question']})
        key[uid]={'occurrences':[{'packet':p,'topic':topic,'reference':s} for p,s in uses]}
    files={'UNITS.json':encode(units),'KEY.json':encode(key)}
    for pass_id in (1,2):
        stream=io.StringIO(newline=''); writer=csv.writer(stream)
        writer.writerow(['unit_id','state','rationale','concern'])
        writer.writerows([u['unit_id'],'','',''] for u in sorted(units,key=lambda u:sha(f"pass{pass_id}:{u['unit_id']}".encode())))
        files[f'PASS_{pass_id}.csv']=stream.getvalue().encode()
    cards_by_id={c['id']:c for c in cards}
    packet=[{'pair_id':f'D{i:03d}','base':cards_by_id[p['base']]['state'],
             'variant':cards_by_id[p['variant']]['state']} for i,p in enumerate(pairs,1)]
    files['PAIR_PACKET.json']=encode(packet)
    stream=io.StringIO(newline=''); writer=csv.writer(stream)
    writer.writerow(['pair_id','decision','rationale','concern'])
    writer.writerows([p['pair_id'],'','',''] for p in packet)
    files['PAIRS.csv']=stream.getvalue().encode()
    files['COVER.json']=encode({'route':'author-audited-synthetic-v1','route_confirmed':False,
        'author':None,'pass_1_completed_at':None,'pass_2_completed_at':None,
        'pass_1_sha256':None,'pass_2_sha256':None,'live_output_exposure':'none_declared',
        'ai_criticism':'not_performed','independent_review':'not_performed'})
    files['ISSUES.json']=encode([])
    return files


def verify():
    verify_previous()
    path=HERE/'freeze.json'
    relative=str(path.relative_to(ROOT))
    committed=subprocess.check_output(['git','show','HEAD:'+relative],cwd=ROOT)
    if committed != path.read_bytes():
        raise ValueError('amendment manifest differs from committed bytes')
    for name,digest in json.loads(committed)['sha256'].items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise ValueError('amendment hash mismatch: '+name)


def export(output):
    output=Path(output).resolve()
    if output==ROOT or ROOT in output.parents:
        raise ValueError('workbook must be outside repository')
    output.mkdir(parents=True,exist_ok=False)
    for name,data in build().items():
        (output/name).write_bytes(data)


def check(directory):
    directory=Path(directory)
    expected=build(); errors=[]
    for name in ('UNITS.json','KEY.json','PAIR_PACKET.json'):
        if (directory/name).read_bytes()!=expected[name]: errors.append('changed source '+name)
    key=json.loads(expected['KEY.json']); pairs=json.loads(expected['PAIR_PACKET.json'])
    cover=json.loads((directory/'COVER.json').read_bytes())
    if cover.get('route')!='author-audited-synthetic-v1' or cover.get('route_confirmed') is not True:
        errors.append('author has not confirmed route')
    if not isinstance(cover.get('author'),str) or not cover['author'].strip(): errors.append('missing author identity')
    if cover.get('live_output_exposure')!='none_declared': errors.append('prospective exposure declaration missing or not clear')
    if cover.get('independent_review')!='not_performed': errors.append('this route cannot attest independent review')
    try:
        dates=[datetime.fromisoformat(cover[f'pass_{i}_completed_at'].replace('Z','+00:00')) for i in (1,2)]
        if any(d.tzinfo is None for d in dates) or dates[1]-dates[0]<timedelta(days=7) or any(d>datetime.now(timezone.utc) for d in dates):
            errors.append('two timezone-aware passes at least seven days apart required')
    except (TypeError,ValueError,AttributeError): errors.append('missing or invalid pass dates')
    rows=[]; flagged=set()
    for i in (1,2):
        path=directory/f'PASS_{i}.csv'
        data=list(csv.DictReader(io.StringIO(path.read_text())))
        mapped={r['unit_id']:r for r in data}; rows.append(mapped)
        if len(data)!=len(key) or set(mapped)!=set(key): errors.append(f'pass {i} coverage invalid')
        if sha(path.read_bytes())!=cover.get(f'pass_{i}_sha256'): errors.append(f'pass {i} saved hash missing/mismatched')
        for uid,row in mapped.items():
            if row.get('state') not in STATES or not row.get('rationale','').strip(): errors.append(f'pass {i} incomplete {uid}')
            refs={o['reference'] for o in key.get(uid,{}).get('occurrences',[])}
            if row.get('concern','').strip() or (row.get('state') in STATES and refs!={row['state']}): flagged.add(uid)
    for uid in set(rows[0])&set(rows[1]):
        if rows[0][uid].get('state')!=rows[1][uid].get('state'): flagged.add(uid)
    data=list(csv.DictReader(io.StringIO((directory/'PAIRS.csv').read_text())))
    mapped={r['pair_id']:r for r in data}
    if len(data)!=len(pairs) or set(mapped)!={p['pair_id'] for p in pairs}: errors.append('pair coverage invalid')
    for pid,row in mapped.items():
        if row.get('decision')!='retain' or not row.get('rationale','').strip(): errors.append('pair incomplete or material defect '+pid)
        if row.get('concern','').strip(): flagged.add(pid)
    issues=json.loads((directory/'ISSUES.json').read_bytes())
    addressed=set(); ids=set()
    dispositions={'JEV_ERROR','ORACLE_AMBIGUITY','QUESTION_DEFECT','EVIDENCE_TRANSLATION_DEFECT','CONSTRUCT_AMBIGUITY','INSUFFICIENT_EVIDENCE','UNRESOLVED'}
    for issue in issues:
        issue_id=issue.get('issue_id')
        if not issue_id or issue_id in ids: errors.append('missing/duplicate issue ID')
        ids.add(issue_id)
        if issue.get('target') not in set(key)|set(mapped): errors.append('unknown issue target')
        for field in ('evidence','alternative_interpretation','rationale','action'):
            if not isinstance(issue.get(field),str) or not issue[field].strip(): errors.append('issue missing '+field)
        if issue.get('disposition') not in dispositions: errors.append('unknown disposition')
        if issue.get('material') is not False or issue.get('status')!='documented_limitation':
            errors.append('material/unresolved issue requires new version or resolution')
        addressed.add(issue.get('target'))
    if flagged-addressed: errors.append('unaddressed concerns: '+','.join(sorted(flagged-addressed)))
    comparable=[u for u in set(rows[0])&set(rows[1]) if rows[0][u].get('state') in STATES and rows[1][u].get('state') in STATES]
    agreement=sum(rows[0][u]['state']==rows[1][u]['state'] for u in comparable)
    return {'author_consistency':{'valid_pairs':len(comparable),'same_state':agreement,'agreement':agreement/len(comparable) if comparable else None},'route':'author-audited-synthetic-v1','status':'PENDING' if errors else 'RECORDED_COMPLETE',
        'errors':errors,'units':len(key),'pairs':len(pairs),
        'boundary':'Recorded author attestations only; no independent validity or live authorization.'}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['export','check'])
    parser.add_argument('--input',type=Path); parser.add_argument('--output',type=Path)
    args=parser.parse_args(); verify()
    if args.action=='export':
        if args.output is None: parser.error('export requires --output')
        export(args.output); print('Blank author workbook exported; human review pending.')
    else:
        if args.input is None: parser.error('check requires --input')
        result=check(args.input); print(json.dumps(result,indent=2)); raise SystemExit(bool(result['errors']))

if __name__=='__main__': main()
