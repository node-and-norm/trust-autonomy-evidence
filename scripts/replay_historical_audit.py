#!/usr/bin/env python3
"""Replay a pinned release's audit in a disposable snapshot, comparing exact bytes."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REPLAYS = {
    'v0.16.0': {
        'commit': '054a7a8eea16454d053752633d71478b7161879c',
        'script': 'scripts/run_coe_integrity_audit.py',
        'outputs': ['audits/v0.16.0/audit-results.json', 'audits/v0.16.0/audit-report.md'],
    },
    'v0.17.0': {
        'commit': '781f7806a626cd4e4fffbe4d453d9d5365b835f9',
        'script': 'scripts/run_policy_integrity_audit_v0_17_0.py',
        'outputs': ['audits/v0.17.0-policy-crosswalk/audit-results.json',
                    'audits/v0.17.0-policy-crosswalk/audit-report.md'],
    },
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def extract_snapshot(archive: bytes, directory: Path) -> None:
    # No symlinks, hardlinks, device entries, absolute paths or parent traversal.
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as stream:
        for member in stream.getmembers():
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or '..' in relative.parts or '\\' in member.name:
                raise ValueError('unsafe snapshot path')
            target = directory.joinpath(*relative.parts)
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with stream.extractfile(member) as source:
                    target.write_bytes(source.read())
            else:
                raise ValueError('snapshot contains a non-regular entry')


def replay(tag: str, output: Path | None = None, repo: Path = ROOT) -> dict:
    specification = REPLAYS[tag]
    resolved = subprocess.check_output(
        ['git', 'rev-parse', '--verify', tag+'^{commit}'], cwd=repo, text=True).strip()
    if resolved != specification['commit']:
        raise ValueError('release tag differs from the reviewed pinned commit')
    if output is not None:
        output = output.resolve()
        if output == repo.resolve() or repo.resolve() in output.parents:
            raise ValueError('replay output must be outside the repository')
        output.mkdir(parents=True, exist_ok=False)
    archive = subprocess.check_output(['git', 'archive', '--format=tar', resolved], cwd=repo)
    with tempfile.TemporaryDirectory(prefix='tae-audit-replay-') as temporary:
        snapshot = Path(temporary)
        extract_snapshot(archive, snapshot)
        expected = {name: (snapshot/name).read_bytes() for name in specification['outputs']}
        # Execute only the reviewed script from the pinned snapshot. Ignore inherited
        # Python paths and forbid socket connections in the audit process.
        bootstrap = '''import runpy, socket, sys
from pathlib import Path
def offline(*args, **kwargs):
    raise RuntimeError("historical audit attempted network access")
socket.socket.connect = offline
socket.socket.connect_ex = offline
socket.create_connection = offline
script = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(script.parent))
sys.argv = [str(script)]
runpy.run_path(str(script), run_name="__main__")
'''
        process = subprocess.run(
            [sys.executable, '-B', '-E', '-c', bootstrap, specification['script']],
            cwd=snapshot, text=True, capture_output=True, timeout=120)
        actual = {name: (snapshot/name).read_bytes() for name in expected}
        comparisons = {name: {'expected_sha256': sha(expected[name]),
            'replayed_sha256': sha(actual[name]), 'identical': actual[name] == expected[name]}
            for name in expected}
        passed = process.returncode == 0 and all(row['identical'] for row in comparisons.values())
        result = {'status': 'PASS' if passed else 'FAIL', 'release_tag': tag,
            'resolved_commit': resolved, 'python_version': sys.version.split()[0],
            'script_sha256': sha((snapshot/specification['script']).read_bytes()),
            'exit_code': process.returncode, 'comparisons': comparisons,
            'audit_stdout': process.stdout.strip(), 'audit_stderr': process.stderr.strip(),
            'boundary': 'Exact historical replay; no new source-truth or independent-validity finding.'}
        if output is not None:
            (output/'replay.json').write_text(json.dumps(result, indent=2)+'\n')
            for label, data in (('expected', expected), ('replayed', actual)):
                for name, payload in data.items():
                    destination = output/label/Path(name).name
                    destination.parent.mkdir(exist_ok=True)
                    destination.write_bytes(payload)
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag', choices=REPLAYS, required=True)
    parser.add_argument('--output', type=Path, help='New directory outside the repository; never overwritten')
    args = parser.parse_args()
    try:
        result = replay(args.tag, args.output)
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        parser.exit(2, f'historical audit replay could not run: {error}\n')
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'PASS' else 1


if __name__ == '__main__':
    raise SystemExit(main())
