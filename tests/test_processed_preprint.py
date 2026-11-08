"""Verify the current unstamped compilation and historical provenance boundary."""
import hashlib
import json
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class ProcessedPreprintTests(unittest.TestCase):
    def test_processed_and_local_provenance(self):
        root = ROOT / 'paper/revisions/2026-11-08'
        current = json.loads((root / 'CURRENT_PDF_PROVENANCE.json').read_text())
        self.assertEqual(hashlib.sha256((root / current['artifact']).read_bytes()).hexdigest(), current['sha256'])
        self.assertEqual((root / current['artifact']).read_bytes(), (root / current['source_path']).read_bytes())
        self.assertIsNone(current['watermark'])
        record = json.loads((root / 'ARXIV_PROCESSED_PROVENANCE.json').read_text())
        self.assertIn('Historical retrieval checkpoint', record['record_scope'])
        self.assertEqual(record['repository_checkpoint'], '9ae31f00a9845b447be2e1c42844ab944a80cccb')
        self.assertNotEqual(record['sha256'], current['sha256'])
        self.assertEqual(record['watermark'], 'arXiv:submit/7973196 [cs.HC] 8 Nov 2026')
        self.assertIn('submission processing only', record['status'])
        self.assertIn('does not establish a public arXiv article identifier', record['status'])
        self.assertIn('on hold', record['processing_status_at_retrieval'])

    def test_revision_checksums(self):
        root = ROOT / 'paper/revisions/2026-11-08'
        for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
            if not line: continue
            digest, name = line.split('  ', 1)
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest, name)

if __name__ == '__main__':
    unittest.main()
