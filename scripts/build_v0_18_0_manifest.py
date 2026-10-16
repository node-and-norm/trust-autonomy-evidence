#!/usr/bin/env python3
"""Seal the staged v0.18.0 repository snapshot, excluding its own manifest."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = 'release/v0.18.0-manifest.json'


def main():
    names = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    files = {}
    for name in sorted(n for n in names if n and n != OUTPUT):
        data = (ROOT / name).read_bytes()
        files[name] = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
    result = {
        'version': '0.18.0', 'paper_version': '2026-10-10',
        'historical_paper_version': '0.17.0', 'date': '2026-10-16',
        'scope': 'Separately approved October reassessment and methods/initial-Jev phase closeout',
        'hash_algorithm': 'SHA-256', 'files': files,
        'boundary': 'Artifact identity and calculations do not validate scientific judgments or resolve publication status.'
    }
    (ROOT / OUTPUT).write_text(json.dumps(result, indent=2) + '\n')
    print('v0.18.0 snapshot manifest: %d files' % len(files))


if __name__ == '__main__':
    main()
