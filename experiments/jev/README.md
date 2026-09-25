# Opt-in Jev synthetic experiment

This experiment measures Jev's agreement with TAE's frozen synthetic assessment contract. It covers 12 cases and 252 determinations (144 trust and 108 practical-control), with 12 optional governance mutations. It cannot establish practical human control in deployed systems. TAE's oracle, released conclusions, manifests and core dependencies remain unchanged.

Use Python 3.12 from the repository root. Local checks need only the existing development dependencies:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s experiments/jev/tests -v
python -m experiments.jev.run --mode dry-run --mutations --output experiments/jev/runs/dry-001
python -m experiments.jev.run --mode mock --mutations --output experiments/jev/runs/mock-001
```

Each output directory must be new. Runs are ignored by Git by default. Dry runs save requests without predictions; mocks return uniform probabilities and an `indeterminate` tie choice, deliberately exposing disagreements. Mock agreement is plumbing evidence only. The optional SDK transport test skips when the SDK is absent; all other checks run without it.

## Live execution

Install the isolated optional dependency, provide `TYPESAFE_API_KEY` through your shell or secret manager, then run:

```bash
python -m pip install -r experiments/jev/requirements-live.txt
python -m unittest discover -s experiments/jev/tests -v
python -m experiments.jev.run --mode live --model jev-1.13.0 --mutations --output experiments/jev/runs/live-001
```

The SDK reads the key from the environment. Do not commit or pass it as a command-line argument. A missing key saves a blocked run and exits 2. API errors produce an incomplete run and exit 2. No automatic retries are enabled; each of the 12 baseline cases and optional 12 mutations receives at most one request with a 30-second timeout. No core validator invokes this runner or imports the SDK.

The endpoint is fixed to TypeSafe's official API. Model overrides are explicit; the response's resolved model is recorded independently. Preserve aliases as requested and analyze resolved versions separately. Inspect `run.json` for completion before interpreting rows. An interrupted run retains completed records but requires a new output directory for another attempt.

## Artifacts and review

`run.json` records mode, timestamps, requested/resolved models, installed SDK version, implementation hashes, Git revision and dirty status, fixture and oracle hashes, per-request and per-response hashes, comparison rows, and mutation results. `run.schema.json` defines the output contract. Each job also saves its request and the exact HTTP response body when available, including bodies rejected during parsing. HTTP status and provider request ID are retained; authentication headers and exception messages are excluded.

`comparisons.jsonl` contains full five-class probabilities, confidence, entropy, oracle label, agreement and multiclass Brier loss (sum across five classes, range 0–2). `disagreements.json` contains the mismatches for human review. Confidence below 0.8 also flags review. This threshold is a prespecified workflow convention, with no empirical calibration claim. Missing/invalid responses are errors with zero scored determinations, never converted into an evidence class. The summary denominator reports actual completed baseline determinations; verify it equals 252 before reporting a complete benchmark.

To preserve a reviewed run in Git, explicitly force-add its directory under `experiments/jev/runs/` after confirming it contains only the public synthetic inputs and provider outputs. Keep every attempted run, including failures, when reporting results. Never copy results into released assessment or oracle paths.

See [protocol](PROTOCOL.md), [limitations](LIMITATIONS.md), and [verification record](VERIFICATION.md).
