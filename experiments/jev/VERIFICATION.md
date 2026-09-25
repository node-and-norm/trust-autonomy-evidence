# Verification record, September 25, 2026

The bounded experiment passed local checks. No live Jev inference was performed: `TYPESAFE_API_KEY` was absent, and the live command saved a blocked manifest and exited 2 before making requests.

| Check | Result |
| --- | --- |
| Repository validator | PASS, including 252 oracle comparisons and 12 mutations |
| Paper validator | PASS |
| Release snapshot validator | PASS: six tags, 821 sealed artifacts, 67 immutable working copies |
| Offline tests with SDK 0.7.1 | 12 passed, no network calls |
| Offline tests without SDK | 10 passed, two SDK transport tests skipped |
| Dry run with mutations | 24 requests planned, zero predictions |
| Mock run with mutations | 252 baseline and 252 mutation comparison rows, zero parsing errors |
| Live run | BLOCKED: missing TYPESAFE_API_KEY; zero requests |

The repository's existing chain-of-evidence audit reports PASS_WITH_EXCEPTIONS as designed. Its historical exceptions were preserved. Validation did not regenerate research artifacts or change any pre-existing tracked repository file.

Logs and compact run summaries are in [verification](verification/). The saved [blocked live manifest](verification/live-blocked.json) records the exact model request, question hash and sealed input hashes. Dry/mock raw artifacts remain in ignored local run directories; their manifest hashes are in `verification/local-runs.json`. They can be regenerated with the commands in the experiment README and carry no model-performance claim.

The first attempted SDK-absent test used a runtime that also lacked the repository's jsonschema dependency. After creating a clean environment containing jsonschema alone, all ten applicable tests passed. The two optional transport tests then passed in the separate SDK environment. The verified SDK tests assert the official endpoint, explicit requested model, raw-body retention on invalid success and HTTP 429 responses, and one attempt per case.

The synthetic fixture and oracle hashes match the original manifest. The experiment's added workflow runs with and without the optional SDK and contains no credentials or live execution step.
