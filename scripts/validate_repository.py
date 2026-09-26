#!/usr/bin/env python3
"""Validate the public research repository and solo-validation artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_VERSION = "0.17.1"
WORKING_VERSION = "0.17.0"
FIGURE_VERSION = "0.16.0"
PUBLIC_CASE_VERSION = "0.3.0"

REQUIRED_FILES = (
    "README.md",
    "RESEARCH_STATUS.md",
    "CLAIMS.md",
    "LIMITATIONS.md",
    "SOURCES.md",
    "CITATION.cff",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "GOVERNANCE.md",
    "LICENSE",
    "requirements-dev.txt",
    "research/trust-autonomy-and-evidence.md",
    "research/frozen-research-agenda.md",
    "research/agenda-discovery-log-v0.10.0.md",
    "research/agenda-discovery-log-v0.12.0.md",
    "research/chain-of-evidence-adaptation.md",
    "evidence/trust-evidence-register.md",
    "evidence/claim-evidence-map.json",
    "evidence/claim-evidence-map-v0.9.0.json",
    "evidence/human-review-attestation-v0.11.0.json",
    "evidence/human-review-attestation-v0.12.0.json",
    "evidence/human-review-attestation-v0.13.0.json",
    "evidence/human-review-attestation-v0.14.0.json",
    "evidence/human-review-attestation-v0.15.0.json",
    "evidence/human-review-attestation-v0.16.0.json",
    "evidence/research-lineage.json",
    "evidence/research-activity-log.json",
    "protocols/independent-review-protocol.md",
    "protocols/practical-human-control-test.md",
    "protocols/solo-validation-protocol.md",
    "protocols/public-case-reconstruction-protocol.md",
    "protocols/coe-integrity-audit.md",
    "protocols/search-coverage-and-full-text-protocol-v0.10.0.md",
    "protocols/oko-evidence-adjudication-v0.6.0.md",
    "cases/README.md",
    "cases/public-case-selection-register.md",
    "cases/data/candidate-search-output.json",
    "cases/public-case-packet-index.json",
    "cases/TAE-PUB-001-oko-1983/case-report.md",
    "cases/TAE-PUB-001-oko-1983/source-manifest.json",
    "cases/TAE-PUB-001-oko-1983/assessment.json",
    "cases/TAE-PUB-001-oko-1983/packet-manifest.json",
    "cases/TAE-PUB-002-patriot-zg710-2003/case-report.md",
    "cases/TAE-PUB-002-patriot-zg710-2003/source-manifest.json",
    "cases/TAE-PUB-002-patriot-zg710-2003/assessment.json",
    "cases/TAE-PUB-002-patriot-zg710-2003/packet-manifest.json",
    "cases/TAE-PUB-003-patriot-fa18-2003/case-report.md",
    "cases/TAE-PUB-003-patriot-fa18-2003/source-manifest.json",
    "cases/TAE-PUB-003-patriot-fa18-2003/assessment.json",
    "cases/TAE-PUB-003-patriot-fa18-2003/packet-manifest.json",
    "schemas/autonomy-profile.schema.json",
    "schemas/solo-case.schema.json",
    "schemas/trust-evidence-assessment.schema.json",
    "schemas/practical-control-assessment.schema.json",
    "schemas/mutation-suite.schema.json",
    "schemas/public-case-assessment.schema.json",
    "schemas/source-manifest.schema.json",
    "schemas/claim-evidence-map.schema.json",
    "schemas/research-lineage.schema.json",
    "schemas/coe-audit-result.schema.json",
    "schemas/coe-audit-mutations.schema.json",
    "schemas/formula-register.schema.json",
    "schemas/adjudication-ledger.schema.json",
    "schemas/literature-support-audit.schema.json",
    "fixtures/synthetic/cases.json",
    "fixtures/mutations/mutations.json",
    "fixtures/coe-audit-mutations.json",
    "fixtures/coe-audit-mutations-v0.9.0.json",
    "fixtures/adjudication-mutations-v0.6.0.json",
    "oracles/solo-validation-v0.2.0.json",
    "oracles/manifest.json",
    "analysis/assessment.py",
    "analysis/run_solo_validation.py",
    "analysis/build_figures.py",
    "analysis/build_claim_evidence_figure.py",
    "analysis/derive_event_control_results.py",
    "assessments/generated-results.json",
    "assessments/event-control-results-v0.16.0.json",
    "reports/solo-validation-v0.2.0.md",
    "reports/public-case-reconstruction-v0.3.0.md",
    "reports/figure-methods.md",
    "reports/claim-evidence-figure-methods-v0.5.0.md",
    "reports/oko-evidence-adjudication-v0.6.0.md",
    "reports/public-case-reconstruction-v0.6.0.md",
    "reports/claim-evidence-figure-methods-v0.6.0.md",
    "figures/README.md",
    "figures/manifest.json",
    "figures/specifications/figure-register.json",
    "figures/specifications/selection-decisions.json",
    "figures/specifications/decision-paths.json",
    "figures/specifications/reproducibility-lineage.json",
    "figures/specifications/claim-evidence-integrity.json",
    "figures/data/fig-1-selection-and-stopping.csv",
    "figures/data/fig-2-practical-control-chain.csv",
    "figures/data/fig-3-decision-paths.csv",
    "figures/data/fig-4-trust-evidence-states.csv",
    "figures/data/fig-a1-mutation-response.csv",
    "figures/data/fig-a2-reproducibility-lineage.csv",
    "figures/data/fig-a3-claim-evidence-integrity.csv",
    "figures/generated/fig-1-selection-and-stopping.png",
    "figures/generated/fig-1-selection-and-stopping.svg",
    "figures/generated/fig-2-practical-control-chain.png",
    "figures/generated/fig-2-practical-control-chain.svg",
    "figures/generated/fig-3-decision-paths.png",
    "figures/generated/fig-3-decision-paths.svg",
    "figures/generated/fig-4-trust-evidence-states.png",
    "figures/generated/fig-4-trust-evidence-states.svg",
    "figures/data/fig-5-formal-search-and-screening.csv",
    "figures/generated/fig-5-formal-search-and-screening.png",
    "figures/generated/fig-5-formal-search-and-screening.svg",
    "figures/data/fig-6-evidence-boundaries.csv",
    "figures/generated/fig-6-evidence-boundaries.png",
    "figures/generated/fig-6-evidence-boundaries.svg",
    "figures/generated/fig-a1-mutation-response.png",
    "figures/generated/fig-a1-mutation-response.svg",
    "figures/generated/fig-a2-reproducibility-lineage.png",
    "figures/generated/fig-a2-reproducibility-lineage.svg",
    "figures/generated/fig-a3-claim-evidence-integrity.png",
    "figures/generated/fig-a3-claim-evidence-integrity.svg",
    "figures/data/fig-a4-oko-versioned-correction.csv",
    "figures/generated/fig-a4-oko-versioned-correction.png",
    "figures/generated/fig-a4-oko-versioned-correction.svg",
    "figures/v0.5.0-manifest.json",
    "figures/v0.6.0-manifest.json",
    "figures/v0.7.0-manifest.json",
    "figures/v0.7.0-claim-evidence-manifest.json",
    "figures/v0.8.0-manifest.json",
    "figures/v0.8.0-claim-evidence-manifest.json",
    "figures/v0.9.0-manifest.json",
    "figures/v0.9.0-claim-evidence-manifest.json",
    "figures/v0.16.0-claim-evidence-manifest.json",
    "formulas/README.md",
    "formulas/formula-register-v0.16.0.json",
    "formulas/formulas-v0.16.0.tex",
    "release/v0.3.0-manifest.json",
    "release/v0.4.0-manifest.json",
    "release/v0.5.0-manifest.json",
    "release/v0.6.0-manifest.json",
    "release/v0.7.0-manifest.json",
    "release/v0.8.0-manifest.json",
    "release/v0.9.0-manifest.json",
    "release/v0.10.0-manifest.json",
    "release/v0.10.0-release-notes.md",
    "release/v0.11.0-manifest.json",
    "release/v0.11.0-release-notes.md",
    "release/v0.12.0-manifest.json",
    "release/v0.12.0-release-notes.md",
    "release/v0.13.0-manifest.json",
    "release/v0.13.0-release-notes.md",
    "release/v0.14.0-manifest.json",
    "release/v0.14.0-release-notes.md",
    "release/v0.15.0-manifest.json",
    "release/v0.15.0-release-notes.md",
    "release/v0.16.0-manifest.json",
    "release/v0.16.0-release-notes.md",
    "release/v0.16.1-manifest.json",
    "release/v0.16.1-release-notes.md",
    "release/v0.16.2-manifest.json",
    "release/v0.16.2-release-notes.md",
    "scripts/build_public_case_candidates.py",
    "scripts/seal_public_case_packets.py",
    "scripts/build_release_manifest.py",
    "scripts/run_coe_integrity_audit.py",
    "scripts/build_v0_11_claim_map.py",
    "scripts/build_v0_12_claim_map.py",
    "scripts/build_forward_citation_tranche_v0_12_0.py",
    "scripts/build_forward_citation_author_screening_v0_13_0.py",
    "scripts/validate_forward_citation_author_screening_v0_13_0.py",
    "scripts/build_v0_13_claim_map.py",
    "scripts/build_v0_14_claim_map.py",
    "scripts/build_v0_15_claim_map.py",
    "scripts/build_v0_16_claim_map.py",
    "scripts/build_v0_16_release_manifest.py",
    "scripts/build_v0_16_1_release_manifest.py",
    "scripts/build_v0_16_2_release_manifest.py",
    "scripts/build_v0_15_release_manifest.py",
    "scripts/build_preprints_source_archive.py",
    "scripts/validate_preprints_package.py",
    "scripts/validate_forward_citation_proposition_review_v0_14_0.py",
    "scripts/build_arxiv_preprint.py",
    "scripts/build_arxiv_monochrome_figures.py",
    "scripts/build_arxiv_source_archive.py",
    "scripts/sync_overleaf_preprint.py",
    "scripts/validate_arxiv_package.py",
    "audits/v0.5.0/audit-plan.md",
    "audits/v0.5.0/audit-results.json",
    "audits/v0.5.0/audit-report.md",
    "audits/v0.5.0/exceptions.md",
    "audits/v0.6.0/audit-plan.md",
    "audits/v0.6.0/audit-results.json",
    "audits/v0.6.0/audit-report.md",
    "audits/v0.6.0/exceptions.md",
    "audits/v0.8.0/audit-plan.md",
    "audits/v0.8.0/audit-results.json",
    "audits/v0.8.0/audit-report.md",
    "audits/v0.8.0/exceptions.md",
    "audits/v0.9.0/audit-plan.md",
    "audits/v0.9.0/audit-results.json",
    "audits/v0.9.0/audit-report.md",
    "audits/v0.9.0/exceptions.md",
    "audits/v0.11.0/audit-plan.md",
    "audits/v0.11.0/audit-results.json",
    "audits/v0.11.0/audit-report.md",
    "audits/v0.11.0/exceptions.md",
    "audits/v0.12.0/audit-plan.md",
    "audits/v0.12.0/audit-results.json",
    "audits/v0.12.0/audit-report.md",
    "audits/v0.12.0/exceptions.md",
    "audits/v0.13.0/audit-plan.md",
    "audits/v0.13.0/audit-results.json",
    "audits/v0.13.0/audit-report.md",
    "audits/v0.13.0/exceptions.md",
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
    "assessments/v0.6.0/TAE-PUB-001-oko-1983.json",
    "assessments/v0.6.0/oko-change-ledger.json",
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
    "paper/manuscript-reader.md",
    "paper/manuscript-pressure-test-v0.8.0.md",
    "paper/review-record-v0.8.0.md",
    "paper/review-record-v0.9.0.md",
    "paper/author-screening-completion-gate.md",
    "paper/next-evidence-gates-v0.10.0.md",
    "paper/inaccessible-risk-sample-v0.11.0.md",
    "paper/forward-citation-retrieval-tranche-v0.12.0.md",
    "paper/forward-citation-author-screening-protocol-v0.13.0.md",
    "paper/forward-citation-author-screening-v0.13.0.md",
    "paper/forward-citation-proposition-review-protocol-v0.14.0.md",
    "paper/forward-citation-proposition-review-v0.14.0.md",
    "paper/preprint-readiness-v0.14.0.md",
    "paper/revision-plan-v0.16.0.md",
    "paper/data/author-screening-gate-v0.8.0.json",
    "paper/data/author-screening-decisions-v0.9.0.csv",
    "paper/data/author-screening-gate-v0.9.0.json",
    "paper/data/close-source-full-text-gate-v0.10.0.csv",
    "paper/data/inaccessible-record-retrieval-v0.10.0.csv",
    "paper/data/inaccessible-risk-sample-v0.11.0.csv",
    "paper/data/inaccessible-risk-sample-v0.11.0.json",
    "paper/data/forward-citation-retrieval-evidence-v0.12.0.json",
    "paper/data/forward-citation-author-review-queue-v0.12.0.csv",
    "paper/data/forward-citation-author-screening-decisions-v0.13.0.csv",
    "paper/data/forward-citation-author-screening-v0.13.0.json",
    "paper/data/forward-citation-proposition-review-v0.14.0.csv",
    "paper/data/forward-citation-proposition-review-v0.14.0.json",
    "paper/data/direct-query-resolution-v0.14.0.json",
    "paper/data/authenticated-interface-searches-v0.10.0.csv",
    "paper/data/next-evidence-gates-v0.10.0.json",
    "paper/literature-support-audit-v0.7.0.json",
    "paper/literature-support-audit-v0.7.0.md",
    "paper/literature-support-audit-v0.9.0.json",
    "paper/literature-support-audit-v0.9.0.md",
    "paper/tables.md",
    "paper/tables/manuscript-tables.tex",
    "paper/REVIEW.md",
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
    "paper/preprints/README.md",
    "paper/preprints/00README.XXX",
    "paper/preprints/metadata.yaml",
    "paper/preprints/main.tex",
    "paper/preprints/source-manifest.json",
    "paper/archive/README.md",
    "paper/archive/v0.15.0/README.md",
    "paper/archive/v0.15.0/preprints-source-v0.15.0.zip",
    "paper/archive/v0.15.0/preprints-compiled-v0.15.0.pdf",
    "paper/preprints/preprints-source-v0.16.0.zip",
    "paper/preprints/preprints-compiled-v0.16.0.pdf",
    "paper/preprints/compile-receipt-v0.16.0.json",
    "paper/preprints/overleaf-compile-receipt.json",
    "paper/archive/v0.15.0/overleaf-compile-receipt-v0.15.0.json",
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
    "scripts/run_formal_literature_search.py",
    "scripts/propose_formal_search_screening.py",
    "scripts/verify_formal_search_metadata.py",
    "scripts/validate_formal_search.py",
    "scripts/validate_release_snapshot.py",
    "scripts/validate_v060_adjudication.py",
    "scripts/validate_literature_support.py",
    "scripts/render_reader_manuscript.py",
    "scripts/validate_author_screening_gate.py",
    "scripts/build_author_screening_decisions_v0_9_0.py",
    "scripts/validate_next_evidence_gates.py",
    "scripts/build_inaccessible_risk_sample_v0_11_0.py",
    "paper/claim-crosswalk.md",
    "paper/scientistone-artifact-pressure-test.md",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/case-proposal.yml",
    ".github/ISSUE_TEMPLATE/construct-ambiguity.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "mappings/governed-decision-intelligence.md",
    "mappings/human-influence-telemetry.md",
    "mappings/cdfi-framework.md",
    "mappings/cdcf-governance.md",
)

PRIVATE_TERMS = (
    "Research Scholar " + "candidacy",
    "application " + "strategy",
    "what Mark " + "can claim",
)

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
CLAIM_ID = re.compile(r"\bTAE-C\d{2}\b")
CASE_DIRECTORIES = (
    "cases/TAE-PUB-001-oko-1983",
    "cases/TAE-PUB-002-patriot-zg710-2003",
    "cases/TAE-PUB-003-patriot-fa18-2003",
)


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def validate_required_files(failures: list[str]) -> None:
    for relative in REQUIRED_FILES:
        path = ROOT / relative
        if not path.is_file():
            fail(f"missing required file: {relative}", failures)
        elif path.stat().st_size == 0:
            fail(f"empty required file: {relative}", failures)


def validate_internal_links(failures: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            clean_target = target.split("#", 1)[0]
            if not clean_target or clean_target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = (path.parent / clean_target).resolve()
            if not resolved.exists():
                relative_source = path.relative_to(ROOT)
                fail(f"broken local link in {relative_source}: {target}", failures)


def validate_versions(failures: list[str]) -> None:
    required_markers = {
        "README.md": f"Version: {REPOSITORY_VERSION}",
        "RESEARCH_STATUS.md": f"**Version:** {REPOSITORY_VERSION}",
        "CITATION.cff": f"version: {REPOSITORY_VERSION}",
        f"release/v{REPOSITORY_VERSION}-release-notes.md": f"# v{REPOSITORY_VERSION}:",
    }
    for relative, marker in required_markers.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        if marker not in text:
            fail(f"version marker missing from {relative}: {marker}", failures)


def validate_claim_ids(failures: list[str]) -> None:
    text = (ROOT / "CLAIMS.md").read_text(encoding="utf-8")
    identifiers = CLAIM_ID.findall(text)
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    if duplicates:
        fail(f"duplicate claim identifiers: {', '.join(duplicates)}", failures)
    if not identifiers:
        fail("no claim identifiers found", failures)


def validate_formula_register(failures: list[str]) -> str:
    register_path = ROOT / "formulas/formula-register-v0.16.0.json"
    schema_path = ROOT / "schemas/formula-register.schema.json"
    try:
        register = json.loads(register_path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        fail(f"formula register could not be read: {exc}", failures)
        return ""

    validator = Draft202012Validator(schema)
    schema_errors = sorted(validator.iter_errors(register), key=lambda error: list(error.path))
    for error in schema_errors:
        locator = "/".join(str(part) for part in error.path) or "root"
        fail(f"formula register schema failure at {locator}: {error.message}", failures)
    if schema_errors:
        return ""

    formulas = register["formulas"]
    identifiers = [row["formula_id"] for row in formulas]
    expected = [f"TAE-F{number:02d}" for number in range(1, 9)]
    if identifiers != expected:
        fail(f"formula register identifier order mismatch: {identifiers}", failures)

    tex = (ROOT / "formulas/formulas-v0.16.0.tex").read_text(encoding="utf-8")
    for formula in formulas:
        formula_id = formula["formula_id"]
        if f"% {formula_id}:" not in tex:
            fail(f"formula identifier missing from LaTeX set: {formula_id}", failures)
        for location in formula["source_locations"]:
            source_path = ROOT / location["path"]
            if not source_path.is_file():
                fail(f"formula source is missing for {formula_id}: {location['path']}", failures)
                continue
            if location["marker"] not in source_path.read_text(encoding="utf-8"):
                fail(f"formula source marker is missing for {formula_id}: {location['path']}", failures)
        for relative in formula["implementation_paths"]:
            if not (ROOT / relative).is_file():
                fail(f"formula implementation is missing for {formula_id}: {relative}", failures)

    compiled = sum(row["publication_status"] == "compiled_paper" for row in formulas)
    supporting = sum(row["publication_status"] == "supporting_repository_method" for row in formulas)
    if (compiled, supporting) != (4, 4):
        fail(f"formula publication-status count mismatch: compiled={compiled}, supporting={supporting}", failures)
    return f"formula register: PASS (v0.16.0; {len(formulas)} formulas; {compiled} compiled-paper, {supporting} supporting)"


def validate_public_boundary(failures: list[str]) -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix not in {".md", ".cff", ".yml", ".yaml"}:
            continue
        text = path.read_text(encoding="utf-8")
        for term in PRIVATE_TERMS:
            if term.lower() in text.lower():
                relative = path.relative_to(ROOT)
                fail(f"private term found in {relative}: {term}", failures)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_public_case_schemas(failures: list[str]) -> None:
    format_checker = FormatChecker()
    assessment_schema = json.loads(
        (ROOT / "schemas/public-case-assessment.schema.json").read_text(encoding="utf-8")
    )
    source_schema = json.loads(
        (ROOT / "schemas/source-manifest.schema.json").read_text(encoding="utf-8")
    )
    assessment_validator = Draft202012Validator(assessment_schema, format_checker=format_checker)
    source_validator = Draft202012Validator(source_schema, format_checker=format_checker)

    for relative in CASE_DIRECTORIES:
        case_dir = ROOT / relative
        assessment = json.loads((case_dir / "assessment.json").read_text(encoding="utf-8"))
        sources = json.loads((case_dir / "source-manifest.json").read_text(encoding="utf-8"))
        for error in assessment_validator.iter_errors(assessment):
            fail(f"assessment schema failure in {relative}: {error.message}", failures)
        for error in source_validator.iter_errors(sources):
            fail(f"source schema failure in {relative}: {error.message}", failures)

        source_ids = {source["source_id"] for source in sources["sources"]}
        refs = set(assessment["autonomy"]["evidence_refs"])
        for section in ("trust_evidence", "practical_control"):
            for finding in assessment[section].values():
                refs.update(finding["evidence_refs"])
        missing = sorted(refs - source_ids)
        if missing:
            fail(f"unknown source references in {relative}: {', '.join(missing)}", failures)

    current = json.loads((ROOT / "assessments/v0.6.0/TAE-PUB-001-oko-1983.json").read_text(encoding="utf-8"))
    for error in assessment_validator.iter_errors(current):
        fail(f"v0.6 Oko assessment schema failure: {error.message}", failures)


def validate_packet_hashes(failures: list[str]) -> None:
    index = json.loads(
        (ROOT / "cases/public-case-packet-index.json").read_text(encoding="utf-8")
    )
    if index.get("version") != PUBLIC_CASE_VERSION or len(index.get("packets", [])) != 3:
        fail("public-case packet index must contain three v0.3.0 packets", failures)
        return

    indexed = {row["directory"]: row for row in index["packets"]}
    for relative in CASE_DIRECTORIES:
        case_dir = ROOT / relative
        manifest_path = case_dir / "packet-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("protocol_freeze_commit") != "180ddda1d70f0ee36faaf8875e839bbc99cbbec2":
            fail(f"protocol freeze commit mismatch in {relative}", failures)
        for name, expected in manifest.get("artifacts", {}).items():
            actual = digest(case_dir / name)
            if actual != expected:
                fail(f"packet hash mismatch in {relative}/{name}", failures)
        row = indexed.get(relative)
        if row is None:
            fail(f"packet missing from index: {relative}", failures)
        elif row.get("manifest_sha256") != digest(manifest_path):
            fail(f"packet index hash mismatch: {relative}", failures)


def validate_candidate_search(failures: list[str]) -> None:
    data = json.loads(
        (ROOT / "cases/data/candidate-search-output.json").read_text(encoding="utf-8")
    )
    aiid = data.get("inputs", {}).get("aiid", {})
    oecd = data.get("inputs", {}).get("oecd", [])
    expected = {
        "version": PUBLIC_CASE_VERSION,
        "candidate_count": 928,
        "aiid_sha256": "97fe770b0e92730c98fbb05bca8f9e2df6803f0f386d94404a19a7677d70f240",
        "aiid_candidates": 828,
        "oecd_sha256": "741bcde4c920a0501589637368831c6242641738a176588312b24056fc27207e",
    }
    if data.get("version") != expected["version"]:
        fail("candidate output version mismatch", failures)
    if data.get("candidate_count") != expected["candidate_count"]:
        fail("candidate output count mismatch", failures)
    if aiid.get("sha256") != expected["aiid_sha256"]:
        fail("AIID input hash mismatch", failures)
    if aiid.get("counts", {}).get("candidate_records") != expected["aiid_candidates"]:
        fail("AIID candidate count mismatch", failures)
    if not oecd or oecd[0].get("sha256") != expected["oecd_sha256"]:
        fail("OECD input hash mismatch", failures)

    first_five = [row.get("candidate_id") for row in data.get("candidates", [])[:5]]
    if first_five != ["AIID-27", "AIID-42", "AIID-79", "AIID-444", "AIID-445"]:
        fail(f"frozen screening order mismatch: {first_five}", failures)
    forbidden_fields = {"text", "article_text", "report_text"}
    for candidate in data.get("candidates", []):
        if forbidden_fields.intersection(candidate):
            fail(f"redistributed article text field in {candidate.get('candidate_id')}", failures)

    register = (ROOT / "cases/public-case-selection-register.md").read_text(encoding="utf-8")
    for marker in ("AIID-27", "INCLUDE-PRE", "AIID-42", "EX-SOURCE", "AIID-79", "EX-BOUNDARY", "AIID-444", "INCLUDE-FORCE", "AIID-445", "INCLUDE-GAP"):
        if marker not in register:
            fail(f"selection register marker missing: {marker}", failures)


def validate_case_interactions(failures: list[str]) -> None:
    assessments = {}
    for relative in CASE_DIRECTORIES:
        data = json.loads((ROOT / relative / "assessment.json").read_text(encoding="utf-8"))
        assessments[data["case_id"]] = data

    oko = json.loads((ROOT / "assessments/v0.6.0/TAE-PUB-001-oko-1983.json").read_text(encoding="utf-8"))["practical_control"]
    for field in ("access", "comprehension", "authority", "feasibility", "exercise", "effect"):
        if oko[field]["state"] != "partially_supported":
            fail(f"TAE-PUB-001 interaction mismatch: {field}", failures)

    tornado = assessments["TAE-PUB-002"]["practical_control"]
    if tornado["authority"]["state"] != "supported":
        fail("TAE-PUB-002 must preserve formal authority", failures)
    for field in ("feasibility", "exercise", "effect"):
        if tornado[field]["state"] != "unsupported":
            fail(f"TAE-PUB-002 interaction mismatch: {field}", failures)

    fa18 = assessments["TAE-PUB-003"]
    if fa18["trust_evidence"]["evidence_completeness"]["state"] != "unsupported":
        fail("TAE-PUB-003 must preserve incomplete evidence", failures)
    for field in ("comprehension", "feasibility", "exercise"):
        if fa18["practical_control"][field]["state"] != "indeterminate":
            fail(f"TAE-PUB-003 missing-evidence mismatch: {field}", failures)


def validate_release_snapshot(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_release_snapshot.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"release snapshot failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_release_candidate(failures: list[str]) -> str:
    relative = f"release/v{WORKING_VERSION}-manifest.json"
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing current release manifest: {relative}", failures)
        return ""
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        fail(f"invalid current release manifest: {exc}", failures)
        return ""
    if manifest.get("version") != WORKING_VERSION:
        fail("current release manifest version mismatch", failures)
    if manifest.get("hash_algorithm") != "SHA-256":
        fail("current release manifest hash algorithm mismatch", failures)
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list) or not artifacts:
        fail("current release manifest artifact list is empty", failures)
        return ""
    indexed = {}
    for row in artifacts:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            fail("current release manifest contains an invalid artifact row", failures)
            continue
        indexed[row["path"]] = row
    if len(indexed) != len(artifacts):
        fail("current release manifest contains duplicate artifact paths", failures)
    # The published tag seals all original bytes. Three current-facing documents
    # have a separately hashed navigation checkpoint; research stays sealed.
    navigation_paths = {"README.md", "CITATION.cff", "RESEARCH_STATUS.md"}
    try:
        navigation = json.loads((ROOT / "docs/navigation-v0.17.0.json").read_text())
        if navigation.get("release_tag") != "v0.17.0":
            raise ValueError("unexpected release tag")
        entries = navigation["artifacts"]
        if not isinstance(entries, dict) or set(entries) != navigation_paths:
            raise ValueError("navigation scope must contain exactly the three declared documents")
        for name, entry in entries.items():
            if entry.get("released_sha256") != indexed[name]["sha256"]:
                raise ValueError("navigation baseline differs from released artifact: " + name)
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        fail(f"invalid current navigation checkpoint: {exc}", failures)
        return ""
    for artifact_path, row in indexed.items():
        file_path = ROOT / artifact_path
        if not file_path.is_file():
            fail(f"current release artifact is missing: {artifact_path}", failures)
            continue
        expected = entries[artifact_path] if artifact_path in navigation_paths else row
        if expected.get("bytes") != file_path.stat().st_size:
            fail(f"current artifact size mismatch: {artifact_path}", failures)
        if expected.get("sha256") != digest(file_path):
            fail(f"current artifact hash mismatch: {artifact_path}", failures)
    return (f"working-tree validation: PASS (v{WORKING_VERSION}; "
            f"{len(indexed) - len(navigation_paths)} preserved release artifacts; "
            f"{len(navigation_paths)} separately hashed navigation documents)")


def validate_solo_suite(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "analysis/run_solo_validation.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + result.stderr).strip()
        fail(f"solo-validation suite failed: {detail}", failures)
        return ""
    return result.stdout.strip()


def validate_figure_set(failures: list[str]) -> str:
    register = json.loads(
        (ROOT / "figures/specifications/figure-register.json").read_text(encoding="utf-8")
    )
    figures = register.get("figures", [])
    identifiers = [row.get("figure_id") for row in figures]
    stubs = [row.get("file_stub") for row in figures]
    expected_identifiers = ["FIG-1", "FIG-2", "FIG-3", "FIG-4", "FIG-5", "FIG-6", "FIG-A1", "FIG-A2", "FIG-A4"]
    if register.get("version") != FIGURE_VERSION or register.get("source_release") != "0.16.0":
        fail("figure register version or source release mismatch", failures)
    if identifiers != expected_identifiers:
        fail(f"figure register identifier mismatch: {identifiers}", failures)
    if len(stubs) != len(set(stubs)):
        fail("duplicate figure file stub", failures)

    result = subprocess.run(
        [sys.executable, "analysis/build_figures.py", "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        detail = (result.stdout + result.stderr).strip()
        fail(f"figure set failed: {detail}", failures)
        return ""
    return result.stdout.strip()


def validate_coe_figure(failures: list[str]) -> str:
    manifest_path = ROOT / "figures/v0.16.0-claim-evidence-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("version") != "0.16.0" or manifest.get("source_audit") != "0.16.0":
        fail("v0.16 claim-evidence figure metadata mismatch", failures)
        return ""
    for section in ("artifacts", "inputs"):
        for row in manifest.get(section, []):
            relative = row["path"]
            path = ROOT / relative
            if (
                not path.is_file()
                or path.stat().st_size != row["bytes"]
                or digest(path) != row["sha256"]
            ):
                fail(f"v0.16 claim-evidence figure mismatch: {relative}", failures)
    with (ROOT / "figures/data/fig-a3-claim-evidence-integrity.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 40:
        fail("v0.16 claim-evidence figure must contain 40 claim rows", failures)
    process = subprocess.run(
        [sys.executable, "analysis/build_claim_evidence_figure.py", "--check"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if process.returncode != 0:
        fail(f"v0.16 claim-evidence figure rebuild failed: {(process.stdout + process.stderr).strip()}", failures)
        return ""
    return "claim-evidence figure: PASS (v0.16.0; 40 claims)"


def validate_coe_audit(failures: list[str]) -> str:
    preserved = ROOT / "audits/v0.9.0/audit-results.json"
    if not preserved.is_file():
        fail("released v0.9 claim-evidence audit is missing", failures)
        return ""
    preserved_result = json.loads(preserved.read_text(encoding="utf-8"))
    if preserved_result.get("version") != "0.9.0" or preserved_result.get("status") != "PASS_WITH_EXCEPTIONS":
        fail("released v0.9 claim-evidence audit metadata mismatch", failures)
        return ""

    for command in (
        [sys.executable, "scripts/build_v0_17_policy_claim_map.py", "--check"],
        [sys.executable, "scripts/run_policy_integrity_audit_v0_17_0.py", "--check"],
    ):
        process = subprocess.run(
            command, cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if process.returncode != 0:
            detail = (process.stdout + process.stderr).strip()
            fail(f"current claim-evidence audit failed: {detail}", failures)
            return ""

    current = json.loads(
        (ROOT / "audits/v0.16.0/audit-results.json").read_text(encoding="utf-8")
    )
    controls = current.get("negative_controls", [])
    detected = sum(1 for row in controls if row.get("detected"))
    claims = current.get("claim_results", [])
    c32 = next((row for row in claims if row.get("claim_id") == "PAPER-C32"), {})
    c33 = next((row for row in claims if row.get("claim_id") == "PAPER-C33"), {})
    c34 = next((row for row in claims if row.get("claim_id") == "PAPER-C34"), {})
    c35 = next((row for row in claims if row.get("claim_id") == "PAPER-C35"), {})
    c36 = next((row for row in claims if row.get("claim_id") == "PAPER-C36"), {})
    c37 = next((row for row in claims if row.get("claim_id") == "PAPER-C37"), {})
    c38 = next((row for row in claims if row.get("claim_id") == "PAPER-C38"), {})
    c39 = next((row for row in claims if row.get("claim_id") == "PAPER-C39"), {})
    c40 = next((row for row in claims if row.get("claim_id") == "PAPER-C40"), {})
    c41 = next((row for row in claims if row.get("claim_id") == "PAPER-C41"), {})
    c42 = next((row for row in claims if row.get("claim_id") == "PAPER-C42"), {})
    c43 = next((row for row in claims if row.get("claim_id") == "PAPER-C43"), {})
    c44 = next((row for row in claims if row.get("claim_id") == "PAPER-C44"), {})
    c45 = next((row for row in claims if row.get("claim_id") == "PAPER-C45"), {})
    c46 = next((row for row in claims if row.get("claim_id") == "PAPER-C46"), {})
    if (
        current.get("version") != "0.16.0"
        or current.get("status") != "PASS_WITH_EXCEPTIONS"
        or len(claims) != 40
        or len(controls) != 39
        or detected != 39
        or c32.get("conclusion_eligible") is not False
        or c33.get("conclusion_eligible") is not True
        or c34.get("conclusion_eligible") is not True
        or c34.get("support") != "pass"
        or c35.get("conclusion_eligible") is not True
        or c36.get("conclusion_eligible") is not True
        or c37.get("conclusion_eligible") is not True
        or c38.get("conclusion_eligible") is not True
        or c39.get("conclusion_eligible") is not True
        or c40.get("conclusion_eligible") is not True
        or c41.get("conclusion_eligible") is not False
        or c41.get("support") != "indeterminate"
        or any(row.get("conclusion_eligible") is not True for row in (c42, c43, c44, c45, c46))
    ):
        fail("current v0.16 claim-evidence audit metadata mismatch", failures)
        return ""
    policy = json.loads(
        (ROOT / "audits/v0.17.0-policy-crosswalk/audit-results.json").read_text(encoding="utf-8")
    )
    policy_controls = policy.get("negative_controls", [])
    policy_claims = policy.get("claim_results", [])
    if (
        policy.get("version") != "0.17.0"
        or policy.get("status") != "PASS_WITH_EXCEPTIONS"
        or len(policy_claims) != 5
        or len(policy_controls) != 9
        or sum(1 for row in policy_controls if row.get("detected")) != 9
        or any(row.get("conclusion_eligible") is not True for row in policy_claims)
    ):
        fail("current v0.17 policy claim-evidence audit metadata mismatch", failures)
        return ""
    return "chain-of-evidence audits: PASS_WITH_EXCEPTIONS (v0.16 preserved: 40 claims and 39/39 controls; v0.17 policy extension: 5 claims and 9/9 controls)"


def validate_adjudication(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_v060_adjudication.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"v0.6 adjudication failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_literature(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_literature_support.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"literature-support audit failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_formal_search(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_formal_search.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"formal-search audit failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_paper_workspace(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_paper.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"paper workspace failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_inaccessible_risk_sample(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/build_inaccessible_risk_sample_v0_11_0.py", "--check"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"inaccessible risk sample failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def validate_forward_citation_screening(failures: list[str]) -> str:
    result = subprocess.run(
        [sys.executable, "scripts/validate_forward_citation_author_screening_v0_13_0.py"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )
    if result.returncode != 0:
        fail(f"forward-citation author screening failed: {(result.stdout + result.stderr).strip()}", failures)
        return ""
    return result.stdout.strip()


def main() -> int:
    failures: list[str] = []
    validate_required_files(failures)
    validate_internal_links(failures)
    validate_versions(failures)
    validate_claim_ids(failures)
    formula_result = validate_formula_register(failures)
    validate_public_boundary(failures)
    validate_public_case_schemas(failures)
    validate_packet_hashes(failures)
    validate_candidate_search(failures)
    validate_case_interactions(failures)
    release_result = validate_release_snapshot(failures)
    release_candidate_result = validate_release_candidate(failures)
    solo_result = validate_solo_suite(failures)
    figure_result = validate_figure_set(failures)
    coe_figure_result = validate_coe_figure(failures)
    coe_audit_result = validate_coe_audit(failures)
    adjudication_result = validate_adjudication(failures)
    literature_result = validate_literature(failures)
    formal_search_result = validate_formal_search(failures)
    risk_sample_result = validate_inaccessible_risk_sample(failures)
    forward_screening_result = validate_forward_citation_screening(failures)
    paper_result = validate_paper_workspace(failures)

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"repository validation: FAIL ({len(failures)} error(s))")
        return 1

    if release_result:
        print(release_result)
    if formula_result:
        print(formula_result)
    if release_candidate_result:
        print(release_candidate_result)
    if solo_result:
        print(solo_result)
    if figure_result:
        print(figure_result)
    if coe_figure_result:
        print(coe_figure_result)
    if coe_audit_result:
        print(coe_audit_result)
    if adjudication_result:
        print(adjudication_result)
    if literature_result:
        print(literature_result)
    if formal_search_result:
        print(formal_search_result)
    if risk_sample_result:
        print(risk_sample_result)
    if forward_screening_result:
        print(forward_screening_result)
    if paper_result:
        print(paper_result)
    print("repository validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
