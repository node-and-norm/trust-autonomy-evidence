# Reproduce the repository checks

Use this guide to verify the current repository or replay a historical audit.
A passing result establishes the checks described below. It does not establish
source truth, independent assessment, legal compliance, or field effectiveness.

## Prepare a clean environment

Use Git and Python 3.12, matching the repository's CI version. The commands below
use a POSIX shell. On Windows, create the same environment with `py -3.12 -m venv
.venv` and invoke `.venv\Scripts\python.exe` directly instead of activating it.

```sh
git clone https://github.com/node-and-norm/trust-autonomy-evidence.git
cd trust-autonomy-evidence
git fetch --tags origin
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python --version
git rev-parse HEAD
```

Record the Python version and Git commit with any verification report. Dependency
installation requires package-index access. The validation and historical replay
commands use local repository data and require no API credentials or Jev SDK.
The optional SDK is unnecessary for this guide.

## Validate the current checkout

```sh
python scripts/validate_repository.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

The aggregate validator includes paper checks, historical release snapshots,
sealed synthetic fixtures, claim-evidence controls, literature/search ledgers,
and figure integrity. Success ends with `repository validation: PASS`.
The audit line intentionally retains `PASS_WITH_EXCEPTIONS`; it does not mean
that the declared research limitations have been resolved.

The release snapshot check currently covers seven tags, 854 sealed artifacts and
98 immutable working copies. The working-tree check preserves 30 v0.17.0 release
artifacts and verifies three separately hashed current-navigation documents.
See [the navigation boundary](current-navigation.md) for why current README and
citation bytes can differ from their released versions.

For a narrower diagnostic, run:

```sh
python scripts/validate_paper.py
python scripts/validate_release_snapshot.py
```

These end with `paper validation: PASS` and `release snapshot validation: PASS`.
Do not rerun historical manifest builders to make a failing check disappear.
A mismatch needs an explanation and a reviewable correction.

## Replay historical audits

```sh
python scripts/replay_historical_audit.py --tag v0.16.0
python scripts/replay_historical_audit.py --tag v0.17.0
```

The runner verifies each tag's pinned commit, exports its tracked files into a
fresh temporary directory, and executes that release's own audit code with socket
connections disabled. It compares the regenerated JSON and Markdown bytes with
that same snapshot's recorded outputs. The current working tree supplies neither
the audit code nor its evidence. The temporary snapshot is removed afterward.

Expected results:

| Tag | Audit output | Replay result |
| --- | --- | --- |
| v0.16.0 | `PASS_WITH_EXCEPTIONS`, 40 claims, 39/39 controls detected | `"status": "PASS"` and all comparisons `"identical": true` |
| v0.17.0 | `PASS_WITH_EXCEPTIONS`, five bounded policy claims, 9/9 controls detected | `"status": "PASS"` and all comparisons `"identical": true` |

To retain the compared artifacts, add `--output` with a new directory outside the
repository, for example `/tmp/tae-v016-replay-001`. Existing directories are never
overwritten. Exit code 1 means a replay failed or differed; exit code 2 means the
replay could not start or complete. A missing tag requires `git fetch --tags origin`.
A moved tag is rejected. Additional tags require a separately reviewed runner entry.

The older `scripts/run_coe_integrity_audit.py --check` reads its checkout directly.
It should not be used on current main to claim historical replay. The isolated
runner is the supported path for the preserved v0.16.0 audit. Do not run the old
script without `--check` on main: it writes historical audit output paths.

## Check the offline Jev experiments

```sh
python -m unittest discover -s experiments/jev/tests -v
python -m unittest discover -s experiments/jev/evidence_v1/tests -v
```

Without the optional SDK, two v1 transport tests are expected to skip. The
remaining v1 tests and the evidence-reconstruction tests should pass. These
checks use mock responses and establish pipeline behavior only. See the
[experiment protocol](../experiments/jev/evidence_v1/PROTOCOL.md) and
[human-review handoff](../experiments/jev/review_evidence_v1/README.md) for the
prespecified methods and incomplete human-review work.

## License source and attribution

`LICENSE` contains the complete text retrieved from the
[Apache Software Foundation](https://www.apache.org/licenses/LICENSE-2.0.txt).
Its SHA-256 is `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.
The existing copyright attribution is preserved in `NOTICE`. This correction
replaces an abbreviated license text; it does not rewrite historical release files
or assert new rights over third-party source material.
