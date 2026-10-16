#!/usr/bin/env python3
"""Validate the v0.17.0 proposition-reviewed preprint workspace."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTHOR = "Mark Julius Banasihan"
ORCID = "0009-0001-8121-2878"
QUESTION = (
    "How can a frozen, evidence-traceable assessment procedure represent formal "
    "human authority, practical human control, and unresolved evidence in a bounded "
    "public incident record?"
)
VERSION_DOI = "10.5281/zenodo.21865007"
REPOSITORY_VERSION = "0.18.0"
PAPER_FILES = (
    "paper/README.md",
    "paper/paper-charter.md",
    "paper/manuscript.md",
    "paper/manuscript-reader.md",
    "paper/manuscript-pressure-test-v0.8.0.md",
    "paper/review-record-v0.8.0.md",
    "paper/review-record-v0.9.0.md",
    "paper/author-screening-completion-gate.md",
    "paper/next-evidence-gates-v0.10.0.md",
    "paper/inaccessible-risk-sample-v0.11.0.md",
    "paper/direct-query-retrieval-tranche-v0.11.0.md",
    "paper/forward-citation-retrieval-tranche-v0.12.0.md",
    "paper/forward-citation-author-screening-protocol-v0.13.0.md",
    "paper/forward-citation-author-screening-v0.13.0.md",
    "paper/forward-citation-proposition-review-protocol-v0.14.0.md",
    "paper/forward-citation-proposition-review-v0.14.0.md",
    "paper/preprint-readiness-v0.14.0.md",
    "paper/revision-plan-v0.16.0.md",
    "paper/tables.md",
    "paper/tables/manuscript-tables.tex",
    "paper/literature-matrix.md",
    "paper/literature-search-log.md",
    "paper/novelty-audit.md",
    "paper/references.bib",
    "paper/claim-evidence-register.md",
    "paper/submission-notes.md",
    "paper/review-record-pr11.md",
    "paper/claim-crosswalk.md",
    "paper/scientistone-artifact-pressure-test.md",
    "paper/citation-chain-log-v0.6.0.md",
    "paper/literature-support-audit-v0.6.0.json",
    "paper/literature-support-audit-v0.6.0.md",
    "paper/formal-literature-search-protocol-v0.7.0.md",
    "paper/formal-citation-chain-v0.7.0.md",
    "paper/formal-search-screening-v0.7.0.md",
    "paper/data/formal-search-v0.7.0.json",
    "paper/data/formal-screening-proposals-v0.7.0.json",
    "paper/data/formal-metadata-verification-v0.7.0.json",
    "paper/data/author-screening-queue-v0.7.0.csv",
    "paper/data/author-screening-decisions-v0.8.0.csv",
    "paper/data/author-screening-gate-v0.8.0.json",
    "paper/data/author-screening-decisions-v0.9.0.csv",
    "paper/data/author-screening-gate-v0.9.0.json",
    "paper/data/close-source-full-text-gate-v0.10.0.csv",
    "paper/data/inaccessible-record-retrieval-v0.10.0.csv",
    "paper/data/inaccessible-risk-sample-v0.11.0.csv",
    "paper/data/inaccessible-risk-sample-v0.11.0.json",
    "paper/data/direct-query-retrieval-evidence-v0.11.0.json",
    "paper/data/forward-citation-retrieval-evidence-v0.12.0.json",
    "paper/data/forward-citation-author-review-queue-v0.12.0.csv",
    "paper/data/forward-citation-author-screening-decisions-v0.13.0.csv",
    "paper/data/forward-citation-author-screening-v0.13.0.json",
    "paper/data/forward-citation-proposition-review-v0.14.0.csv",
    "paper/data/forward-citation-proposition-review-v0.14.0.json",
    "paper/data/direct-query-resolution-v0.14.0.json",
    "evidence/human-review-attestation-v0.11.0.json",
    "evidence/human-review-attestation-v0.12.0.json",
    "evidence/human-review-attestation-v0.13.0.json",
    "evidence/human-review-attestation-v0.14.0.json",
    "evidence/human-review-attestation-v0.15.0.json",
    "evidence/human-review-attestation-v0.16.0.json",
    "evidence/claim-evidence-map.json",
    "audits/v0.14.0/audit-plan.md",
    "audits/v0.14.0/audit-results.json",
    "audits/v0.14.0/audit-report.md",
    "audits/v0.14.0/exceptions.md",
    "audits/v0.15.0/audit-plan.md",
    "audits/v0.15.0/audit-results.json",
    "audits/v0.15.0/audit-report.md",
    "audits/v0.15.0/exceptions.md",
    "audits/v0.16.0/audit-plan.md",
    "audits/v0.16.0/audit-results.json",
    "audits/v0.16.0/audit-report.md",
    "audits/v0.16.0/exceptions.md",
    "release/v0.14.0-release-notes.md",
    "paper/arxiv/main.tex",
    "paper/arxiv/metadata.yaml",
    "paper/arxiv/README.md",
    "paper/arxiv/00README.XXX",
    "paper/arxiv/source-manifest.json",
    "paper/arxiv/figures-bw-manifest.json",
    "paper/arxiv/arxiv-source-v0.14.0.zip",
    "paper/arxiv/preprint-v0.14.0.pdf",
    "paper/arxiv/overleaf-compiled-v0.14.0.pdf",
    "paper/arxiv/overleaf-compile-receipt.json",
    "paper/REVIEW.md",
    "paper/preprints/README.md",
    "paper/preprints/00README.XXX",
    "paper/preprints/metadata.yaml",
    "paper/preprints/main.tex",
    "paper/preprints/source-manifest.json",
    "paper/archive/README.md",
    "paper/archive/v0.15.0/README.md",
    "paper/archive/v0.15.0/preprints-source-v0.15.0.zip",
    "paper/archive/v0.15.0/preprints-compiled-v0.15.0.pdf",
    "paper/archive/v0.15.0/overleaf-compile-receipt-v0.15.0.json",
    "paper/preprints/preprints-source-v0.16.0.zip",
    *tuple(f"paper/arxiv/figures-bw/{name}" for name in (
        "fig-1-selection-and-stopping.png",
        "fig-2-practical-control-chain.png",
        "fig-3-decision-paths.png",
        "fig-4-trust-evidence-states.png",
        "fig-5-formal-search-and-screening.png",
        "fig-6-evidence-boundaries.png",
        "fig-a1-mutation-response.png",
        "fig-a2-reproducibility-lineage.png",
        "fig-a3-claim-evidence-integrity.png",
        "fig-a4-oko-versioned-correction.png",
    )),
    "paper/data/authenticated-interface-searches-v0.10.0.csv",
    "paper/data/next-evidence-gates-v0.10.0.json",
    "paper/literature-support-audit-v0.7.0.json",
    "paper/literature-support-audit-v0.7.0.md",
    "paper/literature-support-audit-v0.9.0.json",
    "paper/literature-support-audit-v0.9.0.md",
)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def validate_files(failures: list[str]) -> None:
    for relative in PAPER_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing paper file: {relative}", failures)
        elif path.stat().st_size == 0:
            fail(f"empty paper file: {relative}", failures)


def validate_identity(failures: list[str]) -> None:
    required_author_files = (
        "paper/manuscript.md",
        "paper/paper-charter.md",
        "paper/submission-notes.md",
    )
    for relative in required_author_files:
        text = (ROOT / relative).read_text(encoding="utf-8")
        if AUTHOR not in text:
            fail(f"full author name missing from {relative}", failures)
    manuscript = (ROOT / "paper/manuscript.md").read_text(encoding="utf-8")
    if ORCID not in manuscript:
        fail("ORCID missing from paper/manuscript.md", failures)
    combined = "\n".join(
        (ROOT / relative).read_text(encoding="utf-8")
        for relative in PAPER_FILES
        if relative.endswith(".md")
    )
    if re.search(r"\bMark Banasihan\b", combined):
        fail("ambiguous author name found in paper workspace", failures)


def validate_question(failures: list[str]) -> None:
    for relative in (
        "paper/README.md",
        "paper/paper-charter.md",
        "paper/manuscript.md",
    ):
        text = (ROOT / relative).read_text(encoding="utf-8")
        if QUESTION not in text:
            fail(f"paper question mismatch in {relative}", failures)


def validate_bibliography(failures: list[str]) -> None:
    text = (ROOT / "paper/references.bib").read_text(encoding="utf-8")
    entries = re.findall(r"^@\w+\{([^,]+),", text, flags=re.MULTILINE)
    if len(entries) < 45:
        fail(f"paper bibliography has {len(entries)} entries; expected at least 45", failures)
    if len(entries) != len(set(entries)):
        fail("duplicate BibTeX keys in paper/references.bib", failures)
    doi_fields = re.findall(r"^\s+doi\s*=", text, flags=re.MULTILINE | re.IGNORECASE)
    if len(doi_fields) < 24:
        fail(f"paper bibliography has {len(doi_fields)} DOI fields; expected at least 24", failures)
    if "\\\\&" in text:
        fail("doubled backslash before ampersand in paper/references.bib", failures)
    manuscript = (ROOT / "paper/manuscript.md").read_text(encoding="utf-8")
    cited = set(re.findall(r"(?<![A-Za-z0-9._%+-])@([A-Za-z0-9_:.+-]+)", manuscript))
    missing = sorted(cited - set(entries))
    if missing:
        fail(f"unresolved manuscript citation keys: {', '.join(missing)}", failures)
    reader = (ROOT / "paper/manuscript-reader.md").read_text(encoding="utf-8")
    if re.search(r"\[@[A-Za-z0-9_:.+-]+", reader):
        fail("reader manuscript contains unresolved Pandoc citation syntax", failures)
    if "## References" not in reader:
        fail("reader manuscript reference list is missing", failures)


def validate_generated_paper_artifacts(failures: list[str]) -> None:
    commands = (
        [sys.executable, "scripts/render_reader_manuscript.py", "--check"],
        [sys.executable, "scripts/validate_author_screening_gate.py", "--check", "--require-complete"],
        [sys.executable, "scripts/validate_next_evidence_gates.py", "--check"],
        [sys.executable, "scripts/validate_forward_citation_author_screening_v0_13_0.py"],
        [sys.executable, "scripts/validate_forward_citation_proposition_review_v0_14_0.py"],
        [sys.executable, "analysis/derive_event_control_results.py", "--check"],
        [sys.executable, "scripts/build_v0_17_policy_claim_map.py", "--check"],
        [sys.executable, "scripts/run_policy_integrity_audit_v0_17_0.py", "--check"],
        [sys.executable, "scripts/validate_preprints_package.py"],
        [sys.executable, "scripts/validate_literature_support.py"],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            fail(f"generated paper artifact failed: {(result.stdout + result.stderr).strip()}", failures)


def validate_boundaries(failures: list[str]) -> None:
    review = (ROOT / "paper/review-record-pr11.md").read_text(encoding="utf-8")
    register = (ROOT / "paper/claim-evidence-register.md").read_text(encoding="utf-8")
    manuscript = (ROOT / "paper/manuscript.md").read_text(encoding="utf-8")
    if "## v0.6.0 resolution" not in review or "resolved by reclassification" not in review.lower():
        fail("v0.6 Oko resolution missing from review record", failures)
    if "C04 | The frozen v0.6 Oko adjudication" not in register:
        fail("current Oko claim missing from claim register", failures)
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    if f"version: {REPOSITORY_VERSION}" not in citation:
        fail(f"CITATION.cff does not identify v{REPOSITORY_VERSION}", failures)
    if VERSION_DOI not in manuscript:
        fail("v0.6.0 version DOI missing from paper/manuscript.md", failures)
    matrix = (ROOT / "paper/literature-matrix.md").read_text(encoding="utf-8")
    if "L24" not in matrix or "ScientistOne" not in matrix or "L28" not in matrix or "L41" not in matrix or "L56" not in matrix:
        fail("required close neighbors missing from literature matrix", failures)
    crosswalk = (ROOT / "paper/claim-crosswalk.md").read_text(encoding="utf-8")
    required_crosswalk = (
        "`PAPER-C04` | Eligible",
        "`PAPER-C09` | Eligible",
        "`PAPER-C15` | Eligible",
        "`PAPER-C22` | Eligible",
        "`PAPER-C23` | Eligible",
        "`PAPER-C24` | Eligible",
        "`PAPER-C25` | Eligible",
        "`PAPER-C26` | Eligible",
        "`PAPER-C35` | Eligible",
        "`PAPER-C36` | Eligible",
        "`PAPER-C37` | Eligible",
        "`PAPER-C38` | Eligible",
        "`TAE-C23` | Ineligible",
    )
    if any(marker not in crosswalk for marker in required_crosswalk):
        fail("eligible paper claims missing from crosswalk", failures)
    if re.search(r"\bnovel\b", manuscript, flags=re.IGNORECASE):
        fail("manuscript contains prohibited novelty wording", failures)
    if "Proposition-reviewed working manuscript, v0.16.0 rebuild" not in manuscript:
        fail("v0.16.0 manuscript status is missing", failures)
    if "**Figure 6. Evidence boundaries" not in manuscript:
        fail("Figure 6 caption is missing from the manuscript", failures)
    if "**Table A3. Availability of coding-stability evidence.**" not in manuscript:
        fail("Table A3 is missing from the manuscript", failures)
    if "**Table 4. Formal authority compared with event-level practical control.**" not in manuscript:
        fail("Table 4 is missing from the manuscript", failures)
    if "**Table 6. Proposal-to-author decision changes.**" not in manuscript:
        fail("Table 6 is missing from the manuscript", failures)
    if "**Table 7. Residual-risk retrieval and screening checkpoint.**" not in manuscript:
        fail("Table 7 is missing from the manuscript", failures)
    gate = (ROOT / "paper/author-screening-completion-gate.md").read_text(encoding="utf-8")
    if "| Total author gate | 89 | 89 | 0 |" not in gate:
        fail("author-screening gate does not expose the completed 89 decisions", failures)


def main() -> int:
    failures: list[str] = []
    validate_files(failures)
    if not failures:
        validate_identity(failures)
        validate_question(failures)
        validate_bibliography(failures)
        validate_boundaries(failures)
        validate_generated_paper_artifacts(failures)
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"paper validation: FAIL ({len(failures)} error(s))")
        return 1
    print("paper validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
