# Jev experiments: current guide

Jev is an optional experimental evaluator within TAE. Core TAE validation remains
deterministic and credential-free. The current published repository release is
v0.17.2; the paper remains v0.17.0. Later pilot and collaborative-review records
are separate additions, not revisions of released research conclusions.

## Experiment map

| Experiment | Question | Record |
| --- | --- | --- |
| JEV-TAE-1: contract fidelity | Does Jev translate categorical synthetic signals into the assessment contract? | [Original frozen experiment](../experiments/jev/README.md) |
| JEV-TAE-2: evidence reconstruction | Does Jev classify bounded documentary-style evidence consistently with authored references? | [Evidence-v2](../experiments/jev/evidence_v2/README.md) |
| JEV-TAE-3: mutation sensitivity | Do governance-relevant changes produce the prespecified exact changes? | [Live report](../experiments/jev/live_results_v1/REPORT.md) |
| JEV-TAE-4: invariance | Do irrelevant wording, order, context and paraphrases change judgments? | [Live report](../experiments/jev/live_results_v1/REPORT.md) |
| JEV-TAE-5: holdout transfer | How do judgments compare on the separately frozen synthetic holdout? | [Live report](../experiments/jev/live_results_v1/REPORT.md) |
| JEV-TAE-6: public-case comparison | How would the method compare on public cases? | Deferred; no result claimed |

The original experiment README and evidence-v1 files are historical frozen
materials. Their instructions should be read in that scope. For the executed
evidence-v2 run, consult the [separate live bridge](../experiments/jev/live_v1/README.md).
The bridge is optional; saved-result verification requires no live call.

## Completed execution and open interpretation

The first live evidence-v2 schedule attempted 282 requests with Jev 1.13.0:
260 valid and 22 invalid, with no retries. Primary reconstruction agreement was
198/231 valid determinations, with 231/252 coverage. These are synthetic agreement
measurements against authored references, not independently established accuracy.
The [post-output diagnostics](../experiments/jev/live_followup_v1/README.md)
preserve probability-sum failures and partial-state disagreements. All 1,079
original adjudication records remain unresolved; later author approvals do not
close them or rescore the run.

## Separate review-assistance pilot

The [development pilot](../experiments/jev/review_queue_results_v1/README.md)
selected 24 already exposed items and ran three repetitions: 70 of 72 responses
were valid. Median request duration was 0.168 seconds, including client handling.
This measures request latency, not total review effort. The planned timed human
comparison was omitted; its baseline export contained no saved assessments.

The later [collaborative author review](../experiments/jev/collaborative_review_v1/README.md)
preserves 24 approved assessments or bounded interpretations. Codex explained
evidence and proposed conclusions; the author approved them in conversation.
Items 8 and 16 retain unresolved classifications. Prior exposure, repeated
excerpts, answer changes and concerns are retained. This did not complete the
original baseline/assisted forms and provides no independent validation or causal
estimate of review benefit. Human time savings and quality improvement remain
unmeasured.

## Verification and future work

Use the [reproducibility guide](REPRODUCIBILITY.md) for offline commands. A saved
hash or passing test establishes the stated integrity checks, not source truth.
The collaborative-review package also records a local historical-replay limitation
in its [verification note](../experiments/jev/collaborative_review_v1/VERIFICATION.md).

Any future live comparison needs a separately documented design accounting for
prior exposure. Preserve existing freezes, raw outputs and invalid responses.
Keep credentials outside the repository. Do not normalize observed failures,
replace historical runs, or treat model/reference agreement as independent truth.
