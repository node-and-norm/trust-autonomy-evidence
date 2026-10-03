# First live Jev evidence-v2 report

All 282 scheduled requests were attempted once. There were 260 valid and 22 invalid responses; no transport errors, retries or interruptions. The run status is `incomplete` because invalid requests retain missing determinations. This is a synthetic agreement experiment, not independent scientific validation.

## Execution and provenance

- Run: `live-001`; mode: `live`; started `2026-10-03T01:54:26.868677+00:00`, finished `2026-10-03T01:55:38.784138+00:00` (UTC).
- Source/bridge commit: `f9b404a60ef8fd731495839c2b335e1c135f75e8`; frozen evidence-v2 manifest: `5ecc3e4594d027f6c25d7f1a389beeb465457f263c224b3d43f02bf6cf5450a7`.
- Requested and resolved model: `jev-1.13.0`; SDK: `0.7.1`. No missing resolved-version metadata.
- Schedule: 94 packets × 3 repetitions; 4,962 scheduled determinations, 4,500 valid. Repetition 1 is primary. Original ordering retained.
- No live outputs were observed by the implementing assistant before the freezes and pre-execution review. The author previously confirmed no external live TAE outputs. This is not independently verified exposure history.
- The bridge review was AI-assisted and author-directed, not independent review. CEC sandbox evidence was not imported.
- Provider-reported usage: 1,494,666 input tokens and 295,014 output tokens. This is usage metadata, not a billing receipt.
- `live-001.tar.gz` retains every canonical request, actual SDK body, raw response, original schedule, run record, reports, environment inventory, preflight and pre-execution review.
- `manifest.json` hashes the archive and every member. `report.json` is the full machine-readable frozen analysis. Credential value was checked absent before packaging.

## Primary results: repetition 1

Agreement denominators include only valid determinations; coverage is shown to expose missingness. Suites remain separate.

| Suite | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| authority | 16/16 | 11/16 (68.75%) | 5/16 | 0.503500 |
| boundary | 63/63 | 55/63 (87.30%) | 8/63 | 0.179806 |
| holdout | 126/126 | 110/126 (87.30%) | 16/126 | 0.158368 |
| invariance | 903/1008 | 753/903 (83.39%) | 150/903 | 0.216545 |
| mutation | 189/189 | 186/189 (98.41%) | 3/189 | 0.025114 |
| reconstruction | 231/252 | 198/231 (85.71%) | 33/231 | 0.197269 |

## Invalid responses

All 22 invalid responses failed `probabilities do not sum to one`. 23 question-level distributions failed within those requests. Under the frozen rule, the entire affected request is invalid; no probabilities are normalized and no valid-looking subanswers are rescued.

The raw records alone do not establish whether this is rounding, serialization, model behavior or another provider-side cause. `invalid-diagnostics.json` in the archive records the observed sums. Any later normalization or rule revision would be a separately labeled post-output analysis or amended experiment.

## Sensitivity, invariance and repetition

| Repetition | Pair suite | Exact deltas / evaluable | Scheduled | Choice invariance failures |
| --- | --- | --- | --- | --- |
| 1 | boundary | 3/3 | 3 | 0 |
| 1 | invariance | 32/39 | 48 | 7 |
| 1 | mutation | 7/9 | 9 | None |
| 2 | boundary | 2/3 | 3 | 1 |
| 2 | invariance | 32/41 | 48 | 9 |
| 2 | mutation | 6/8 | 9 | None |
| 3 | boundary | 2/2 | 3 | 0 |
| 3 | invariance | 27/34 | 48 | 7 |
| 3 | mutation | 7/9 | 9 | None |

Mutation pairs require the entire observed from/to set to match, including unchanged fields. The following diagnostic counts are descriptive, may overlap within a pair, and do not replace the frozen exact-delta score.

| Repetition | Missing expected fields | Extra changed fields | Wrong from/to values on shared fields |
| --- | --- | --- | --- |
| 1 | 0 | 0 | 3 |
| 2 | 0 | 0 | 3 |
| 3 | 0 | 0 | 3 |

| Repetition | Nuisance | Choice failures / evaluable | Scheduled | Maximum probability shift |
| --- | --- | --- | --- | --- |
| 1 | context | 1/9 | 12 | 0.150000 |
| 1 | order | 3/10 | 12 | 0.350000 |
| 1 | paraphrase | 3/9 | 12 | 0.260000 |
| 1 | wording | 0/11 | 12 | 0.100000 |
| 2 | context | 0/10 | 12 | 0.150000 |
| 2 | order | 4/10 | 12 | 0.320000 |
| 2 | paraphrase | 3/10 | 12 | 0.170000 |
| 2 | wording | 2/11 | 12 | 0.090000 |
| 3 | context | 2/9 | 12 | 0.180000 |
| 3 | order | 2/8 | 12 | 0.340000 |
| 3 | paraphrase | 3/9 | 12 | 0.200000 |
| 3 | wording | 0/8 | 12 | 0.200000 |

Repeated-request variability was evaluable for 74/94 packets. 10 had at least one choice change across the three repetitions. Maximum probability shift among evaluable packets: 0.200000.

Input-identical boundary pairs are reported separately above. Unavailable pairs remain visible in `report.json`; there were no resolved-version mismatches. Probability shifts are descriptive, with no post-hoc tolerance or causal claim.

## Adjudication

1079 records remain open and UNRESOLVED: 617 valid-output disagreements and 462 determinations in invalid requests. Closed records: zero. Each of JEV_ERROR, ORACLE_AMBIGUITY, QUESTION_DEFECT, EVIDENCE_TRANSLATION_DEFECT, CONSTRUCT_AMBIGUITY and INSUFFICIENT_EVIDENCE has zero assigned dispositions.

The archive preserves original records and their dated v2 imports, source hashes and downstream status `not_assessed`. There are no fabricated reviewer identities, blind notes or reconciliation. Author acceptance of the earlier AI-assisted corpus review does not supply two independent reviewers for these outcomes. Raw scores have not been adjusted.

## Evidence, inference and unresolved questions

**Observed:** the primary reconstruction suite agreed with the frozen references on 198/231 valid determinations, with 231/252 coverage. The authority set agreed on 11/16; all five partial-reference authority cases were classified unsupported. Holdout agreement was 110/126. Primary mutation exact deltas matched in 7/9 pairs; nuisance choice changes occurred in 7/39 evaluable pairs out of 48 scheduled.

**Bounded inference:** partial-state interpretation is a useful focus for adjudication. These observations do not by themselves distinguish model error from question, construct or translation ambiguity. The authored reference is not presumed infallible.

**Unresolved:** the probability-sum failures, the causes of partial-state disagreement, and the validity of the synthetic operationalization require further work. Repeated templates, dependent case families, topic-isolated excerpts, public compositional holdouts and author/AI design exposure limit generalization. No population confidence interval, significance test, model superiority, real-world control finding or empirical calibration claim is made.

The author-approved AI-assisted successor route remains disclosed; no independent or delayed unassisted review is claimed. No evidence-v1 pooling or released TAE conclusion changes. JEV-TAE-6 public cases remain deferred.

## Detailed frozen metrics

Every suite/repetition below includes all constructs, a five-class confusion matrix (gold rows), and recall with valid and scheduled gold counts. `pooled_secondary` is descriptive only; repetition 1 remains primary.

### authority · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 16/16 | 11/16 | 5/16 | 0.503500 |
| control__authority | 16/16 | 11/16 | 5/16 | 0.503500 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 5 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 5 | 0 | 0 |
| unsupported | 0 | 0 | 6 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 5/5 | 5 | 1.000000 |
| partially_supported | 0/5 | 5 | 0.000000 |
| unsupported | 6/6 | 6 | 1.000000 |
| indeterminate | 0/0 | 0 | null |
| outside_scope | 0/0 | 0 | null |

### boundary · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 63/63 | 55/63 | 8/63 | 0.179806 |
| control__access | 3/3 | 3/3 | 0/3 | 0.006800 |
| control__authority | 3/3 | 2/3 | 1/3 | 0.432133 |
| control__comprehension | 3/3 | 3/3 | 0/3 | 0.153600 |
| control__correction | 3/3 | 2/3 | 1/3 | 0.201667 |
| control__effect | 3/3 | 3/3 | 0/3 | 0.003267 |
| control__exercise | 3/3 | 3/3 | 0/3 | 0.028133 |
| control__feasibility | 3/3 | 3/3 | 0/3 | 0.023000 |
| control__reform | 3/3 | 3/3 | 0/3 | 0.053333 |
| control__repair | 3/3 | 2/3 | 1/3 | 0.277533 |
| trust__capability | 3/3 | 3/3 | 0/3 | 0.141600 |
| trust__evidence_completeness | 3/3 | 2/3 | 1/3 | 0.510467 |
| trust__governance_update | 3/3 | 3/3 | 0/3 | 0.009133 |
| trust__harm_correction | 3/3 | 2/3 | 1/3 | 0.481733 |
| trust__human_authority | 3/3 | 2/3 | 1/3 | 0.375000 |
| trust__identity | 3/3 | 3/3 | 0/3 | 0.005533 |
| trust__integrity | 3/3 | 2/3 | 1/3 | 0.523400 |
| trust__monitoring | 3/3 | 3/3 | 0/3 | 0.019133 |
| trust__reconstructability | 3/3 | 2/3 | 1/3 | 0.437533 |
| trust__reliability | 3/3 | 3/3 | 0/3 | 0.002400 |
| trust__scope | 3/3 | 3/3 | 0/3 | 0.089733 |
| trust__uncertainty | 3/3 | 3/3 | 0/3 | 0.000800 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 42 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 9 | 8 | 0 | 0 |
| unsupported | 0 | 0 | 0 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 4 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 42/42 | 42 | 1.000000 |
| partially_supported | 9/17 | 17 | 0.529412 |
| unsupported | 0/0 | 0 | null |
| indeterminate | 4/4 | 4 | 1.000000 |
| outside_scope | 0/0 | 0 | null |

### holdout · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 126/126 | 110/126 | 16/126 | 0.158368 |
| control__access | 6/6 | 6/6 | 0/6 | 0.047633 |
| control__authority | 6/6 | 5/6 | 1/6 | 0.270433 |
| control__comprehension | 6/6 | 5/6 | 1/6 | 0.101400 |
| control__correction | 6/6 | 6/6 | 0/6 | 0.009133 |
| control__effect | 6/6 | 6/6 | 0/6 | 0.008300 |
| control__exercise | 6/6 | 6/6 | 0/6 | 0.006633 |
| control__feasibility | 6/6 | 6/6 | 0/6 | 0.001167 |
| control__reform | 6/6 | 4/6 | 2/6 | 0.417167 |
| control__repair | 6/6 | 5/6 | 1/6 | 0.093133 |
| trust__capability | 6/6 | 6/6 | 0/6 | 0.031000 |
| trust__evidence_completeness | 6/6 | 4/6 | 2/6 | 0.522567 |
| trust__governance_update | 6/6 | 5/6 | 1/6 | 0.241367 |
| trust__harm_correction | 6/6 | 4/6 | 2/6 | 0.390800 |
| trust__human_authority | 6/6 | 5/6 | 1/6 | 0.228033 |
| trust__identity | 6/6 | 6/6 | 0/6 | 0.008667 |
| trust__integrity | 6/6 | 5/6 | 1/6 | 0.242433 |
| trust__monitoring | 6/6 | 5/6 | 1/6 | 0.169733 |
| trust__reconstructability | 6/6 | 5/6 | 1/6 | 0.224433 |
| trust__reliability | 6/6 | 6/6 | 0/6 | 0.007667 |
| trust__scope | 6/6 | 5/6 | 1/6 | 0.104333 |
| trust__uncertainty | 6/6 | 5/6 | 1/6 | 0.199700 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 25 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 10 | 16 | 0 | 0 |
| unsupported | 0 | 0 | 25 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 25 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 25 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 25/25 | 25 | 1.000000 |
| partially_supported | 10/26 | 26 | 0.384615 |
| unsupported | 25/25 | 25 | 1.000000 |
| indeterminate | 25/25 | 25 | 1.000000 |
| outside_scope | 25/25 | 25 | 1.000000 |

### invariance · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 903/1008 | 753/903 | 150/903 | 0.216545 |
| control__access | 43/48 | 40/43 | 3/43 | 0.086535 |
| control__authority | 43/48 | 29/43 | 14/43 | 0.430949 |
| control__comprehension | 43/48 | 39/43 | 4/43 | 0.139009 |
| control__correction | 43/48 | 35/43 | 8/43 | 0.170363 |
| control__effect | 43/48 | 43/43 | 0/43 | 0.006116 |
| control__exercise | 43/48 | 43/43 | 0/43 | 0.014544 |
| control__feasibility | 43/48 | 43/43 | 0/43 | 0.013051 |
| control__reform | 43/48 | 31/43 | 12/43 | 0.444465 |
| control__repair | 43/48 | 30/43 | 13/43 | 0.229102 |
| trust__capability | 43/48 | 41/43 | 2/43 | 0.096498 |
| trust__evidence_completeness | 43/48 | 25/43 | 18/43 | 0.620223 |
| trust__governance_update | 43/48 | 31/43 | 12/43 | 0.399265 |
| trust__harm_correction | 43/48 | 29/43 | 14/43 | 0.410363 |
| trust__human_authority | 43/48 | 33/43 | 10/43 | 0.247177 |
| trust__identity | 43/48 | 43/43 | 0/43 | 0.010391 |
| trust__integrity | 43/48 | 33/43 | 10/43 | 0.352460 |
| trust__monitoring | 43/48 | 31/43 | 12/43 | 0.259716 |
| trust__reconstructability | 43/48 | 29/43 | 14/43 | 0.486316 |
| trust__reliability | 43/48 | 43/43 | 0/43 | 0.004870 |
| trust__scope | 43/48 | 43/43 | 0/43 | 0.047619 |
| trust__uncertainty | 43/48 | 39/43 | 4/43 | 0.078409 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 452 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 71 | 147 | 0 | 0 |
| unsupported | 0 | 0 | 142 | 0 | 0 |
| indeterminate | 0 | 0 | 3 | 68 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 20 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 452/452 | 452 | 1.000000 |
| partially_supported | 71/218 | 252 | 0.325688 |
| unsupported | 142/142 | 184 | 1.000000 |
| indeterminate | 68/71 | 100 | 0.957746 |
| outside_scope | 20/20 | 20 | 1.000000 |

### mutation · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 189/189 | 186/189 | 3/189 | 0.025114 |
| control__access | 9/9 | 9/9 | 0/9 | 0.008711 |
| control__authority | 9/9 | 9/9 | 0/9 | 0.006289 |
| control__comprehension | 9/9 | 9/9 | 0/9 | 0.000022 |
| control__correction | 9/9 | 8/9 | 1/9 | 0.128400 |
| control__effect | 9/9 | 9/9 | 0/9 | 0.000000 |
| control__exercise | 9/9 | 9/9 | 0/9 | 0.038444 |
| control__feasibility | 9/9 | 9/9 | 0/9 | 0.000089 |
| control__reform | 9/9 | 9/9 | 0/9 | 0.072333 |
| control__repair | 9/9 | 9/9 | 0/9 | 0.000156 |
| trust__capability | 9/9 | 9/9 | 0/9 | 0.000733 |
| trust__evidence_completeness | 9/9 | 8/9 | 1/9 | 0.064289 |
| trust__governance_update | 9/9 | 9/9 | 0/9 | 0.008244 |
| trust__harm_correction | 9/9 | 8/9 | 1/9 | 0.172200 |
| trust__human_authority | 9/9 | 9/9 | 0/9 | 0.000600 |
| trust__identity | 9/9 | 9/9 | 0/9 | 0.000267 |
| trust__integrity | 9/9 | 9/9 | 0/9 | 0.001422 |
| trust__monitoring | 9/9 | 9/9 | 0/9 | 0.017800 |
| trust__reconstructability | 9/9 | 9/9 | 0/9 | 0.000533 |
| trust__reliability | 9/9 | 9/9 | 0/9 | 0.002156 |
| trust__scope | 9/9 | 9/9 | 0/9 | 0.004000 |
| trust__uncertainty | 9/9 | 9/9 | 0/9 | 0.000711 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 178 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 2 | 0 | 0 |
| unsupported | 0 | 0 | 8 | 0 | 0 |
| indeterminate | 0 | 0 | 1 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 178/178 | 178 | 1.000000 |
| partially_supported | 0/2 | 2 | 0.000000 |
| unsupported | 8/8 | 8 | 1.000000 |
| indeterminate | 0/1 | 1 | 0.000000 |
| outside_scope | 0/0 | 0 | null |

### reconstruction · repetition 1 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 231/252 | 198/231 | 33/231 | 0.197269 |
| control__access | 11/12 | 10/11 | 1/11 | 0.097600 |
| control__authority | 11/12 | 8/11 | 3/11 | 0.405018 |
| control__comprehension | 11/12 | 11/11 | 0/11 | 0.064636 |
| control__correction | 11/12 | 8/11 | 3/11 | 0.215818 |
| control__effect | 11/12 | 11/11 | 0/11 | 0.006236 |
| control__exercise | 11/12 | 11/11 | 0/11 | 0.011691 |
| control__feasibility | 11/12 | 11/11 | 0/11 | 0.022218 |
| control__reform | 11/12 | 9/11 | 2/11 | 0.269600 |
| control__repair | 11/12 | 8/11 | 3/11 | 0.222436 |
| trust__capability | 11/12 | 11/11 | 0/11 | 0.115273 |
| trust__evidence_completeness | 11/12 | 7/11 | 4/11 | 0.556836 |
| trust__governance_update | 11/12 | 9/11 | 2/11 | 0.260345 |
| trust__harm_correction | 11/12 | 8/11 | 3/11 | 0.370182 |
| trust__human_authority | 11/12 | 9/11 | 2/11 | 0.227836 |
| trust__identity | 11/12 | 11/11 | 0/11 | 0.008527 |
| trust__integrity | 11/12 | 8/11 | 3/11 | 0.433964 |
| trust__monitoring | 11/12 | 9/11 | 2/11 | 0.166818 |
| trust__reconstructability | 11/12 | 7/11 | 4/11 | 0.539927 |
| trust__reliability | 11/12 | 11/11 | 0/11 | 0.004036 |
| trust__scope | 11/12 | 11/11 | 0/11 | 0.072018 |
| trust__uncertainty | 11/12 | 10/11 | 1/11 | 0.071636 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 106 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 20 | 32 | 0 | 0 |
| unsupported | 0 | 0 | 43 | 0 | 0 |
| indeterminate | 0 | 0 | 1 | 24 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 5 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 106/106 | 113 | 1.000000 |
| partially_supported | 20/52 | 63 | 0.384615 |
| unsupported | 43/43 | 46 | 1.000000 |
| indeterminate | 24/25 | 25 | 0.960000 |
| outside_scope | 5/5 | 5 | 1.000000 |

### authority · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 16/16 | 11/16 | 5/16 | 0.496675 |
| control__authority | 16/16 | 11/16 | 5/16 | 0.496675 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 5 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 5 | 0 | 0 |
| unsupported | 0 | 0 | 6 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 5/5 | 5 | 1.000000 |
| partially_supported | 0/5 | 5 | 0.000000 |
| unsupported | 6/6 | 6 | 1.000000 |
| indeterminate | 0/0 | 0 | null |
| outside_scope | 0/0 | 0 | null |

### boundary · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 63/63 | 54/63 | 9/63 | 0.180968 |
| control__access | 3/3 | 3/3 | 0/3 | 0.013200 |
| control__authority | 3/3 | 2/3 | 1/3 | 0.453867 |
| control__comprehension | 3/3 | 2/3 | 1/3 | 0.180267 |
| control__correction | 3/3 | 2/3 | 1/3 | 0.264600 |
| control__effect | 3/3 | 3/3 | 0/3 | 0.003267 |
| control__exercise | 3/3 | 3/3 | 0/3 | 0.018000 |
| control__feasibility | 3/3 | 3/3 | 0/3 | 0.024867 |
| control__reform | 3/3 | 3/3 | 0/3 | 0.065200 |
| control__repair | 3/3 | 2/3 | 1/3 | 0.220600 |
| trust__capability | 3/3 | 3/3 | 0/3 | 0.112600 |
| trust__evidence_completeness | 3/3 | 2/3 | 1/3 | 0.498867 |
| trust__governance_update | 3/3 | 3/3 | 0/3 | 0.009133 |
| trust__harm_correction | 3/3 | 2/3 | 1/3 | 0.464933 |
| trust__human_authority | 3/3 | 2/3 | 1/3 | 0.360200 |
| trust__identity | 3/3 | 3/3 | 0/3 | 0.008200 |
| trust__integrity | 3/3 | 2/3 | 1/3 | 0.546933 |
| trust__monitoring | 3/3 | 3/3 | 0/3 | 0.018733 |
| trust__reconstructability | 3/3 | 2/3 | 1/3 | 0.426800 |
| trust__reliability | 3/3 | 3/3 | 0/3 | 0.002267 |
| trust__scope | 3/3 | 3/3 | 0/3 | 0.107067 |
| trust__uncertainty | 3/3 | 3/3 | 0/3 | 0.000733 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 42 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 8 | 9 | 0 | 0 |
| unsupported | 0 | 0 | 0 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 4 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 42/42 | 42 | 1.000000 |
| partially_supported | 8/17 | 17 | 0.470588 |
| unsupported | 0/0 | 0 | null |
| indeterminate | 4/4 | 4 | 1.000000 |
| outside_scope | 0/0 | 0 | null |

### holdout · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 126/126 | 111/126 | 15/126 | 0.161351 |
| control__access | 6/6 | 6/6 | 0/6 | 0.049533 |
| control__authority | 6/6 | 5/6 | 1/6 | 0.258600 |
| control__comprehension | 6/6 | 5/6 | 1/6 | 0.094433 |
| control__correction | 6/6 | 6/6 | 0/6 | 0.009067 |
| control__effect | 6/6 | 6/6 | 0/6 | 0.007300 |
| control__exercise | 6/6 | 6/6 | 0/6 | 0.005933 |
| control__feasibility | 6/6 | 6/6 | 0/6 | 0.001267 |
| control__reform | 6/6 | 4/6 | 2/6 | 0.418433 |
| control__repair | 6/6 | 6/6 | 0/6 | 0.082933 |
| trust__capability | 6/6 | 6/6 | 0/6 | 0.050500 |
| trust__evidence_completeness | 6/6 | 4/6 | 2/6 | 0.532400 |
| trust__governance_update | 6/6 | 5/6 | 1/6 | 0.254767 |
| trust__harm_correction | 6/6 | 4/6 | 2/6 | 0.413633 |
| trust__human_authority | 6/6 | 5/6 | 1/6 | 0.208933 |
| trust__identity | 6/6 | 6/6 | 0/6 | 0.016000 |
| trust__integrity | 6/6 | 5/6 | 1/6 | 0.242433 |
| trust__monitoring | 6/6 | 5/6 | 1/6 | 0.165133 |
| trust__reconstructability | 6/6 | 5/6 | 1/6 | 0.231900 |
| trust__reliability | 6/6 | 6/6 | 0/6 | 0.008733 |
| trust__scope | 6/6 | 5/6 | 1/6 | 0.141800 |
| trust__uncertainty | 6/6 | 5/6 | 1/6 | 0.194633 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 25 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 11 | 15 | 0 | 0 |
| unsupported | 0 | 0 | 25 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 25 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 25 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 25/25 | 25 | 1.000000 |
| partially_supported | 11/26 | 26 | 0.423077 |
| unsupported | 25/25 | 25 | 1.000000 |
| indeterminate | 25/25 | 25 | 1.000000 |
| outside_scope | 25/25 | 25 | 1.000000 |

### invariance · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 924/1008 | 766/924 | 158/924 | 0.218111 |
| control__access | 44/48 | 41/44 | 3/44 | 0.087945 |
| control__authority | 44/48 | 30/44 | 14/44 | 0.417632 |
| control__comprehension | 44/48 | 39/44 | 5/44 | 0.136682 |
| control__correction | 44/48 | 35/44 | 9/44 | 0.168673 |
| control__effect | 44/48 | 44/44 | 0/44 | 0.004282 |
| control__exercise | 44/48 | 44/44 | 0/44 | 0.014441 |
| control__feasibility | 44/48 | 44/44 | 0/44 | 0.012714 |
| control__reform | 44/48 | 32/44 | 12/44 | 0.424882 |
| control__repair | 44/48 | 31/44 | 13/44 | 0.229250 |
| trust__capability | 44/48 | 42/44 | 2/44 | 0.090995 |
| trust__evidence_completeness | 44/48 | 25/44 | 19/44 | 0.631545 |
| trust__governance_update | 44/48 | 32/44 | 12/44 | 0.377336 |
| trust__harm_correction | 44/48 | 29/44 | 15/44 | 0.437036 |
| trust__human_authority | 44/48 | 31/44 | 13/44 | 0.288050 |
| trust__identity | 44/48 | 44/44 | 0/44 | 0.011264 |
| trust__integrity | 44/48 | 33/44 | 11/44 | 0.383023 |
| trust__monitoring | 44/48 | 33/44 | 11/44 | 0.224945 |
| trust__reconstructability | 44/48 | 29/44 | 15/44 | 0.503755 |
| trust__reliability | 44/48 | 44/44 | 0/44 | 0.006200 |
| trust__scope | 44/48 | 44/44 | 0/44 | 0.053527 |
| trust__uncertainty | 44/48 | 40/44 | 4/44 | 0.076145 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 437 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 80 | 153 | 0 | 0 |
| unsupported | 2 | 0 | 157 | 0 | 0 |
| indeterminate | 0 | 0 | 3 | 72 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 20 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 437/437 | 452 | 1.000000 |
| partially_supported | 80/233 | 252 | 0.343348 |
| unsupported | 157/159 | 184 | 0.987421 |
| indeterminate | 72/75 | 100 | 0.960000 |
| outside_scope | 20/20 | 20 | 1.000000 |

### mutation · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 168/189 | 165/168 | 3/168 | 0.027680 |
| control__access | 8/9 | 8/8 | 0/8 | 0.009025 |
| control__authority | 8/9 | 8/8 | 0/8 | 0.004425 |
| control__comprehension | 8/9 | 8/8 | 0/8 | 0.000000 |
| control__correction | 8/9 | 7/8 | 1/8 | 0.148250 |
| control__effect | 8/9 | 8/8 | 0/8 | 0.000000 |
| control__exercise | 8/9 | 8/8 | 0/8 | 0.030825 |
| control__feasibility | 8/9 | 8/8 | 0/8 | 0.000125 |
| control__reform | 8/9 | 8/8 | 0/8 | 0.093075 |
| control__repair | 8/9 | 8/8 | 0/8 | 0.000150 |
| trust__capability | 8/9 | 8/8 | 0/8 | 0.000725 |
| trust__evidence_completeness | 8/9 | 7/8 | 1/8 | 0.066675 |
| trust__governance_update | 8/9 | 8/8 | 0/8 | 0.007075 |
| trust__harm_correction | 8/9 | 7/8 | 1/8 | 0.193675 |
| trust__human_authority | 8/9 | 8/8 | 0/8 | 0.001200 |
| trust__identity | 8/9 | 8/8 | 0/8 | 0.000200 |
| trust__integrity | 8/9 | 8/8 | 0/8 | 0.001500 |
| trust__monitoring | 8/9 | 8/8 | 0/8 | 0.015000 |
| trust__reconstructability | 8/9 | 8/8 | 0/8 | 0.000575 |
| trust__reliability | 8/9 | 8/8 | 0/8 | 0.003175 |
| trust__scope | 8/9 | 8/8 | 0/8 | 0.004950 |
| trust__uncertainty | 8/9 | 8/8 | 0/8 | 0.000650 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 159 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 2 | 0 | 0 |
| unsupported | 0 | 0 | 6 | 0 | 0 |
| indeterminate | 0 | 0 | 1 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 159/159 | 178 | 1.000000 |
| partially_supported | 0/2 | 2 | 0.000000 |
| unsupported | 6/6 | 8 | 1.000000 |
| indeterminate | 0/1 | 1 | 0.000000 |
| outside_scope | 0/0 | 0 | null |

### reconstruction · repetition 2 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 231/252 | 188/231 | 43/231 | 0.242833 |
| control__access | 11/12 | 10/11 | 1/11 | 0.100818 |
| control__authority | 11/12 | 7/11 | 4/11 | 0.454691 |
| control__comprehension | 11/12 | 10/11 | 1/11 | 0.164364 |
| control__correction | 11/12 | 7/11 | 4/11 | 0.269836 |
| control__effect | 11/12 | 11/11 | 0/11 | 0.007073 |
| control__exercise | 11/12 | 11/11 | 0/11 | 0.010691 |
| control__feasibility | 11/12 | 11/11 | 0/11 | 0.017491 |
| control__reform | 11/12 | 8/11 | 3/11 | 0.407673 |
| control__repair | 11/12 | 7/11 | 4/11 | 0.276727 |
| trust__capability | 11/12 | 11/11 | 0/11 | 0.112909 |
| trust__evidence_completeness | 11/12 | 6/11 | 5/11 | 0.707600 |
| trust__governance_update | 11/12 | 8/11 | 3/11 | 0.400218 |
| trust__harm_correction | 11/12 | 7/11 | 4/11 | 0.522709 |
| trust__human_authority | 11/12 | 8/11 | 3/11 | 0.301655 |
| trust__identity | 11/12 | 11/11 | 0/11 | 0.007891 |
| trust__integrity | 11/12 | 8/11 | 3/11 | 0.428364 |
| trust__monitoring | 11/12 | 8/11 | 3/11 | 0.199764 |
| trust__reconstructability | 11/12 | 7/11 | 4/11 | 0.555509 |
| trust__reliability | 11/12 | 11/11 | 0/11 | 0.003036 |
| trust__scope | 11/12 | 11/11 | 0/11 | 0.062618 |
| trust__uncertainty | 11/12 | 10/11 | 1/11 | 0.087855 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 113 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 21 | 42 | 0 | 0 |
| unsupported | 0 | 0 | 25 | 0 | 0 |
| indeterminate | 0 | 0 | 1 | 24 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 5 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 113/113 | 113 | 1.000000 |
| partially_supported | 21/63 | 63 | 0.333333 |
| unsupported | 25/25 | 46 | 1.000000 |
| indeterminate | 24/25 | 25 | 0.960000 |
| outside_scope | 5/5 | 5 | 1.000000 |

### authority · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 16/16 | 11/16 | 5/16 | 0.490475 |
| control__authority | 16/16 | 11/16 | 5/16 | 0.490475 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 5 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 5 | 0 | 0 |
| unsupported | 0 | 0 | 6 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 5/5 | 5 | 1.000000 |
| partially_supported | 0/5 | 5 | 0.000000 |
| unsupported | 6/6 | 6 | 1.000000 |
| indeterminate | 0/0 | 0 | null |
| outside_scope | 0/0 | 0 | null |

### boundary · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 42/63 | 42/42 | 0/42 | 0.008443 |
| control__access | 2/3 | 2/2 | 0/2 | 0.000200 |
| control__authority | 2/3 | 2/2 | 0/2 | 0.000000 |
| control__comprehension | 2/3 | 2/2 | 0/2 | 0.000000 |
| control__correction | 2/3 | 2/2 | 0/2 | 0.000000 |
| control__effect | 2/3 | 2/2 | 0/2 | 0.000000 |
| control__exercise | 2/3 | 2/2 | 0/2 | 0.022500 |
| control__feasibility | 2/3 | 2/2 | 0/2 | 0.000100 |
| control__reform | 2/3 | 2/2 | 0/2 | 0.113200 |
| control__repair | 2/3 | 2/2 | 0/2 | 0.000200 |
| trust__capability | 2/3 | 2/2 | 0/2 | 0.000800 |
| trust__evidence_completeness | 2/3 | 2/2 | 0/2 | 0.000000 |
| trust__governance_update | 2/3 | 2/2 | 0/2 | 0.014500 |
| trust__harm_correction | 2/3 | 2/2 | 0/2 | 0.000100 |
| trust__human_authority | 2/3 | 2/2 | 0/2 | 0.000000 |
| trust__identity | 2/3 | 2/2 | 0/2 | 0.000200 |
| trust__integrity | 2/3 | 2/2 | 0/2 | 0.001300 |
| trust__monitoring | 2/3 | 2/2 | 0/2 | 0.016200 |
| trust__reconstructability | 2/3 | 2/2 | 0/2 | 0.000200 |
| trust__reliability | 2/3 | 2/2 | 0/2 | 0.003200 |
| trust__scope | 2/3 | 2/2 | 0/2 | 0.003800 |
| trust__uncertainty | 2/3 | 2/2 | 0/2 | 0.000800 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 42 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 0 | 0 | 0 |
| unsupported | 0 | 0 | 0 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 42/42 | 42 | 1.000000 |
| partially_supported | 0/0 | 17 | null |
| unsupported | 0/0 | 0 | null |
| indeterminate | 0/0 | 4 | null |
| outside_scope | 0/0 | 0 | null |

### holdout · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 126/126 | 112/126 | 14/126 | 0.157376 |
| control__access | 6/6 | 6/6 | 0/6 | 0.050500 |
| control__authority | 6/6 | 5/6 | 1/6 | 0.252867 |
| control__comprehension | 6/6 | 6/6 | 0/6 | 0.071700 |
| control__correction | 6/6 | 6/6 | 0/6 | 0.006467 |
| control__effect | 6/6 | 6/6 | 0/6 | 0.007633 |
| control__exercise | 6/6 | 6/6 | 0/6 | 0.006800 |
| control__feasibility | 6/6 | 6/6 | 0/6 | 0.001600 |
| control__reform | 6/6 | 4/6 | 2/6 | 0.419567 |
| control__repair | 6/6 | 6/6 | 0/6 | 0.080100 |
| trust__capability | 6/6 | 6/6 | 0/6 | 0.034833 |
| trust__evidence_completeness | 6/6 | 4/6 | 2/6 | 0.538700 |
| trust__governance_update | 6/6 | 5/6 | 1/6 | 0.234433 |
| trust__harm_correction | 6/6 | 4/6 | 2/6 | 0.411467 |
| trust__human_authority | 6/6 | 5/6 | 1/6 | 0.242800 |
| trust__identity | 6/6 | 6/6 | 0/6 | 0.006933 |
| trust__integrity | 6/6 | 5/6 | 1/6 | 0.249067 |
| trust__monitoring | 6/6 | 5/6 | 1/6 | 0.159933 |
| trust__reconstructability | 6/6 | 5/6 | 1/6 | 0.234100 |
| trust__reliability | 6/6 | 6/6 | 0/6 | 0.010633 |
| trust__scope | 6/6 | 5/6 | 1/6 | 0.088100 |
| trust__uncertainty | 6/6 | 5/6 | 1/6 | 0.196667 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 25 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 12 | 14 | 0 | 0 |
| unsupported | 0 | 0 | 25 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 25 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 25 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 25/25 | 25 | 1.000000 |
| partially_supported | 12/26 | 26 | 0.461538 |
| unsupported | 25/25 | 25 | 1.000000 |
| indeterminate | 25/25 | 25 | 1.000000 |
| outside_scope | 25/25 | 25 | 1.000000 |

### invariance · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 882/1008 | 755/882 | 127/882 | 0.193517 |
| control__access | 42/48 | 39/42 | 3/42 | 0.082871 |
| control__authority | 42/48 | 30/42 | 12/42 | 0.386443 |
| control__comprehension | 42/48 | 37/42 | 5/42 | 0.121781 |
| control__correction | 42/48 | 34/42 | 8/42 | 0.153395 |
| control__effect | 42/48 | 42/42 | 0/42 | 0.009562 |
| control__exercise | 42/48 | 42/42 | 0/42 | 0.016443 |
| control__feasibility | 42/48 | 42/42 | 0/42 | 0.010438 |
| control__reform | 42/48 | 33/42 | 9/42 | 0.353257 |
| control__repair | 42/48 | 34/42 | 8/42 | 0.204557 |
| trust__capability | 42/48 | 38/42 | 4/42 | 0.096452 |
| trust__evidence_completeness | 42/48 | 26/42 | 16/42 | 0.576976 |
| trust__governance_update | 42/48 | 33/42 | 9/42 | 0.312590 |
| trust__harm_correction | 42/48 | 30/42 | 12/42 | 0.377919 |
| trust__human_authority | 42/48 | 34/42 | 8/42 | 0.229148 |
| trust__identity | 42/48 | 42/42 | 0/42 | 0.008567 |
| trust__integrity | 42/48 | 33/42 | 9/42 | 0.341643 |
| trust__monitoring | 42/48 | 33/42 | 9/42 | 0.211124 |
| trust__reconstructability | 42/48 | 29/42 | 13/42 | 0.474348 |
| trust__reliability | 42/48 | 42/42 | 0/42 | 0.005629 |
| trust__scope | 42/48 | 42/42 | 0/42 | 0.044324 |
| trust__uncertainty | 42/48 | 40/42 | 2/42 | 0.046395 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 445 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 58 | 124 | 0 | 0 |
| unsupported | 0 | 0 | 160 | 0 | 0 |
| indeterminate | 0 | 0 | 3 | 72 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 20 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 445/445 | 452 | 1.000000 |
| partially_supported | 58/182 | 252 | 0.318681 |
| unsupported | 160/160 | 184 | 1.000000 |
| indeterminate | 72/75 | 100 | 0.960000 |
| outside_scope | 20/20 | 20 | 1.000000 |

### mutation · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 189/189 | 186/189 | 3/189 | 0.026599 |
| control__access | 9/9 | 9/9 | 0/9 | 0.006378 |
| control__authority | 9/9 | 9/9 | 0/9 | 0.003933 |
| control__comprehension | 9/9 | 9/9 | 0/9 | 0.000000 |
| control__correction | 9/9 | 8/9 | 1/9 | 0.135222 |
| control__effect | 9/9 | 9/9 | 0/9 | 0.000000 |
| control__exercise | 9/9 | 9/9 | 0/9 | 0.030556 |
| control__feasibility | 9/9 | 9/9 | 0/9 | 0.000133 |
| control__reform | 9/9 | 9/9 | 0/9 | 0.092978 |
| control__repair | 9/9 | 9/9 | 0/9 | 0.000178 |
| trust__capability | 9/9 | 9/9 | 0/9 | 0.000956 |
| trust__evidence_completeness | 9/9 | 8/9 | 1/9 | 0.073800 |
| trust__governance_update | 9/9 | 9/9 | 0/9 | 0.010733 |
| trust__harm_correction | 9/9 | 8/9 | 1/9 | 0.176133 |
| trust__human_authority | 9/9 | 9/9 | 0/9 | 0.001667 |
| trust__identity | 9/9 | 9/9 | 0/9 | 0.000200 |
| trust__integrity | 9/9 | 9/9 | 0/9 | 0.001578 |
| trust__monitoring | 9/9 | 9/9 | 0/9 | 0.015800 |
| trust__reconstructability | 9/9 | 9/9 | 0/9 | 0.000600 |
| trust__reliability | 9/9 | 9/9 | 0/9 | 0.002311 |
| trust__scope | 9/9 | 9/9 | 0/9 | 0.004822 |
| trust__uncertainty | 9/9 | 9/9 | 0/9 | 0.000600 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 178 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 2 | 0 | 0 |
| unsupported | 0 | 0 | 8 | 0 | 0 |
| indeterminate | 0 | 0 | 1 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 178/178 | 178 | 1.000000 |
| partially_supported | 0/2 | 2 | 0.000000 |
| unsupported | 8/8 | 8 | 1.000000 |
| indeterminate | 0/1 | 1 | 0.000000 |
| outside_scope | 0/0 | 0 | null |

### reconstruction · repetition 3 · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 189/252 | 169/189 | 20/189 | 0.156268 |
| control__access | 9/12 | 9/9 | 0/9 | 0.028289 |
| control__authority | 9/12 | 7/9 | 2/9 | 0.350178 |
| control__comprehension | 9/12 | 9/9 | 0/9 | 0.047067 |
| control__correction | 9/12 | 7/9 | 2/9 | 0.168200 |
| control__effect | 9/12 | 9/9 | 0/9 | 0.001956 |
| control__exercise | 9/12 | 9/9 | 0/9 | 0.009644 |
| control__feasibility | 9/12 | 9/9 | 0/9 | 0.011289 |
| control__reform | 9/12 | 8/9 | 1/9 | 0.203356 |
| control__repair | 9/12 | 7/9 | 2/9 | 0.173444 |
| trust__capability | 9/12 | 9/9 | 0/9 | 0.076800 |
| trust__evidence_completeness | 9/12 | 6/9 | 3/9 | 0.495533 |
| trust__governance_update | 9/12 | 8/9 | 1/9 | 0.190800 |
| trust__harm_correction | 9/12 | 7/9 | 2/9 | 0.302511 |
| trust__human_authority | 9/12 | 8/9 | 1/9 | 0.191600 |
| trust__identity | 9/12 | 9/9 | 0/9 | 0.003667 |
| trust__integrity | 9/12 | 7/9 | 2/9 | 0.372844 |
| trust__monitoring | 9/12 | 8/9 | 1/9 | 0.104778 |
| trust__reconstructability | 9/12 | 6/9 | 3/9 | 0.489600 |
| trust__reliability | 9/12 | 9/9 | 0/9 | 0.003422 |
| trust__scope | 9/12 | 9/9 | 0/9 | 0.055778 |
| trust__uncertainty | 9/12 | 9/9 | 0/9 | 0.000867 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 106 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 11 | 20 | 0 | 0 |
| unsupported | 0 | 0 | 43 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 4 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 5 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 106/106 | 113 | 1.000000 |
| partially_supported | 11/31 | 63 | 0.354839 |
| unsupported | 43/43 | 46 | 1.000000 |
| indeterminate | 4/4 | 25 | 1.000000 |
| outside_scope | 5/5 | 5 | 1.000000 |

### authority · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 48/48 | 33/48 | 15/48 | 0.496883 |
| control__authority | 48/48 | 33/48 | 15/48 | 0.496883 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 15 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 15 | 0 | 0 |
| unsupported | 0 | 0 | 18 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 15/15 | 15 | 1.000000 |
| partially_supported | 0/15 | 15 | 0.000000 |
| unsupported | 18/18 | 18 | 1.000000 |
| indeterminate | 0/0 | 0 | null |
| outside_scope | 0/0 | 0 | null |

### boundary · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 168/189 | 151/168 | 17/168 | 0.137401 |
| control__access | 8/9 | 8/8 | 0/8 | 0.007550 |
| control__authority | 8/9 | 6/8 | 2/8 | 0.332250 |
| control__comprehension | 8/9 | 7/8 | 1/8 | 0.125200 |
| control__correction | 8/9 | 6/8 | 2/8 | 0.174850 |
| control__effect | 8/9 | 8/8 | 0/8 | 0.002450 |
| control__exercise | 8/9 | 8/8 | 0/8 | 0.022925 |
| control__feasibility | 8/9 | 8/8 | 0/8 | 0.017975 |
| control__reform | 8/9 | 8/8 | 0/8 | 0.072750 |
| control__repair | 8/9 | 6/8 | 2/8 | 0.186850 |
| trust__capability | 8/9 | 8/8 | 0/8 | 0.095525 |
| trust__evidence_completeness | 8/9 | 6/8 | 2/8 | 0.378500 |
| trust__governance_update | 8/9 | 8/8 | 0/8 | 0.010475 |
| trust__harm_correction | 8/9 | 6/8 | 2/8 | 0.355025 |
| trust__human_authority | 8/9 | 6/8 | 2/8 | 0.275700 |
| trust__identity | 8/9 | 8/8 | 0/8 | 0.005200 |
| trust__integrity | 8/9 | 6/8 | 2/8 | 0.401700 |
| trust__monitoring | 8/9 | 8/8 | 0/8 | 0.018250 |
| trust__reconstructability | 8/9 | 6/8 | 2/8 | 0.324175 |
| trust__reliability | 8/9 | 8/8 | 0/8 | 0.002550 |
| trust__scope | 8/9 | 8/8 | 0/8 | 0.074750 |
| trust__uncertainty | 8/9 | 8/8 | 0/8 | 0.000775 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 126 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 17 | 17 | 0 | 0 |
| unsupported | 0 | 0 | 0 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 8 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 126/126 | 126 | 1.000000 |
| partially_supported | 17/34 | 51 | 0.500000 |
| unsupported | 0/0 | 0 | null |
| indeterminate | 8/8 | 12 | 1.000000 |
| outside_scope | 0/0 | 0 | null |

### holdout · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 378/378 | 333/378 | 45/378 | 0.159032 |
| control__access | 18/18 | 18/18 | 0/18 | 0.049222 |
| control__authority | 18/18 | 15/18 | 3/18 | 0.260633 |
| control__comprehension | 18/18 | 16/18 | 2/18 | 0.089178 |
| control__correction | 18/18 | 18/18 | 0/18 | 0.008222 |
| control__effect | 18/18 | 18/18 | 0/18 | 0.007744 |
| control__exercise | 18/18 | 18/18 | 0/18 | 0.006456 |
| control__feasibility | 18/18 | 18/18 | 0/18 | 0.001344 |
| control__reform | 18/18 | 12/18 | 6/18 | 0.418389 |
| control__repair | 18/18 | 17/18 | 1/18 | 0.085389 |
| trust__capability | 18/18 | 18/18 | 0/18 | 0.038778 |
| trust__evidence_completeness | 18/18 | 12/18 | 6/18 | 0.531222 |
| trust__governance_update | 18/18 | 15/18 | 3/18 | 0.243522 |
| trust__harm_correction | 18/18 | 12/18 | 6/18 | 0.405300 |
| trust__human_authority | 18/18 | 15/18 | 3/18 | 0.226589 |
| trust__identity | 18/18 | 18/18 | 0/18 | 0.010533 |
| trust__integrity | 18/18 | 15/18 | 3/18 | 0.244644 |
| trust__monitoring | 18/18 | 15/18 | 3/18 | 0.164933 |
| trust__reconstructability | 18/18 | 15/18 | 3/18 | 0.230144 |
| trust__reliability | 18/18 | 18/18 | 0/18 | 0.009011 |
| trust__scope | 18/18 | 15/18 | 3/18 | 0.111411 |
| trust__uncertainty | 18/18 | 15/18 | 3/18 | 0.197000 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 75 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 33 | 45 | 0 | 0 |
| unsupported | 0 | 0 | 75 | 0 | 0 |
| indeterminate | 0 | 0 | 0 | 75 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 75 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 75/75 | 75 | 1.000000 |
| partially_supported | 33/78 | 78 | 0.423077 |
| unsupported | 75/75 | 75 | 1.000000 |
| indeterminate | 75/75 | 75 | 1.000000 |
| outside_scope | 75/75 | 75 | 1.000000 |

### invariance · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 2709/3024 | 2274/2709 | 435/2709 | 0.209582 |
| control__access | 129/144 | 120/129 | 9/129 | 0.085823 |
| control__authority | 129/144 | 89/129 | 40/129 | 0.411916 |
| control__comprehension | 129/144 | 115/129 | 14/129 | 0.132606 |
| control__correction | 129/144 | 104/129 | 25/129 | 0.164262 |
| control__effect | 129/144 | 129/129 | 0/129 | 0.006612 |
| control__exercise | 129/144 | 129/129 | 0/129 | 0.015127 |
| control__feasibility | 129/144 | 129/129 | 0/129 | 0.012085 |
| control__reform | 129/144 | 96/129 | 33/129 | 0.408090 |
| control__repair | 129/144 | 95/129 | 34/129 | 0.221161 |
| trust__capability | 129/144 | 121/129 | 8/129 | 0.094606 |
| trust__evidence_completeness | 129/144 | 76/129 | 53/129 | 0.610005 |
| trust__governance_update | 129/144 | 96/129 | 33/129 | 0.363566 |
| trust__harm_correction | 129/144 | 88/129 | 41/129 | 0.408898 |
| trust__human_authority | 129/144 | 98/129 | 31/129 | 0.255248 |
| trust__identity | 129/144 | 129/129 | 0/129 | 0.010095 |
| trust__integrity | 129/144 | 99/129 | 30/129 | 0.359363 |
| trust__monitoring | 129/144 | 97/129 | 32/129 | 0.232036 |
| trust__reconstructability | 129/144 | 87/129 | 42/129 | 0.488367 |
| trust__reliability | 129/144 | 129/129 | 0/129 | 0.005571 |
| trust__scope | 129/144 | 129/129 | 0/129 | 0.048561 |
| trust__uncertainty | 129/144 | 119/129 | 10/129 | 0.067214 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 1334 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 209 | 424 | 0 | 0 |
| unsupported | 2 | 0 | 459 | 0 | 0 |
| indeterminate | 0 | 0 | 9 | 212 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 60 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 1334/1334 | 1356 | 1.000000 |
| partially_supported | 209/633 | 756 | 0.330174 |
| unsupported | 459/461 | 552 | 0.995662 |
| indeterminate | 212/221 | 300 | 0.959276 |
| outside_scope | 60/60 | 60 | 1.000000 |

### mutation · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 546/567 | 537/546 | 9/546 | 0.026418 |
| control__access | 26/27 | 26/26 | 0/26 | 0.008000 |
| control__authority | 26/27 | 26/26 | 0/26 | 0.004900 |
| control__comprehension | 26/27 | 26/26 | 0/26 | 0.000008 |
| control__correction | 26/27 | 23/26 | 3/26 | 0.136869 |
| control__effect | 26/27 | 26/26 | 0/26 | 0.000000 |
| control__exercise | 26/27 | 26/26 | 0/26 | 0.033369 |
| control__feasibility | 26/27 | 26/26 | 0/26 | 0.000115 |
| control__reform | 26/27 | 26/26 | 0/26 | 0.085862 |
| control__repair | 26/27 | 26/26 | 0/26 | 0.000162 |
| trust__capability | 26/27 | 26/26 | 0/26 | 0.000808 |
| trust__evidence_completeness | 26/27 | 23/26 | 3/26 | 0.068315 |
| trust__governance_update | 26/27 | 26/26 | 0/26 | 0.008746 |
| trust__harm_correction | 26/27 | 23/26 | 3/26 | 0.180169 |
| trust__human_authority | 26/27 | 26/26 | 0/26 | 0.001154 |
| trust__identity | 26/27 | 26/26 | 0/26 | 0.000223 |
| trust__integrity | 26/27 | 26/26 | 0/26 | 0.001500 |
| trust__monitoring | 26/27 | 26/26 | 0/26 | 0.016246 |
| trust__reconstructability | 26/27 | 26/26 | 0/26 | 0.000569 |
| trust__reliability | 26/27 | 26/26 | 0/26 | 0.002523 |
| trust__scope | 26/27 | 26/26 | 0/26 | 0.004577 |
| trust__uncertainty | 26/27 | 26/26 | 0/26 | 0.000654 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 515 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 0 | 6 | 0 | 0 |
| unsupported | 0 | 0 | 22 | 0 | 0 |
| indeterminate | 0 | 0 | 3 | 0 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 0 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 515/515 | 534 | 1.000000 |
| partially_supported | 0/6 | 6 | 0.000000 |
| unsupported | 22/22 | 24 | 1.000000 |
| indeterminate | 0/3 | 3 | 0.000000 |
| outside_scope | 0/0 | 0 | null |

### reconstruction · repetition pooled_secondary · jev-1.13.0

| Construct | Valid / scheduled | Agreement | Disagreement | Brier mean |
| --- | --- | --- | --- | --- |
| overall | 651/756 | 555/651 | 96/651 | 0.201533 |
| control__access | 31/36 | 29/31 | 2/31 | 0.078619 |
| control__authority | 31/36 | 22/31 | 9/31 | 0.406723 |
| control__comprehension | 31/36 | 30/31 | 1/31 | 0.094923 |
| control__correction | 31/36 | 22/31 | 9/31 | 0.221161 |
| control__effect | 31/36 | 31/31 | 0/31 | 0.005290 |
| control__exercise | 31/36 | 31/31 | 0/31 | 0.010742 |
| control__feasibility | 31/36 | 31/31 | 0/31 | 0.017368 |
| control__reform | 31/36 | 25/31 | 6/31 | 0.299361 |
| control__repair | 31/36 | 22/31 | 9/31 | 0.227477 |
| trust__capability | 31/36 | 31/31 | 0/31 | 0.103265 |
| trust__evidence_completeness | 31/36 | 19/31 | 12/31 | 0.592535 |
| trust__governance_update | 31/36 | 25/31 | 6/31 | 0.289787 |
| trust__harm_correction | 31/36 | 22/31 | 9/31 | 0.404658 |
| trust__human_authority | 31/36 | 25/31 | 6/31 | 0.243510 |
| trust__identity | 31/36 | 31/31 | 0/31 | 0.006890 |
| trust__integrity | 31/36 | 23/31 | 8/31 | 0.414232 |
| trust__monitoring | 31/36 | 25/31 | 6/31 | 0.160497 |
| trust__reconstructability | 31/36 | 20/31 | 11/31 | 0.530845 |
| trust__reliability | 31/36 | 31/31 | 0/31 | 0.003503 |
| trust__scope | 31/36 | 31/31 | 0/31 | 0.063968 |
| trust__uncertainty | 31/36 | 29/31 | 2/31 | 0.056845 |

| Gold / predicted | supported | partially_supported | unsupported | indeterminate | outside_scope |
| --- | --- | --- | --- | --- | --- |
| supported | 325 | 0 | 0 | 0 | 0 |
| partially_supported | 0 | 52 | 94 | 0 | 0 |
| unsupported | 0 | 0 | 111 | 0 | 0 |
| indeterminate | 0 | 0 | 2 | 52 | 0 |
| outside_scope | 0 | 0 | 0 | 0 | 15 |

| State | Correct / valid gold | Scheduled gold | Recall |
| --- | --- | --- | --- |
| supported | 325/325 | 339 | 1.000000 |
| partially_supported | 52/146 | 189 | 0.356164 |
| unsupported | 111/111 | 138 | 1.000000 |
| indeterminate | 52/54 | 75 | 0.962963 |
| outside_scope | 15/15 | 15 | 1.000000 |

## Reproduce the saved analysis

From repository root, with the credential-free validation dependencies installed:

```sh
python -B -m experiments.jev.live_results_v1.verify
```

This command validates saved bytes and recomputes metrics; it never calls Jev.
