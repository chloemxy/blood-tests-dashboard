/* The guide is per visit: two loads sharing one localStorage prove that a
 * refresh opens at step 1 again, and that Skip lasts for the visit only.
 *
 * Marks do persist — the tutorial teaches the action, so step 1 ticks on a
 * mark made now, never on one left over from last time. That is what stopped
 * a refresh from resuming at step 2. */
/* Two loads of the same document, sharing one localStorage, to prove a refresh
   starts the guide again — and that Skip lasts only for the visit. */
const fs=require('fs'),{JSDOM}=require('jsdom');
const path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','..','index.html'),'utf8');
let store={};
function load(tag,cb){
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,
  beforeParse(w){
   w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
   Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return 1600}});
   Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return 900}});
   Object.keys(store).forEach(k=>w.localStorage.setItem(k,store[k]));
  }});
 setTimeout(()=>{
  const w=dom.window,d=w.document;
  console.log(tag+':', 'guiding', d.body.classList.contains('guiding'),
   '| step', (d.getElementById('gK')||{}).textContent,
   '| concerns', d.querySelectorAll('.map .row.cnc').length);
  cb(w,d,()=>{ store={}; for(let i=0;i<w.localStorage.length;i++){const k=w.localStorage.key(i); store[k]=w.localStorage.getItem(k);} });
 },700);
}
load('first load',(w,d,persist)=>{
 // finish the whole guide
 d.querySelector('#gEx [data-ex="iron"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 d.querySelector('.map [data-cn]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 d.querySelector('.map [data-test]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
 console.log('  after finishing: guiding', d.body.classList.contains('guiding'));
 persist();
 load('after refresh',(w2,d2,p2)=>{
  const ok = d2.body.classList.contains('guiding') && /Step 1 of 3/.test((d2.getElementById('gK')||{}).textContent);
  console.log('  starts at step 1 again:', ok);
  // and Skip only lasts the visit
  d2.getElementById('gSkip').dispatchEvent(new w2.MouseEvent('click',{bubbles:true}));
  console.log('  after Skip: guiding', d2.body.classList.contains('guiding'));
  p2();
  load('after refresh 2',(w3,d3)=>{
   const ok2 = d3.body.classList.contains('guiding');
   console.log('  skip did not stick across a refresh:', ok2);
   const fail=[];
   if(!ok) fail.push('a refresh did not open at step 1');
   if(!ok2) fail.push('Skip persisted across a refresh');
   console.log(fail.length ? '\nFAIL:\n - '+fail.join('\n - ') : '\nALL PASS');
   if(fail.length) process.exitCode = 1;
  });
 });
});
