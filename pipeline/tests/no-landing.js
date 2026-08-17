/* The route chooser is retired: the atlas is the front door and the four tabs
 * are the navigation. No address may land on a screen whose only job is to
 * ask which way to go — including an old #landing bookmark. */
const fs=require('fs'),{JSDOM,VirtualConsole}=require('jsdom');
const path=require('path');
const R=path.join(__dirname,'..','..')+path.sep;
const html=fs.readFileSync(R+'catalogue.html','utf8');
function load(hash,cb){
 const vc=new VirtualConsole(); vc.on('jsdomError',e=>{ if(!/Not implemented/.test(e.message)) console.log('ERR',e.message.slice(0,100)); });
 const dom=new JSDOM(html,{url:'http://localhost/catalogue.html'+hash,runScripts:'dangerously',pretendToBeVisual:true,virtualConsole:vc,
  beforeParse(w){w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
   Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return 1600}});
   Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return 900}});}});
 setTimeout(()=>{const d=dom.window.document;
  cb({hash:hash||'(none)',
   landing:d.getElementById('cxRoute').classList.contains('cx-on'),
   feel:d.getElementById('cxApp').classList.contains('cx-on'),
   tests:d.getElementById('app').style.display==='grid'});
 },800);
}
const out=[];
['', '#landing', '#feel', '#tests'].forEach((h,i)=>load(h,r=>{out.push(r);
 if(out.length===4){ out.forEach(r=>console.log(JSON.stringify(r)));
  const bad=out.filter(r=>r.landing);
  const dead=out.filter(r=>!r.landing&&!r.feel&&!r.tests);
  if(dead.length) console.log('FAIL: nothing at all is shown for '+dead.map(b=>b.hash).join(', '));
  console.log(bad.length?'\nFAIL: the route chooser still appears for '+bad.map(b=>b.hash).join(', '):'\nALL PASS');
  if(bad.length||dead.length) process.exitCode=1;
 }}));
