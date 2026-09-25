# Protocol: jev-tae-v1

The question is whether Jev reproduces TAE's existing categorical synthetic contract and responds to prespecified evidence mutations. This protocol freezes the initial question set before any live inference. Human reviewers retain all authority over research claims and subsequent changes.

## Mapping and freeze

The source revision is `7f2c12b21cff50dcadefafcafccbaa5ef946d7b2`. `questions-v1.json` defines one Choice question for each of the 12 trust propositions and nine practical-control stages in `analysis/assessment.py`. Every entry carries its assessment, field and source path. Its criteria encode the existing signal-to-label contract. All 252 mappings are defensible as contract agreement tests because each fixture has exactly one categorical signal for each oracle field. No mapping is asserted for public-case evidence or overall human control.

The nine control questions address access, comprehension, authority, feasibility, exercise, effect, correction, repair and reform separately. Five-way Choice retains supported, partially_supported, unsupported, indeterminate and outside_scope. These evidence classes must not be collapsed into a binary probability: uncertainty in a model answer and indeterminate evidence are different things. The experiment asks no composite control question.

`frozen-v1.json` hashes the exact question-file bytes. The runner verifies this hash and every file in TAE's sealed oracle manifest before execution. Future question changes require a new versioned question file, freeze and documented protocol amendment; do not silently revise v1 after observing results. This initial freeze is an internal prespecification, not independent preregistration.

## Input and oracle separation

Only trust signals, control signals, outcome context and autonomy enter model state. The title and purpose contain answer cues and are excluded, along with case identity. Oracle labels, expected mutation deltas and generated assessments never enter requests. Question criteria expose the published mapping by design; this is a constrained instruction-following experiment. The runner reads gold labels solely for local comparisons.

## Execution and analysis

Use pinned `typesafe-sdk==0.7.1` and default model `jev-1.13.0`. Save requested and resolved versions separately. Run all baseline cases once, with one request containing 21 questions per case. TypeSafe evaluates questions independently against the shared state. Keep full class distributions and confidence separately. Report agreement counts, confusion tables from the saved rows, and mean multiclass Brier loss with explicit denominators. Calibration plots or estimates are exploratory with only 12 constructed cases; do not treat the 252 dependent determinations as independent samples or select a threshold using these same fixtures.

A response must contain exactly the requested question identifiers, valid Choice labels, finite probabilities and confidence in [0,1], probability sums within 1e-5 of one, and a maximum-probability selected label. Invalid responses are retained and excluded from scoring, with their failures counted. Preserve zero probabilities without adding an undocumented floor; log-loss calculations require a separately declared policy.

## Governance mutations

`--mutations` copies cases in memory and applies the sealed 12-mutation suite. Expected mutated labels derive only from sealed base labels and prespecified deltas. Compare the full observed 21-field before/after delta set with the expected set, and log the maximum probability shift. Extra changes count as delta mismatches. Erroring pairs remain not_evaluated.

Mutations exercise access timing, advisory authority, ineffective authority, mutable records, incomplete correction, bypassed monitoring, missing evidence, failed repair and absent reform. Title, outcome and impact-radius mutations test invariance. Title is removed by normalization, so its input-identical result tests the adapter boundary only. Outcome and impact radius remain in state, so those tests can reveal model sensitivity to irrelevant fields. Repeated API outputs may vary even for identical requests; an observed shift alone does not establish a causal effect.

## Verified provider surface

Official documentation checked September 25, 2026:

- [Python SDK](https://docs.typesafe.ai/sdk/python): distribution `typesafe-sdk`, import `typesafe_sdk`.
- [Synchronous client](https://docs.typesafe.ai/sdk/python/api/clients/sync): `TypeSafeClient.system_one(state=..., questions=..., model=...)`, dictionary questions, `RetryPolicy(max_retries=0)`, timeouts and custom HTTP transport.
- [Responses](https://docs.typesafe.ai/sdk/python/api/types/responses): answer map, resolved model, usage and `raw_http_response`.
- [SDK changelog](https://docs.typesafe.ai/sdk/python/changelog): version 0.7.1.
- [Models](https://docs.typesafe.ai/models): versioned model `jev-1.13.0` and moving aliases.

The installed SDK is exercised with an in-memory HTTP transport, including endpoint and request-shape assertions. No community endpoint or invented SDK surface is used.
