ADDITIONAL ZG710 REASSESSMENT PUBLIC REPRODUCIBILITY SUPPLEMENT
Version: additional-reassessment-v2-public-2026-10-10
Prepared for final public-packaging review on 10 October 2026.

PURPOSE AND AUTHOR APPROVAL
This separately versioned public derivative records the author's approval of the
revised preprint and additional ZG710 reassessment on 10 October 2026. The dated
public_author_approval.json replaces private approval communications and their
identifiers. Scientific inputs, case boundaries, condition definitions and the
aggregation rule are unchanged. Approval does not provide independent empirical
validation. Upload, publication and resubmission remain separate actions.

The original private review package is retained separately and is not included in
this public ZIP. The historical checker ZIP described below is a different,
earlier artifact without private approval communications; it remains byte-identical.

OFFLINE RUN
Requires Python 3.8+; tested with Python 3.12.14. Standard library only; no network,
installation, credentials or external packages. The checker is readable Python.
After extracting the ZIP, enter reproducibility_additional_public and run:

  python3 check_additional_reassessment_public.py --verify-saved

This read-only command recomputes results/tests, compares both saved output files
byte-for-byte, and verifies all nine content-file hashes in SHA256SUMS_PUBLIC.txt.
Success exits 0. Invalid input, a failed test or a mismatch exits nonzero.

To write a separate regenerated copy:

  python3 check_additional_reassessment_public.py --output-dir rerun

To regenerate the two public output files in place:

  python3 check_additional_reassessment_public.py

Checks also remain active under optimized Python:

  python3 -O check_additional_reassessment_public.py --verify-saved

The default input is recorded_inputs_public.json beside the checker. Optional
--input PATH selects another input whose referenced dependencies are beside it.
Only the two output files are written in generation mode. Source records, inputs,
approval statement and the historical ZIP are never rewritten by the checker.

PRESERVED HISTORICAL DEPENDENCY
Staged_Aggregation_Reproducibility_original.zip.b64 is preserved byte-for-byte:
SHA-256 9ddfa8651d14e5a9f041ce906215e7fc8e3152bdd22d848a7270ea9d6e90ac76
Its scientific ledger SHA-256 is:
a7ad4f0870eeea07e21229613ae820bf5611f03c36f0774c41d10e992f2a76d5

The checker reads Stage 1 and Stage 2 inputs and outputs directly from that ZIP,
verifies its bytes and pinned inputs/ledger, and compares the reproduced results.
It does not extract or execute the archived checker. The archive may separately
be extracted to run its own documented verification.

Historical author-review and pending-approval labels inside that archive remain
as records of its earlier status. The public approval statement applies to the
current revised preprint and bounded additional reassessment; it does not adopt
the archive's broader Stage 3 proposal. Stage 3 remains explicitly unadopted.
The preserved additional_reassessment_source_snapshot.txt also predates approval;
its provisional wording is historical, not a claim that current approval is absent.
Hashes establish byte identity, not source truth or authenticity of interpretation.

SCIENTIFIC INPUTS AND DEPENDENCIES
Fixed condition order: access, comprehension, authority, feasibility, exercise,
propagation (the historical assessment field is called effect).

Oko:     P / P / P / P / P / P
ZG710:   P / I / {P,I} / {P,I} / {P,I} / {P,I}
F/A-18C: P / I / {P,I} / I / I / {P,I}

The only additional changes to Stage 2 are ZG710 comprehension U to I, feasibility
U to {P,I}, and exercise U to {P,I}. All other Stage 2 cells are retained. The
checker rejects changes outside that approved scope. P/I choices remain unresolved,
not a fifth state or probabilities. Cartesian enumeration claims no independence
of the underlying evidence.

The released classification-to-destruction boundary, direct-contemporaneous S
requirement and active-judgment-OR-intervention criterion are retained. Crew evidence
addresses the same crew-level proposition without establishing individual cognition.
No retrospective-S, action-plus-evaluation, simple-withholding or other Stage 3
amendment is adopted. Adverse evidence and the strongest retained-U arguments remain
in the scientific rationale. Their necessary-failure inferences were judged
insufficiently established, not disproved by arithmetic.

RESULTS
Unchanged rule: any necessary U yields Fail; otherwise all six S yields Pass;
otherwise P/I with no U yields Unresolved. Uncertainty never overrides U.

Historical Stage 1: 0 Pass / 2 Fail / 1 Unresolved, one assignment.
Limited Stage 2: 0 Pass / 1 Fail / 2 Unresolved, all 16 joint assignments.
Additional reassessment: conditional 0 Pass / 0 Fail / 3 Unresolved, all 64 assignments.

There are 16 ZG710 variants and four F/A-18C variants, with one Oko row: 1 x 16 x 4
= 64. Additional cell-count ranges are S=0, P=8..14, U=0, I=4..10; the P/I ranges
are linked and always sum to 18. The case-result vector remains invariant across
the recorded alternatives, conditional on the supplied judgments and retained
Stage 2 cells. Calculation cannot establish those inputs.

Three separate rule illustrations restore U at ZG710 comprehension, feasibility
or exercise, producing 0 Pass / 1 Fail / 2 Unresolved across 64, 32 and 32 joint
assignments respectively. These are not adopted states or empirical sensitivity
analysis. General tests cover necessary U at every condition position.

TEST COVERAGE
- All 4^6 = 4,096 legal rows: 1 Pass, 3,367 Fail and 728 Unresolved.
- 1,458 explicit single-U rows across all six positions; uncertainty is nondecisive.
- All-S and 12 single-P/I cases; 14 invalid/missing-state rejections.
- All required input-field deletions, invalid/scope mutations and duplicate JSON keys.
- Historical Stage 1/2 regression, all 64 additional assignments and three U examples.
- Two in-memory tests confirming computed results follow states rather than case names.

FILES
README_PUBLIC.txt; check_additional_reassessment_public.py; recorded_inputs_public.json;
results_public.json; results_public.txt; public_author_approval.json;
additional_reassessment_source_snapshot.txt; Staged_Aggregation_Reproducibility_original.zip.b64;
PUBLIC_PACKAGING_CHANGES.txt; SHA256SUMS_PUBLIC.txt (the nine-file manifest).

LIMITS
This is computational reproduction of supplied categorical judgments, not independent
historical or empirical validation, inter-rater reliability, or proof of practical
human control. Jev and collaborative review do not independently validate these
classifications. The public package is prepared for a final packaging check; this
checker performs no upload, publication, resubmission or public repository change.

ARXIV TRANSPORT NOTE (10 October 2026): arXiv recursively expands archives based on content, even after extension changes. The original ZIP is therefore preserved as Base64 text in the .zip.b64 file. The checker decodes it in memory, verifies the unchanged original ZIP SHA-256, and reads its exact historical members. Decode this file with a standard Base64 decoder to recover the byte-identical original archive. Saved outputs and hashes were regenerated for this transport representation; scientific calculations are unchanged.
