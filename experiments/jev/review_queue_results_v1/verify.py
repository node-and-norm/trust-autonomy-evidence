"""Verify the diagnostic pilot archive and its prospectively defined summary."""
import json
from pathlib import Path
import tarfile
import tempfile
from experiments.jev.run import sha
from experiments.jev.review_queue_v1.summarize import summarize

HERE=Path(__file__).resolve().parent


def verify():
    manifest=json.loads((HERE/'manifest.json').read_bytes())
    archive=HERE/'live-001.tar.gz'
    if sha(archive.read_bytes())!=manifest['archive_sha256']:raise ValueError('Archive changed')
    files={}
    with tarfile.open(archive,'r:gz') as tar:
        for m in tar.getmembers():
            if not m.isfile() or Path(m.name).name!=m.name or m.name in files:raise ValueError('Unsafe archive member')
            files[m.name]=tar.extractfile(m).read()
    if {k:sha(v) for k,v in files.items()}!=manifest['members_sha256']:raise ValueError('Archive members changed')
    with tempfile.TemporaryDirectory() as directory:
        path=Path(directory)
        for name,data in files.items():(path/name).write_bytes(data)
        result=summarize(path)
    if result!=json.loads((HERE/'summary.json').read_bytes()) or result!=json.loads(files['summary.json']):raise ValueError('Summary differs')
    return result


if __name__=='__main__':
    result=verify();print(json.dumps({'verified':True,'scheduled':result['scheduled'],'statuses':result['statuses']}))
