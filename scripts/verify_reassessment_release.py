#!/usr/bin/env python3
"""Verify the separately approved revision without changing historical inputs."""
import base64
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REVISION = ROOT / 'paper/revisions/2026-10-10'
ORIGINAL_SHA = '9ddfa8651d14e5a9f041ce906215e7fc8e3152bdd22d848a7270ea9d6e90ac76'
PDF_SHA = '881aa58249ec7ebfcd3fa8fcda493821d0ecc8b5e038c499d2044121b9120edb'
SOURCE_SHA = '7fa4a8344c10b00c810ffc86290a479f3c79b229947b1b7c799673598582a5cc'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify():
    entries = {}
    for line in (REVISION / 'SHA256SUMS.txt').read_text().splitlines():
        expected, name = line.split('  ', 1)
        relative = Path(name)
        require(not relative.is_absolute() and '..' not in relative.parts, 'unsafe manifest path')
        require(name not in entries, 'duplicate manifest path')
        path = REVISION / relative
        require(path.is_file() and not path.is_symlink(), 'missing artifact: ' + name)
        require(digest(path.read_bytes()) == expected, 'artifact hash mismatch: ' + name)
        entries[name] = expected
    actual = {str(p.relative_to(REVISION)) for p in REVISION.rglob('*')
              if p.is_file() and p != REVISION / 'SHA256SUMS.txt'}
    require(set(entries) == actual, 'revision manifest inventory differs')
    require(entries['preprint.pdf'] == PDF_SHA, 'approved PDF identity differs')
    require(entries['source.tar.gz'] == SOURCE_SHA, 'approved source identity differs')
    supplement = REVISION / 'supplement'
    encoded = supplement / 'Staged_Aggregation_Reproducibility_original.zip.b64'
    original = base64.b64decode(encoded.read_bytes().strip(), validate=True)
    require(digest(original) == ORIGINAL_SHA, 'historical archive identity differs')
    with zipfile.ZipFile(io.BytesIO(original)) as archive:
        for name in archive.namelist():
            target = supplement / name
            require(target.is_file() and target.read_bytes() == archive.read(name),
                    'extracted historical member differs: ' + name)
    with tarfile.open(REVISION / 'source.tar.gz') as archive:
        for member in archive.getmembers():
            require(member.isfile() and not Path(member.name).is_absolute()
                    and '..' not in Path(member.name).parts, 'unsafe source archive member')
            if member.name.startswith('anc/reproducibility_additional_public/'):
                name = member.name.split('anc/reproducibility_additional_public/', 1)[1]
                require(archive.extractfile(member).read() == (supplement / name).read_bytes(),
                        'source and standalone supplement differ: ' + name)
    forbidden = ('verbatim_text', 'Sentinel_', 'approval_message_id', 'approval_timestamp_utc',
                 '/Users/', 'chatgpt-conversation://', 'chatgpt.com/s/')
    for path in supplement.rglob('*'):
        if path.is_file():
            text = path.read_text(encoding='utf-8')
            require(not any(value in text for value in forbidden),
                    'private-provenance pattern in supplement: ' + path.name)
    commands = [
        ([sys.executable, '-B', 'check_additional_reassessment_public.py', '--verify-saved'], supplement),
        ([sys.executable, '-B', '-O', 'check_additional_reassessment_public.py', '--verify-saved'], supplement),
        ([sys.executable, '-B', 'check_staged_aggregation.py', '--verify-saved'], supplement / 'reproducibility'),
    ]
    for command, cwd in commands:
        subprocess.run(command, cwd=cwd, check=True)
    result = json.loads((supplement / 'results_public.json').read_text())
    calculation = result['calculations']
    require(calculation['additional_reassessment']['joint_assignment_count'] == 64, '64 assignments required')
    require(calculation['additional_reassessment']['possible_case_result_counts'] ==
            [{'Pass': 0, 'Fail': 0, 'Unresolved': 3}], 'conditional aggregate differs')
    require('unapproved' in calculation['stage_3'], 'broader amendments must remain unapproved')
    print('Approved October revision: PASS (%d hashed artifacts; private provenance absent from supplement)' % len(entries))


if __name__ == '__main__':
    verify()
