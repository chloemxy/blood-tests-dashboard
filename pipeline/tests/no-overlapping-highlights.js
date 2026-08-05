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
  d.getElementById('pAll').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));   // densest case
  d.querySelector('[data-cn]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  [['marker','.map .row.mkr'],['concern','.map .row.cnc'],['follow-up','.map .row.tst']].forEach(([nm,sel])=>{
   const boxes=[...d.querySelectorAll(sel+' .hitbox')].map(r=>({t:+r.getAttribute('y'),h:+r.getAttribute('height')}))
     .sort((a,b)=>a.t-b.t);
   let worst=1e9;
   for(let k=1;k<boxes.length;k++) worst=Math.min(worst, boxes[k].t-(boxes[k-1].t+boxes[k-1].h));
   console.log(W+'x'+H,nm.padEnd(9),'boxes',boxes.length,'tightest gap between highlights',worst.toFixed(1));
   if(worst<0) fail.push(W+'x'+H+' '+nm+': highlights overlap by '+(-worst).toFixed(1)+'px');
  });
  go();},700);
})();
