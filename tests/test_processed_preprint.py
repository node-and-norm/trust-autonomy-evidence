"""Ensure official processed copy and retained local compile remain distinct."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class ProcessedPreprintTests(unittest.TestCase):
    def test_processed_and_local_provenance(self):
        root = ROOT / 'paper/revisions/2026-11-08'
        record = json.loads((root / 'ARXIV_PROCESSED_PROVENANCE.json').read_text())
        self.assertEqual(hashlib.sha256((root / record['artifact']).read_bytes()).hexdigest(), record['sha256'])
        local = record['preserved_local_compile']
        self.assertEqual(hashlib.sha256((root / local['path']).read_bytes()).hexdigest(), local['sha256'])
        self.assertNotEqual(record['sha256'], local['sha256'])
        self.assertEqual(record['watermark'], 'arXiv:submit/7973196 [cs.HC] 8 Nov 2026')
        self.assertIn('Declined', record['status'])
        self.assertIn('not publicly announced', record['status'])
        self.assertIn('on hold', record['processing_status_at_retrieval'])

    def test_revision_checksums(self):
        root = ROOT / 'paper/revisions/2026-11-08'
        for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
            if not line: continue
            digest, name = line.split('  ', 1)
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest, name)

if __name__ == '__main__':
    unittest.main()
