# Editorial revision: November 1, 2026

**[Read the 47-page preprint](preprint.pdf)** — *From Formal Authority to Practical Human Control*, by Mark Julius Banasihan.

This is the current editorial revision. The author authorized its repository publication on November 1, 2026. It preserves the research findings in the [October 10 revision](../2026-10-10/README.md). The methods phase remains closed; this update adds no experiment or new validation claim.

## Files

| Artifact | Purpose |
| --- | --- |
| [preprint.pdf](preprint.pdf) | Exact PDF supplied by the author for this update; 47 pages. |
| [main.tex](main.tex) | Editable manuscript source, identical to the source package member. |
| [source.tar.gz](source.tar.gz) | Complete submitted source: manuscript, figures, compiler configuration and public reproducibility supplement. |
| [VERIFICATION.json](VERIFICATION.json) | File identities, source comparison, publication status and verification limits. |
| [SHA256SUMS.txt](SHA256SUMS.txt) | Checksums for all files in this directory except the checksum file itself. |

## What changed

- Removed the October 10 running-header date from page 2 onward.
- Revised repetitive or unclear prose and applied American English, retaining official source names and titles.
- Expanded the AI-assistance disclosure to distinguish substantive research assistance, source inspection, author decisions, software checks, retained records and their limits.
- Clarified the relationship between this editorial revision, the archived October edition and the existing arXiv submission.

The source package differs from the archived October package in `main.tex` and `00README.json`. The compiler configuration additionally marks an existing ancillary Base64 archive as ignored by the TeX compiler. All figures and ancillary files are byte-identical. The supplied PDF and the PDF compiled by arXiv have different file bytes; their complete `pdftotext -layout` outputs match. This comparison does not establish visual identity or independently validate the research.

## Publication status

The existing arXiv submission was updated on November 1, 2026. The authenticated confirmation reported **“Article submitted”**, and the account continued to show **on hold**. Submission `7973196` is not a public arXiv article identifier. No arXiv acceptance, announcement or peer review is claimed, and no reason for the moderation hold is established here.

The [October revision on Zenodo](https://doi.org/10.5281/zenodo.23423847), published October 16, remains a separate archived edition. **That DOI does not identify this November revision.** No new Zenodo DOI or repository release is assigned by this update; v0.18.0 remains the repository's closeout release.

## Findings and limits retained

| Comparison | Pass / Fail / Unresolved |
| --- | --- |
| Historical v0.17.0 baseline | 0 / 2 / 1 |
| Limited correction, all 16 retained assignments | 0 / 1 / 2 |
| Additional reassessment, all 64 retained assignments | Conditional 0 / 0 / 3 |

These are documentary results conditional on the recorded judgments. Unresolved findings do not establish that control worked or that it was absent. Any justified failure of a necessary condition still produces Fail. Broader Stage 3 amendments remain unadopted; the original Jev adjudications and external-validation limits remain unresolved.

The unchanged [public supplement](../2026-10-10/supplement/README_PUBLIC.txt) is also included under `anc/reproducibility_additional_public/` in this source package. Existing reproduction instructions and checks remain applicable. The [research status](../../../RESEARCH_STATUS.md) and [phase closeout](../../../docs/research-phase-closeout-2026-10-16.md) describe the remaining research boundaries.

## Cite the version used

Banasihan, M. J. (2026). *From Formal Authority to Practical Human Control: A traceable method for reconstructing human control in automated decisions* (Editorial revision, November 1, 2026) [Preprint]. [GitHub revision archive](https://github.com/node-and-norm/trust-autonomy-evidence/tree/main/paper/revisions/2026-11-01).

Use the October Zenodo DOI only when citing that edition. Earlier manuscript packages and their historical review instructions remain preserved; start with this dated archive for the current paper.
