# TAE personal source-passage review

Recorded November 3, 2026 (America/New_York). Repository base: `2f462dcb147613c6634aab143102da81fcdbff93`. This additive record documents Mark Julius Banasihan's reported source reading and proposed wording corrections, with Codex assistance. It does not revise the manuscript, website, historical attestations, source packets, scores or closed research phase.

The [November 1 manuscript](../paper/revisions/2026-11-01/main.tex) is the comparison target. Personal reading, AI inspection, wording proposals and approval of an exact manuscript are separate states. This is a targeted review of material passages, not a new systematic literature review or independent validation.

## Current review status

| Item | Source reading | TAE context reading | Wording disposition |
| :--- | :--- | :--- | :--- |
| TAE-SR-01 | Reported complete for the section 3.4 content described below and both numbered links; reused earlier retrievals | Reported complete: first two section 2.1 paragraphs, bibliography entry 40 and the full review record, through raw files at the pinned commits | Corrected three-sentence candidate accepted for a later draft only; manuscripts unchanged; see completion receipt |
| TAE-SR-02 | Reported complete for the three Tracking/Tracing blocks and the first two ideas in the identified earlier passage; supplementary access route not restated | First section 2.1 paragraph compared using the previously read raw manuscript at the pinned commit | Three-sentence replacement and revised closing summary recorded as proposals; modality and attribution limits retained; no manuscript approval |
| TAE-SR-03 | Reported complete for the selected IFAC PDF passages, including the page-776 continuation and rare-intervention discussion | All four Bainbridge citation contexts and historical provenance reviewed within the reported scope; neighboring-source claims remain unreviewed | Author proposals and dated provenance supplement recorded; challenge-opportunity source remains unresolved; no exact-draft approval |
| TAE-SR-04 | Complete abstract reported read through an unidentified library-catalog record; publisher abstract display, publication details and body unread by the author | Compared with the already-reviewed TAE claims at 117/201/1189 | Three wording proposals recorded; detailed definition, workload and challenge-opportunity claims remain unverified; no manuscript approval |
| TAE-SR-05 | Five assigned v1 sections reported read, including all of 5.3.1 through before 5.3.2; section-page confirmation, cited originals and journal body remain unchecked | Quoted passages at 131/253/1189 assessed in the earlier reply; efficacy comparison recorded as author interpretation | Earlier candidates and new summary remain proposals; citation/version treatment unresolved; historical line 1640 and partial receipt preserved; no manuscript approval |

Further passage assignments are not fixed by this first receipt. Matching earlier HIT reading may be reused within its actual scope, without assuming approval of a different TAE proposition.

## TAE-SR-01: Cavalcante Siebert and colleagues, Property 4

### Source and access

Source: [Meaningful human control: actionable properties for AI system development](https://link.springer.com/article/10.1007/s43681-022-00167-3), DOI `10.1007/s43681-022-00167-3`. The journal volume is AI and Ethics 3, 241–255 (2023), with online publication May 18, 2022.

The author reports reading section 3.4 through its forward/backward-link entries, stopping before Figure 5. He used the Springer article text retrieved earlier for the HIT SR-04 check, cross-checked against a publisher-formatted PDF whose exact URL and version are unidentified. He did not fetch the Springer page again for this review. No identity of retrieved copies or historical bytes is asserted.

He reports three pre-list paragraphs where Codex's extraction grouped the same material into five. Use content locators rather than paragraph counts. His account covers the opening tracing problem, the explicit-link requirement, moral understanding, logging/reporting, loss of tracing despite aware decisions, and both numbered links. Codex rechecked those content groups in the current publisher HTML and identified no additional requested text beyond that account. This does not authenticate the earlier copies.

Figure 5 and section 3.4.1 remain outside this review. The author says an earlier retrieval included section 3.4.1 but he used none of it for this answer. Availability in retrieved text is not a reading attestation.

### Reported reading and corrections

| Content locator | Retained account and boundary |
| :--- | :--- |
| Property 4 heading and opening | Actions must be linked to humans aware of their moral responsibility. The preceding three properties leave the need to trace system effects to relevant humans' moral understanding. |
| Link requirement | The proposed links are explicit, explainable and inspectable, connecting system actions to morally loaded human decisions and actions. The authors acknowledge a more demanding tracing requirement than the original account. |
| Moral understanding and logging | Humans making morally consequential decisions about design, deployment or use should demonstrate moral understanding. Relevant decisions, including design, use and policy, should be logged and reported to link AI actions with aware human decisions. |
| Awareness without an identifiable link | Responsible, fully aware decisions still lose tracing if the link from system action to underlying human decisions is not readily identifiable. Awareness and linkage have distinct roles. |
| Forward link | Humans should be aware of the responsibility associated with morally consequential decisions, even when AI executes the action. |
| Backward link | Human decisions and actions leading to a consequence of system operation should be readily identifiable. |

The author distinguishes Property 3's ability–authority–responsibility relationship from Property 4's linkage and logging requirements. TAE's “including” compresses those separate properties. His earlier reported section 3.3 reading supplies the first part's source scope, with the [HIT RW-02 receipt's access qualifications and section 3.3/3.3.1 ordering inconsistency](https://github.com/node-and-norm/human-influence-telemetry/blob/22b6a8ad5ea5ef43f1d20c9b63b790cf7294ffbb/paper/source-checks-ofqual-related-work-2026-10-17.md#sr-04-rw-02-personal-source-review-and-selected-review-completion-november-3-2026) retained; it does not establish a newly verified hierarchy.

### Manuscript location and author name

The target sentence is in [section 2.1, line 184](../paper/revisions/2026-11-01/main.tex#L184):

> Siebert et al. (2023) link ability, authority, and responsibility, including logged human decisions that can be connected to system actions.

The author read the repository README only to place this sentence and explicitly had not found its manuscript location, surrounding context or bibliography entry. Those personal checks remain pending. Codex located the immediately preceding tracking/tracing paragraph at line 181, the target paragraph at line 184 and [bibliography entry 40 at line 1535](../paper/revisions/2026-11-01/main.tex#L1535).

The bibliography already gives Luciano Cavalcante Siebert's full name. The publisher's recommended citation uses Cavalcante Siebert as the citation surname. Record an in-text citation correction for later review, keeping the 2023 volume and 2022 online dates distinct. No bibliography or manuscript edit is performed here.

### Proposed wording and scope qualifications

Author's proposed replacement, preserved verbatim:

> Cavalcante Siebert et al. (2023) propose that a human’s responsibility be matched by their ability and authority to control a human-AI system (Property 3). Separately, they propose that system actions be explicitly and inspectably linked to logged human decisions with moral implications, made by people aware of their moral responsibility (Property 4). These are proposed design properties; the paper offers no test of whether such links yield effective control.

The last sentence is broader than the reported reading establishes. Limit the no-test statement to the reviewed section 3.4 passage. Preserve explainability and reporting alongside explicitness, inspectability and logging.

Codex-prepared bounded candidate for the next context check, not an approved manuscript revision:

> Cavalcante Siebert et al. (2023) propose matching a human’s responsibility with their ability and authority to control a human-AI system (Property 3). Separately, they call for explicit, explainable and inspectable links between system actions and logged and reported human decisions with moral implications, made by people aware of their moral responsibility (Property 4). Section 3.4 sets out these design requirements without reporting a test of whether the links establish effective control.

The author's comparison with TAE's traceability column is an interpretive analogy. TAE's locator-resolution check and Property 4's morally aware, explainable action-to-decision links are different constructs. Do not treat them as equivalent, reduce the earlier framework to working references, or imply that evidence fitness and practical control are concerns unique to TAE. The selected passage neither validates TAE nor establishes a paper-wide absence of empirical evaluation.

### Disposition

The selected source content is reported read, with the stated access and exclusion limits. Review of the quoted sentence is recorded; personal manuscript-context and bibliography reading remains pending. The proposed and scope-qualified wording is retained for review only.

Historical author attestations, screening/proposition permissions, the closed methods phase, original Jev adjudications and the completed 24-item collaborative review remain unchanged. This receipt creates no full-paper attestation, independent verification, new research finding, manuscript approval or publication authorization. The manuscript and website are unchanged.

## TAE-SR-01 context review and bounded-use decision: November 3, 2026

Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance. This receipt completes the stated source-and-context item; it does not authorize manuscript changes.

### Reported reading and access

The author reports reading all requested items: the first two paragraphs of section 2.1 and bibliography entry 40 in `paper/revisions/2026-11-01/main.tex` at commit `2f462dcb147613c6634aab143102da81fcdbff93`, and the full initial review record at commit `28ea98d31897f881f10107123bd8db0404a03f77`, including its proposed-wording section. GitHub's blob pages refused his automated access; he read the same pinned files through GitHub's raw file host. This is his reported access route, not an attestation of viewing the GitHub wrapper or reproducing the research.

He identifies the first paragraph's tracking/tracing account and the second paragraph's opening, target sentence, Davidovic citation and closing institutional questions. He reports that reference 40 lists all thirteen authors in publisher order, beginning with Luciano Cavalcante Siebert, with the 2023 volume, pages 241–255 and correct DOI. Its contents match the publisher PDF header he previously checked. His reading of this reference does not establish personal reading of the publisher's recommended-citation block.

### Corrected candidate accepted for a later draft

The author accepts the candidate with a scope correction and a fidelity addition. Property 3 remains direction-neutral, preserving the earlier ability–authority ordering qualification. Property 4 restores human actions alongside decisions. The final sentence now names Property 4 alone: section 3.4 must not be described as setting out Property 3.

Author's corrected candidate, preserved verbatim:

> Cavalcante Siebert et al. (2023) propose matching a human’s responsibility with their ability and authority to control a human-AI system (Property 3). Separately, they call for explicit, explainable and inspectable links between system actions and logged and reported human decisions and actions with moral implications, made by people aware of their moral responsibility (Property 4). Section 3.4 sets out the Property 4 requirements without reporting a test of whether such links establish effective control.

The author considers this consistent with the paragraph's opening reference to developing the prior relationship and its closing questions about whose control, over which decisions and for what purpose. He notes that three sentences increase the paragraph's length and suggests possible compression for a later draft. That optional compression is not substituted for the accepted wording here.

### Updated PDF description and attribution limits

The earlier receipt preserves what was identified at its checkpoint. The author now identifies the cross-checked PDF as the Politecnico di Torino institutional-repository copy, carrying the header AI and Ethics (2023) 3:241–255 and the received, accepted and online-publication dates. Record that reported institution and publisher-format description. An exact download URL or file hash has not been supplied, so byte identity or a specifically pinned institutional file is not established.

The author explicitly has not read the publisher's recommended-citation block. The earlier statement that it uses Cavalcante Siebert is Codex's separate check of the publisher's Cite this article section, not his verification. The current reference's full author list and his PDF reading have their own reported scopes. Keep the 2023 volume citation distinct from online publication on May 18, 2022.

### New source-comparison lead

The author flags a possible difference between TAE's first paragraph, which connects each system action to a person, and Cavalcante Siebert and colleagues' section 2 restatement involving at least one relevant human agent. He has not read Santoni de Sio and van den Hoven (2018), the original source cited by that TAE paragraph. This is a proposed comparison to check against the original, not an established difference in logical strength, an accepted correction to the first paragraph or a new source-reading attestation.

Disposition: TAE-SR-01's selected source-content and manuscript-context reading are reported complete with the stated routes and exclusions. The corrected candidate is accepted for a later draft only. Figure 5 and section 3.4.1 remain excluded, and the publisher citation-block check remains attributed to Codex. Historical attestations, source packets, screening/proposition permissions, scores, original Jev adjudications, the closed research phase and broader claims remain unchanged. No manuscript revision, website update or publication approval is performed or authorized by this receipt.

## TAE-SR-02: Santoni de Sio and van den Hoven, selected Tracking/Tracing passages

Recorded November 3, 2026. Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance.

### Source, reading route and scope

Source: [Meaningful Human Control over Autonomous Systems: A Philosophical Account](https://www.frontiersin.org/journals/robotics-and-ai/articles/10.3389/frobt.2018.00015/full), DOI `10.3389/frobt.2018.00015`, Frontiers in Robotics and AI 5, article 15 (2018).

The author reports reading all three assigned blocks through a direct fetch of the Frontiers full-text HTML: Tracking's dual-tracking explanation through the paragraph after the first necessary condition; Tracking's closing qualifications about whose reasons count and moral goodness; and Tracing's closing definition through the paragraph following the second necessary condition. He stopped before the weapons-implications section and did not open the PDF. The attached footnotes 9, 11, 13 and 14 appeared in retrieved text but were not relied on; availability does not attest their personal inspection.

He compared these passages with TAE section 2.1's first paragraph as previously read through raw `main.tex` at commit `2f462dcb147613c6634aab143102da81fcdbff93`. This is reported comparison against that pinned paragraph, not a new whole-manuscript review.

### Reported reading and corrections

| Content | Retained account and boundary |
| :--- | :--- |
| Dual tracking | The account requires relevant world facts to be represented and relevant human moral reasons to be tracked and implemented. The first condition calls for demonstrable, verifiable responsiveness. Reducing it to generic human reasons omits both its moral qualifier and the epistemic part. |
| Whose reasons | The source leaves the relevant human agents context-dependent. Reasons may belong to designers, programmers, legislators, policy-makers or other humans along the chain, without matching the operator's or deployer's reasons in every circumstance. |
| Control and moral goodness | The authors allow meaningful human control alongside bad purposes. They describe it as necessary but insufficient for moral or societal goodness, while retaining normative disagreement over whose reasons and which values matter. This claim about goodness is separate from whether tracking and tracing are necessary or sufficient for meaningful control itself. |
| Tracing scope | Preserve actions and states, one or more relevant humans, and the design-history or use-context span. Do not restrict the responsible human to the immediate operator. |
| Two understanding qualifications | Both subconditions permit understanding or being in a position to understand: system capabilities/possible effects, and legitimate moral reactions toward the person because of those effects and their role. Actual understanding alone is stronger wording. A documentary record of opportunity to understand does not demonstrate actual comprehension. |
| Understanding and endorsement | The closing paragraph concerns tracing system actions/states to relevant human understanding and endorsement. It supplies a philosophical condition, not a newly measured effect or validation of TAE's documentary method. |

The author recommends describing the contribution as two proposed necessary conditions. Record that source positioning without using the distinct moral-goodness qualification as a logical reason that the authors could not define meaningful control. No whole-paper judgment of philosophical completeness follows from these blocks.

### Earlier quantifier concern resolved within this review

The author withdraws the earlier concern that TAE's each-system-action wording is stronger merely because the source mentions at least one human. He distinguishes the scope of actions/states from the number of relevant humans. His remaining corrections concern the design/use span and the capacity-to-understand qualification.

This records his revised interpretation, not a formal proof that every paraphrase or quantifier arrangement is equivalent. It does not require one fixed person to be responsible for all actions or change any historical case coding.

### Author's proposed replacement

Preserved verbatim:

> Santoni de Sio and van den Hoven (2018) propose two necessary conditions for meaningful human control. Tracking requires a decision-making system to be demonstrably and verifiably responsive to the human moral reasons relevant in the circumstances, while also tracking the morally relevant facts of its environment; those reasons may belong to humans anywhere along the chain, from designers and policy-makers to operators. Tracing requires the system’s actions and states to be traceable to at least one human in its design history or use context who understands, or is in a position to understand, its capabilities and possible effects, and that others may have legitimate moral reactions toward them because of those effects and their role.

The author supplies this as suggested wording. It is recorded as a proposal, not approval of an exact manuscript revision. His prior reading of the target paragraph is retained; it need not be repeated to record this comparison.

### Human-presence sentence: bounded follow-up

The author did not establish TAE's fourth sentence about human presence from the three assigned blocks and points to the earlier Toward a Theory of Meaningful Human Control section. Codex inspected that section and located the passage beginning with the account's three ideas: mere presence or loop participation is insufficient; causal intervention may miss relevant links or lack information/options; and even substantive causal contribution can be insufficient given psychological or capability-understanding limits.

This is Codex's additional source inspection. Personal reading of that passage is not yet reported. The source directly addresses insufficiency of presence for meaningful control; whether to retain TAE's stronger phrasing about establishing neither particular relationship or recast it as TAE's inference remains a wording decision. No fourth sentence is silently added to the proposed replacement.

### Dates and provenance

The author reports a displayed February 28, 2018 date and machine metadata he interpreted as online publication on February 1, 2018. Codex separately checked the current official page's publication history: Received October 24, 2017; Accepted February 1, 2018; Published February 28, 2018. The exact machine-readable field behind the author's report was not identified, so no explanation of its labeling is invented. February 1 is explicitly labeled acceptance in the inspected history, not publication.

The manuscript's year/volume/article citation remains 2018, volume 5, article 15. No day-level citation change is required or made here. The source dates and this November 3, 2026 review date remain distinct.

Disposition: the three assigned source blocks and their comparison with the previously read TAE paragraph are reported complete. The author's corrected replacement is retained as a proposal; the human-presence sentence has a separately identified, not-yet-personally-read passage. This establishes no full-paper or cited-originals review, empirical verification, accepted manuscript revision or new scientific finding. Historical attestations, screening/proposition permissions, case packets, scores, Jev adjudications, the closed phase, website and manuscripts are unchanged.

## TAE-SR-02 supplementary human-presence review: November 3, 2026

Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance.

### Reported scope

The author reports reading the framing and the first and second ideas in Toward a Theory of Meaningful Human Control, beginning with the passage introducing three ideas and stopping before Thirdly. He does not restate his access route for this supplementary reading. The earlier report's direct Frontiers HTML route remains attached to that earlier reading; no fresh direct retrieval is inferred here.

### Corrections to the proposed summary

| Point | Retained account and boundary |
| :--- | :--- |
| First idea | Mere presence or loop participation is categorically insufficient for control of the described (military) activity. A person may causally influence some parts while lacking influence over other morally relevant parts, or sufficient information and options. |
| Second idea | Even a substantive causal contribution through intentional action may fall short of meaningful control. The authors give examples involving psychological capacity and appreciation of the system's real capabilities. Preserve the conditional wording; this is not a universal claim that intentional contribution is always insufficient. |
| Scope | The account begins with military activity and proposes a philosophical requirement. These passages do not establish a tested result across domains, a frequency of failure or the practical effectiveness of any arrangement. |
| Tracking/tracing attribution | TAE's wording about establishing neither relationship connects this earlier discussion to the conditions introduced later. The author treats that connection as TAE's inference, not a direct statement made in this passage about those two named relationships. |

Codex's earlier candidate flattened the second idea's modal qualification and collapsed substantive intentional contribution into generic causal influence. The author's corrections are retained rather than carrying forward that candidate unchanged.

Author's closer summary, preserved verbatim:

> Their account holds that human presence, or being in the loop, is insufficient for control, and that even a substantive causal contribution through intentional action may fall short of meaningful control, for example without the capacity to respond appropriately or to appreciate the system’s real capabilities.

This is recorded as proposed wording, alongside the earlier three-sentence Tracking/Tracing replacement. Neither has been approved as an exact revised manuscript paragraph in this reply. The source supports the conceptual insufficiency claim with examples, including a button-pushing illustration quoted from Horowitz and Scharre. The cited original was not personally reviewed in this step. No empirical claim about institutional performance is adopted from these examples.

Disposition: TAE-SR-02's assigned blocks and supplementary passage are now reported read within the stated scopes. The target TAE paragraph was compared using the previously reported pinned-file reading. The remaining task for these wordings is a bounded later-draft disposition, not another attestation of reading the same passages. All prior source and context receipts, publication/date qualifications, historical attestations, case packets, screening/proposition permissions, scores, original Jev adjudications and the closed research phase remain intact. The manuscript and website are unchanged.

## TAE-SR-03: Bainbridge, selected Ironies of Automation passages

Recorded November 3, 2026. Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance.

### Source, reading scope and access

Source: Lisanne Bainbridge, [Ironies of Automation](https://tc.ifac-control.org/4/1/newsletter/ironies-of-automation/@@download/file/Bainbridge1983_Automatica_Ironies%20of%20automation.pdf), Automatica 19(6), 775–779 (1983), DOI `10.1016/0005-1098(83)90046-8`. The [IFAC technical-committee page](https://tc.ifac-control.org/4/1/newsletter/ironies-of-automation/view) hosts the journal-formatted five-page PDF. Codex checked the host, paper header and selected text. This is distinct from personal source reading.

The author reports reading the abstract and opening scope paragraph on printed page 775; additionally, section 1's opening; sections 1.1–1.1.2, including both long-term knowledge and working storage and the continuation onto page 776; section 2.3's final paragraph; and section 3's opening through its discussion of supporting skills and motivation on page 777.

He reports using the IFAC-hosted journal text with a PDF-extraction caveat: page 777's two columns interleave in the extracted order, so he located the relevant material by headings and opening words. No fresh download, file hash or visual inspection of the complete PDF is attested. Retrieving a complete journal-formatted file is not personal reading of the whole article.

He excludes section 1.1.3 through section 2.3's body, except its assigned final paragraph; sections 3.1–4; and the references. The two TAE claims at [line 117](../paper/revisions/2026-11-01/main.tex#L117) and [line 201](../paper/revisions/2026-11-01/main.tex#L201) are assessed in his reply. A fresh manuscript access route is not stated for this comparison.

### Reported findings and corrections

| Passage or issue | Retained account and boundary |
| :--- | :--- |
| Scope and classic approach | The abstract and scope concern process-industry control with flight-deck examples, including operators left responsible for abnormal conditions. This is not a demonstrated result about modern AI. Applying the mechanism to AI-assisted decisions is TAE's analogy. |
| Task allocation | Designers can leave operators the tasks they could not automate, with inadequate support. Removing easier work can make the remaining difficult work harder. Describe work left unautomated rather than claiming that automation necessarily transfers a new set of tasks to the operator. |
| Manual skills | The selected discussion describes physical-skill deterioration through nonuse and possible difficulty with takeover during abnormal conditions. It does not provide a new ranking of which operators are least prepared. |
| Long-term knowledge | Retrieval depends on use, and useful process knowledge develops through practice and feedback. Bainbridge frames reliance on former manual operators' acquired skills as a concern, including the preparation of later generations. |
| Working storage | Building knowledge of the current process state takes time; an urgent takeover can begin with limited information. Keep this distinct from a fresh measurement of modern-AI situation awareness. |
| Rare intervention and training | Frequent alarms can give normal-work practice. Bainbridge suggests that highly successful automated systems with rare manual intervention may need the greatest training investment. Preserve this countercondition and tentative wording. |
| Human-computer integration | The section 3 opening argues that task allocation alone is insufficient without considering integration, skill and motivation. It is a proposed account of the human-system problem, not a measured causal effect established by TAE. |

### Argument, cited evidence and strength of claims

The author reports no new measurements in the passages he read. He identifies cited studies, including Edwards and Lees (1974), Bainbridge's earlier work (1975, 1981), and the quoted Bibby and colleagues (1975) account. The original cited studies were not personally reviewed in this step. Their presence does not convert this reading into empirical replication.

He notes assertions about nonuse, knowledge retrieval and the concern about inherited operator skills, as well as modal language including may, one can argue and perhaps. Preserve the strength of each claim in its location; do not describe every sentence as tentative or every asserted mechanism as newly measured.

At line 117, the author recommends argued or described rather than attributing a fully demonstrated mechanism to Bainbridge, and adding the process-control domain. At line 201, he recommends argued instead of shows, replacing transfers with the tasks-left-unautomated account, and retaining the practice/training condition. The paragraph's nominal-oversight/practical-force conclusion is TAE's synthesis alongside other authors, not Bainbridge's terminology or demonstrated modern-AI finding.

### Author's proposed wording

For line 117, preserved verbatim:

> Bainbridge (1983) argued that, in process-control automation, operators left responsible for abnormal conditions may be least prepared for them, because manual skills and process knowledge decline without regular use.

For line 201, preserved verbatim:

> Drawing on process-industry and flight-deck examples and earlier studies, Bainbridge (1983) argued that automation leaves operators the difficult tasks designers could not automate, while routine automatic operation erodes the skills those tasks require; the most reliable systems, with rare need for intervention, may therefore need the greatest investment in operator training.

These remain author proposals. Least prepared implies a comparative ranking not established in the selected passages. Routine automatic operation erodes skills is stronger than the practice-dependent account, especially given the explicitly read frequent-alarms countercondition. The paper's most successful systems phrasing should not be converted into a measured reliability result.

Codex-prepared conditional options for later review, not approved manuscript text:

- Line 117: Bainbridge (1983) argued that process-control automation can leave operators responsible for abnormal conditions while reducing the practice needed to maintain their manual skills and process knowledge.
- Line 201: In her process-industry and flight-deck discussion, Bainbridge (1983) argued that automation can leave difficult tasks with operators while reducing opportunities to practice the skills needed for them. She suggested that successful automated systems with rare manual intervention may need the greatest investment in operator training.

### Additional citation contexts and historical provenance

The author located, but did not evaluate, the other Bainbridge citations at [line 128](../paper/revisions/2026-11-01/main.tex#L128) and [line 1189](../paper/revisions/2026-11-01/main.tex#L1189). Their claims remain a separate context check. Bainbridge's selected passages do not establish the contributions attributed to the neighboring, unreviewed Endsley, Laux, Ezell or Burr–Leslie sources.

The author flags [line 1640](../paper/revisions/2026-11-01/main.tex#L1640), which records earlier inspection through author-republished or university-hosted passages with incomplete direct-download access. Preserve that as the earlier review's provenance. Today's IFAC access can be recorded as a dated supplement; it does not retroactively alter that access history or establish personal reading of the complete article.

Disposition: the stated Bainbridge source passages and comparison with the two assigned TAE claims are reported complete. The other citation contexts and a dated provenance clarification remain to be reviewed. Author proposals and conditional options are retained for later consideration, without exact-draft approval. Historical attestations, source packets, screening/proposition permissions, scores, Jev adjudications, the closed phase, manuscripts and website remain unchanged.

## TAE-SR-03 remaining citation contexts and provenance: November 3, 2026

Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance.

### Reported reading and access

The author reports reading all three requested paragraphs, at manuscript lines 128, 1189 and 1640, from the same raw `main.tex` copy at commit `2f462dcb147613c6634aab143102da81fcdbff93` used for the preceding checks. He did not retry the automated-access-refusing GitHub blob pages. He also read the preceding paragraph about established concepts to identify what those relationships refers to; content locators are retained where line-number representations differ.

He supplies the local hash prefix `6a3dceac…` and explicitly says he has not compared it with a repository-side record. The algorithm and full hash are not given. Record this as his local identifier, not verified byte identity with the committed file or a new authenticated preservation claim.

### Attribution and construct distinctions

| Manuscript location | Author's reading and retained boundary |
| :--- | :--- |
| Line 128: skill | Bainbridge's selected section 1.1.1 supports the disuse/practice argument about manual skill. Attribute this as an argued mechanism in the inspected process-control context. |
| Line 128: information and time | Section 1.1.2 discusses limited information at urgent takeover and the time needed to build current-process-state knowledge. Time to build that knowledge and time available to intervene are distinct; do not silently substitute one for the other. |
| Line 128: neighboring claims | The human moral reasons correction from TAE-SR-02 remains relevant to the Santoni de Sio and van den Hoven account. Laux's institutional claims are unreviewed here. The clustered sources motivate the six conditions; this reading does not validate those conditions. A more specific human-factors proposition should carry its own source attribution. |
| Line 1189: loss of practice | Manual skill and process knowledge through nonuse are within the inspected Bainbridge scope. The author proposes separating the attributions by item. |
| Line 1189: situation awareness | The named situation-awareness construct is attributed to Endsley and remains unreviewed here. Bainbridge's working-storage account concerns time to build current-state knowledge; similarity does not make the constructs interchangeable. |
| Line 1189: challenge opportunity | The checked Bainbridge passages do not support the output-challenge-opportunity item. Section 1.1.3 was visible in extracted text but was not checked. The clause needs a verified source or a later wording disposition; neither Endsley nor another source is confirmed by this reply. |
| Line 1189: TAE synthesis | Assigned role and AI-output framing are TAE's analogy. The neighboring Ezell and Burr–Leslie sentence is outside this check, as are the substantive claims of other authors in the preceding paragraph. |

The author's correction from explains why to argues or describes is retained for Bainbridge's contribution. This check does not determine the evidentiary strength of all human-factors research cited elsewhere.

### Proposed attribution split

Author's suggested restructuring, preserved verbatim:

> An operator may lose manual skill and process knowledge through disuse (Bainbridge, 1983), lack situation awareness (Endsley, 2017), or have too little opportunity to challenge an output [source to be confirmed].

This is a proposal with an explicit unresolved source placeholder, not an approved manuscript substitution. The parenthetical Endsley attribution is not verified by this Bainbridge review.

### Historical provenance and the new selected reading

The author asks that the older line-1640 access record remain unchanged. He cannot personally verify its earlier routes, and the IFAC check does not replace them. The source host identifies where a copy is available; it does not by itself establish republication, endorsement or independent verification. The inspected PDF carries the IFAC copyright and Pergamon imprint.

Author's proposed dated supplement, preserved verbatim:

> A later selected check (November 2026) read Bainbridge’s abstract and opening scope paragraph, section 1’s opening and sections 1.1–1.1.2, the final paragraph of section 2.3, and the opening of section 3, in a journal-formatted copy hosted by IFAC Technical Committee 4.1. PDF text extraction interleaved the two columns on page 777. Sections 1.1.3, 1.2, the remainder of 2, and 3.1–4 were outside that check. Lee and See’s access record is unchanged.

Here, the remainder of section 2 excludes the specifically read final paragraph of section 2.3; the earlier receipt retains the precise selection. The actual reports in this record are dated November 3, 2026. A month-level supplement can be considered in a later draft without changing the archived provenance.

The author regards the Bainbridge components at lines 117, 128 and 201, and the practice component at 1189, as supported by the read passages. Retain the prior scope and wording qualifications: that judgment does not endorse every neighboring claim, the comparative least-prepared phrase, inevitable skill erosion, or a demonstrated modern-AI effect. The challenge-opportunity component remains unresolved. Lee and See's source and access record are unchanged.

Disposition: TAE-SR-03's selected source reading and all four identified citation-context checks are reported complete within the stated limits. Its proposed wording and provenance supplement remain for later consideration, without exact-manuscript approval. The adjacent unreviewed sources and unresolved clause stay visible. All earlier receipts, historical attestations, source packets, screening/proposition permissions, scores, Jev adjudications, the closed phase, manuscripts and website remain unchanged.

## TAE-SR-04: Endsley, abstract-only review through a library catalog

Recorded November 3, 2026. Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance.

### Source identity, access and dates

Source: Mica R. Endsley, [From Here to Autonomy: Lessons Learned From Human–Automation Research](https://journals.sagepub.com/doi/10.1177/0018720816681350), DOI `10.1177/0018720816681350`.

The author reports that SAGE blocked automated access. He did not read the publisher's abstract display or publication details. He read the complete abstract through a Bavarian library-union discovery record sourced from ProQuest. He reports that record's citation as Human Factors, February 2017, 59(1), 5–27, ISSNs 0018-7208 and 1547-8181, with the DOI above. No exact catalog URL or record identifier was provided, so the particular record and its bytes are not independently matched here.

He reports a SAGE issue-contents search snippet giving first publication on December 15, 2016; this was snippet-level only for him. Codex separately opened the current official publisher page and confirmed its first-published-online label of December 15, 2016 and volume 59, issue 1. This is Codex's publisher-page check, not the author's reading of that page. The online-first date, the reported February 2017 issue and the November 3, 2026 review remain distinct.

The body is restricted in the available publisher retrieval. No personal reading of the body or references is attested, and no support is inferred from them. Press releases and secondary summaries were not used. Codex's canonical abstract retrieval confirms the broad content discussed below; it does not establish the identity of the unlinked catalog copy or authenticate the author's access.

### Abstract-level account and limits

The author reports the abstract's discussion of challenges in human oversight and interaction with autonomous and semiautonomous systems, including automotive, aviation, cyber and robotics applications. Its automation-conundrum account links increasing autonomy, reliability and robustness with lower operator situation awareness and less likelihood of manual takeover when needed.

The abstract describes a human–autonomy systems oversight model integrating earlier research on situation awareness, out-of-the-loop performance problems, monitoring and trust. It also names interface features, levels of automation, adaptive automation and granularity of control among the design approaches, with recommendations and future research.

The author finds no new measurements reported in the abstract. This does not establish that the unread article body contains no empirical material. Treat these statements as the abstract's model/research-synthesis account, not independently reproduced causal effects, a universal rule for every automated system or validation of TAE.

### Comparison with the TAE claims

| Manuscript location | Supported account within this reading | Unverified or qualified part |
| :--- | :--- | :--- |
| Line 117 | The abstract connects lower situation awareness with less likelihood of taking over manual control. | The perception–understanding–projection definition and operating-conditions formulation are absent from the abstract and remain unverified for this citation. A definition from another work cannot be silently substituted. |
| Line 201 | Situation awareness, monitoring, trust and out-of-the-loop performance problems appear in the model's stated scope. | Workload is not mentioned. Autonomous-system performance shifts the subject from the human operator's oversight and interaction. Preserve the performance-problems wording without inferring a measured degradation rate. |
| Line 1189 | Lower situation awareness is within the abstract's account; loss of practice retains the separately reviewed Bainbridge basis. | Lack can suggest absence rather than lower awareness. Taking over manual control is not the same act as challenging an output. Challenge opportunity is unverified by the selected Bainbridge passages and this abstract, without claiming either full paper cannot support it. |

### Author's proposed wording

For line 117, preserved verbatim:

> As autonomy, reliability and robustness increase, operators’ situation awareness may fall and takeover of manual control may become less likely (Endsley, 2017).

For line 201, preserved verbatim:

> Endsley integrates research on operator situation awareness, out-of-the-loop performance problems, monitoring and trust into a model of human oversight of autonomous systems (Endsley, 2017).

For line 1189, preserved verbatim:

> An operator may lose manual skill and process knowledge through disuse (Bainbridge, 1983), have lower situation awareness as automation becomes more autonomous and reliable (Endsley, 2017), or have too little opportunity to challenge an output [source to be confirmed].

These are recorded as author proposals, not accepted manuscript replacements. The first and third sentences must retain attribution to Endsley's abstract/model account rather than presenting a newly measured causal effect. The source placeholder remains unresolved. A separately checked source or later removal/reformulation is needed before claiming support for the detailed definition, workload or challenge-opportunity wording.

### Transfer and source separation

The abstract's applications do not specifically establish a result about AI-mediated institutional decisions. That application is TAE's analogy. The author notes a conceptual parallel with Bainbridge's account of rare intervention and operator investment; preserve their different constructs and evidentiary scopes. Neither the parallel nor these readings demonstrate that high reliability necessarily causes weak human control.

Disposition: the assigned abstract reading is reported complete through the stated alternative route. Publisher-display and publication-detail reading remain unattested, while the separate Codex date check is identified. Body-level claims, source identity limits and unresolved wording stay explicit; no additional full-text reading is required to close this abstract-only item. All earlier receipts, historical attestations, source packets, screening/proposition permissions, scores, Jev adjudications, the closed phase, manuscripts and website remain unchanged.

## TAE-SR-05: Burr and Leslie, selected arXiv v1 sections

Recorded November 3, 2026. Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation, including a separate clarification of unread material. Recorded with Codex assistance.

### Version, access and personal reading scope

Source: Christopher Burr and David Leslie, [Ethical Assurance: A practical approach to the responsible design, development, and deployment of data-driven technologies, arXiv v1](https://arxiv.org/pdf/2110.05164v1), identifier `2110.05164v1`. The author identifies the PDF's displayed date as October 12, 2021. Codex separately confirmed that header and the [arXiv submission history](https://arxiv.org/abs/2110.05164), which gives October 11, 2021 for v1. Those source dates and this review date have different meanings.

The author reports reading sections 1.2, 2.3.1, 4.3.3 and 4.3.4 in extracted preprint text. He located passages by section headings because the extraction had no page markers. The exact retrieval route, copy identifier and byte identity were not newly supplied. All printed page numbers remain personally unconfirmed; the page numbers in the assignment are locators supplied by Codex, not evidence of the author's page inspection.

The author expressly confirms that section 5.3.1 in full remains unread. It is a pending part of the original assignment. No review of its efficacy discussion is inferred from his general assessment of the passages he did read. Figures were outside scope; he saw captions only. The cited originals, including Toulmin and Cartwright and Hardie, were not read for this check. Neighboring section 4.3.2 and the section 5 introduction were seen in passing and were not relied on.

TAE cites the journal version, DOI `10.1007/s43681-022-00178-0` (2023). Its body has not been compared here. The 2021 preprint reading supports only the passages of that version inspected; it does not establish that the journal body is identical or that the existing journal citation supports every proposed sentence. Final citation/version treatment remains unresolved.

### Reported account and scope qualifications

| Section locator | Author's reading and retained boundary |
| :--- | :--- |
| 1.2 | Argument-based assurance communicates to another party that a claim about a system property is warranted by the available evidence. The authors generalize the approach to wider normative goals, including sustainability, accountability, fairness and explainability, and connect participation with legitimacy, social license and countering ethics washing. Their safety-critical-industry adoption statement does not demonstrate ethical-assurance effectiveness. |
| 2.3.1 | The Goal Structuring Notation account names goals, solutions, strategies, contexts, assumptions and justifications, with a claims-to-evidence process. Clarity, accessibility, understanding and inquiry are part of the account. Preserve which details concern this notation rather than treating its elements as mandatory for every assurance method. |
| 4.3.3 | Some claims require documented evidential artifacts. Self-evident or well-established claims may need no further artifact; a trusting reviewer may also accept a propositional claim without documented evidence. One artifact can support multiple claims. These are the preprint's allowances, not TAE's automatic rule for accepting unsupported claims. |
| 4.3.4 | A warrant connects evidence to a claim and makes assumptions explicit. In the fairness-process example, support depends on whether the process is reliable or appropriate. A qualifier may be needed. Constructing an argument late raises post hoc concerns and can also expose assumptions that need further work. The discussion does not establish that every inference always requires a separately documented artifact. |

The author characterizes the inspected passages as a proposed methodology illustrated through a hypothetical healthcare decision-support project. He reports no applied evaluation or measured outcome in those passages. Keep that finding at the inspected level: section 5.3.1 remains unread, and this is not a whole-paper determination about efficacy or a validation of TAE's retrospective procedure. References to earlier work do not constitute personal reading or reproduction of that work.

### Comparison with the pinned TAE manuscript

The comparison target remains `paper/revisions/2026-11-01/main.tex` at commit `2f462dcb147613c6634aab143102da81fcdbff93`. The reply evaluates the quoted passages at lines 131, 253 and 1189. It does not newly identify a manuscript retrieval route or attest reading the complete manuscript.

| TAE location | Correction or qualification proposed by the author |
| :--- | :--- |
| Line 131 | The warrant account supports explaining why evidence supports a claim and making assumptions explicit. Reconstruction from incident records is TAE's retrospective adaptation of a prospective development/deployment account. The dependencies wording has partial support through shared artifacts and jointly supporting claims; inspectability has broad support through inquiry and participation. The Pittaras and McGregor contribution is unreviewed here. |
| Line 253 | Retain the communicative purpose and the available-evidence qualification. Uncertainty has limited support in the inspected warrant/qualifier discussion. The extension includes participatory process and deliberation, not only an argument structure. The neighboring AMLAS and audit sources are outside this check. |
| Line 1189 | Require is stronger than the bounded account inspected. The preprint proposes making warrants explicit, with its final step needed in many cases and exceptions to documented artifacts. Preserve the distinction between an explicit inferential link and a documentary artifact for every claim. The Ezell contribution remains unreviewed here. |

### Author's proposed wording

For line 253, preserved verbatim:

> Argument-based assurance uses structured argument to show another party that a claim about a system is warranted by the available evidence, with assumptions made explicit. In a 2021 preprint, Burr and Leslie generalise it to ethical goals such as fairness, explainability and accountability, adding participatory deliberation as a condition of legitimacy (Burr & Leslie, 2023 [journal version; preprint passages checked]).

For line 1189's second sentence, preserved verbatim:

> Incident analysis identifies records useful for reconstructing such conditions (Ezell et al., 2025), and argument-based assurance proposes making the warrant from evidence to claim explicit, while allowing that some well-established claims need no documented artefact (Burr & Leslie, 2023).

These are suggestions for later consideration, without approval of an exact manuscript or a completed citation decision. The author explicitly identifies the citation format as a placeholder. The first candidate's assumptions wording should remain within the reviewed warrant discussion; the second does not verify Ezell or exhaust all artifact exceptions described above. No candidate has been inserted into a manuscript.

### Historical provenance preserved

The existing line-1640 note says that the full author preprint was examined and that the final article was available only at preview level in the earlier review. That note predates this check and does not identify a preprint version. At the author's instruction it remains as written. This dated receipt separately names v1 and the four sections personally reported read, with section 5.3.1, page-number confirmation and the journal body explicitly unread. It neither replaces the older access history nor converts that older full-preprint statement into a new personal whole-paper attestation.

Disposition: four section readings are reported complete within the stated extraction and version limits; TAE-SR-05 remains partial because the assigned section 5.3.1 reading is pending. Wording and citation decisions remain proposals. All earlier receipts, historical attestations, source packets, screening/proposition permissions, scores, Jev adjudications, the closed phase, manuscripts and website remain unchanged.

## TAE-SR-05 efficacy passage and selected-reading completion: November 3, 2026

Reviewer and decision authority: Mark Julius Banasihan, reporting directly in the current source-review conversation. Recorded with Codex assistance. This receipt supplements the earlier partial entry; its reading status was accurate when recorded and remains preserved as history.

### Reported route and completed selection

The author reports reading all of section 5.3.1, Evaluating Efficacy of Ethical Assurance, and stopping at the section 5.3.2 heading. He identifies his route as an uploaded PDF named `2110_05164v1.pdf` supplied directly in his context. He reports matching its title-page date of October 12, 2021 and arXiv v1 stamp of October 11, 2021 to the requested version. He also reports that its opening matched earlier snippet fragments and that he now relies on the section text for this account.

Record this as the author's reported copy and route. Codex has not inspected or matched that uploaded file, and no hash or authenticated byte identity has been established. Codex separately inspected section 5.3.1 in the publicly available [arXiv v1 PDF](https://arxiv.org/pdf/2110.05164v1); that check does not authenticate the uploaded copy or the author's access.

Together with the earlier receipt, the author now reports reading all five assigned text sections: 1.2, 2.3.1, 4.3.3, 4.3.4 and 5.3.1. Section 5.3.2 and the cited originals remain outside the assignment. Section-page confirmation remains unreported, beyond his title-page identification. The journal-version body is still unread and has not been compared with v1. No complete-preprint personal reading is asserted.

### Efficacy account, attributions and limits

| Content locator in section 5.3.1 | Author's correction and retained boundary |
| :--- | :--- |
| Opening inconclusive-benefits account | The authors discuss whether argument-based assurance and safety cases deliver the benefits attributed to them. Their extension of measurement difficulties to ethical assurance is an analogy. This is not a measured finding about ethical assurance's effectiveness. |
| Named failure | The section refers generally to failures but develops one named illustration: the 2006 loss of RAF Nimrod XV230. Its quotations and account of the safety case come through Burr and Leslie's presentation of the Haddon-Cave review. That review has not been personally checked in this assignment. |
| Organizational conditions | Burr and Leslie interpret part of the Nimrod failure through organizational culture and argue that the case does not justify abandoning argument-based assurance. They also cite conditional optimism about digital-health safety cases from Sujan and Habli. These are their interpretations and attributed claims, not an independently established causal finding from this review. |
| Two measurement obstacles | The authors attribute to Sujan and Habli the difficulty of obtaining causal-impact evidence for rare, severe events and the difficulty of isolating relevant factors when safety-case practices vary across domains. The original Sujan and Habli work remains unread here. |
| Extension to ethical assurance | Burr and Leslie expect related difficulties to apply to ethical assurance. They cite Ananny and Crawford on limited empirical confirmation of a transparency-to-trust relationship; that original also remains unread. Preserve the distinction between their analogical reasoning and their cited findings. |
| Closing research step | They call for research into substantive and structural factors contributing to success or failure. The inspected section specifies no study design, outcome measure or evaluation method for that research. |

The author reports no new measurements in section 5.3.1 and finds no evaluation of ethical assurance or validation of TAE in that section. His broader phrase about efficacy evidence in the preprint is retained only at the inspected-section level: the selected reading does not establish a whole-preprint absence of empirical material. Organizational culture is a proposed explanatory condition in this discussion; this review neither measures it nor establishes its causal effect.

### Internal cross-reference and TAE interpretation

The author flags that section 5.3.1 refers to benefits in section 2.3, while the benefits heading is in section 2.2 and section 2.3 concerns building a case. Codex separately confirmed those headings in v1. This identifies an internal-reference mismatch to consider if the passage is used later. It does not attest the author's full reading of section 2.2, authorize correction of the source, or establish the corresponding journal text.

The author connects the measurement problem for rare consequential events with TAE's retrospective case-based procedure and treats the Nimrod discussion as a warning about documentary assurance losing practical force. Record these as his interpretations. The analogy does not measure TAE's causal impact or demonstrate that its procedure addresses the failure described. The selected passage does not establish that a particular assurance document was complete and signed or that its producers had stopped reasoning; those additional details would need their own source support before use as case facts.

### Author's proposed review-record wording

Preserved verbatim as a proposal:

> In the 2021 preprint (§5.3.1), Burr and Leslie report that evidence on whether assurance cases deliver their stated benefits remains inconclusive. Drawing on the Nimrod review and Sujan and Habli (2021), they attribute part of one safety-case failure to organisational culture, give two reasons safety-case efficacy is hard to measure, expect similar difficulties for ethical assurance, and call for research on which substantive and structural factors shape its success or failure.

The proposed paragraph should be read with the attribution split above: the Nimrod review supplies the failure account as presented by Burr and Leslie, while Sujan and Habli supply the two measurement obstacles as attributed by them. The underlying originals remain unchecked. This paragraph and the two earlier manuscript candidates remain proposals; no final wording, citation/version treatment or manuscript substitution is approved by this reply.

Disposition: TAE-SR-05's five assigned section readings are reported complete within the stated access and version limits. Page-location uncertainty, unread originals, the unread journal body, version treatment and bounded wording proposals remain explicit. The historical line-1640 note and earlier partial receipt remain as written. Historical attestations, source packets, screening/proposition permissions, scores, Jev adjudications, the closed phase, manuscripts and website remain unchanged.
