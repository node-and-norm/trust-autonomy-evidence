"""Opt-in synthetic experiment; writes only to a new experiment run directory."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from .adapter import DEFAULT_MODEL, LABELS, JevAdapter, MockAdapter, validate_response

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encode(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def load(path):
    return json.loads(path.read_bytes())


def now():
    return datetime.now(timezone.utc).isoformat()


def materials():
    frozen = load(HERE / 'frozen-v1.json')
    for name, digest in frozen['sha256'].items():
        if sha((HERE / name).read_bytes()) != digest:
            raise ValueError('frozen experiment question set changed')
    manifest = load(ROOT / 'oracles/manifest.json')
    for name, digest in manifest['sha256'].items():
        if sha((ROOT / name).read_bytes()) != digest:
            raise ValueError('sealed TAE artifact changed: ' + name)
    cases = load(ROOT / 'fixtures/synthetic/cases.json')['cases']
    oracle = load(ROOT / 'oracles/solo-validation-v0.2.0.json')['expected']
    questions = load(HERE / 'questions-v1.json')['questions']
    ids = [c['case_id'] for c in cases]
    if len(ids) != 12 or len(set(ids)) != 12 or set(ids) != set(oracle):
        raise ValueError('unexpected case/oracle inventory')
    for case in cases:
        expected = {(g, f) for g in ('trust', 'control') for f in oracle[case['case_id']][g]}
        mapped = {(q['assessment'], q['field']) for q in questions.values()}
        if len(questions) != 21 or mapped != expected:
            raise ValueError('mapping does not cover the 21 determinations')
        for q in questions.values():
            group, field = q['source_path'].split('.')
            if field not in case[group]:
                raise ValueError('missing source signal')
    mutations = load(ROOT / 'fixtures/mutations/mutations.json')['mutations']
    return cases, oracle, questions, mutations, manifest


def normalized(case):
    # Exclude label-bearing title/purpose and case identity. Keep declared nuisance
    # variables so outcome and impact-radius invariance remain nontrivial tests.
    return {k: copy.deepcopy(case[k]) for k in
            ('trust_signals', 'control_signals', 'context', 'autonomy')}


def jobs(cases, oracle, mutations, include_mutations):
    result = [(c['case_id'], c, oracle[c['case_id']], None) for c in cases]
    by_id = {c['case_id']: c for c in cases}
    if include_mutations:
        for mutation in mutations:
            case = copy.deepcopy(by_id[mutation['base_case_id']])
            expected = copy.deepcopy(oracle[mutation['base_case_id']])
            for change in mutation['changes']:
                path = change['path'].split('.')
                target = case
                for part in path[:-1]:
                    target = target[part]
                target[path[-1]] = change['value']
            for delta in mutation['expected_deltas']:
                if expected[delta['assessment']][delta['field']] != delta['from']:
                    raise ValueError('mutation starting label differs from oracle')
                expected[delta['assessment']][delta['field']] = delta['to']
            result.append((mutation['mutation_id'], case, expected, mutation))
    return result


def comparison_rows(doc, expected, questions, job_id, kind):
    rows = []
    for qid, q in questions.items():
        answer = doc['answers'][qid]
        truth = expected[q['assessment']][q['field']]
        probs = answer['probabilities']
        rows.append({'job_id': job_id, 'kind': kind, 'question_id': qid,
            'oracle': truth, 'choice': answer['choice'], 'agreement': answer['choice'] == truth,
            'probabilities': probs, 'confidence': answer['confidence'],
            'entropy_bits': -sum(p * math.log2(p) for p in probs.values() if p),
            'review_required': answer['confidence'] < 0.8 or answer['choice'] != truth,
            'brier_multiclass': sum((probs[l] - int(l == truth)) ** 2 for l in LABELS),
            'oracle_probability': probs[truth]})
    return rows


def mutation_comparisons(records, mutations, questions):
    by_id = {r['job_id']: r for r in records}
    results = []
    for m in mutations:
        before, after = by_id.get(m['base_case_id']), by_id.get(m['mutation_id'])
        item = {'mutation_id': m['mutation_id'], 'base_case_id': m['base_case_id'],
                'expected_deltas': m['expected_deltas'], 'status': 'not_evaluated'}
        if before and after and before['status'] == after['status'] == 'ok':
            b = {r['question_id']: r for r in before['rows']}
            a = {r['question_id']: r for r in after['rows']}
            actual = [{'assessment': q['assessment'], 'field': q['field'],
                       'from': b[qid]['choice'], 'to': a[qid]['choice']}
                      for qid, q in questions.items() if b[qid]['choice'] != a[qid]['choice']]
            key = lambda d: (d['assessment'], d['field'])
            item.update(status='evaluated', observed_deltas=actual,
                exact_delta_match=sorted(actual, key=key) == sorted(m['expected_deltas'], key=key),
                max_probability_shift=max(abs(a[q]['probabilities'][l] - b[q]['probabilities'][l])
                                          for q in a for l in LABELS),
                input_identical=before['state_sha256'] == after['state_sha256'])
        results.append(item)
    return results


def run(mode, output, model=DEFAULT_MODEL, include_mutations=False, adapter=None):
    if mode not in ('dry-run', 'mock', 'live'):
        raise ValueError('invalid run mode')
    cases, oracle, questions, mutations, seal = materials()
    output = Path(output).resolve()
    # Restrict writes to this namespace, and prohibit overwriting an existing run.
    if HERE / 'runs' not in output.parents:
        raise ValueError('output must be a new directory under experiments/jev/')
    output.mkdir(parents=True, exist_ok=False)
    wire_questions = {qid: q['question'] for qid, q in questions.items()}
    plan = jobs(cases, oracle, mutations, include_mutations)
    meta = {'schema_version': 'jev-tae-run-v1', 'mode': mode, 'status': 'running',
        'started_at': now(), 'finished_at': None, 'requested_model': model,
        'resolved_models': [], 'sdk_version': None, 'python_version': platform.python_version(),
        'question_set_sha256': sha((HERE / 'questions-v1.json').read_bytes()),
        'sealed_artifacts': seal['sha256'], 'planned_cases': 12,
        'planned_base_determinations': 252, 'planned_requests': len(plan),
        'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'git_dirty': bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip()),
        'implementation_sha256': {p.name: sha(p.read_bytes()) for p in (HERE/'run.py', HERE/'adapter.py')},
        'records': [], 'mutation_results': []}
    (output / 'questions.json').write_bytes(encode(wire_questions))
    def save():
        (output / 'run.json').write_bytes(encode(meta))
    save()
    try:
        if mode == 'live' and adapter is None:
            try:
                adapter = JevAdapter()
            except Exception as exc:
                meta.update(status='blocked', reason=('missing TYPESAFE_API_KEY' if
                    str(exc) == 'missing TYPESAFE_API_KEY' else 'SDK setup failed: ' + type(exc).__name__))
                return meta
        if mode == 'mock' and adapter is None:
            adapter = MockAdapter()
        meta['sdk_version'] = getattr(adapter, 'sdk_version', None)
        for job_id, case, expected, mutation in plan:
            state = normalized(case)
            request = {'model': model, 'state': state, 'questions': wire_questions}
            request_bytes = encode(request)
            (output / (job_id + '.request.json')).write_bytes(request_bytes)
            record = {'job_id': job_id, 'kind': 'mutation' if mutation else 'base',
                'status': 'planned', 'started_at': now(), 'finished_at': None,
                'request_sha256': sha(request_bytes), 'state_sha256': sha(encode(state)),
                'fixture_sha256': sha(encode(case)), 'response_sha256': None,
                'resolved_model': None, 'rows': []}
            meta['records'].append(record)
            if mode != 'dry-run':
                try:
                    raw = adapter.evaluate(state, wire_questions, model)
                    (output / (job_id + '.response.json')).write_bytes(raw)
                    record['response_sha256'] = sha(raw)
                    doc = validate_response(raw, set(questions))
                    record.update(status='ok', resolved_model=doc['model'], usage=doc.get('usage'),
                        rows=comparison_rows(doc, expected, questions, job_id, record['kind']))
                except Exception as exc:
                    # Avoid persisting exception text, which can contain credentials.
                    record.update(status='error', error_type=type(exc).__name__)
                    raw = getattr(adapter, 'last_raw', None)
                    if raw is not None:
                        (output / (job_id + '.response.json')).write_bytes(raw)
                        record['response_sha256'] = sha(raw)
                record['http_status'] = getattr(adapter, 'last_http_status', None)
                record['request_id'] = getattr(adapter, 'last_request_id', None)
            record['finished_at'] = now()
            save()
        meta['resolved_models'] = sorted({r['resolved_model'] for r in meta['records'] if r['resolved_model']})
        meta['mutation_results'] = mutation_comparisons(meta['records'], mutations, questions) if include_mutations else []
        rows = [row for r in meta['records'] for row in r['rows']]
        with (output/'comparisons.jsonl').open('wb') as stream:
            for row in rows:
                stream.write(json.dumps(row, sort_keys=True, allow_nan=False).encode()+b'\n')
        (output/'disagreements.json').write_bytes(encode([r for r in rows if not r['agreement']]))
        base = [r for r in rows if r['kind'] == 'base']
        meta['summary'] = {'evaluated_base_determinations': len(base),
            'base_agreements': sum(r['agreement'] for r in base),
            'base_brier_mean': sum(r['brier_multiclass'] for r in base)/len(base) if base else None,
            'errors': sum(r['status'] == 'error' for r in meta['records'])}
        meta['status'] = 'dry-run' if mode == 'dry-run' else ('incomplete' if meta['summary']['errors'] else 'complete')
        return meta
    except BaseException:
        meta['status'] = 'interrupted'
        raise
    finally:
        meta['finished_at'] = now()
        save()
        if adapter:
            adapter.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=['dry-run', 'mock', 'live'], default='dry-run')
    parser.add_argument('--model', default=DEFAULT_MODEL)
    parser.add_argument('--mutations', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.mode, args.output, args.model, args.mutations)
    print(json.dumps({k: result[k] for k in ('mode', 'status', 'planned_requests')}))
    return 2 if result['status'] in ('blocked', 'incomplete') else 0


if __name__ == '__main__':
    sys.exit(main())
