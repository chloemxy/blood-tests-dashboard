const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1440,900],[1600,900],[1920,1080],[1280,720]];
let i=0,fail=[];
(function go(){
 if(i>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[i++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});
 }});
 setTimeout(()=>{
  const w=dom.window,d=w.document;
  d.querySelector('[data-cn]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  const gaps=(sel,lbSel)=>{
   const g=[...d.querySelectorAll(sel)].map(n=>{
     const ys=[...n.querySelectorAll(lbSel)].map(t=>+t.getAttribute('y'));
     return {top:Math.min(...ys),bot:Math.max(...ys)};
   }).filter(o=>isFinite(o.top)).sort((a,b)=>a.top-b.top);
   const out=[]; for(let k=1;k<g.length;k++) out.push(g[k].top-g[k-1].bot);
   return out;
  };
  [['marker','.map .row.mkr','text.lb'],['concern','.map .row.cnc','text.lb'],['follow-up','.map .row.tst','text']].forEach(([nm,a,b2])=>{
   let gg=gaps(a,b2); if(!gg.length) return;
   // Drop the group boundaries rather than the interior gaps: one per panel
   // header after the first in the marker column, one for the concern divider.
   const nHeads = new Set([...d.querySelectorAll('.map text.grphd')].map(x=>+x.getAttribute('y'))).size;
   const drop = nm==='marker' ? Math.max(0, nHeads-1) : nm==='concern' ? 1 : 0;
   const boundaries = gg.slice().sort((x,y)=>y-x).slice(0,drop);
   boundaries.forEach(v=>{ gg.splice(gg.indexOf(v),1); });
   const mn=Math.min(...gg),mx=Math.max(...gg),sp=mx-mn;
   console.log(W+'x'+H,nm.padEnd(9),'rows',gg.length+1,'gap min',mn.toFixed(1),'max',mx.toFixed(1),'spread',sp.toFixed(2));
   if(sp>0.6) fail.push(W+'x'+H+' '+nm+' column: uneven gaps, spread '+sp.toFixed(1)+'px');
  });
  go();
 },700);
})();
