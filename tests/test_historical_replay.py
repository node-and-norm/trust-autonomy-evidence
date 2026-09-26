import hashlib
import io
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from scripts.replay_historical_audit import ROOT, REPLAYS, extract_snapshot, replay


class HistoricalReplayTests(unittest.TestCase):
    def test_complete_license_and_attribution(self):
        self.assertEqual(hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest(),
                         'cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30')
        self.assertIn('Copyright 2026 Mark Julius Banasihan',(ROOT/'NOTICE').read_text())

    def test_replay_ignores_current_working_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            clone=Path(temp)/'repo'
            subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(clone)],check=True,capture_output=True)
            poisoned=['scripts/run_coe_integrity_audit.py','scripts/run_policy_integrity_audit_v0_17_0.py',
                      'evidence/claim-evidence-map.json','README.md','paper/manuscript.md']
            for name in poisoned:
                path=clone/name;path.parent.mkdir(parents=True,exist_ok=True)
                path.write_text('deliberately different from historical release\n')
            for tag in REPLAYS:
                with self.subTest(tag=tag):
                    output=Path(temp)/tag
                    result=replay(tag,output,clone)
                    self.assertEqual(result['status'],'PASS')
                    self.assertTrue(all(x['identical'] for x in result['comparisons'].values()))
                    with self.assertRaises(FileExistsError):
                        replay(tag,output,clone)
            for name in poisoned:
                self.assertEqual((clone/name).read_text(),'deliberately different from historical release\n')

    def test_moved_tag_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            clone=Path(temp)/'repo'
            subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(clone)],check=True,capture_output=True)
            subprocess.run(['git','update-ref','refs/tags/v0.16.0','HEAD'],cwd=clone,check=True)
            with self.assertRaisesRegex(ValueError,'pinned commit'):
                replay('v0.16.0',repo=clone)

    def test_unsafe_archive_entries_rejected(self):
        for name,kind in [('../escape',tarfile.REGTYPE),('/absolute',tarfile.REGTYPE),('link',tarfile.SYMTYPE)]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as temp:
                data=io.BytesIO()
                with tarfile.open(fileobj=data,mode='w') as tar:
                    entry=tarfile.TarInfo(name);entry.type=kind;entry.linkname='../escape'
                    tar.addfile(entry)
                with self.assertRaises(ValueError):
                    extract_snapshot(data.getvalue(),Path(temp))

    def test_output_cannot_overwrite_repository(self):
        with self.assertRaises(ValueError):
            replay('v0.16.0',ROOT/'audits/new-output')


if __name__=='__main__':
    unittest.main()
