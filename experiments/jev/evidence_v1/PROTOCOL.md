# JEV-TAE evidence-v1 prespecification

Status: offline materials frozen before any Phase 2 Jev output. This is an internal,
publicly inspectable prespecification, not independent registration. Mock output is
plumbing evidence only. No result here establishes Jev accuracy or practical human control.

## Experiment taxonomy

| ID | Question | Materials and interpretation |
| --- | --- | --- |
| JEV-TAE-1 | Can Jev follow the categorical assessment contract? | Existing v1, unchanged. Its questions expose signal mappings. |
| JEV-TAE-2 | Can Jev reconstruct the state from bounded documentary-style evidence? | 12 translated cases, 21 separate questions each; authority challenge reported separately. |
| JEV-TAE-3 | Does a governance-relevant evidence change produce exactly the expected changes? | Nine nonempty sealed mutation deltas, translated to excerpts; all 21 outputs count. |
| JEV-TAE-4 | Do irrelevant transformations preserve judgments? | 48 nontrivial nuisance variants, plus three inherited normalization-boundary checks. |
| JEV-TAE-5 | Do the frozen questions transfer to reserved synthetic compositions? | Six new mixed-state packets, 126 determinations; no question development on their output. |
| JEV-TAE-6 | How do judgments compare on public cases? | Deferred. Requires a separate source/rights protocol, evidence sufficiency rules and human adjudication. No public-case claims here. |

## Evidence and inference boundary

The original fixture contains categorical signals, not underlying source documents.
`author.py` operationalizes these signals into newly authored synthetic excerpts.
Times, trial counts, permission logs and receipts are illustrative assumptions,
not facts recovered from a historical event. `translation.json` records every
non-generic translation. Missing and excluded topics use explicit packet/charter
statements. These statements are evidence about the supplied synthetic packet,
not evidence of real-world absence or exclusion.

A packet contains independent, topic-bounded excerpts. Each question assesses only
its named topic. It must not infer another field from that excerpt. This preserves
the source contract's independence, including mutations whose cross-topic narratives
could otherwise conflict. It limits ecological validity: cross-document synthesis,
causal consistency and real-world control remain untested. All 21 questions retain
the five evidence states. Indeterminate evidence is distinct from model uncertainty.

`cards.json` contains only documentary state plus local routing metadata. The wire
request contains `state`, semantic `questions`, and the pinned model name. Local
IDs, suite names, source paths, categorical signals, gold labels, mutation deltas,
and provenance never enter requests. Construct names identify the question and
excerpt; they are not answers. Generic state criteria appear in questions because
the classification task needs definitions; fixture token-to-label mappings do not.

The corpus is intentionally simple. It can still reward recognition of repeated
phrases. Its success would support bounded evidence reconstruction only. A later
independent-author corpus would be needed to test broader documentary judgment.

## Authority challenge

Sixteen one-question packets cross eight authority types with absence/presence of
recorded use: review, recommend, object, delay, suspend, cancel, override, and
approval-required. Review/recommend/object have an explicit advisory permission
boundary even when used. The remaining types have explicit binding permissions;
use is supported by an execution record. Role titles and verbs alone are insufficient.
Temporary binding delay/suspension counts as authority for this experiment, without
implying permanent cancellation power or satisfaction of other control stages.
Assigned permission without recorded use is partial under TAE's authority construct.
These are new experimental judgments, not sealed-oracle extensions.

## Holdout and nuisance controls

Holdouts are five balanced rotating state combinations and a sixth combination
using alternative supported signals where available. Labels follow the existing
assessment contract. They share translation templates with reconstruction cases,
so JEV-TAE-5 measures compositional transfer only. They are public and known to the
author; “unseen” means no observed Jev responses and no output-informed tuning.
There is no claim that a model provider has never seen the public repository.

Each baseline has four variants: reverse excerpt order, neutral packet wording,
irrelevant storage context, and equivalent paraphrase. The paraphrase rewrites
access timing substantively while adding a neutral reporting frame elsewhere.
All preserve permissions, times, actions and outcomes. `pairs.json` fixes the
expected empty deltas. The three inherited title/outcome/autonomy mutations are
input-identical after normalization and are reported as boundary/repetition checks,
separately from nontrivial invariance. No post-output paraphrase selection is allowed.

## Repetition and stochasticity policy

`policy.json` fixes three scheduled repetitions of every request, in corpus order,
with repetition as the outer loop. Primary results use repetition 1. Repetitions
2 and 3 are sensitivity analyses, reported separately and pooled descriptively;
no majority-vote substitution, best-run selection or adaptive stopping is allowed.
There are 94 requests and 1,654 determinations per repetition, 282 requests and
4,962 determinations in total. The mock follows the same schedule.

Identical requests have identical serialized bytes and hashes across repetitions.
No seed or temperature is sent because v1's verified SDK surface does not specify
such controls. Record requested and resolved model, SDK version, code hashes,
freeze hash, request/response bytes and attempt status. Use exactly one attempt per
scheduled request and no retries; invalid/transport failures remain missing for
that scheduled position. Do not replace them with indeterminate labels. Retain all
available raw responses. A rerun is a separately identified protocol deviation,
never a replacement of the original run.

Live execution is deliberately unavailable in this offline harness. A later live
transport must use the frozen request manifest unchanged, verify these hashes and
the sealed oracle first, use the v1 pinned SDK/model with no retries, retain raw
responses and report unavailable version metadata. Any provider incompatibility,
model change or request change requires a versioned amendment before new output.
Mixed resolved versions are not pooled; between-version pairs are not evaluated.
This repository change makes no live request even when credentials exist.

## Analysis

Report each suite and repetition separately, with descriptive pooled summaries as
secondary outputs. Agreement and disagreement use valid determinations as their
denominator; report valid/scheduled coverage beside them. The five-class confusion
matrix uses gold rows and predicted columns in the frozen state order, including
zero cells. Recall is diagonal divided by valid gold-state count, with null when
that count is zero; also report scheduled gold-state counts to expose selective
missingness. Multiclass Brier is mean sum over five squared probability errors,
range 0–2, without a probability floor. It is not a calibration claim.

Report overall and per-construct agreement, recall, Brier, disagreement rate,
request failures, invalid responses, resolved-version inventory, missing versions,
and within-request repeated-choice changes/max probability shifts. Delta success
requires equality of the complete observed from/to set with the fixed expected
set; unchanged extra fields count, and equal wrong baseline/follow-up labels can
produce a matching empty set. Report absolute accuracy alongside delta metrics.
Pairs require two valid responses from the same resolved version. Report paired
coverage, input-identical status and non-evaluable pairs explicitly. Invariance
failures include any changed choice; probability shifts are descriptive, without
an after-the-fact tolerance or causal claim.

The independent sampling unit is a constructed case family, not a determination.
Variants and repeated calls are dependent. No significance test, population
confidence interval, real-world error rate or benchmark superiority claim is
prespecified for this small authored corpus. Raw metrics remain unchanged by
adjudication. `REPORT_TEMPLATE.md` is the required human reporting shell.

## Adjudication

Open a record for every disagreement and invalid response. Two reviewers first
assess the excerpt/question without the Jev distribution or reference label, then
inspect both with provenance. Record their identities, independent notes, evidence
references, uncertainty, and reconciliation. The author cannot claim independent
review of their own translation. If two reviewers are unavailable, retain an open
UNRESOLVED record. Reviewers must distinguish the sealed categorical reference
from the experimental translation; neither is presumed infallible.

Dispositions are JEV_ERROR, ORACLE_AMBIGUITY, QUESTION_DEFECT,
EVIDENCE_TRANSLATION_DEFECT, CONSTRUCT_AMBIGUITY, INSUFFICIENT_EVIDENCE, UNRESOLVED.
A model error requires adequate evidence and a defensible question/reference;
an oracle ambiguity records a contested interpretation without editing the seal;
a question defect concerns wording/scope; a translation defect concerns added,
lost or altered facts; construct ambiguity concerns the definition itself;
insufficient evidence concerns the bounded packet. Multiple candidate diagnoses
belong in reviewer notes; one primary disposition or UNRESOLVED is retained.
`adjudication.schema.json` defines the append-only record shape. Closed records
require two distinct reviewers and rationale. Supersession links preserve earlier
records. Corrections require a new versioned experiment and new hashes, while raw
scores, v1 materials and released findings remain unchanged. Any adjusted analysis
is separately labeled exploratory, with its complete exclusion denominator.

## Freeze and amendments

`freeze.json` hashes all prespecified material bytes, authoring/analysis code,
schemas, templates, tests, and the complete pre-existing v1 namespace. It also
records the source commit and protected source/oracle hashes. Verify hashes before
reading requests or scores. The implementation checks the manifest against its
committed Git blob to detect local replacement of both material and manifest.
Git review of the freeze commit remains the trust root; this is not an external
timestamp service. Never regenerate or edit this version after live inference.
Amendments use a new directory and document the reason, timing and observed output.
