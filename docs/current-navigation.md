# Current navigation and the v0.18.0 closeout

The current repository checkpoint is **v0.18.0**, dated 16 October 2026. The preferred paper is the author-approved **2026-10-10 revision**, separately archived at [paper/revisions/2026-10-10/](../paper/revisions/2026-10-10/README.md). Its PDF, editable source, public supplement and verification record travel together. The [closeout record](research-phase-closeout-2026-10-16.md) distinguishes completed work from future validation studies and external venue status.

The current README, preferred citation and research status identify [10.5281/zenodo.23423847](https://doi.org/10.5281/zenodo.23423847), the October revision published on Zenodo on 16 October. Its public downloads match the release files. The historical v0.17.0 paper DOI [10.5281/zenodo.22970968](https://doi.org/10.5281/zenodo.22970968) remains attached to its earlier preprint. The paper concept DOI and repository concept DOI identify separate collections.

The current comparison distinguishes historical 0 Pass / 2 Fail / 1 Unresolved, limited-correction 0 / 1 / 2, and conditional additional-reassessment 0 / 0 / 3 results. All 64 additional joint assignments share the latter result under the recorded inputs. Any justified necessary-condition failure still produces Fail. Broader Stage 3 construct amendments remain unadopted. Jev scores, its 1,079 original unresolved adjudications, the omitted timed human comparison and unmeasured benefits retain their recorded status.

## Historical integrity boundary

The v0.17.0 tag, manifest, release assets, manuscript, source archive, compiled PDF, claim maps, audit results and case states remain unchanged. The tagged manifest seals its original 33 artifact bytes. Historical release validation checks the tag and the unchanged working copies of the 30 non-navigation v0.17.0 artifacts and the manifest itself.

Three current-facing documents use the separate navigation checkpoint:

- `README.md`
- `CITATION.cff`
- `RESEARCH_STATUS.md`

[`navigation-v0.17.0.json`](navigation-v0.17.0.json) records their original release hashes and their current hashes and sizes. The fixed three-path scope permits current navigation updates while the original research artifacts remain checked against the released manifest. It is refreshed for the v0.18.0 checkpoint; it does not reseal or retag the old release. Do not run the historical manifest builder to represent current navigation as original v0.17.0 bytes.

The historical v0.17.0 PDF SHA-256 is `d7609d47f4f92629c58d400e3222b29026a6a152de7da1ec79ad7239a1b4b4ee`; its source archive SHA-256 is `840a08784753cbc569e506bcd71bfc577fe43dddfef1dcedce934572213a4be9`. They remain historical checks, not the current revision's digests. The new [verification record](../paper/revisions/2026-10-10/VERIFICATION.json) identifies the current archive checks.

Earlier navigation updates in v0.17.1, v0.17.2 and later merged Jev records preserved their release snapshots. Their tags and manifests continue to describe those historical checkpoints. Frozen paper entry points in `paper/preprints/` and earlier review documents retain their release identities; the new revision has its own entry point.

## Verification

Run the repository's existing validation workflow and `python -m unittest discover -s tests -p 'test_navigation.py' -v`. The navigation tests reject unrecorded changes, expanded checkpoint scope, incorrect historical baselines and changes to sealed research artifacts. They verify that the v0.17.0 manifest still equals its tagged copy. Computational checks and author approval provide no independent validation of evidence judgments.
