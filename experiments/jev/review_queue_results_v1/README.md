# Jev-assisted review queue: first development pilot

This separate post-output pilot uses 24 previously exposed semantic-review items
(12 original agreements and 12 disagreements) and routes all 22 invalid source
requests deterministically. It changes no original research result or adjudication.

## What was measured

- Frozen implementation commit before pilot inference: `e9e7cd1d2a5e710cd24600d6bed82daacacb3259`.
- Model: jev-1.13.0; three repetitions; 72 attempts, 70 valid and 2 invalid, no retries.
- One invalid response failed the probability-sum check; the other selected a choice that was not its maximum-probability option. Neither was repaired or retried.
- Median attempt duration: 0.168 seconds, including client handling.
- Scheduled execution: 13.466 seconds; runner wall time including initial verification: 18.418 seconds.
- These timings exclude development, form preparation, human review and later checking overhead.
- Repeat consistency was evaluable for 22/24 items; 2 had a change in at least one suggested answer. No majority-vote replacement.
- Primary valid assistance: 23/24 items. Unavailable assistance never removes the item from human review.
- Provider-reported usage: 85,473 input tokens and 16,831 output tokens; not a billing receipt.

`summary.json` contains the complete route/flag counts by repetition and resolved
version, plus item-level repetition differences. The archive retains 221 files
with all raw requests, SDK bodies, responses, schedule and timing records. Hashes
and the saved-data verifier support reproducibility; they do not establish truth.

## What remains unmeasured

**Human time saving and review quality are null.** There are no completed human
baseline or assisted assessments. Rapid model responses do not establish that the
review process is faster, that concerns are correct, or that important concerns
were not missed. Jev reviewing its own outputs is not independent validation.

The [frozen protocol](../review_queue_v1/PROTOCOL.md) prescribes paired active time,
workflow overhead, helpfulness, missed concerns and author route changes. The
baseline is not a gold standard, and fixed baseline-first order is confounded with
learning and fatigue. There is no diagnostic accuracy, recall, causal speedup or
independent-review claim. No issue-free suggestion auto-closes a record.

## Author workflow

1. Complete the blank baseline form before opening item-level pilot suggestions.
   Enter your reviewer name, disclose prior exposure, start/resume the timer, and
   record your own choices and concern notes for all 24 items. The timer pauses
   when the tab is hidden. Export the completed JSON before closing the tab.
2. Complete the separate assisted form, then export its JSON. Rate helpfulness and
   whether assistance missed an important concern; do not silently adopt suggestions.
3. Retain both records and a separate account of setup, checking, repair and Jev
   execution overhead. Leave net time saving unmeasured if overhead is unavailable.

The local form source passed a JavaScript syntax check; interactive browser
preview was blocked by the browser's local-file URL policy. Browser timing and
exported records are editable, not independently verified. Forms keep answers in
memory until export; they do not transmit them to Jev or store them in the repo.
The pilot assistant did not fill any author assessments.

The source renderer is `experiments.jev.review_queue_v1.forms.render`. Pass an
output path outside the repository for the baseline. For the assisted form, pass
a mapping of unit IDs to primary-repetition saved suggestions/statuses. The forms
are not an access-control or blinding mechanism; disclose any advance exposure.

After both exports, use `forms.compare(baseline, assisted, overhead_seconds)` with
parsed JSON records. It rejects incomplete inventories, wrong options, nonfinite
or nonpositive timings and reversed pass order. It returns descriptive paired
time differences, quality self-reports and route changes. Overhead must include
Jev execution as well as preparation/checking/repair; do not substitute request
latency for the total workflow cost.

## Reproduce saved results, without inference

```sh
python -B -m experiments.jev.review_queue_results_v1.verify
```

No additional live calls are needed to inspect this pilot. The prior v0.17.2
release, original evidence corpus and all 1,079 original unresolved records remain
unchanged. CEC remains context only.

## Milestone closure: human comparison omitted

After pilot execution, the author elected to omit the human time/quality
comparison and authorized closure of this development milestone. The received
baseline export was incomplete and contained zero saved item assessments. It
supplies no usable review timing or completed assessment record. No assisted-pass
export was received. Human time saving and review quality remain unmeasured;
there is no end-to-end acceleration claim.

Separately, the author approved Codex-drafted notes for items 1–3 and viewed a
draft for item 4. Those local notes are disclosed AI-assisted author review,
not an unassisted baseline, independent validation, or completed 24-item review.
Item 4 approval was not recorded. The original export and intake disclosure are
retained locally; no personal review files are published by this closure.

The frozen protocol, implementation, raw outputs and summary are unchanged.
All original adjudication records remain unresolved. No new live calls or
replacement runs are needed for this stopping point. A future human comparison
would require a separately documented design accounting for prior exposure.
