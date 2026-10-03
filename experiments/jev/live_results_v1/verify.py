"""Verify archived run bytes and recompute frozen analysis without credentials."""
import json
from pathlib import Path
import tarfile

from experiments.jev.evidence_v2 import run as frozen
from experiments.jev.run import encode, sha
from experiments.jev.adjudication_v2.records import validate

HERE = Path(__file__).resolve().parent


def verify():
    manifest = json.loads((HERE/'manifest.json').read_bytes())
    archive = HERE/'live-001.tar.gz'
    if sha(archive.read_bytes()) != manifest['archive_sha256']:
        raise ValueError('Archive hash mismatch')
    files = {}
    with tarfile.open(archive, 'r:gz') as tar:
        for member in tar.getmembers():
            if not member.isfile() or member.name in files or Path(member.name).name != member.name:
                raise ValueError('Unexpected archive member')
            files[member.name] = tar.extractfile(member).read()
    if {k: sha(v) for k, v in files.items()} != manifest['members_sha256']:
        raise ValueError('Archived members differ from manifest')
    run = json.loads(files['run.json'])
    schedule = json.loads(files['schedule.json'])
    cards, gold, questions, pairs, policy = frozen.materials()
    if len(run['records']) != 282 or len(schedule['records']) != 282:
        raise ValueError('Wrong schedule length')
    expected = [(rep, card) for rep in (1,2,3) for card in cards]
    for row, planned, (rep, card) in zip(run['records'], schedule['records'], expected):
        if (row['job_id'], row['repetition'], row['suite']) != (card['id'], rep, card['suite']):
            raise ValueError('Schedule changed')
        for key in ('job_id','suite','repetition','request_file','request_sha256'):
            if row[key] != planned[key]:
                raise ValueError('Plan and execution differ')
        raw = files[row['request_file']]
        if raw != encode(frozen.request(card, questions, policy)) or sha(raw) != row['request_sha256']:
            raise ValueError('Frozen request mismatch')
        for file_key, hash_key in [('http_request_file','http_request_sha256'),('response_file','response_sha256')]:
            if sha(files[row[file_key]]) != row[hash_key]:
                raise ValueError('Request/response hash mismatch')
        if json.loads(files[row['http_request_file']]) != json.loads(raw):
            raise ValueError('SDK altered request')
        response = files[row['response_file']]
        try:
            doc = frozen.validate_response(response, set(json.loads(raw)['questions']))
        except (ValueError, TypeError, KeyError):
            if row['status'] != 'invalid':
                raise ValueError('Invalid response not accounted for')
        else:
            if row['status'] != 'ok' or row['answers'] != doc['answers'] or row['resolved_model'] != doc['model']:
                raise ValueError('Valid response differs from run record')
    report = frozen.report(run['records'], cards, gold, pairs, policy, 'live')
    report.update(experiment_version=policy['version'],review_route=policy['review_route'],
                  interpretation='Synthetic evidence-v2 agreement only; not independent validation or real-world control evidence')
    if report != json.loads(files['report.json']) or report != json.loads((HERE/'report.json').read_bytes()):
        raise ValueError('Frozen analysis differs')
    original = json.loads(files['adjudications.json'])
    if original != frozen.adjudications(run['records'], gold, 'live-001'):
        raise ValueError('Adjudication inventory differs')
    adjudications = json.loads(files['adjudications-v2.json'])
    if len(adjudications) != len(original):
        raise ValueError('Adjudication migration coverage differs')
    for item, source in zip(adjudications, original):
        validate(item)
        if item['source']['record'] != source or item['source']['run_sha256'] != sha(files['run.json']):
            raise ValueError('Adjudication provenance differs')
    return files, run, report


if __name__ == '__main__':
    files, run, report = verify()
    print(json.dumps({'verified': True, 'requests': len(run['records']),
                      'statuses': report['request_status_counts'], 'archive_files':len(files)}))
