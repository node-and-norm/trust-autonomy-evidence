# Post-output examination of live-001

This author-directed, AI-assisted examination follows the author's acceptance of
the first live results on 2 October 2026 (America/New_York). It is explicitly
post-output and is not independent adjudication. The original run, report,
probabilities, reference labels and 1,079 open UNRESOLVED records remain unchanged.
No new Jev requests were made for this analysis.

## Probability-sum failures

The 22 invalid requests contain 23 distributions whose probabilities sum to
approximately 0.99 rather than 1.00. The frozen validator uses an absolute
tolerance of 0.00001, and rejects the entire request if any distribution fails.
Consequently, 462 determinations were excluded, although only 23 distributions
triggered the sum check. The other 439 subanswers were not recovered or rescored.

The common one-percentage-point deficit is compatible with an output-rounding
issue, but the saved values do not establish how TypeSafe produced them. It is
not evidence that the underlying categorical decisions are all wrong. It is also
not permission to normalize the values after observing results. The appropriate
provider question is whether the API deliberately rounds each class probability
independently, and what precision/normalization contract consumers should expect.
No message has been sent to the provider as part of this examination.

Any relaxed tolerance or renormalization would be a labeled post-output sensitivity
analysis or a prospectively amended experiment. Neither is included here.

## Partial-state disagreements

Primary repetition 1 shows the following valid partial-reference determinations:

| Suite | Partial reference retained | Predicted unsupported | Valid partial / scheduled partial |
| --- | --- | --- | --- |
| Reconstruction | 20 | 32 | 52/63 |
| Authority challenge | 0 | 5 | 5/5 |
| Compositional holdout | 10 | 16 | 26/26 |

These are descriptions of agreement with an authored key, not final error
diagnoses. `diagnostics.json` gives every construct and disagreement reference for
all suites and repetitions, without pooling dependent observations.

The five primary authority disagreements concern binding delay, suspend, cancel,
override and approval-required permission without recorded use. Each excerpt
states that permission is granted and that no use is recorded. The frozen
question asks about permission **used with a corresponding operational response**;
its partial criterion allows a declaration, limited record or incomplete
demonstration. Its general criteria also distinguish absent records from contrary
observations. The reference applies the permission-without-recorded-use case as
partial support.

This exposes a boundary worth reviewing: partial evidence toward the complete
proposition versus demonstrated non-satisfaction of that proposition. Missing
records of exercise must not silently become proof that exercise did not occur.
The outputs contain choices and probabilities, not explanations of the model's
reasoning, so they cannot establish why it selected unsupported.

Candidate explanations include model misapplication of the partial-state rule,
question/criterion tension, construct ambiguity, or a disputed experimental
reference. They remain candidates, not assigned dispositions. The source
categorical oracle and the authored documentary translation are distinct; neither
the model nor the reference is treated as infallible.

## Next research decision

Preserve live-001 as the original unadjusted run. A provider-contract clarification
and a separately designed partial-state diagnostic would address different
questions. Any revised wording, reference, validator or new request requires a
versioned post-output amendment before use. Do not describe a new diagnostic as
unseen or tune it while claiming the original holdout remains untouched by output
exposure. No automatic rerun, revised question or new experiment is authorized by
this report itself.

The author's acceptance permits merging and release; it is not independent
review, does not retrospectively complete the original two-human review route,
and does not close the preserved adjudication records. The v0.17.0 paper findings,
sealed oracle and historical releases remain unchanged. CEC is context only.

## Reproduce

```sh
python -B -m experiments.jev.live_followup_v1.analyze --check
```

The script verifies the saved archive and frozen corpus first, then reproduces
descriptive diagnostics. It requires no credentials or optional TypeSafe SDK.
