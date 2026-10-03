import hashlib
import io
import json
import tarfile
import unittest

from scripts.verify_repository_release import check


def snapshot(version, mutate=None):
    files={'example.txt': b'preserved evidence'}
    manifest={'version':version,'paper_version':'0.17.0','files':{
        name:{'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()}
        for name,value in files.items()}}
    files[f'release/v{version}-manifest.json']=json.dumps(manifest).encode()
    if mutate:mutate(files)
    buffer=io.BytesIO()
    with tarfile.open(fileobj=buffer,mode='w') as tar:
        for name,data in files.items():
            info=tarfile.TarInfo(name);info.size=len(data);tar.addfile(info,io.BytesIO(data))
    return buffer.getvalue()


class SnapshotTests(unittest.TestCase):
    def test_both_repository_versions(self):
        for version in ('0.17.1','0.17.2'):
            self.assertEqual(check(snapshot(version)),1)

    def test_changed_missing_and_extra_files_rejected(self):
        mutations=[lambda f:f.update({'example.txt':b'altered'}),
                   lambda f:f.pop('example.txt'),lambda f:f.update({'extra':b'new'})]
        for mutate in mutations:
            with self.assertRaises(ValueError):check(snapshot('0.17.2',mutate))
