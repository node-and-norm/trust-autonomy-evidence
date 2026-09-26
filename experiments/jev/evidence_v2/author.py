"""Approved pre-live successor edits; new stipulations are authored, not recovered facts."""
import copy
from pathlib import Path
from experiments.jev.run import ROOT,encode,sha,load
from experiments.jev.evidence_v1.run import materials

HERE=Path(__file__).resolve().parent
REPLACEMENTS={
'The action occurred at 10:00. The reviewer received every item in the decision packet at 09:50.':('T01','The scenario’s stipulated evidence inventory contains every item needed for this decision. The reviewer received every inventory item at 09:50; execution occurred at 10:00.'),
'At 09:50 the reviewer received the entire decision packet. Execution followed at 10:00.':('T01','Every item needed for the decision is included in the scenario’s stipulated evidence inventory. All inventory items reached the reviewer at 09:50. Execution followed at 10:00.'),
'An independent custodian compared the manifest with the source inventory and accounted for every listed item.':('T09','An independent custodian checked the source inventory against the scenario’s complete source register, found no omitted sources, and verified that every registered item was retained in the packet.'),
'The manifest lists the source items and identifies two items absent from the packet.':('T10','The manifest identifies source items, including two not retained in the packet. No independent check establishes whether the manifest lists every source.'),
'The evaluation report gives counts of successes and failures separately for every declared operating condition.':('T12/T13','The report gives success and failure counts for every declared operating condition; each meets its predeclared acceptance threshold.'),
'The recorded success counts fall below the reliability claim under its stated operating conditions.':('T13','The report gives success and failure counts for every declared operating condition; at least one falls below its predeclared acceptance threshold.')}


def revised(text):
    prefix='The supplied extract states the following: '
    frame=prefix if text.startswith(prefix) else ''
    original=text[len(frame):]
    if original in REPLACEMENTS:
        issue,new=REPLACEMENTS[original];return frame+new,issue
    if 'object the proposed action' in original:
        return frame+original.replace('object the proposed action','object to the proposed action'),'T03'
    if 'The reviewer recorded an objection and the executor continued.' in original:
        if 'reviewer recommend the proposed action' in original:
            return frame+original.replace('The reviewer recorded an objection','The reviewer recommended cancellation'),'T04'
        if 'reviewer review the proposed action' in original:
            return frame+original.replace('The reviewer recorded an objection','The reviewer inspected the proposed action, recorded a review note requesting cancellation,' ).replace('cancellation, and','cancellation, and'),'T04'
    return text,None


def decision(topic,text,previous):
    # Reassess every determination for the five changed question/evidence constructs.
    t=text.removeprefix('The supplied extract states the following: ')
    if topic not in {'control__access','control__comprehension','control__exercise','trust__evidence_completeness','trust__reliability'}:
        return previous,'Unchanged proposition and evidence, or role-specific advisory clarification preserving the explicit nonbinding boundary; inherited experimental reference, not independent validation.'
    if 'explicitly excludes' in t:return 'outside_scope','Explicit charter exclusion.'
    if t in ('The supplied packet contains no record for this topic.','No record about this topic appears in the supplied packet.'):
        return 'indeterminate','No topic evidence supplied.'
    rules={
      'control__access': [('stipulated evidence inventory','supported'),('source appendix','partially_supported'),('first received','unsupported'),('Execution preceded','unsupported')],
      'control__comprehension':[('independently checked alternative','supported'),('explanatory materials','partially_supported'),('solely because','unsupported')],
      'control__exercise':[('unattended rule','unsupported'),('checked review box','partially_supported'),('edited the proposed','supported'),('comparing two alternatives','supported')],
      'trust__evidence_completeness':[('found no omitted sources','supported'),('No independent check','partially_supported'),('found omitted source records','unsupported')],
      'trust__reliability':[('each meets its predeclared','supported'),('at least one falls below','unsupported'),('one overall success rate','partially_supported')]}
    matches=[(token,state) for token,state in rules[topic] if token in t]
    if len(matches)!=1:raise ValueError('Successor determination needs explicit decision: '+topic+' '+t)
    token,state=matches[0]
    return state,'Successor operationalization applied to explicit excerpt evidence: '+token+'. This is an authored benchmark reference, not a sealed-oracle amendment.'


def build():
    oldcards,oldgold,oldquestions,pairs,policy=materials()
    cards=copy.deepcopy(oldcards); questions=copy.deepcopy(oldquestions);policy=copy.deepcopy(policy)
    additions={
      'control__access':' When some required evidence is available before action and other required evidence arrives afterward, classify partially_supported. When no required decision evidence arrives before action, classify unsupported. Partial evidence does not satisfy the complete-access requirement.',
      'control__comprehension':' Recorded delivery of explanatory materials without a recorded independent comparison or challenge is partially_supported as a documented precursor only; it does not demonstrate comprehension. No topic evidence is indeterminate.',
      'control__exercise':' A recorded review attestation without reasoning or an edit is partially_supported as an attestation only. A record explicitly showing unattended approval without human action is unsupported.',
      'trust__capability':' Repeated means at least two recorded task trials for this synthetic assessment. One successful trial is partial. Repetition does not establish generalization or statistical reliability.'}
    for topic,extra in additions.items():questions[topic]['question']['instructions']+=extra
    q=questions['trust__reliability']['question']
    q['instructions']=q['instructions'].replace('reliability evidence separated by operating condition','reliability meeting declared acceptance conditions, with success and failure counts separately reported for every declared operating condition')
    q['instructions']+=' Condition-separated counts meeting every declared threshold are supported; a documented threshold failure is unsupported. Aggregate-only performance evidence without a condition-specific breakdown is partially_supported.'
    changes=[]; gold={}; decisions=[]
    for card in cards:
        gold[card['id']]={}
        for doc in card['state']['documents']:
            old=doc['text'];doc['text'],issue=revised(old)
            if issue:changes.append({'packet':card['id'],'topic':doc['topic'],'issue':issue,'before':old,'after':doc['text'],'boundary':'Approved authored successor wording; added facts are synthetic stipulations.'})
            state,reason=decision(doc['topic'],doc['text'],oldgold[card['id']][doc['topic']])
            gold[card['id']][doc['topic']]=state
            decisions.append({'packet':card['id'],'topic':doc['topic'],'previous':oldgold[card['id']][doc['topic']],'successor':state,'rationale':reason})
    policy.update(version='jev-tae-evidence-v2',review_route='author_reviewed_ai_assisted_v1',live_enabled=False)
    return {'cards.json':cards,'gold.json':gold,'questions.json':questions,'pairs.json':pairs,'policy.json':policy,
       'changes.json':changes,'label-decisions.json':decisions,
       'provenance.json':{'source_freeze_sha256':sha((ROOT/'experiments/jev/evidence_v1/freeze.json').read_bytes()),'source_provenance_sha256':sha((ROOT/'experiments/jev/evidence_v1/provenance.json').read_bytes()),'changes':'changes.json','label_decisions':'label-decisions.json','assumptions':'New facts are authored synthetic stipulations; no historical documentary facts were recovered.'}}

if __name__=='__main__':
    for name,value in build().items():
        path=HERE/name;data=encode(value)
        if path.exists() and path.read_bytes()!=data:raise SystemExit('Refusing to overwrite different material: '+name)
        path.write_bytes(data)
