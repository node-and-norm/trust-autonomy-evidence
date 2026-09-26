"""Offline import and validation of append-only v2 adjudication records."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import json
from functools import lru_cache
from pathlib import Path
import sys

from jsonschema import Draft202012Validator, FormatChecker
from experiments.jev.run import ROOT, encode, sha
from experiments.jev.evidence_v1.run import verify as verify_experiment

HERE = Path(__file__).resolve().parent


def load(path):
    def reject(value):
        raise ValueError('nonfinite JSON number')
    return json.loads(Path(path).read_bytes(), parse_constant=reject)


def verify():
    verify_experiment()
    manifest = load(HERE/'AMENDMENT.json')
    for name, expected in manifest['sha256'].items():
        if sha((ROOT/name).read_bytes()) != expected:
            raise ValueError('adjudication amendment hash mismatch: '+name)


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None:
        raise ValueError('timestamp requires a timezone')
    return result


@lru_cache(maxsize=1)
def validator():
    return Draft202012Validator(load(HERE/'record.schema.json'), format_checker=FormatChecker())


def validate(record):
    validator().validate(record)
    source, current = record['source'], record['record']
    if source['record_sha256'] != sha(encode(source['record'])):
        raise ValueError('original adjudication record changed')
    for name in ('run_id','job_id','repetition','question_id','evidence_refs'):
        if source['record'][name] != current[name]:
            raise ValueError('source identity/evidence changed: '+name)
    if current['record_id'] == source['record']['record_id'] or not current['supersedes']:
        raise ValueError('v2 record must have a new ID and supersession link')
    if current['supersedes'] == current['record_id']:
        raise ValueError('self-supersession is invalid')
    dates = record['reviewer_dates']
    names = [d['identity'].strip().casefold() for d in dates]
    reviewers = [r['identity'].strip().casefold() for r in current['reviewers']]
    if any(not name for name in names + reviewers):
        raise ValueError('reviewer identities cannot be blank')
    if len(set(names)) != len(names) or len(set(reviewers)) != len(reviewers):
        raise ValueError('reviewer identities must be distinct')
    if set(names) != set(reviewers):
        raise ValueError('reviewer dates must match recorded reviewers')
    timestamp(record['created_at'])
    completed = timestamp(record['reviewed_at']) if record['reviewed_at'] else None
    for date in dates:
        blind = timestamp(date['blind_reviewed_at'])
        reconciled = timestamp(date['reconciled_at']) if date['reconciled_at'] else None
        if reconciled and reconciled < blind:
            raise ValueError('reconciliation precedes independent review')
        if completed and (not reconciled or reconciled > completed):
            raise ValueError('completion requires dated reconciliation')
    downstream = record['downstream']
    changes = downstream['changes']
    if downstream['status'] in ('not_assessed','no_change') and changes:
        raise ValueError('no-change/unassessed disposition cannot contain changes')
    if downstream['status'] != 'not_assessed' and not downstream['rationale'].strip():
        raise ValueError('downstream disposition requires rationale')
    if downstream['status'] in ('change_proposed','change_applied') and not changes:
        raise ValueError('downstream changes must be itemized')
    for change in changes:
        if downstream['status'] == 'change_proposed' and (change['changed_at'] or change['after_sha256']):
            raise ValueError('proposed change cannot claim completed action')
        if downstream['status'] == 'change_applied' and (not change['changed_at'] or not change['after_sha256']):
            raise ValueError('applied change requires timestamp and resulting artifact hash')
    if current['status'] == 'closed':
        if not current['rationale'].strip():
            raise ValueError('closed record requires substantive rationale')
        if completed is None or len(reviewers) != 2 or downstream['status'] == 'not_assessed':
            raise ValueError('closure requires two dated reviewers and an explicit downstream disposition')
    elif completed is not None:
        raise ValueError('open record cannot claim completed review')


class RunContext:
    """One read-only source snapshot per operation; never cache across operations."""
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.digest = sha(self.path.read_bytes())
        self.run = load(self.path)
        if self.run['mode'] not in ('mock', 'live'):
            raise ValueError('only observed mock/live attempts have adjudication records')
        self.rows = {}
        for row in self.run['records']:
            key = (row['job_id'], row['repetition'])
            if key in self.rows:
                raise ValueError('duplicate run request identity')
            self.rows[key] = row
        self.checked = {}

    def record(self, original):
        key = (original['job_id'], original['repetition'])
        row = self.rows.get(key)
        if row is None or row['status'] not in ('ok', 'invalid', 'error', 'interrupted'):
            raise ValueError('source run must identify exactly one attempted request')
        for file_key, hash_key in (('request_file', 'request_sha256'), ('response_file', 'response_sha256')):
            name, expected = row[file_key], row[hash_key]
            if name is None:
                if file_key == 'request_file' or expected is not None:
                    raise ValueError('inconsistent artifact reference')
                continue
            path = (self.path.parent/name).resolve()
            if Path(name).name != name or path.parent != self.path.parent:
                raise ValueError('source artifact must be directly inside the run directory')
            if name not in self.checked:
                self.checked[name] = path.read_bytes()
            if sha(self.checked[name]) != expected:
                raise ValueError('source artifact hash mismatch: '+name)
        request = json.loads(self.checked[row['request_file']])
        if original['question_id'] not in request['questions']:
            raise ValueError('question absent from original request')
        if row['request_file'] not in original['evidence_refs']:
            raise ValueError('evidence references must include original request file')
        return self.run, row


def verify_source(item, context):
    source = item['source']
    if context.digest != source['run_sha256']:
        raise ValueError('original run bytes changed')
    run, row = context.record(source['record'])
    if run['mode'] != source['run_mode']:
        raise ValueError('run mode differs')
    for name in ('request_file','request_sha256','response_file','response_sha256','resolved_model'):
        if row.get(name) != source[name]:
            raise ValueError('source run metadata differs: '+name)


def migrate(originals, run_path, created_at):
    timestamp(created_at)
    context = RunContext(run_path)
    ids = [r['record_id'] for r in originals]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate source record IDs')
    output = []
    for original in originals:
        run, row = context.record(original)
        current = copy.deepcopy(original)
        current.update(record_id=original['record_id']+'.v2.1',supersedes=original['record_id'],
            status='open',disposition='UNRESOLVED',reviewers=[],rationale='')
        # Preserve any prior decision verbatim in source.record. Missing review dates
        # and downstream effects are never guessed, even for closed legacy records.
        item = {'schema_version':'jev-tae-adjudication-v2',
            'source':{'record':copy.deepcopy(original),'record_sha256':sha(encode(original)),
                'run_sha256':context.digest,'run_mode':run['mode'],
                **{name:row.get(name) for name in ('request_file','request_sha256','response_file','response_sha256','resolved_model')}},
            'record':current,'created_at':created_at,'reviewed_at':None,'reviewer_dates':[],
            'downstream':{'status':'not_assessed','rationale':'','changes':[]}}
        validate(item)
        output.append(item)
    return output


def validate_all(items, run_path):
    context = RunContext(run_path)
    ids = [r['record']['record_id'] for r in items]
    if len(ids) != len(set(ids)):
        raise ValueError('duplicate v2 record IDs')
    by_id = dict(zip(ids,items))
    for item in items:
        validate(item)
        verify_source(item,context)
        previous = item['record']['supersedes']
        visited = {item['record']['record_id']}
        while previous in by_id:
            if previous in visited:
                raise ValueError('cyclic supersession')
            visited.add(previous)
            ancestor=by_id[previous]
            if ancestor['source']['record_sha256'] != item['source']['record_sha256']:
                raise ValueError('supersession crosses source records')
            if timestamp(ancestor['created_at']) > timestamp(item['created_at']):
                raise ValueError('supersession predates ancestor creation')
            previous=ancestor['record']['supersedes']
        if previous != item['source']['record']['record_id']:
            raise ValueError('supersession chain must reach the original source record')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('migrate','validate'))
    parser.add_argument('--input',type=Path,required=True)
    parser.add_argument('--run',type=Path,required=True)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--created-at',help='Actual import timestamp; defaults to current UTC time')
    args=parser.parse_args()
    verify()
    items=load(args.input)
    if args.action=='migrate':
        if args.output is None:
            parser.error('migrate requires a new output file')
        output=args.output.resolve()
        if ROOT==output or ROOT in output.parents:
            parser.error('output must be outside the repository to protect frozen inputs')
        items=migrate(items,args.run.resolve(),args.created_at or datetime.now(timezone.utc).isoformat())
        validate_all(items,args.run.resolve())
        with output.open('x') as stream:
            stream.write(encode(items).decode())
    else:
        validate_all(items,args.run.resolve())
    print(json.dumps({'action':args.action,'records':len(items),'status':'PASS',
        'boundary':'Record integrity only; no human review performed or inferred.'}))


if __name__=='__main__':
    main()
