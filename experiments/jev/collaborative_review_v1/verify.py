"""Credential-free integrity checks for the separate collaborative review."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def verify(directory=HERE):
    directory = Path(directory)
    manifest = json.loads((directory / 'manifest.json').read_bytes())
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    expected = {'README.md', 'review.json'} | {f'records/item-{i:02}.json' for i in range(1, 25)}
    if set(manifest['files']) != expected:
        raise ValueError('Unexpected preserved file inventory')
    for name, checksum in manifest['files'].items():
        if digest(directory / name) != checksum:
            raise ValueError(f'Changed preserved file: {name}')
    cohort_path = ROOT / 'experiments/jev/review_queue_v1/cohort.json'
    if manifest['cohort_path'] != str(cohort_path.relative_to(ROOT)) or digest(cohort_path) != manifest['cohort_sha256']:
        raise ValueError('Source cohort changed')
    cohort = json.loads(cohort_path.read_bytes())
    bundle = json.loads((directory / 'review.json').read_bytes())
    if bundle['approved_items'] != 24 or len(bundle['records']) != 24 or len(cohort['units']) != 24:
        raise ValueError('Incomplete review')
    if bundle['unresolved_classification_items'] != [8, 16]:
        raise ValueError('Unresolved classifications changed')
    if bundle['human_time_savings'] is not None or bundle['quality_improvement'] is not None:
        raise ValueError('Unmeasured benefits must remain null')
    if set(bundle['record_sha256']) != {f'item-{i:02}.json' for i in range(1, 25)}:
        raise ValueError('Unexpected record hash inventory')
    for i, (unit, record) in enumerate(zip(cohort['units'], bundle['records']), 1):
        path = directory / f'records/item-{i:02}.json'
        if json.loads(path.read_bytes()) != record or digest(path) != bundle['record_sha256'][path.name]:
            raise ValueError('Individual and consolidated records differ')
        for key in ('source_request_sha256', 'source_response_sha256'):
            if record[key] != unit[key]:
                raise ValueError('Source hash mismatch')
        if record['unit_id'] != unit['id'] or record['human_approval'] != 'approved':
            raise ValueError('Identity or approval mismatch')
        if not record['approval_evidence']['text'] or not record['approval_evidence']['scope']:
            raise ValueError('Missing approval record')
        if record['human_active_seconds'] is not None or record['eligible_for_unassisted_time_comparison'] is not False:
            raise ValueError('Invalid baseline or timing claim')
        if i in (8, 16) and record['assessment']['conclusion'] is not None:
            raise ValueError('Unresolved classification was assigned')
    return {'verified': True, 'approved_records': 24, 'unresolved_classification_items': [8, 16],
            'human_time_savings': None, 'quality_improvement': None}


if __name__ == '__main__':
    print(json.dumps(verify()))
