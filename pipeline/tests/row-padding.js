const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1600,900],[1920,1080]];let i=0,fail=[];
(function go(){ if(i>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[i++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});}});
 setTimeout(()=>{const w=dom.window,d=w.document;
  d.querySelector('[data-cn]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  const pads={};
  [['marker','.map .row.mkr'],['concern','.map .row.cnc'],['follow-up','.map .row.tst']].forEach(([nm,sel])=>{
   const vals=new Set();
   d.querySelectorAll(sel).forEach(g=>{
    const r=g.querySelector('.hitbox'); const ts=[...g.querySelectorAll('text')].filter(t=>/lb|nm/.test(t.getAttribute('class')||'')||sel.includes('tst'));
    const ys=ts.map(t=>+t.getAttribute('y')).filter(v=>!isNaN(v)); if(!ys.length) return;
    const top=+r.getAttribute('y'), h=+r.getAttribute('height');
    // distance from box top to the first baseline, and last baseline to box bottom
    vals.add((Math.min(...ys)-top).toFixed(1)+'/'+(top+h-Math.max(...ys)).toFixed(1));
   });
   pads[nm]=[...vals];
  });
  const all=new Set([].concat(...Object.values(pads)));
  console.log(W+'x'+H, JSON.stringify(pads));
  if(all.size!==1) fail.push(W+'x'+H+': padding differs between rows/columns -> '+[...all].join(' , '));
  go();},700);
})();
