# Pre-live translation review handoff

Status: prepared; no human reviewer has completed this audit. This supplementary
packet leaves every frozen experiment byte unchanged. It adds no model result.

The immediate decision is whether the authored excerpts and semantic questions
justify proceeding with this experiment version. Review correctness and ambiguity
before spending live calls. This pre-live audit is separate from the frozen
post-response disagreement-adjudication workflow.

## Independent pass

A coordinator gives each of two human reviewers `BLIND_PACKET.json`, one blank
`REVIEWER_A.csv` or `REVIEWER_B.csv`, and these instructions. Each form contains
1,654 determinations across 94 packets. Reviewer identity, date, expertise,
conflicts and familiarity with the corpus should be recorded in a separate signed
cover note. The forms contain no invented reviewer identity or completed judgment.

Use the question's own five-state criteria and only its named topic excerpt.
Record an evidence state, any translation/question concern, and independent notes.
Read related-looking packets independently; repeated wording is expected. Keep
permission, use and effect distinct. Missing records do not establish failure.
Document exclusions and partially demonstrated propositions separately.

Complete and save both independent passes before consulting `COORDINATOR_KEY.json`,
source fixtures, reference labels, pair relationships or any model response.
The packet omits those fields and uses opaque review IDs. Blinding is procedural:
all repository files remain public, and no provider-training secrecy is claimed.
A reviewer who has already read the source labels must disclose that exposure.

## Reconciliation

After independent notes are fixed, the coordinator uses `COORDINATOR_KEY.json` to
join the forms to the frozen `provenance.json`, source signals, reference labels
and mutation/invariance pairs. Review every reviewer/reference disagreement and
flagged concern. Confirm that translations add no governance-relevant assumption
beyond the documented operationalization, that nuisance pairs retain facts, and
that the authority labels follow the declared permission/use boundary.

Record each concern with both original notes, the relevant text and source field,
a proposed disposition from the seven categories in the experiment protocol,
and an explicit resolution or unresolved status. Agreement alone does not prove
validity. Retain original notes even if reviewers reconcile their judgments.
Do not count agent-generated observations as independent human review.

A material defect requires a versioned amendment; never repair a frozen card in
place. Keep the original corpus, labels and audit evidence. Any new version must
state which material changed and whether any Jev output had been observed.

## Next steps

1. Complete this translation audit and review PR #32; merge the reviewed checkpoint.
2. Prepare a separately versioned live-execution bridge using the frozen request
   schedule, pinned model/SDK, no retries and complete raw-response retention.
   Validate that bridge with offline transports before any provider call.
3. Once access is available, execute the prescribed repetitions and report all
   scheduled positions, invalid responses and resolved model versions.
4. Apply the two-reviewer disagreement workflow and publish the bounded report.
5. Design JEV-TAE-6 separately, with source rights, evidence sufficiency and public
   case selection fixed before judging those cases.

Run `python -m experiments.jev.review_evidence_v1.build_packet` from the repository
root to reproduce the exports. It verifies the source freeze first and refuses to
overwrite edited reviewer forms. `manifest.json` records the source freeze and
export hashes. The coordinator key must be withheld during the independent pass.
