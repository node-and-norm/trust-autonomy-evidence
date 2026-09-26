# Jev/TAE adjudication record amendment v2

This additive amendment supplies explicit review dates and downstream-change
records missing from the frozen evidence-v1 adjudication schema. It does not
change an experiment, question, evidence card, oracle, metric, repetition policy,
model response, or released conclusion. No human review or live Jev output is
asserted by this amendment.

## Boundary and provenance

`record.schema.json` embeds the original v1 record schema verbatim (apart from
its nested `$schema` declaration). Every v2 record retains the complete original
record in `source.record`, its canonical JSON hash, the raw run-file hash,
request/response filenames and hashes, run mode, and resolved model as recorded
by the run. Missing responses and model versions remain null. They are never
filled from a requested model or a mock result.

`AMENDMENT.json` hashes this amendment's code, schema, documentation, tests and
workflow, plus the original experiment freeze and adjudication schema. Its
committed Git revision supplies the reviewable manifest anchor. The CLI verifies
these hashes and the existing experiment freeze before importing or validating.
Future changes require a separately versioned amendment; do not update this
manifest to conceal a mismatch. Use the committed manifest as the trusted copy:
a file hash is an integrity check, not a digital signature or proof of authorship.

The embedded original adjudication record is an export supplied by the operator.
Retain its original file and provenance alongside the run. Validation checks the
embedded record hash, request identity/question, and raw artifact hashes; it does
not prove who authored that export or that reviewers actually acted independently.
A run can be relocated as a complete directory: its old `run_id` is preserved,
not inferred from the new directory name. Source files must remain unchanged for
the duration of an import/validation operation.

## Import an existing run, offline

Use Python 3.12 and the repository's `requirements-dev.txt`. No SDK, credential,
or network connection is required. Supply paths to an existing evidence-v1 run:

```sh
python -m experiments.jev.adjudication_v2.records migrate \
  --input /path/to/run/adjudications.json \
  --run /path/to/run/run.json \
  --output /tmp/jev-adjudications-v2.json
python -m experiments.jev.adjudication_v2.records validate \
  --input /tmp/jev-adjudications-v2.json \
  --run /path/to/run/run.json
```

The output must be a new file outside the repository in an existing directory.
Import never overwrites files. It accepts observed `mock` or `live` run records,
including invalid responses, errors, and interrupted attempts. It performs no
model calls. Planned dry-run requests have no observations and are rejected.
The current evidence-v1 runner itself still permits only dry-run and mock modes.
Accepting an archived live record is not authorization or implementation of live
execution.

Every import creates an **open, UNRESOLVED** record with empty reviewers,
null review date, and `not_assessed` downstream status. This also applies to a
closed legacy record: its old decision remains intact in `source.record`, but
missing dates and effects are not guessed. `created_at` records the actual import
time (UTC by default); `--created-at` exists for a known, recorded import time.
Never use it to manufacture a pre-result review date.

## Human workflow and append-only revisions

1. Preserve the raw run, legacy adjudication export and first v2 import. Keep
   mock and live records visibly separate; mock disagreements are tooling checks.
2. Two reviewers independently inspect the evidence and question before learning
   the competing classification, following the existing
   [adjudication protocol](../evidence_v1/PROTOCOL.md). Record each reviewer's actual
   identity, blind notes and `blind_reviewed_at` timestamp. Keep access/review
   attestations separately; the validator cannot establish independence.
3. Reconcile the two reviews, recording each `reconciled_at`, the shared
   `reviewed_at` completion timestamp, rationale and one original disposition:
   `JEV_ERROR`, `ORACLE_AMBIGUITY`, `QUESTION_DEFECT`,
   `EVIDENCE_TRANSLATION_DEFECT`, `CONSTRUCT_AMBIGUITY`,
   `INSUFFICIENT_EVIDENCE`, or `UNRESOLVED`. Unresolved work stays open.
4. Assess the downstream effect explicitly. Choose `no_change` with rationale,
   `change_proposed` with itemized targets and evidence references, or
   `change_applied` with the actual change date and resulting artifact hash.
   `before_sha256` may be null for a new artifact. A proposed change has no
   completion date or resulting hash. Preserve an applied change's supporting
   artifact/commit with its record; the validator checks the recorded hash's
   shape but does not retrieve that downstream artifact.
5. Append a new record with a unique `record_id`, the same `source`, and
   `record.supersedes` pointing to the preceding v2 ID. Preserve earlier records
   in the same JSON array and retain the previous file/export separately. First
   imports supersede the legacy ID. Never edit an earlier decision in place.
6. Run the validator against the unchanged raw run. Closure requires two distinct,
   dated reviewers, reconciliation dates no earlier than blind review and no later
   than completion, a substantive rationale, and an assessed downstream effect.
   Review dates may predate record serialization; record creation is not a claim
   that review occurred at that moment. Each appended revision's creation date
   must be no earlier than its predecessors'.

Use both the schema and the Python validator. Cross-field chronology, raw-file
hashes and supersession chains are checked by Python, not JSON Schema alone.
The validator checks integrity of the supplied history, not whether an earlier
export was secretly replaced; preserve external version history for that purpose.

Downstream changes are limited to separately versioned experiments, explicitly
exploratory reports, or documentation corrections. No adjudication authorizes
editing a sealed oracle, frozen corpus, historical release result, or original
response. Original metrics remain reported against the original oracle; any
adjudication-informed analysis must be separately labeled exploratory and retain
its original disagreement count. This amendment does not itself apply changes
or compute revised performance metrics.

## Verification

```sh
python -m unittest discover -s experiments/jev/adjudication_v2/tests -v
```

Tests use explicitly synthetic reviewer names and dates, not completed reviews.
They cover source preservation, malformed and missing responses, tampering,
question identity, incomplete review, dates, downstream status, supersession and
path escape. CI runs without the Jev SDK. The existing blind evidence-card
[review packet](../review_evidence_v1/README.md) still needs real human review;
this amendment does not fill its forms or satisfy that gate.
