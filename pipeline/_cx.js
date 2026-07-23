/* ================= CONDITION EXPLORER + ROUTER (scoped, cx-*) ================= */
(function(){
"use strict";
/* ---- DATA (authored from verbatim MedlinePlus/NIH quotes; see IMPROVEMENT-PLAN.md) ---- */
const CONCERNS=__CONCERNS__;
const CONDITIONS=__CONDITIONS__;
const CGROUPS=__CGROUPS__;
const PANEL_SLUGS=__PANEL_SLUGS__;
const byId=id=>CONDITIONS.find(c=>c.id===id);
function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
const $=id=>document.getElementById(id);

const state={picked:new Set(),had:new Set(),result:{},cond:null,from:'cand'};

/* ---------- top-level route ---------- */
function setMode(m){
 $('cxRoute').classList.toggle('cx-on',m==='landing');
 $('cxApp').classList.toggle('cx-on',m==='feel');
 const app=$('app'); if(app) app.style.display=(m==='tests')?'grid':'none';
 window.scrollTo(0,0);
}
window.__cxSetMode=setMode;

/* ---------- inner screens ---------- */
const screens={home:'cxScHome',cand:'cxScCand',browse:'cxScBrowse',lens:'cxScLens'};
function show(name){
 Object.values(screens).forEach(id=>$(id).classList.remove('cx-on'));
 $(screens[name]).classList.add('cx-on');
 drawCrumb(name); window.scrollTo(0,0);
}
function drawCrumb(name){
 const c=$('cxCrumb'), home='<a data-nav="home">Feelings</a>';
 if(name==='home'){ c.innerHTML=''; return; }
 if(name==='cand') c.innerHTML=home+'<span class="sep">/</span><b>Candidate conditions</b>';
 else if(name==='browse') c.innerHTML=home+'<span class="sep">/</span><b>All conditions</b>';
 else if(name==='lens'){
  const back=state.from==='browse'?'<a data-nav="browse">All conditions</a>':'<a data-nav="cand">Candidate conditions</a>';
  c.innerHTML=home+'<span class="sep">/</span>'+back+'<span class="sep">/</span><b>'+esc(byId(state.cond).label)+'</b>';
 }
}

/* ---------- home concern picker ---------- */
function drawConcerns(){
 $('cxConcernChips').innerHTML=CONCERNS.map(c=>'<button class="cx-chip'+(state.picked.has(c.id)?' on':'')+'" data-concern="'+c.id+'">'+esc(c.label)+'</button>').join('');
 const m=matchedConds(), btn=$('cxGoCand');
 btn.disabled=!m.length;
 $('cxCandCount').textContent=state.picked.size?(m.length+' condition'+(m.length===1?'':'s')+' match'):'Pick at least one.';
}
function matchedConds(){
 if(!state.picked.size) return [];
 const score={};
 CONCERNS.forEach(c=>{ if(state.picked.has(c.id)) c.conds.forEach(id=>score[id]=(score[id]||0)+1); });
 return Object.keys(score).sort((a,b)=>score[b]-score[a]).map(id=>({id:id,n:score[id]}));
}

/* ---------- candidates ---------- */
function drawCandidates(){
 const m=matchedConds(), picks=CONCERNS.filter(c=>state.picked.has(c.id)).map(c=>c.label);
 $('cxCandBecause').innerHTML='Because you chose: '+picks.map(p=>'<b style="color:var(--slate)">'+esc(p)+'</b>').join(', ')+'. Conditions sharing more of your feelings come first.';
 const silent=CONDITIONS.filter(c=>c.silent).length;
 const note=$('cxSilentNote');
 note.style.display='block';
 note.innerHTML='Heads up: some conditions have <b>no symptoms</b> — high cholesterol, and early kidney, liver or diabetes can be silent. Those won’t show from a feeling. Use <a data-nav="browse" style="cursor:pointer">Browse all conditions</a> to reach them.';
 $('cxCandList').innerHTML=m.map(o=>{
  const c=byId(o.id), shared=CONCERNS.filter(x=>state.picked.has(x.id)&&x.conds.indexOf(o.id)>=0).map(x=>x.label);
  return '<button class="cx-ccard" data-open="'+c.id+'" data-from="cand"><div class="cn">'+esc(c.label)+'</div>'+
    '<div class="co">'+esc(c.one)+'</div><div class="cm">'+shared.map(s=>'<span class="cx-matchtag">'+esc(s)+'</span>').join('')+
    '<span class="cx-grptag">'+esc(c.grp)+'</span></div></button>';
 }).join('');
}

/* ---------- browse ---------- */
function drawBrowse(){
 $('cxBrowseList').innerHTML=CGROUPS.map(g=>{
  const items=CONDITIONS.filter(c=>c.grp===g); if(!items.length) return '';
  return '<div class="cx-browsegrp"><h3>'+esc(g)+'</h3>'+items.map(c=>{
   const tag=c.silent?'<div class="cm"><span class="cx-silenttag">often silent</span></div>':'';
   return '<button class="cx-ccard" data-open="'+c.id+'" data-from="browse"><div class="cn">'+esc(c.label)+'</div><div class="co">'+esc(c.one)+'</div>'+tag+'</button>';
  }).join('')+'</div>';
 }).join('');
}

/* ---------- lens ---------- */
function openLens(id,from){
 state.cond=id; state.from=from||'cand';
 const c=byId(id);
 $('cxTitle').textContent=c.label; $('cxOne').textContent=c.one; $('cxGrp').textContent=c.grp;
 $('cxDisc').innerHTML='Educational only. Not a diagnosis, not medical advice, and not a recommendation to get tested. A “miniDx” here is a plain-language pattern read of results <em>you</em> enter — always talk it through with a clinician. Diagnostic thresholds vary between guidelines; this build quotes named sources and notes where cut-offs differ.';
 drawSources(c); renderLens(); show('lens');
}
function renderLens(){ drawRipple(); drawMarkers(); drawPath(); drawMiniDx(); }

function drawRipple(){
 const c=byId(state.cond),W=900,H=460,cx=W/2,cy=H/2,parts=[],sy=c.symptoms,mk=c.markers;
 const edge=(x1,y1,x2,y2,col,w)=>parts.push('<path d="M'+x1+' '+y1+' C '+((x1+x2)/2)+' '+y1+', '+((x1+x2)/2)+' '+y2+', '+x2+' '+y2+'" fill="none" stroke="'+col+'" stroke-width="'+w+'" opacity=".45"/>');
 const leftX=150,sN=sy.length;
 sy.forEach((s,i)=>{const y=52+i*((H-104)/Math.max(1,sN-1));edge(leftX,y,cx,cy,'#9aa7ab',1.4);});
 const rightX=748,mN=mk.length;
 mk.forEach((m,i)=>{const y=52+i*((H-104)/Math.max(1,mN-1));const had=state.had.has(m.slug);edge(cx,cy,rightX,y,had?'#2E7D5B':'#B84A0E',had?1.6:2.2);});
 parts.push('<circle cx="'+cx+'" cy="'+cy+'" r="66" fill="#24434D"/>');
 wrapText(c.label,cx,cy,'#fff',12,parts,15);
 sy.forEach((s,i)=>{const y=52+i*((H-104)/Math.max(1,sN-1));
  parts.push('<circle cx="'+leftX+'" cy="'+y+'" r="6" fill="#5A6B70"/>');
  parts.push('<text x="'+(leftX-14)+'" y="'+(y+4)+'" text-anchor="end" font-size="12" fill="#24434D">'+esc(s)+'</text>');});
 mk.forEach((m,i)=>{const y=52+i*((H-104)/Math.max(1,mN-1));const had=state.had.has(m.slug);const col=had?'#2E7D5B':'#B84A0E';
  parts.push('<circle cx="'+rightX+'" cy="'+y+'" r="7" fill="'+col+'"/>');
  parts.push('<text x="'+(rightX+15)+'" y="'+(y-1)+'" font-size="12.5" font-weight="600" fill="#24434D">'+esc(m.name)+'</text>');
  parts.push('<text x="'+(rightX+15)+'" y="'+(y+14)+'" font-size="10.5" fill="'+col+'">'+(had?'tested':'not tested — missing signal')+(m.panel?'':' · outside annual panel')+'</text>');});
 parts.push('<text x="'+leftX+'" y="24" text-anchor="middle" font-size="10.5" letter-spacing="1" fill="#8B9799">HOW YOU FEEL</text>');
 parts.push('<text x="'+rightX+'" y="24" text-anchor="middle" font-size="10.5" letter-spacing="1" fill="#8B9799">BLOOD MARKERS</text>');
 $('cxRipple').innerHTML=parts.join('');
}
function wrapText(t,x,y,fill,size,parts,lh){
 const words=t.replace('–','- ').split(' '),lines=[];let cur='';
 words.forEach(w=>{if((cur+' '+w).trim().length>14){lines.push(cur.trim());cur=w;}else cur+=' '+w;});
 if(cur.trim())lines.push(cur.trim());
 const start=y-(lines.length-1)*lh/2;
 lines.forEach((l,i)=>parts.push('<text x="'+x+'" y="'+(start+i*lh+4)+'" text-anchor="middle" font-size="'+size+'" font-weight="700" fill="'+fill+'">'+esc(l)+'</text>'));
}

function drawMarkers(){
 const c=byId(state.cond);
 $('cxMBody').innerHTML=c.markers.map(m=>{
  const had=state.had.has(m.slug);
  const where=m.panel?'<span class="cx-pill panel">in annual panel</span> <span class="cx-pill '+m.step+'">'+m.step+'</span>'
                     :'<span class="cx-pill out">outside panel</span> <span class="cx-pill '+m.step+'">'+m.step+'</span>';
  const gap=(!had&&!m.panel)?'<span class="cx-gapflag">← signal you haven’t tested for</span>':'';
  const rz=m.reasoned?'<span class="cx-reasoned">reasoned</span>':'';
  const res=had?'<div class="cx-resrow"><span class="rl">result:</span>'+['low','normal','high'].map(r=>'<button class="cx-res '+r+(state.result[m.slug]===r?' on':'')+'" data-res="'+m.slug+'" data-val="'+r+'">'+r+'</button>').join('')+'</div>':'';
  return '<tr><td><span class="cx-mname">'+esc(m.name)+'</span> <span class="cx-mabbr">'+esc(m.abbr)+'</span>'+rz+gap+
    '<div class="cx-msig">'+esc(m.sig)+'</div></td><td>'+where+'</td>'+
    '<td><div class="cx-hadtog"><button data-had="'+m.slug+'" data-v="1" class="'+(had?'on':'')+'">had it</button>'+
    '<button data-had="'+m.slug+'" data-v="0" class="'+(!had?'on':'')+'">not yet</button></div>'+res+'</td></tr>';
 }).join('');
}

function drawPath(){
 const c=byId(state.cond),order=[['screen','Screen'],['confirm','Confirm'],['cause','Find the cause']];
 const steps=order.map(o=>{const ms=c.markers.filter(m=>m.step===o[0]);return ms.length?{role:o[0],label:o[1],markers:ms}:null;}).filter(Boolean);
 let nextIdx=steps.findIndex(s=>s.markers.some(m=>!state.had.has(m.slug)));
 const wrap=$('cxPath'); wrap.style.gridTemplateColumns='repeat('+steps.length+',1fr)';
 wrap.innerHTML=steps.map((s,i)=>{
  const toks=s.markers.map(m=>{const had=state.had.has(m.slug);return '<span class="cx-ptok '+(had?'had':'gap')+'">'+esc(m.abbr)+(had?' ✓':'')+'</span>';}).join('');
  const done=s.markers.filter(m=>state.had.has(m.slug)).length,all=done===s.markers.length;
  const stat=all?'<div class="cx-pstatus ok">✓ you’ve had this step</div>':'<div class="cx-pstatus todo">'+(s.markers.length-done)+' of these still to do</div>';
  const sig=s.role==='screen'?'The first flag — often a test you already get, or a quick add-on.':s.role==='confirm'?'Pins down the diagnosis. Usually requested on purpose.':'Explains why, once the diagnosis is made.';
  return '<div class="cx-pstep '+s.role+(i===nextIdx?' next':'')+'"><div class="role">'+esc(s.label)+(i===nextIdx?' · next step':'')+'</div>'+
    '<h4>Step '+(i+1)+'</h4><div class="psig">'+sig+'</div><div class="cx-ptests">'+toks+'</div>'+stat+'</div>';
 }).join('');
}

function readMiniDx(){
 const c=byId(state.cond),cm=c.markers.find(m=>m.slug===c.confirm),cr=state.result[c.confirm];
 if(!state.had.has(c.confirm)||!cr) return {status:'locked'};
 const supAbn=c.support.some(sl=>{const sm=c.markers.find(m=>m.slug===sl);return sm&&state.result[sl]===sm.abn;});
 if(cr===cm.abn) return supAbn?{status:'consistent',read:c.reads.strong}:{status:'consistent',read:c.reads.supportive};
 if(cr==='normal') return supAbn?{status:'partial',read:c.reads.partial}:{status:'against',read:c.reads.against};
 return {status:'partial',read:c.reads.partial};
}
function drawMiniDx(){
 const c=byId(state.cond),el=$('cxMinidx'),r=readMiniDx(),cm=c.markers.find(m=>m.slug===c.confirm);
 if(r.status==='locked'){
  const need=!state.had.has(c.confirm)?'mark <b>'+esc(cm.name)+'</b> as had':'add a <b>'+esc(cm.name)+'</b> result (low / normal / high)';
  el.className='locked';
  el.innerHTML='<div class="cx-mdxlab">MiniDx · locked</div><div class="cx-mdxlock"><span class="lk">\u{1F512}</span><div>A provisional read appears once the confirming test exists. Right now the pattern can’t be completed.</div></div>'+
   '<div class="cx-mdxneed">To unlock: '+need+'.'+(cm.panel?'':' '+esc(cm.name)+' is the piece the annual panel leaves out.')+'</div>';
  return;
 }
 const low=c.label.toLowerCase();
 const titles={consistent:'Pattern consistent with '+low,partial:'Mixed pattern — needs a clinician’s eye',against:'Not a '+low+' pattern'};
 el.className=r.status;
 const chip=sl=>{const m=c.markers.find(x=>x.slug===sl),v=state.result[sl];return (m&&v)?('<span class="cx-badge '+(v==='normal'?'q':'inf')+'">'+esc(m.abbr)+': '+v+'</span> '):'';};
 const shown=[c.confirm].concat(c.support).filter((v,i,a)=>a.indexOf(v)===i);
 el.innerHTML='<div class="cx-mdxlab">MiniDx · provisional pattern read</div><div class="cx-mdxhead">'+esc(titles[r.status])+'</div>'+
  '<div class="cx-mdxbody">'+r.read+'</div><div style="margin-top:11px">'+shown.map(chip).join('')+'</div>'+
  '<div class="cx-mdxneed" style="margin-top:12px;color:var(--muted)">Based on results you entered, read against the sourced thresholds. '+
  '<span class="cx-badge inf">reasoned</span> combining these into one pattern is clinical reasoning, not a single quoted rule.</div>';
}

function drawSources(c){
 $('cxSrc').innerHTML=c.src.map(s=>{
  const badge=s.k==='q'?'<span class="cx-badge q">quoted</span>':'<span class="cx-badge inf">reasoned</span>';
  const cite=s.url?esc(s.who)+' · <a href="'+s.url+'" target="_blank" rel="noopener">verify</a>':esc(s.who);
  return '<div class="cx-srcitem '+(s.k==='inf'?'inf':'')+'">'+badge+' <q>'+esc(s.quote)+'</q><span class="cite">— '+cite+'</span></div>';
 }).join('');
}

/* ---------- events ---------- */
$('cxConcernChips').addEventListener('click',e=>{const b=e.target.closest('[data-concern]');if(!b)return;const id=b.dataset.concern;state.picked.has(id)?state.picked.delete(id):state.picked.add(id);drawConcerns();});
$('cxGoCand').addEventListener('click',()=>{drawCandidates();show('cand');});
$('cxGoBrowse').addEventListener('click',()=>{drawBrowse();show('browse');});
$('cxBack1').addEventListener('click',()=>show('home'));
$('cxBack2').addEventListener('click',()=>show('home'));
$('cxBackLens').addEventListener('click',()=>show(state.from==='browse'?'browse':'cand'));
$('cxCrumb').addEventListener('click',e=>{const a=e.target.closest('[data-nav]');if(!a)return;const n=a.dataset.nav;if(n==='home')show('home');else if(n==='cand'){drawCandidates();show('cand');}else if(n==='browse'){drawBrowse();show('browse');}});
$('cxSilentNote').addEventListener('click',e=>{const a=e.target.closest('[data-nav="browse"]');if(a){drawBrowse();show('browse');}});
$('cxApp').addEventListener('click',e=>{const o=e.target.closest('[data-open]');if(o)openLens(o.dataset.open,o.dataset.from);});
$('cxMBody').addEventListener('click',e=>{
 const h=e.target.closest('[data-had]');
 if(h){const sl=h.dataset.had;if(h.dataset.v==='1')state.had.add(sl);else{state.had.delete(sl);delete state.result[sl];}renderLens();return;}
 const r=e.target.closest('[data-res]');
 if(r){const sl=r.dataset.res;state.result[sl]=(state.result[sl]===r.dataset.val)?null:r.dataset.val;renderLens();}
});
$('cxSeedBtn').addEventListener('click',function(){
 const inThis=byId(state.cond).markers.filter(m=>m.panel).map(m=>m.slug);
 const on=PANEL_SLUGS.every(sl=>state.had.has(sl));
 if(on){PANEL_SLUGS.forEach(sl=>{state.had.delete(sl);delete state.result[sl];});this.classList.remove('done');this.textContent="I've had a standard annual panel";}
 else{PANEL_SLUGS.forEach(sl=>state.had.add(sl));this.classList.add('done');this.textContent="✓ annual panel marked as done";}
 renderLens();
});

/* route landing + menu */
$('cxRouteFeel').addEventListener('click',()=>{setMode('feel');show('home');});
$('cxRouteTests').addEventListener('click',()=>{ if(window.__cxEnsureTests)window.__cxEnsureTests(); setMode('tests'); });
$('cxMenuBtn').addEventListener('click',()=>setMode('landing'));

/* inject a "Menu" button into the existing dashboard header so tests-mode can return */
(function(){
 const hdr=document.querySelector('#app header.top');
 if(hdr && !document.getElementById('cxToMenu')){
  const b=document.createElement('button');
  b.id='cxToMenu'; b.className='cxmenu'; b.textContent='← Menu';
  b.style.marginRight='4px';
  b.addEventListener('click',()=>setMode('landing'));
  hdr.insertBefore(b,hdr.firstChild);
 }
})();

drawConcerns();
setMode('landing');
})();
