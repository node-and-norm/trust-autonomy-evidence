"""Local timed review forms. No responses are prefilled for the author."""
import json
from pathlib import Path

from .pilot import verify


def render(output, assistance=None):
    cohort=verify()
    data={'units':cohort['units'],'questions':cohort['questions'],'assistance':assistance,
          'source_run_sha256':cohort['source_run_sha256']}
    template='''<!doctype html><meta charset="utf-8"><title>Jev review pilot</title>
<style>body{font:17px system-ui;max-width:950px;margin:40px auto;padding:20px;color:#172c3b}pre{white-space:pre-wrap;background:#f2f5f7;padding:20px}button,select,input,textarea{font:inherit;margin:8px;padding:8px}textarea{width:90%;height:90px}fieldset{margin:15px 0}#hint{border-left:5px solid #946018;padding:14px}label{display:block}</style>
<h1 id="title"></h1><p>This is author review of AI assistance, not independent adjudication. No original scores or records are changed. Timers are editable browser records, not independently verified. Export before closing this tab.</p>
<label>Reviewer name <input id="reviewer"></label><label>Have you already seen item-level pilot suggestions? <select id="exposure"><option value="">Select</option><option>no</option><option>yes</option><option>uncertain</option></select></label>
<p id="progress"></p><section id="item" hidden><pre id="evidence"></pre><pre id="hint" hidden></pre>
<div id="questions"></div><label>Concern or explanation (including a bounded “none identified”)<textarea id="notes"></textarea></label>
<fieldset id="quality" hidden><legend>Assistance assessment</legend><label>Helpfulness <select id="help"><option value="">Select</option><option>helpful</option><option>neutral</option><option>misleading</option><option>uncertain</option></select></label><label>Did assistance miss an important concern? <select id="miss"><option value="">Select</option><option>yes</option><option>no</option><option>unassessed</option></select></label></fieldset>
</section><button id="timer">Start / resume timer</button><button id="pause">Pause</button><span id="seconds">0 active seconds</span><br>
<button id="save">Save item and next</button><button id="export">Export review JSON</button><p id="message" role="status"></p>
<script>const data=PAYLOAD;const assisted=data.assistance!==null;let index=0,started=null,elapsed=0,records=[];
const $=id=>document.getElementById(id);$('title').textContent=assisted?'Assisted review':'Baseline review — before opening Jev suggestions';
function pause(){if(started!==null){elapsed+=(performance.now()-started)/1000;started=null;} $('seconds').textContent=elapsed.toFixed(1)+' active seconds';$('item').hidden=true;}
document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
function show(){const u=data.units[index];$('progress').textContent='Item '+(index+1)+' of '+data.units.length+' — '+u.id;$('evidence').textContent=JSON.stringify(u.state,null,2);$('questions').replaceChildren();
Object.entries(data.questions).forEach(([id,q])=>{const label=document.createElement('label');label.textContent=q.instructions;const select=document.createElement('select');select.id='answer-'+id;select.add(new Option('Select',''));Object.entries(q.criteria).forEach(([v,text])=>select.add(new Option(v+' — '+text,v)));label.append(select);$('questions').append(label);});
$('notes').value='';$('help').value='';$('miss').value='';$('quality').hidden=!assisted;$('hint').hidden=!assisted;
if(assisted)$('hint').textContent='Jev suggestions — not final dispositions\n'+JSON.stringify(data.assistance[u.id]||{status:'unavailable'},null,2);elapsed=0;started=null;$('item').hidden=true;$('seconds').textContent='0 active seconds';}
$('timer').onclick=()=>{if(started===null){started=performance.now();$('item').hidden=false;}};$('pause').onclick=pause;
$('save').onclick=()=>{pause();const answers=Object.fromEntries(Object.keys(data.questions).map(q=>[q,$('answer-'+q).value]));
if(!$('reviewer').value.trim()||!$('exposure').value||Object.values(answers).some(x=>!x)||!$('notes').value.trim()||elapsed<=0||(assisted&&(!$('help').value||!$('miss').value))){$('message').textContent='Complete every field and record active review time first.';return;}
records.push({unit_id:data.units[index].id,answers,notes:$('notes').value,active_seconds:elapsed,reviewed_at:new Date().toISOString(),helpfulness:assisted?$('help').value:null,missed_concern:assisted?$('miss').value:null});index++;
if(index<data.units.length){show();$('message').textContent='Saved locally in this tab. Export to keep your work.';}else{$('save').disabled=true;$('timer').disabled=true;$('message').textContent='All items complete. Export your record now.';}};
$('export').onclick=()=>{pause();const record={mode:assisted?'assisted':'baseline',reviewer:$('reviewer').value,prior_suggestion_exposure:$('exposure').value,source_run_sha256:data.source_run_sha256,complete:records.length===data.units.length,records};const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(record,null,2)],{type:'application/json'}));a.download=(assisted?'assisted':'baseline')+'-review.json';a.click();URL.revokeObjectURL(a.href);};show();</script>'''
    path=Path(output)
    with path.open('x') as f:f.write(template.replace('PAYLOAD',json.dumps(data).replace('<','\\u003c')))


def compare(baseline,assisted,overhead_seconds=None):
    cohort=verify();ids=[u['id'] for u in cohort['units']]
    for record,mode in ((baseline,'baseline'),(assisted,'assisted')):
        if record.get('mode')!=mode or record.get('complete') is not True or not record.get('reviewer','').strip():raise ValueError('Incomplete review')
        if record['source_run_sha256']!=cohort['source_run_sha256']:raise ValueError('Wrong source')
        if [r['unit_id'] for r in record['records']]!=ids:raise ValueError('Wrong review inventory/order')
        for r in record['records']:
            import math
            if type(r['active_seconds']) not in (int,float) or not math.isfinite(r['active_seconds']) or r['active_seconds']<=0:raise ValueError('Invalid timing')
            if not r['notes'].strip() or set(r['answers'])!=set(cohort['questions']):raise ValueError('Incomplete assessment')
            if any(r['answers'][q] not in x['criteria'] for q,x in cohort['questions'].items()):raise ValueError('Invalid assessment option')
            if mode=='assisted' and (r['helpfulness'] not in ('helpful','neutral','misleading','uncertain') or r['missed_concern'] not in ('yes','no','unassessed')):raise ValueError('Incomplete quality assessment')
    if baseline['reviewer']!=assisted['reviewer']:raise ValueError('Paired review requires same reviewer')
    from datetime import datetime
    if min(datetime.fromisoformat(r['reviewed_at'].replace('Z','+00:00')) for r in assisted['records'])<=max(datetime.fromisoformat(r['reviewed_at'].replace('Z','+00:00')) for r in baseline['records']):raise ValueError('Baseline must precede assisted pass')
    import statistics
    from collections import Counter
    deltas=[a['active_seconds']-b['active_seconds'] for a,b in zip(baseline['records'],assisted['records'])]
    if overhead_seconds is not None and (type(overhead_seconds) not in (int,float) or not math.isfinite(overhead_seconds) or overhead_seconds<0):raise ValueError('Invalid overhead')
    return {'interpretation':'Descriptive baseline-first author pilot; learning/order confounded; no causal speedup or independent quality claim',
            'prior_suggestion_exposure':baseline.get('prior_suggestion_exposure','unreported'),
            'active_seconds_difference':sum(deltas),'median_paired_difference':statistics.median(deltas),
            'net_seconds_difference':None if overhead_seconds is None else sum(deltas)-overhead_seconds,
            'overhead_seconds_including_jev_and_setup':overhead_seconds,
            'helpfulness':dict(Counter(r['helpfulness'] for r in assisted['records'])),
            'missed_concerns':dict(Counter(r['missed_concern'] for r in assisted['records'])),
            'route_changes':sum(a['answers']['route']!=b['answers']['route'] for a,b in zip(baseline['records'],assisted['records']))}
