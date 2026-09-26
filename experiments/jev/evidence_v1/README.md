# Offline evidence-reconstruction experiment

Read [PROTOCOL.md](PROTOCOL.md) before interpreting any output. All materials are
synthetic; no Jev responses were observed during authoring. The existing v1 freeze
and released TAE records are preserved byte for byte.

From the repository root:

```sh
python -m unittest discover -s experiments/jev/evidence_v1/tests -v
python -m experiments.jev.evidence_v1.run --mode dry-run --output experiments/jev/evidence_v1/runs/dry-001
python -m experiments.jev.evidence_v1.run --mode mock --output experiments/jev/evidence_v1/runs/mock-001
```

Only new directories inside this experiment's `runs/` are allowed. Dry-run emits
frozen request bytes; mock returns the same uninformative distribution for every
question. Neither reads credentials or imports the live SDK. `report.json` provides
metrics and denominators; `adjudications.json` queues disagreements and invalid
responses for human review under `adjudication.schema.json`. Finish a research
report using [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md).

`cards.json` is the inference corpus. `gold.json`, `provenance.json`, `pairs.json`
and `translation.json` are local evaluation/authoring material and never wire
inputs. `author.py` can reproduce corpus bytes into a new temporary directory for
comparison. It cannot regenerate in this frozen directory. `freeze.json` anchors
materials, implementation, tests, schemas, v1 bytes and protected source files.

There is no live mode in this phase. Credentials are unnecessary. A future live
transport requires review against the frozen repetition and model-version policy.
