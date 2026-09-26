# Evidence reconstruction v2: author-reviewed AI-assisted successor

This successor applies the author's approved triage proposals before live Jev
execution. It preserves evidence_v1 and all historical releases, sealed oracles,
original author-audit materials and AI assessments. It is not a silent repair of
an earlier freeze. No independent review or live Jev accuracy result is claimed.

## Approval and exposure

The author reviewed and accepted 216 AI-assisted assessments, including 30 flagged
units. The assistant grouped them into 14 issues (eight material and six bounded
limitations/minor corrections), provided exact proposals, and the author replied
“Reviewed. Proceed.” This author decision approves implementation of those
proposals. The assistant's assessments had prior design exposure. Acceptance is
not an unassisted author pass, delayed consistency test, or independent review.
The author previously confirmed no live Jev outputs observed; the implementing
assistant has made no live calls. Mock output was observed and is plumbing evidence
only. No external registration or independently verified timestamp is claimed.

The route for this version is `author_reviewed_ai_assisted_v1`. It prospectively
replaces the unavailable independent-review and unassisted/delayed-pass progression
gates for this successor only. It requires disclosed author review of AI assistance,
a preserved issue ledger, explicit author approval of proposed material changes,
and offline validation of implementation. It does not retroactively complete those
other routes. This release is still offline: live execution requires a separate
reviewed transport bridge and compatible provider configuration.

## What changed

- T01 makes decision-relevant inventory completeness an explicit scenario stipulation.
- T02 prespecifies partial access versus no pre-action access.
- T03 fixes the objection preposition; T04 gives recommend/review their own recorded actions.
- T05/T07 explicitly label explanatory materials and checkbox attestations as partial
  precursors/attestations, not demonstrations of comprehension or human exercise.
- T08 defines repetition as at least two trials, without claiming statistical adequacy.
- T09 explicitly stipulates inventory exhaustiveness and independently checked retention.
- T10 distinguishes unverified inventory completeness from absent packet items.
- T12/T13 align reliability evidence with both condition-specific reporting and declared
  threshold attainment, changing both positive and negative excerpts and the question.
- T06/T11/T14 retain limitations on causation, external detectability and calibration.

`approved-triage.json` retains all original proposals and evidence. `changes.json`
records every changed packet/topic and before/after text. Neutral framing and the
separate access paraphrase are retained. `label-decisions.json` contains all 1,654
successor label decisions, not just changes. For the five affected evidence/meaning
constructs, explicit rules evaluate the revised text; other references are inherited
with rationale, not presented as independent validation. Reference labels happen
to remain equal to v1; that equality is checked rather than assumed. These are
experimental labels, not a resealed core oracle.

Added complete inventories, threshold attainment and role-specific actions are
newly authored synthetic facts. They are not inferred historical evidence. The
source provenance is hash-linked and the original source files remain untouched.

## Preserved experimental controls

The taxonomy JEV-TAE-2 through JEV-TAE-5, 94 packets, 1,654 determinations per
repetition, three repetitions, 282 scheduled requests and 4,962 determinations
remain. Pair identities and expected deltas remain. The six holdouts are revised
compositions of the same authored templates: exposed to author/AI review, never
claimed secret or independent-author data, and not tuned on live Jev outputs.
JEV-TAE-1 remains original contract fidelity; JEV-TAE-6 public cases remain deferred.

The original repetition, failure accounting, raw-byte retention, no-retry policy,
resolved-version separation, metric definitions and evidence/inference boundaries
in ../evidence_v1/PROTOCOL.md apply except for the explicitly amended wording and
review route above. Primary results remain repetition 1. Do not pool v1 and v2
metrics, revise original scores or infer accuracy from uniform mock responses.
Report coverage, all five classes, per-state recall, Brier, per-construct agreement,
mutation exact deltas, nuisance failures, invalid responses and resolved model
metadata using REPORT_TEMPLATE.md.

## Remaining limitations

Synthetic assertions of causal linkage do not establish real-world causal effects.
No retained alteration trail does not rule out external detection. Repeated trials
do not establish generalization. A stipulated tolerance result does not establish
empirical calibration without bins, samples and outcomes. The corpus still uses
repeated phrases and topic-isolated records; ecological and independent interpretive
validity remain unresolved. Explicit partial-state criteria improve consistency but
make the intended operationalization easier to recognize. They are not proof of
broader semantic judgment. Model error diagnoses remain author-only interpretations
unless the original two-reviewer protocol is actually completed.

## Reproduce and inspect, offline

```sh
python -m unittest discover -s experiments/jev/evidence_v2/tests -v
python -m experiments.jev.evidence_v2.run --mode dry-run --output experiments/jev/evidence_v2/runs/first-dry
python -m experiments.jev.evidence_v2.run --mode mock --output experiments/jev/evidence_v2/runs/first-mock
```

No live mode exists, even with credentials. The runner projects only state, questions
and the previously pinned model name into requests. Local IDs, provenance, labels
and triage never enter the request. Outputs require new directories in this
version's runs directory. The original two-reviewer adjudication schema is retained
for optional independent adjudication; no author-only action closes those records.

`author.build()` regenerates material for byte comparison. It never runs during
inference and refuses to overwrite changed files. `freeze.json` checks committed
bytes, all successor material and original freeze chains. Future changes require
another explicitly versioned amendment. Git history is the reviewable trust anchor.
