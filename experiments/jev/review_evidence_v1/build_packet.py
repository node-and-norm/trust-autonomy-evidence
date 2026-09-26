"""Export pre-live human review materials without modifying the frozen experiment."""
import csv
import hashlib
import io
import json
from pathlib import Path
from experiments.jev.evidence_v1.run import materials, HERE
from experiments.jev.run import encode

OUT = Path(__file__).resolve().parent


def build():
    cards, gold, questions, pairs, policy = materials()
    packet, key, rows = [], {}, []
    # Opaque review IDs hide suite/source identity. Stable hash order is reproducible.
    ordered = sorted(cards, key=lambda c: hashlib.sha256(('review-v1:'+c['id']).encode()).hexdigest())
    for i, card in enumerate(ordered, 1):
        rid = f'R{i:03d}'
        topics = {d['topic'] for d in card['state']['documents']}
        packet.append({'review_id':rid,'state':card['state'],
            'questions':{q:questions[q]['question'] for q in questions if q in topics}})
        key[rid] = {'source_id':card['id'],'suite':card['suite'],'reference_labels':gold[card['id']]}
        rows.extend([rid,q,'','',''] for q in sorted(topics))
    files = {'BLIND_PACKET.json':encode(packet),'COORDINATOR_KEY.json':encode(key)}
    stream = io.StringIO(newline='')
    writer = csv.writer(stream)
    writer.writerow(['review_id','question_id','evidence_state','translation_or_question_concern','independent_notes'])
    writer.writerows(rows)
    for reviewer in ('A','B'):
        files[f'REVIEWER_{reviewer}.csv'] = stream.getvalue().encode()
    manifest = {'source_freeze_sha256':hashlib.sha256((HERE/'freeze.json').read_bytes()).hexdigest(),
        'packets':len(packet),'determinations_per_reviewer':len(rows),
        'status':'blank forms; no human review completed',
        'sha256':{name:hashlib.sha256(data).hexdigest() for name,data in files.items()}}
    files['manifest.json']=encode(manifest)
    return files


if __name__=='__main__':
    for name,data in build().items():
        path=OUT/name
        if path.exists() and path.read_bytes()!=data:
            raise SystemExit('Refusing to overwrite changed review material: '+name)
        path.write_bytes(data)
