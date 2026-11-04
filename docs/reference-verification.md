# Verify the TAE reference draft

These commands check the review branch in a disposable copy. They preserve the research checkout you already use. The environment matches the existing [Python 3.12 workflow](../.github/workflows/validate.yml) and [pinned dependencies](../requirements-dev.txt).

## Prepare and run the checks

Use Git, Python 3.12 and a POSIX shell on macOS or Linux. The clone and dependency installation need network access. The verification commands use local records and need no AI credentials. [Reproduction contract](REPRODUCIBILITY.md).

Copy the complete block into a POSIX shell. Its subshell stops on an error and leaves your original working directory unchanged.

```sh
(
set -eu
tae_check_root=$(mktemp -d "${TMPDIR:-/tmp}/tae-reference.XXXXXX")
git clone --branch docs/tae-reference-design-2026-11-03 --no-single-branch \
  https://github.com/node-and-norm/trust-autonomy-evidence.git \
  "$tae_check_root/checkout"
cd "$tae_check_root/checkout"
git fetch --tags origin
python3.12 -m venv "$tae_check_root/venv"
. "$tae_check_root/venv/bin/activate"
python -m pip install -r requirements-dev.txt
python --version
git rev-parse HEAD
python -m pip freeze
python -B scripts/validate_repository.py
python -B scripts/validate_paper.py
python -B scripts/validate_release_snapshot.py
python -B scripts/verify_reassessment_release.py
python -B -m unittest discover -s tests -p 'test_*.py' -v
if command -v shasum >/dev/null 2>&1; then
  (cd paper/revisions/2026-11-01 && shasum -a 256 -c SHA256SUMS.txt)
else
  (cd paper/revisions/2026-11-01 && sha256sum -c SHA256SUMS.txt)
fi
git diff --exit-code
git status --short
)
```

Keep the printed Python version, commit and dependency list with the result. This guide selects the reference-design branch while it awaits review. The [full reproduction guide](REPRODUCIBILITY.md) also documents Windows setup and historical replay.

## Read the results

The expected successful messages come from the linked implementation. A result becomes a recorded pass only after the command finishes successfully.

| Command | Expected output | What it checks |
| :--- | :--- | :--- |
| Aggregate validator | `repository validation: PASS` | Declared artifact, synthetic-case, paper and integrity conditions. [Implementation](../scripts/validate_repository.py) |
| Paper validator | `paper validation: PASS` | Declared manuscript-package and supporting-record conditions. [Implementation](../scripts/validate_paper.py) |
| Release validator | `release snapshot validation: PASS` | Historical tags and immutable working copies. [Implementation](../scripts/validate_release_snapshot.py) |
| Reassessment verifier | `Approved October revision: PASS` | Preserved supplement, file identities and saved calculation. [Implementation](../scripts/verify_reassessment_release.py) |
| Existing unit tests | `OK` | Navigation, license and isolated historical-replay checks. [Tests](../tests/) |
| Tracked-file comparison | No diff; exit code 0 | Tracked bytes remain unchanged during verification. Inspect any untracked paths reported by the final status command. |

The saved audit status includes `PASS_WITH_EXCEPTIONS`. Those exceptions retain their original scope. A passing technical check leaves source truth, assessor judgment and institutional effectiveness unresolved. [Research limits](../RESEARCH_STATUS.md#open-limits-and-future-studies).

## Account for writes

Both aggregate and paper validation invoke a screening builder. That builder writes the five tracked paths below. This is why the instructions use a disposable clone. [Screening validator](../scripts/validate_forward_citation_author_screening_v0_13_0.py), [builder](../scripts/build_forward_citation_author_screening_v0_13_0.py).

<details>
<summary>Tracked paths written by the nested builder</summary>

- `paper/data/forward-citation-author-screening-decisions-v0.13.0.csv`
- `paper/data/inaccessible-record-retrieval-v0.10.0.csv`
- `paper/data/forward-citation-author-screening-v0.13.0.json`
- `paper/forward-citation-author-screening-v0.13.0.md`
- `evidence/human-review-attestation-v0.13.0.json`

</details>

Keep any changed output in the disposable copy for inspection. Do not copy it into the research record or rebuild a historical manifest to clear a mismatch. The [navigation boundary](current-navigation.md) identifies the separately mutable README checkpoint.

## Check the November archive

The complete command block checks this archive before leaving the disposable copy. It selects `shasum` when available and otherwise uses `sha256sum`.

All five named files should report `OK`. The [checksum manifest](../paper/revisions/2026-11-01/SHA256SUMS.txt) checks byte identity. It performs no manuscript compilation or source reappraisal.

Use the [current review guide](current-review.md) to connect these file checks to the paper, publication receipt and research limits.
