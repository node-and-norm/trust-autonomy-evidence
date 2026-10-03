# Jev-assisted review queue v1

This is a post-output development pilot designed after live-001 and its follow-up
were observed. It is not JEV-TAE-6, independent validation, an unseen holdout, or
adjudication of the original results. All earlier freezes, raw scores, references,
releases and open records remain unchanged. Jev may assist review of its own
outputs; this supplies no independent evidence of correctness.

## Cohort and frozen schedule

Select two primary-repetition valid agreements and two valid disagreements from
each of six live-001 suites: 24 semantic-review units. Within each suite/outcome
stratum, sort `job_id/question_id` by SHA-256 and take the first two. This is an
outcome-stratified, author-exposed development sample, not a prevalence estimate.
Retain all 22 invalid source requests in a separate deterministic queue. They
require arithmetic validation, not additional semantic inference.

Each semantic unit sends only its bounded excerpt, original question/criteria,
provisional reference and observed choice. The reference is explicitly contestable.
Source probabilities, suite/outcome-stratum names, IDs and provenance are not
sent. Four independent Choice questions propose a first review route and flags
for question tension, missingness inference and partial-state boundaries. These
are suggestions, not official adjudication dispositions or explanations of why
the original model answered as it did.

Three repetitions in repetition-then-cohort order: 72 scheduled requests, one
attempt each, no retries or substitutions. Repetition 1 is primary; later passes
describe suggestion consistency without majority voting. Pin jev-1.13.0 and SDK
0.7.1. Reuse the official-endpoint transport with no seed or temperature. Freeze
cohort, questions, code, tests and this protocol in Git before any pilot inference.
Verify the previous frozen corpus and live archive first. Save canonical requests,
actual SDK bodies and every available response/error byte, including invalid ones.
An interrupted position remains in the full denominator. Do not resume selectively.

## Response rules and reporting

Require exactly four answers with the declared option sets, finite probabilities
and confidence in [0,1], a nonblank resolved model, sum-to-one tolerance 0.00001,
and a maximum-probability choice. Do not relax or normalize the sum rule after the
earlier 0.99 observation. Invalid responses remain unavailable assistance; the
original item stays reviewable. Versions remain separate and cross-version
repetition consistency is not evaluated. No performance-based early stop.

Report scheduled/attempted/valid/invalid/error/interrupted counts, response latency
including client handling, available token usage, resolved model, primary route
and flag counts, and repeat-choice changes. These are workflow measurements, not
accuracy or reviewer-time savings. Do not treat agreements as clean examples or
disagreements as proven model errors. Every item remains subject to review;
NO_ISSUE_IDENTIFIED never auto-approves, hides or closes an item. There is no
confidence-based auto-disposition or published prioritization-benefit claim.

## Time and quality comparison

The author may complete the baseline form before opening item-level Jev suggestions,
then complete the assisted form for the same 24 items in the same order. The
baseline includes the same evidence, original question, reference and original
choice, but not pilot suggestions. Both passes record a route, concern notes,
active seconds and reviewer identity. The assisted pass additionally records
helpfulness (helpful/neutral/misleading/uncertain) and whether an important concern
was missed (yes/no/unassessed). No fields are filled by the assistant on behalf of
the reviewer. Prior exposure, interruptions and tooling overhead must be disclosed.

Report paired baseline-minus-assisted active time per item and its median, total
human active time, Jev request time, and separately logged setup/checking/repair
overhead. A net workflow saving requires the overhead measurement; missing overhead
means net saving is unmeasured. Exported browser timers and self-reports are
editable records, not independent verification. Baseline-first repeated exposure
confounds assistance with learning/fatigue; there is no causal speedup claim.

Report all helpfulness and missed-concern categories, all changes in the author's
route, and notes on corrections. Baseline choices are not a quality oracle. No
sensitivity, specificity or false-negative rate can be established without an
independent issue inventory. A favorable time result with unassessed/missed
concerns does not establish that quality was preserved. Human comparison outcomes
stay null until actual records exist; program execution never fabricates them.

The forms are conveniences, not access-control or blinding mechanisms. If the
reviewer sees suggestions before baseline, retain that disclosure and describe the
comparison as exposed. An independent, randomized study would be a later design.

## Operational boundaries

Credential-free tests/dry-run/mock are separate from explicit live execution.
API keys stay outside Git. No provider messages, credential changes, original
adjudication closures, release replacements, or source edits occur in this pilot.
Any post-output repair of frozen code/questions uses a new version. The TypeSafe
skill and official Choice/SDK documentation were consulted. SDK/examples are not
evidence of diagnostic accuracy.

Commands from repository root:

```sh
python -B -m unittest discover -s experiments/jev/review_queue_v1/tests -v
python -B -m experiments.jev.review_queue_v1.pilot --mode dry-run --output experiments/jev/review_queue_v1/runs/plan-001
python -B -m experiments.jev.review_queue_v1.pilot --mode mock --output experiments/jev/review_queue_v1/runs/mock-001
```

Live mode requires `--mode live --execute`, a private TYPESAFE_API_KEY, a committed
freeze and a fresh output path. This protocol is an internal prespecification,
not external registration. Core TAE validation stays deterministic and credential-free.
