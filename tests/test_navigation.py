"""Regression checks for a narrow current-navigation/historical-release boundary."""
import copy
import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import validate_repository as validator

ROOT=Path(__file__).resolve().parents[1]

class NavigationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        self.manifest=json.loads((ROOT/'release/v0.17.0-manifest.json').read_text())
        paths=[a['path'] for a in self.manifest['artifacts']]+['release/v0.17.0-manifest.json','docs/navigation-v0.17.0.json']
        for name in paths:
            target=self.root/name
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,target)

    def tearDown(self):
        self.temp.cleanup()

    def check(self):
        failures=[]
        with patch.object(validator,'ROOT',self.root):
            validator.validate_release_candidate(failures)
        return failures

    def edit_checkpoint(self,fn):
        path=self.root/'docs/navigation-v0.17.0.json'
        doc=json.loads(path.read_text());fn(doc)
        path.write_text(json.dumps(doc))

    def test_valid_navigation(self):
        self.assertEqual(self.check(),[])

    def test_unrecorded_navigation_change(self):
        path=self.root/'README.md';path.write_text(path.read_text()+'\nchanged')
        self.assertTrue(any('README.md' in e for e in self.check()))

    def test_missing_checkpoint(self):
        (self.root/'docs/navigation-v0.17.0.json').unlink()
        self.assertTrue(self.check())

    def test_cannot_expand_scope(self):
        self.edit_checkpoint(lambda d:d['artifacts'].update({'paper/preprints/main.tex':copy.deepcopy(d['artifacts']['README.md'])}))
        self.assertTrue(self.check())

    def test_wrong_release_baseline(self):
        self.edit_checkpoint(lambda d:d['artifacts']['README.md'].update(released_sha256='0'*64))
        self.assertTrue(self.check())

    def test_research_change_rejected(self):
        path=self.root/'paper/preprints/main.tex';path.write_text(path.read_text()+'\nchanged')
        self.assertTrue(any('paper/preprints/main.tex' in e for e in self.check()))

    def test_manifest_and_release_assets_unchanged(self):
        name='release/v0.17.0-manifest.json'
        tagged=subprocess.check_output(['git','show','v0.17.0:'+name],cwd=ROOT)
        self.assertEqual((ROOT/name).read_bytes(),tagged)
        for artifact in self.manifest['artifacts']:
            if artifact['path'] not in {'README.md','CITATION.cff','RESEARCH_STATUS.md'}:
                self.assertEqual(hashlib.sha256((ROOT/artifact['path']).read_bytes()).hexdigest(),artifact['sha256'])

if __name__=='__main__':
    unittest.main()
