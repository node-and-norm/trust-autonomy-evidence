"""Current reader routes must not reassign historical edition identities."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ReaderNavigationTests(unittest.TestCase):
    def test_badges_separate_editions(self):
        readme = (ROOT / 'README.md').read_text()
        self.assertIn('tae-latest-20261108.svg', readme)
        self.assertIn('tae-deposit-20261101.svg', readme)
        self.assertIn('https://doi.org/10.5281/zenodo.23852566', readme)
        self.assertIn('not yet included here', readme)

    def test_readers_are_static_with_unique_cells(self):
        books = [ROOT / 'TAE_STUDY_MAP.ipynb', *sorted((ROOT / 'notebooks/historical-study').glob('*.ipynb'))]
        self.assertEqual(len(books), 5)
        for path in books:
            book = json.loads(path.read_text())
            self.assertEqual(book['nbformat'], 4)
            self.assertEqual(len({c['id'] for c in book['cells']}), len(book['cells']))
            self.assertTrue(all(c['cell_type'] == 'markdown' for c in book['cells']))
            text = ''.join(''.join(c['source']) for c in book['cells'])
            self.assertIn('2026-11-08', text)

    def test_source_manifest_digests_are_preserved(self):
        root = ROOT / 'notebooks/historical-study'
        previous = json.loads((root / 'MANIFEST.json').read_text())
        current = json.loads((root / 'NAVIGATION_MANIFEST_20261108.json').read_text())
        self.assertEqual(set(previous['files']), set(current['files']))
        for name, digest in current['files'].items():
            self.assertEqual(hashlib.sha256((root / name).read_bytes()).hexdigest(), digest, name)
            if name.startswith('sources/'):
                self.assertEqual(digest, previous['files'][name], name)

if __name__ == '__main__':
    unittest.main()
