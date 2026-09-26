# Current navigation and the v0.17.0 release

The current release and preprint are v0.17.0, published on 6 September 2026.
The preferred citation, current PDF and compile receipt now agree across the root
README, citation metadata, research status and existing paper entry points.
Repository URLs use node-and-norm; the author profile remains mj3b.

The original root README still described the v0.16.0 manuscript as current, and
research status still called v0.17.0 a local candidate. The correction adopts the
reviewed README structure, points current readers to the released v0.17.0 paper,
updates the validation-control count from 22 to 39 base controls plus nine policy
controls, and distinguishes five inherited exceptions from two policy exceptions.
Older release narratives, case/figure/audit version identifiers and the v0.14.0 DOI
retain their historical identities. A visual-review approval does not close the
substantive author-review or independent-assessment gates.

## Integrity boundary

The v0.17.0 tag, manifest, release assets, manuscript, source archive, compiled PDF,
claim maps, audit results and case states remain unchanged. The tagged manifest
continues to seal all 33 original artifact bytes. The historical release validator
now verifies v0.17.0 directly against its tag, as it already does for six earlier
release snapshots. It also checks the unchanged working copies of the 30
non-navigation v0.17.0 artifacts and the manifest itself.

Only three current-facing documents use a separate checkpoint:

- README.md
- CITATION.cff
- RESEARCH_STATUS.md

`navigation-v0.17.0.json` records their original release hashes and current hashes
and sizes. The repository validator fixes this three-path scope in code and checks
every current document against the new checkpoint. All other release artifacts
remain checked against the unmodified released manifest. This is a navigation
correction on the development branch, not a rebuilt or retagged v0.17.0 release.
Do not run the historical manifest builder to reseal current navigation as though
it were the original release.

## Verification

The PDF SHA-256 is
`d7609d47f4f92629c58d400e3222b29026a6a152de7da1ec79ad7239a1b4b4ee`;
the source archive SHA-256 is
`840a08784753cbc569e506bcd71bfc577fe43dddfef1dcedce934572213a4be9`.
Both match the published GitHub v0.17.0 asset digests and the compile receipt.
The versioned GitHub release is the preferred citation target. The earlier
v0.14.0 DOI is not reassigned to this paper.

Run the repository's existing validation workflow and
`python -m unittest discover -s tests -p 'test_navigation.py' -v`.
Negative tests reject unrecorded navigation changes, missing/expanded checkpoints,
wrong release baselines and research-artifact changes. They also verify that the
v0.17.0 manifest itself still equals its tagged copy.
