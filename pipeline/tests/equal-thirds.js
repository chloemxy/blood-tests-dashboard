const fs=require('fs'),{JSDOM}=require('jsdom');
const html=fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
const sizes=[[1280,720],[1440,900],[1600,900],[1920,1080]];let i=0,fail=[];
(function go(){ if(i>=sizes.length){console.log(fail.length?'\nFAIL:\n - '+fail.join('\n - '):'\nALL PASS'); if(fail.length) process.exitCode = 1;return;}
 const [W,H]=sizes[i++];
 const dom=new JSDOM(html,{url:'http://localhost/',runScripts:'dangerously',pretendToBeVisual:true,beforeParse(w){
  w.matchMedia=q=>({matches:false,addEventListener(){},addListener(){}});
  Object.defineProperty(w.HTMLElement.prototype,'clientWidth',{get(){return W}});
  Object.defineProperty(w.HTMLElement.prototype,'clientHeight',{get(){return H}});}});
 setTimeout(()=>{const w=dom.window,d=w.document,L=w.eval('LAYOUT'),b=w.eval('BOX');
  const c1=L.xM-b.L, c2=L.xCend-L.xC, c3=b.R-L.xT;
  const g1=L.xC-L.xM, g2=L.xT-L.xCend;
  console.log(W+'x'+H,'cols',c1.toFixed(1),c2.toFixed(1),c3.toFixed(1),'| gaps',g1.toFixed(1),g2.toFixed(1));
  if(Math.max(c1,c2,c3)-Math.min(c1,c2,c3)>0.5) fail.push(W+'x'+H+': columns differ');
  if(Math.abs(g1-g2)>0.5) fail.push(W+'x'+H+': dot-run gaps differ ('+g1.toFixed(1)+' vs '+g2.toFixed(1)+')');
  const hd=[...d.querySelectorAll('.colbar span')].slice(0,3).map(t=>+22);
  console.log('   header baselines',hd.join(','),'| titles',[...d.querySelectorAll('.colbar span')].slice(0,3).map(t=>t.textContent).join(' / '));
  if(new Set(hd).size!==1) fail.push('column titles not on one baseline');
  go();},700);
})();
