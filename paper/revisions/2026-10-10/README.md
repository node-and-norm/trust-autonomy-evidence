# Approved revision: 10 October 2026

This directory preserves the author-approved 46-page revision of **From Formal
Authority to Practical Human Control** and its reproducibility supplement. The
repository v0.18.0 closeout release makes this dated revision the current paper.
It does not overwrite the historical v0.17.0 manuscript or case assessments.

The revised paper was published on Zenodo on 16 October 2026 at
[10.5281/zenodo.23423847](https://doi.org/10.5281/zenodo.23423847).
The arXiv submission remains on hold, confirmed by the author on 16 October.

| Artifact | Purpose |
| --- | --- |
| [preprint.pdf](preprint.pdf) | Exact latest PDF supplied by the author for release; 46 pages, including the arXiv submission stamp. |
| [source.tar.gz](source.tar.gz) | Exact source package downloaded from arXiv and verified on 10 October, containing `main.tex`, figures, and ancillary files. |
| [supplement/README_PUBLIC.txt](supplement/README_PUBLIC.txt) | Offline reproduction instructions for the additional reassessment. |
| [VERIFICATION.json](VERIFICATION.json) | Artifact identity, provenance, conditional results, and verification boundaries. |
| [SHA256SUMS.txt](SHA256SUMS.txt) | All files in this directory except the manifest itself. |

The source and PDF use different TeX build environments. The approved public PDF
and supplied arXiv PDF differ in pagination, hyphenation, and the arXiv submission
stamp; their manuscript content is preserved. The supplied PDF is not labeled as
an announced arXiv publication. `submit/7973196` is a submission identifier.

## Findings and approval scope

Condition order: access, comprehension, authority, feasibility, exercise,
propagation.

| Comparison | Oko | ZG710 | F/A-18C | Pass / Fail / Unresolved |
| --- | --- | --- | --- | --- |
| Historical v0.17.0 baseline | Unresolved | Fail | Fail | 0 / 2 / 1 |
| Limited correction, all 16 joint assignments | Unresolved | Fail | Unresolved | 0 / 1 / 2 |
| Additional ZG710 reassessment, all 64 joint assignments | Unresolved | Unresolved | Unresolved | conditional 0 / 0 / 3 |

The additional ZG710 row is `P / I / {P,I} / {P,I} / {P,I} / {P,I}`.
Only comprehension, feasibility, and exercise change from the limited comparison.
Authority and propagation alternatives and every other case cell are retained
inputs. The alternatives remain unresolved coding choices. Any justified
necessary-condition `U` produces **Fail**, regardless of uncertainty elsewhere.
Broader Stage 3 amendments remain unadopted.

The dated public approval statement in the supplement records author approval.
It contains no private-chat transcript or message identifier. Hashes and successful
calculation do not independently validate sources or assessor judgments. Jev and
collaborative review do not independently validate the historical findings.

## Reproduce

From the repository root, run:

```sh
python scripts/verify_reassessment_release.py
```

The supplement preserves the historical ZIP as Base64 text because arXiv
automatically extracts nested archives. Its checker decodes the original bytes
in memory, verifies the original SHA-256, and applies the unchanged calculation.
No credentials, network calls, or live Jev requests are needed. The earlier
Stage 3 proposal remains a historical proposal inside that preserved archive.

See the [research phase closeout](../../../docs/research-phase-closeout-2026-10-16.md)
for publication status, remaining limitations, and the boundary for future work.
