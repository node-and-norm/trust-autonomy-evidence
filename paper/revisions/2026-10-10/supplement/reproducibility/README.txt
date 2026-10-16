STAGED AGGREGATION REPRODUCIBILITY CHECK
Author-review packet only | 10 October 2026

PURPOSE AND LIMIT
This is a mechanical check of recorded categorical labels. It is NOT validation
of the evidence, historical truth, or source-to-condition judgments behind those
labels. Stage 3 is a conditional, unadopted proposal. No manuscript, released
assessment, historical record, or repository is modified by this package.

RUN OFFLINE
Requirements: Python 3.8 or later; standard library only. Tested with Python
3.12.14. No installation, internet connection, credentials, or dependencies.
The .py file is readable source text; no binary executable is included.

Unzip the bundle. In its reproducibility directory, run:

  python3 check_staged_aggregation.py --verify-saved

This recomputes all results and tests, byte-compares results.json and results.txt,
and verifies all six content-file hashes in SHA256SUMS.txt. It is read-only.
Success exits 0; invalid inputs or mismatches exit nonzero with an error.

To regenerate the two saved results from the recorded inputs:

  python3 check_staged_aggregation.py

To write a separate copy instead:

  python3 check_staged_aggregation.py --output-dir rerun

The default input is recorded_inputs.json beside the script, independent of the
current working directory. An explicit --input PATH is also supported; the ledger
snapshot must be beside that input. The checker reads state assignments from the
JSON. It does not contain hard-coded per-case expected results. Its fixed constants
are the six-condition order, four legal states, unchanged aggregation rule and
schema/status safeguards. Test expectations check the rule itself.

FILES
- recorded_inputs.json: all three recorded stages; exact ledger row quotations;
  source hash and baseline identifiers; separately labeled diagnostic and
  counterfactual substitutions. No external retrieval is needed.
- check_staged_aggregation.py: input validation, aggregation, full alternative
  enumeration, explicit decisive-cell explanations, and self-tests.
- author_case_derivation_ledger.txt: exact authoritative ledger snapshot.
- results.json: machine-readable results, every case alternative, every joint
  assignment, cell counts, provenance hashes and self-test results.
- results.txt: readable case-by-case results and decisive/blocking cells.
- SHA256SUMS.txt: integrity hashes for the six content files, excluding itself.

LEDGER IDENTITY
SHA-256: a7ad4f0870eeea07e21229613ae820bf5611f03c36f0774c41d10e992f2a76d5
The checker verifies this snapshot against the input's recorded hash, checks exact
quoted rows and their state expressions, and validates all required fields.
Hashes identify bytes; they do not authenticate or validate the historical
sources, evidence, or inferences. Baseline Git identifiers and the frozen evidence
cutoff are recorded provenance, not independently retrieved artifacts.

UNCHANGED RULE
Condition order: access, comprehension, authority, feasibility, exercise,
propagation. The historical JSON field named effect is called propagation here.
Any U yields Fail. Otherwise all six S yield Pass. Otherwise at least one P/I
and no U yields Unresolved. P/I never overrides a U. For Fail, results list each
decisive U; other P/I cells are explicitly nondecisive. For Unresolved, results
list every P/I cell blocking an all-S Pass.

RECORDED RESULTS
Stage 1, historical: Oko Unresolved; ZG710 Fail; F/A-18C Fail.
Totals: 0 Pass, 2 Fail, 1 Unresolved. Cell counts: S=2, P=8, U=5, I=3.

Stage 2, limited corrections: Oko Unresolved; ZG710 Fail; F/A-18C Unresolved.
Authority and propagation each allow P or I for each Patriot case. There are four
assignments per Patriot case and 16 joint assignments; every one gives totals
0 Pass, 1 Fail, 2 Unresolved. ZG710 retains comprehension, feasibility and exercise
U in this comparison. Retention is not revalidation. Cell counts vary with the
unadjudicated choices: S=0, P=8..12, U=3, I=3..7; the case results do not vary.

Stage 3, full amended proposal, CONDITIONAL AND UNADOPTED:
Oko S/P/P/S/S/S; ZG710 P/I/P/P/P/S; F/A-18C P/I/P/P/P/P.
Totals: 0 Pass, 0 Fail, 3 Unresolved. Cell counts: S=5, P=11, U=0, I=2.
These totals depend on author acceptance of the amendments and row judgments.

SEPARATE RULE ILLUSTRATIONS
Propagation-only diagnostic: allow S/P/I at each Patriot propagation cell, keeping
all other Stage 1 cells. All nine joint assignments give 0 Pass, 1 Fail,
2 Unresolved. This does not establish that S meets the original evidence policy.

Three counterfactual single-U illustrations start from Stage 3 and separately
replace ZG710 comprehension, feasibility, or exercise with U. Each gives ZG710
Fail and totals 0 Pass, 1 Fail, 2 Unresolved. These are rule illustrations, not
adopted historical states or empirical sensitivity analysis. All substitutions
are recorded separately in the input and never overwrite the main stage rows.

Sets are alternative assignments, not a fifth state. Cartesian enumeration
asserts no probability or evidentiary independence.

TEST COVERAGE
- All 4^6 = 4,096 legal rows: 1 Pass, 3,367 Fail, 728 Unresolved.
- 1,458 explicit single-U rows, across all six positions and every other-state
  combination; unknowns never override the U or become a Fail explanation.
- All-S and 12 explicit single-P/I rows with no U.
- 14 invalid/missing row-state rejections.
- 120 missing input-field rejections, 16 invalid input mutations and duplicate
  JSON-key rejection.
- Two in-memory computation mutations prove results depend on the input states.
- All three labeled ZG710 single-U counterfactuals.

All tests use explicit exceptions rather than assert, so checks remain active
under python3 -O. The checker writes only the two result files in normal mode;
--verify-saved writes nothing. It never adjudicates or updates the recorded states.
