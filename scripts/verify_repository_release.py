"""Check the complete v0.17.1 Git snapshot without freezing future working files."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ROOT=Path(__file__).resolve().parents[1]
MANIFEST='release/v0.17.1-manifest.json'


def check(archive):
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:') as tar:
        files={m.name:tar.extractfile(m).read() for m in tar.getmembers() if m.isfile()}
        if any(not (m.isfile() or m.isdir()) for m in tar.getmembers()):
            raise ValueError('unsupported non-regular Git snapshot entry')
    manifest=json.loads(files.pop(MANIFEST))
    if manifest['version']!='0.17.1' or manifest['paper_version']!='0.17.0':
        raise ValueError('unexpected version boundary')
    if set(files)!=set(manifest['files']):raise ValueError('snapshot inventory differs')
    for name,data in files.items():
        entry=manifest['files'][name]
        if len(data)!=entry['bytes'] or hashlib.sha256(data).hexdigest()!=entry['sha256']:
            raise ValueError('snapshot hash mismatch: '+name)
    return len(files)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref',default='v0.17.1');args=parser.parse_args()
    commit=subprocess.check_output(['git','rev-parse','--verify',args.ref+'^{commit}'],cwd=ROOT,text=True).strip()
    archive=subprocess.check_output(['git','archive','--format=tar',commit],cwd=ROOT)
    count=check(archive)
    print(f'Repository release snapshot: PASS (v0.17.1; {count} files; commit {commit})')

if __name__=='__main__':main()
