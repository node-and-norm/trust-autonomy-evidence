# Offline verification record

This record is post-freeze verification evidence, excluded from prespecified input
hashes. No live Jev request was made. No credentials were inspected or required.
The final prespecification is commit `91d9055`; the initial freeze was `a154d3b`.

The first offline test run detected that H06 repeated H01's facts after ignoring
excerpt order. Commit `91d9055` gives H06 a different state composition and retains
the novelty assertion. That commit also counts interrupted attempts and preserves
resolved-model metadata on invalid responses. These changes followed synthetic
mock/testing output only, with no Jev output observed. The five other holdouts,
question semantics, primary metrics and repetition policy were unchanged.

## Completed checks

- Phase 2: 12 tests pass on Python 3.9.6 without the SDK and Python 3.12.14 with
  the pinned SDK. Tests forbid socket connections, reproduce the corpus exactly,
  check all six holdouts for distinct facts, reject hash tampering, inspect every
  dry-run request for the data boundary, and verify metrics against hand calculations.
- Original v1: 12 tests pass on Python 3.12.14 with typesafe-sdk 0.7.1; the
  credential-free environment passes the same suite with its two SDK tests skipped.
  SDK tests use an in-memory transport and make no service calls.
- Standalone Phase 2 dry-run and mock: 282 scheduled requests each. The mock
  completes all requests using the uninformative `mock-only` response. Three
  repetitions contain 4,962 determinations. Its 0.8 Brier loss is a uniform-distribution
  arithmetic check, not a measurement of Jev.
- `python3 scripts/validate_repository.py`: PASS, including 252 original oracle
  comparisons and 12 original mutation tests. The pre-existing chain-of-evidence
  audit retains its reported PASS_WITH_EXCEPTIONS status.
- `python3 scripts/validate_paper.py`: PASS.
- `python3 scripts/validate_release_snapshot.py`: PASS: six tags, 821 sealed
  artifacts and 67 immutable working copies.
- `git diff --check`: PASS. All changes are inside `experiments/jev/evidence_v1/`
  and the existing Jev-only offline workflow. No prior v1 file, core validator,
  sealed oracle, released conclusion or historical result changed.

`verification/offline-runs.json` records hashes and coverage of the retained local
runs. Request and response artifacts are reproducible under the documented runner
and remain in the ignored `runs/` directory. They are deliberately excluded from
the research-input freeze. GitHub's SDK-absent/installed matrix runs both suites.

A first attempt to create a fresh optional-SDK environment used the system Python
3.9.6, for which the pinned SDK was unavailable. Validation then used the existing
Python 3.12.14 environment with SDK 0.7.1. This was an environment issue; no package
pin or experiment material was changed to accommodate it.

## Interpretation boundary

The tests establish corpus stability and offline pipeline behavior. They do not
validate the translations through independent human review, establish model
accuracy, or demonstrate public-case transfer. Disagreement records remain open
until the prespecified human adjudication process is completed. The live transport
is intentionally deferred; future use must preserve the frozen requests and policy.
