"""Additive transport bridge for frozen evidence-v2; no corpus modification."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from experiments.jev.adapter import MockAdapter, validate_response
from experiments.jev.evidence_v2 import run as frozen
from experiments.jev.run import ROOT, encode, load, sha

HERE = Path(__file__).resolve().parent


def now():
    return datetime.now(timezone.utc).isoformat()


def verify():
    frozen.verify()
    manifest = HERE / 'BRIDGE.json'
    if manifest.read_bytes() != subprocess.check_output(
            ['git', 'show', 'HEAD:'+manifest.relative_to(ROOT).as_posix()], cwd=ROOT):
        raise ValueError('Bridge manifest is not committed')
    for name, digest in load(manifest)['sha256'].items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise ValueError('Bridge hash mismatch: '+name)


def new_output(output):
    output = Path(output).resolve()
    runs = HERE/'runs'
    if runs.resolve() != runs or runs not in output.parents:
        raise ValueError('Output must be a new directory within live_v1/runs')
    output.mkdir(parents=True, exist_ok=False)
    return output


def save(path, value):
    temp = path.with_suffix(path.suffix+'.tmp')
    temp.write_bytes(encode(value))
    temp.replace(path)


def run(mode, output, *, adapter=None):
    if mode not in ('dry-run', 'mock', 'live'):
        raise ValueError('Unknown mode')
    verify()
    cards, gold, questions, pairs, policy = frozen.materials()
    # Initialize optional SDK before making an output directory; no network call here.
    if mode == 'live' and adapter is None:
        from .transport import Transport
        adapter = Transport()
    try:
        output = new_output(output)
        meta = {'mode': mode, 'status': 'running', 'started_at': now(),
                'experiment_version': policy['version'], 'review_route': policy['review_route'],
                'bridge_version': 'jev-live-v1', 'requested_model': policy['requested_model'],
                'sdk_version': getattr(adapter, 'sdk_version', None),
                'git_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                'freeze_sha256': sha((frozen.HERE/'freeze.json').read_bytes()),
                'bridge_sha256': sha((HERE/'BRIDGE.json').read_bytes()), 'records': []}
        for rep in range(1, policy['repetitions']+1):
            for card in cards:
                name = f"{card['id']}-r{rep}.request.json"
                wire = encode(frozen.request(card, questions, policy))
                (output/name).write_bytes(wire)
                meta['records'].append({'job_id': card['id'], 'suite': card['suite'],
                    'repetition': rep, 'request_file': name, 'request_sha256': sha(wire),
                    'response_file': None, 'response_sha256': None, 'resolved_model': None,
                    'status': 'planned'})
        # Immutable initial schedule preserves the denominator even after abrupt termination.
        (output/'schedule.json').write_bytes(encode(meta))
        save(output/'run.json', meta)
        try:
            if mode != 'dry-run':
                for row in meta['records']:
                    body = (output/row['request_file']).read_bytes()
                    if sha(body) != row['request_sha256']:
                        raise ValueError('Planned request changed')
                    payload = json.loads(body)
                    row.update(status='interrupted', started_at=now())
                    save(output/'run.json', meta)

                    def capture(raw_request):
                        name = row['request_file'].replace('.request.json', '.http-request.json')
                        (output/name).write_bytes(raw_request)
                        row.update(http_request_file=name, http_request_sha256=sha(raw_request))
                        save(output/'run.json', meta)

                    raw = None
                    try:
                        if mode == 'mock':
                            raw = MockAdapter().evaluate(**payload)
                        else:
                            raw = adapter.evaluate(payload, capture)
                    except (KeyboardInterrupt, SystemExit):
                        if adapter and adapter.last_raw is not None:
                            raw = adapter.last_raw
                        raise
                    except Exception as exc:
                        row.update(status='error', error_type=type(exc).__name__)
                        raw = getattr(adapter, 'last_raw', None)
                    else:
                        row['status'] = 'received'
                    finally:
                        row['finished_at'] = now()
                        if adapter:
                            row.update(http_status=adapter.last_http_status, request_id=adapter.last_request_id)
                        if raw is not None:
                            name = row['request_file'].replace('.request.json', '.response.json')
                            (output/name).write_bytes(raw)
                            row.update(response_file=name, response_sha256=sha(raw))
                        save(output/'run.json', meta)
                    if raw is not None:
                        try:
                            parsed = json.loads(raw)
                            if isinstance(parsed, dict) and isinstance(parsed.get('model'), str) and parsed['model'].strip():
                                row['resolved_model'] = parsed['model']
                            doc = validate_response(raw, set(payload['questions']))
                        except (ValueError, TypeError, KeyError):
                            if row['status'] == 'received' or row.get('http_status') == 200:
                                row['status'] = 'invalid'
                        else:
                            if row['status'] == 'received':
                                row.update(status='ok', resolved_model=doc['model'], answers=doc['answers'])
                    save(output/'run.json', meta)
            meta['status'] = 'dry-run' if mode == 'dry-run' else (
                'complete' if all(r['status'] == 'ok' for r in meta['records']) else 'incomplete')
        except BaseException:
            meta['status'] = 'interrupted'
            raise
        finally:
            meta['finished_at'] = now()
            save(output/'run.json', meta)
            result = frozen.report(meta['records'], cards, gold, pairs, policy, mode)
            result.update(experiment_version=policy['version'], review_route=policy['review_route'])
            if mode == 'live':
                result['interpretation'] = 'Synthetic evidence-v2 agreement only; not independent validation or real-world control evidence'
            save(output/'report.json', result)
            save(output/'adjudications.json', frozen.adjudications(meta['records'], gold, output.name))
        return meta
    finally:
        if adapter:
            adapter.close()


def preflight(output):
    verify()
    from .transport import Transport
    adapter = Transport()
    try:
        output = new_output(output)
        record = {'kind': 'authentication_only', 'started_at': now(), 'inference_calls': 0,
                  'requested_model': 'jev-1.13.0', 'sdk_version': adapter.sdk_version}
        try:
            record.update(models=adapter.preflight(), status='authenticated')
        except Exception as exc:
            record.update(status='failed', error_type=type(exc).__name__)
        record.update(finished_at=now(), http_status=adapter.last_http_status)
        save(output/'preflight.json', record)
        return record
    finally:
        adapter.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('dry-run', 'mock', 'preflight', 'live'), default='dry-run')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--execute-frozen-schedule', action='store_true')
    args = parser.parse_args()
    if args.mode == 'live' and not args.execute_frozen_schedule:
        parser.error('Live inference requires --execute-frozen-schedule (282 requests)')
    result = preflight(args.output) if args.mode == 'preflight' else run(args.mode, args.output)
    print(json.dumps({'mode': args.mode, 'status': result['status']}))
    return 0 if result['status'] in ('dry-run', 'complete', 'authenticated') else 2


if __name__ == '__main__':
    raise SystemExit(main())
