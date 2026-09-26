# Author-audited synthetic benchmark: amendment v1

Status: protocol and blank workbooks prepared; author review is pending. This is
an alternative, explicitly non-independent route for an independent researcher
who cannot obtain two qualified reviewers. It is not completion of the original
two-reviewer protocol. Select and disclose this route before live execution.

## Scope and timing

The original evidence-v1 protocol, review packet, v2 adjudication records and
all their hashes remain unchanged. This amendment changes the review gate and
interpretation, not the evidence, expected labels, question wording, request
schedule, metric denominators, repetitions or holdouts. The named route is
`author-audited-synthetic-v1`; reports must name it rather than imply adherence
to the unamended independent-review protocol.

Only mock responses have been observed in the implementing assistant's work.
The author explicitly confirmed in the task conversation, before this freeze,
that no live Jev outputs had been observed. This declaration is carried into the
workbook and must be updated if circumstances change. Unknown exposure does not count as no exposure. If live output was
already seen, retain this protocol but report it as a post-observation amendment;
it cannot authorize a claim of prospective prespecification. Public Git history
is the timestamp record, not external registration.

## What this benchmark can establish

Report agreement with the author's explicit synthetic specification, sensitivity
to controlled fact changes, stability under irrelevant transformations, missing
responses and repetition variability. The frozen metrics remain descriptive.
They do not establish independent interpretive reliability, real-world accuracy,
source truth, construct validity, legal sufficiency or operational effectiveness.
Author agreement with an author-derived reference is not an independent test of
that reference. AI consensus is not a substitute for independent human review.

Use this report statement:

> This study used an author-audited synthetic specification. Independent human
> review was unavailable. Automated controls assess pipeline and transformation
> behavior; author assessments and AI critiques do not establish independent
> validity. Original reference-based scores are retained without adjudication-based
> correction.

## Before any live execution

1. Verify the original freezes and this amendment. Export a fresh workbook outside
   the repository with the command below. Keep original blank files unchanged.
2. The author completes pass 1 for all 216 distinct topic/excerpt units, using only
   the question and excerpt. Record a state, rationale, concern, identity and actual
   timestamp. The unit mapping covers all 1,654 determinations; repeated units are
   not independent observations. Packet context is separately covered by 60 pairs.
   Authority challenges and compositional holdouts are included. Holdouts remain
   untouched for model-output tuning; author exposure was already disclosed.
3. Save and hash pass 1. Wait at least seven full days, then complete pass 2 in its
   different deterministic order without consulting pass 1 or the reference key.
   This interval is a prespecified practical choice, not an empirically validated
   memory washout. The author may recognize their wording; report that limitation.
   Retain both original files. Timestamps and identity are attestations, not proof.
4. Only after both passes are fixed, inspect KEY.json, all 60 pair comparisons and
   the original provenance/translation assumptions. Complete every pair assessment.
   For each pass disagreement, author/reference disagreement or flagged concern,
   retain an issue record with evidence, alternative interpretation, disposition,
   rationale and proposed action. No issue may be silently dropped.
5. Automated checks and optional AI criticism supplement the author assessment.
   Preserve criticism, including disagreements with the author. An AI critic must
   never fill an author form or be listed as a second human reviewer. The prompts
   below prescribe two fresh-context passes; they are optional, and must be marked
   not performed if no such passes occur. Shared training and model correlations
   preclude treating two models as independent validators.
6. The author records the route choice, exposure declaration, resolved concerns and
   any material defect. A material evidence/question defect stops this version's
   live progression and requires a new version with preserved old materials. An
   unresolved material concern also stops progression. Proceeding despite a
   nonmaterial ambiguity requires a cited rationale and explicit report limitation.

No live bridge is implemented here. Even a completed author audit requires a
separately reviewed transport bridge and compatible credentials/model metadata.
This amendment does not permit retrospective repair, selective exclusions,
replacement calls, tuning on holdout output or modification of original scores.

## Post-response author assessments

Keep the original disagreement record open/UNRESOLVED in the original two-reviewer
system, including adjudication_v2. Add a separately identified author assessment
with `assessment_basis: author_only`, source record ID and hash, raw run/request/
response references and hashes, actual author/date, evidence and competing
interpretations, one of the original seven dispositions, rationale, uncertainty,
and downstream proposed/applied changes with dates and hashes. Label its status
`author_assessed`, never `independently_adjudicated` or a closed v2 record.
Supersede by appending a new assessment with a new ID and prior ID link; preserve
earlier exports. An author's JEV_ERROR designation is an author interpretation,
not an independently established error. Publish raw disagreement counts unchanged.
The existing v2 two-reviewer route remains available if reviewers become available.

## Workbooks and checks

```sh
python -m experiments.jev.author_audit_v1.audit export --output /tmp/tae-author-audit-001
python -m experiments.jev.author_audit_v1.audit check --input /tmp/tae-author-audit-001
python -m unittest discover -s experiments/jev/author_audit_v1/tests -v
```

Export creates a new directory outside the repository and never overwrites one.
`PASS_1.csv` and `PASS_2.csv` require actual author entries. `PAIRS.csv` requires a
rationale and `retain` or `material_defect`. `COVER.json` starts with null identity,
null dates, the author’s recorded no-live-output declaration, and an unconfirmed route. `ISSUES.json`
starts empty; check requires an issue for every detected disagreement/concern.
The checker reports missing work with a nonzero exit; passing checks establish
workbook completeness and recorded consistency only, not the truth of attestations.
It does not execute Jev or close independent-review records.

`KEY.json` contains reference states and original packet/topic mappings. Keep it
out of view during author passes; this is procedural self-blinding in a public
repository. `UNITS.json` and `PAIR_PACKET.json` expose bounded text and paired
facts respectively. Pair review occurs after the two classification passes.
All completed workbooks belong in a separately preserved audit record, not in
this frozen directory.

## Prespecified AI criticism prompts

Critic A receives only UNITS.json, without KEY.json, provenance or model outputs:
“Identify ambiguous wording, unstated assumptions, evidence insufficiency and
plausible alternative interpretations. Cite exact unit IDs and excerpts. Do not
claim human review or infer missing facts. Return objections, including uncertainty.”

Critic B receives PAIR_PACKET.json, without expected reference deltas or outputs:
“List facts changed between each pair. Distinguish permission, actual use, timing
and effect. Flag purportedly irrelevant changes that may alter interpretation.
Cite pair IDs and exact text. Do not decide benchmark validity or claim independence.”

Save exact prompts, supplied-file hashes, provider/model/version if known, time,
raw outputs and every failed attempt. Fresh contexts reduce direct answer leakage
but do not demonstrate statistical independence. No AI criticism was performed
by merely drafting these prompts; automated unit tests are separate evidence.
