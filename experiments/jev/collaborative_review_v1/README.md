# Collaborative TAE–Jev author review

All 24 selected items have an author-approved local assessment or approved bounded interpretation. Each record preserves its source request/response hashes and the approval scope. The consolidated JSON contains the original records and their SHA-256 hashes.

## Findings retained

- Items 8 (record integrity) and 16 (reconstructability) retain unresolved final classifications. Approval confirmed preservation of the ambiguity, not a resolved label.
- Recurring concerns distinguish documented permission or plans from demonstrated use or delivery, and missing evidence from contrary evidence.
- Item 14 preserves the limitation that the underlying monitoring trace was not independently inspected.
- Item 17 preserves the author's concern that reviewers may overlook relevant details without closer examination or a flag. Flagging benefits remain untested.
- Repeated excerpts and prior exposure are disclosed in the individual records.

## Interpretation boundary

This is a collaborative, AI-assisted author review. The assistant explained evidence and proposed conclusions; the author approved them. It is not independent validation, an unassisted baseline, or an estimate of model accuracy. Agreement after discussion does not measure an improvement in review quality.

Human time savings and quality improvement remain unmeasured. No usable paired timing or completed standardized form comparison exists. Missing fields in the differently shaped local records were not fabricated. The previously omitted comparison remains omitted; this later review is a separate record.

No original adjudication was closed, no frozen result was rescored, and no live Jev call was made for this review. This preservation package is prepared locally for later publication review.

## Provenance and use

This package preserves the 24 individual records and consolidated review byte for
byte from the local review workspace. The approval excerpts and discussion notes
were recorded by Codex from the conversation; they are not cryptographic signatures
or independently authenticated transcripts. Item numbers follow the frozen
[review cohort](../review_queue_v1/cohort.json). No new Jev inference is involved.

The records intentionally retain their original field shapes. Items 1–4 retain
an early draft-type label despite their later approved status. Some conclusions
appear in prose rather than a separate field. Absent initial answers, flags,
ratings and timestamps are not inferred or backfilled. The author approved
bounded interpretations with unresolved classifications for items 8 and 16.

The original comparison was omitted and closed before this later collaborative
review was completed. This package supplements that chronology; it does not
retroactively complete the original baseline/assisted forms. Teaching, suggested
answers, repeated wording and model/reference disclosure prevent treating final
agreement as independent accuracy evidence or a causal improvement measurement.
No aggregate reviewer accuracy or model benefit score is calculated.

`manifest.json` pins the preserved files and source cohort. To verify their
integrity and correspondence without credentials or network access, run:

```sh
python -B -m experiments.jev.collaborative_review_v1.verify
```

Hash verification establishes consistency of saved bytes, not truth of the
underlying synthetic evidence or independent validity of the assessments.
