# Evidence-v2 live transport bridge

Prospective implementation, 2 October 2026 (America/New_York). No live Jev outputs
were observed during implementation. This is a separate execution layer for the
frozen `evidence_v2` experiment, not a new corpus, model or question revision.
The original v1/v2 freezes, adjudication controls and release findings remain unchanged.

## Scope and review boundary

The author confirmed that Jev continues in TAE, with the Control Evidence Corpus
(CEC) repository as context. CEC's TAE/HIT sandbox and its technical-evaluation
labels remain separate. No CEC packet is imported, no scripted actor establishes
human control, and no CEC or TAE/HIT empirical result follows from this bridge.
See CEC's `experiments/us-control-sandbox/RECONCILIATION.md` and `README.md` at
<https://github.com/node-and-norm/node-norm-control-evidence>.

Implementation is AI-assisted and author-directed, not independent review.
The bridge must be committed and reviewed before first live use. `BRIDGE.json`
anchors its implementation and documentation to committed Git bytes. This is
not independent registration. After any live inference, amendments require a
new version rather than changing this bridge or its recorded run.

## Preserved schedule and analysis

The bridge imports the frozen request projection and analysis functions. All 94
packets, 1,654 determinations per repetition, three repetitions, 282 total requests
and 4,962 determinations are retained in the original order. Requested model is
`jev-1.13.0`, SDK is `typesafe-sdk==0.7.1`, with no temperature/seed or retries.
One attempt is made for each scheduled request. No subset, resume or automatic
rerun option exists. Repetition 1 stays primary; mixed model versions stay separate.

Before any inference, all canonical request bytes and the complete initial
schedule are saved. SDK JSON serialization may differ in whitespace; its body
must equal the frozen JSON value before dispatch. The actual SDK request body is
saved separately before sending, without headers or credentials. Both byte hashes
are retained. This does not change the frozen semantic request manifest.

Every available raw response, including HTTP errors and SDK parse failures, is
retained. Invalid replies never become indeterminate judgments. Exceptions retain
only their type, not potentially sensitive message text. Status and timestamps
are saved for each attempt. An in-flight request is recorded as interrupted
before dispatch, so abrupt termination cannot silently erase its scheduled position.
Catchable interruption writes reports; a hard kill can leave reports absent or
stale, with `schedule.json` and `run.json` authoritative. Do not restart that run.
Filesystem failure may prevent complete retention; any such run is incomplete.

Frozen metric calculations and unresolved disagreement records are reused.
Live report wording removes the mock-only disclaimer but retains the synthetic,
non-independent interpretation. Complete the frozen evidence-v2 report template
and use the existing append-only adjudication workflow; raw scores never change.

## Setup and offline checks

Use an isolated Python environment (Python 3.11 or later) and install
`jsonschema==4.25.1` plus `experiments/jev/requirements-live.txt`. The SDK is optional
for core TAE validation. Offline CI uses a fake transport and forbids socket connections.

```sh
python -B -m unittest discover -s experiments/jev/live_v1/tests -v
python -B -m experiments.jev.live_v1.run --mode dry-run --output experiments/jev/live_v1/runs/plan-001
python -B -m experiments.jev.live_v1.run --mode mock --output experiments/jev/live_v1/runs/mock-001
```

Every output directory must be new. Run directories are excluded from Git to
prevent automatic publication of provider responses; publish reviewed artifacts
deliberately with their manifests. Never commit an API key or paste one into chat.

## Account check and execution

Sign into the TypeSafe console, confirm account access/credits, and configure
`TYPESAFE_API_KEY` through a private environment or secret manager. The email login
is not an API credential. This runner uses only the official HTTPS endpoint and
ignores proxy/base-URL environment overrides.

```sh
python -B -m experiments.jev.live_v1.run --mode preflight --output experiments/jev/live_v1/runs/auth-001
```

Preflight calls only `GET /v1/models`, once, without research state or questions.
Success confirms authentication, not budget sufficiency or inference availability.
The list may contain aliases without the pinned version; do not silently switch models.
Record account budget and the completed implementation review before running:

```sh
python -B -m experiments.jev.live_v1.run --mode live --execute-frozen-schedule --output experiments/jev/live_v1/runs/live-001
```

Do not send an exploratory research-case smoke test. If provider compatibility
fails, retain every failure and document a versioned amendment before a new run.
There is no automatic stop based on performance or automatic replacement of failures.

## Sources checked before implementation

The installed TypeSafe skill was used with current official documentation:
<https://docs.typesafe.ai/api>, <https://docs.typesafe.ai/models>,
<https://docs.typesafe.ai/sdk/python/api/clients/sync> and
<https://docs.typesafe.ai/primitives/choice>. Current documentation lists the pinned
model and the same request structure; offline transport tests check SDK behavior.
This is not proof of account-specific live compatibility.
